from pathlib import Path
import json
import re
import shutil
import subprocess
import sys
import time
from html.parser import HTMLParser
from opencc import OpenCC

ROOT = Path(__file__).resolve().parents[2]
INDEX = ROOT / 'index.html'


def decode_js(body: str) -> str:
    out=[]; i=0
    common={'n':'\n','r':'\r','t':'\t','b':'\b','f':'\f','v':'\v','0':'\0','"':'"',"'":"'",'\\':'\\','/':'/'}
    while i < len(body):
        if body[i] != '\\': out.append(body[i]); i += 1; continue
        if i + 1 >= len(body): out.append('\\'); break
        k=body[i+1]
        if k=='u' and i+5 < len(body) and re.fullmatch(r'[0-9a-fA-F]{4}',body[i+2:i+6]):
            code=int(body[i+2:i+6],16); i += 6
            if 0xD800 <= code <= 0xDBFF and i+5 < len(body) and body[i:i+2]=='\\u' and re.fullmatch(r'[0-9a-fA-F]{4}',body[i+2:i+6]):
                low=int(body[i+2:i+6],16)
                if 0xDC00 <= low <= 0xDFFF:
                    code=0x10000+((code-0xD800)<<10)+(low-0xDC00); i += 6
            out.append(chr(code)); continue
        if k=='x' and i+3 < len(body) and re.fullmatch(r'[0-9a-fA-F]{2}',body[i+2:i+4]):
            out.append(chr(int(body[i+2:i+4],16))); i += 4; continue
        out.append(common.get(k,k)); i += 2
    return ''.join(out)


def patch_index():
    s=INDEX.read_text(encoding='utf-8')
    before=s
    styles_before=re.findall(r'<style\b[^>]*>.*?</style>',before,re.S|re.I)
    assets_before=sorted(re.findall(r'assets/images/[A-Za-z0-9._-]+',before))
    en_before=re.findall(r'en:"((?:\\.|[^"\\])*)"',before)
    ja_before=re.findall(r'ja:"((?:\\.|[^"\\])*)"',before)

    cc=OpenCC('s2twp')
    phrase_replacements=[
        ('公司特色','公司簡介'),
        ('案例研究 Apple','案例研究：Apple'),
        ('案例研究: Apple','案例研究：Apple'),
        ('創始人','創辦人'),
        ('世界杯','世界盃'),
        ('營銷','行銷'),
        ('聯繫我們','聯絡我們'),
        ('聯繫 Sam','聯絡 Sam'),
        ('團隊聯繫','團隊聯絡'),
    ]
    counts={'total':0,'changed':0}
    pat=re.compile(r'zh:"((?:\\.|[^"\\])*)"')
    def repl(m):
        counts['total']+=1
        raw=m.group(1)
        text=decode_js(raw)
        new=cc.convert(text)
        for a,b in phrase_replacements:new=new.replace(a,b)
        enc=json.dumps(new,ensure_ascii=True)[1:-1]
        if enc!=raw:counts['changed']+=1
        return 'zh:"'+enc+'"'
    s=pat.sub(repl,s)
    if counts['total'] < 90 or counts['changed'] < 75:
        raise RuntimeError(f'Unexpected Chinese translation coverage: {counts}')

    # Keep the unified heading copy on the same Chinese source and fix the requested colon.
    old="capabilities:['案例','案例研究 Apple','展現高水準的協調促成能力']"
    new="capabilities:['案例','案例研究：Apple','展現高水準的協調促成能力']"
    if old in s:s=s.replace(old,new,1)
    elif new not in s:raise RuntimeError('Chinese Case Study unified heading source not found')

    # Make the unified heading controller read the explicit 4-language mode first.
    old="function lang(){var a=document.querySelector('.lang-switch button.active'),t=txt(a);if(t==='日')return'ja';if(t==='中')return'zh';var h=(document.documentElement.getAttribute('lang')||'').toLowerCase();return h.indexOf('ja')===0?'ja':h.indexOf('zh')===0?'zh':'en'}"
    new="function lang(){var m=document.documentElement.getAttribute('data-ss-lang-mode')||'';if(m==='zhtw'||m==='zhcn')return'zh';if(m==='ja')return'ja';var a=document.querySelector('.lang-switch button.active'),t=txt(a);if(t==='日')return'ja';if(t==='中')return'zh';var h=(document.documentElement.getAttribute('lang')||'').toLowerCase();return h.indexOf('ja')===0?'ja':h.indexOf('zh')===0?'zh':'en'}"
    if old in s:s=s.replace(old,new,1)
    elif new not in s:raise RuntimeError('Unified heading language detector not found')

    # React's original Chinese button writes lang="zh" after the custom handler. Preserve the explicit script variant.
    old='onClick:()=>{t(n),document.documentElement.lang=n}'
    new='onClick:()=>{t(n),document.documentElement.lang=n==="zh"?(document.documentElement.getAttribute("data-ss-lang-mode")==="zhcn"?"zh-Hans":"zh-Hant"):n}'
    if s.count(old)!=1 and new not in s:
        raise RuntimeError(f'Expected one React language setter, found {s.count(old)}')
    if old in s:s=s.replace(old,new,1)

    # Source-level audit: every compiled zh string must now be free of Simplified-only conversions.
    check_cc=OpenCC('s2tw')
    residues=[]
    for m in pat.finditer(s):
        txt=decode_js(m.group(1))
        converted=check_cc.convert(txt)
        if converted!=txt:
            residues.append((txt,converted))
    if residues:
        for a,b in residues[:30]:print('SOURCE RESIDUE',repr(a),'=>',repr(b))
        raise RuntimeError('Simplified characters remain in compiled zh source')

    if re.findall(r'<style\b[^>]*>.*?</style>',s,re.S|re.I)!=styles_before:raise RuntimeError('Unexpected CSS/style change')
    if sorted(re.findall(r'assets/images/[A-Za-z0-9._-]+',s))!=assets_before:raise RuntimeError('Unexpected image asset change')
    if re.findall(r'en:"((?:\\.|[^"\\])*)"',s)!=en_before:raise RuntimeError('Unexpected English translation change')
    if re.findall(r'ja:"((?:\\.|[^"\\])*)"',s)!=ja_before:raise RuntimeError('Unexpected Japanese translation change')

    INDEX.write_text(s,encoding='utf-8')
    print('Patched compiled Chinese source:',counts,'; CSS/assets/English/Japanese unchanged')


def runtime_audit():
    s=INDEX.read_text(encoding='utf-8')
    audit=r'''<script>
window.addEventListener('load',function(){
  setTimeout(function(){
    var sel=document.querySelector('.lang-dropdown-select');
    if(!sel||sel.options.length<4){document.body.innerHTML='<pre id="audit-output">NO DROPDOWN</pre>';return;}
    function labels(){return [].slice.call(sel.options).map(function(o){return o.text}).join(' / ')}
    function nav(){var n=document.querySelector('.site-header nav');return n?[].slice.call(n.querySelectorAll('a')).map(function(a){return (a.textContent||'').trim()}).join(' | '):''}
    function headings(){return [].slice.call(document.querySelectorAll('.ss-unified-heading')).map(function(h){return ((h.querySelector('.ss-unified-kicker')||{}).textContent||'').trim()+' > '+((h.querySelector('.ss-unified-title')||{}).textContent||'').trim()+' > '+((h.querySelector('.ss-unified-support')||{}).textContent||'').trim()}).join(' || ')}
    sel.value='3';sel.dispatchEvent(new Event('change',{bubbles:true}));
    setTimeout(function(){
      var toggle=document.querySelector('.career-toggle');if(toggle&&toggle.getAttribute('aria-expanded')!=='true')toggle.click();
      setTimeout(function(){
        var tradText=(document.body.innerText||'').replace(/\u00a0/g,' ').replace(/[ \t]+\n/g,'\n').replace(/\n{3,}/g,'\n\n').trim();
        var tradMode=document.documentElement.getAttribute('data-ss-lang-mode')||'',tradLang=document.documentElement.getAttribute('lang')||'';
        var tradNav=nav(),tradHeads=headings(),tradDrop=labels();
        sel=document.querySelector('.lang-dropdown-select');sel.value='2';sel.dispatchEvent(new Event('change',{bubbles:true}));
        setTimeout(function(){
          var simpText=(document.body.innerText||'').replace(/\u00a0/g,' ').replace(/[ \t]+\n/g,'\n').replace(/\n{3,}/g,'\n\n').trim();
          var simpMode=document.documentElement.getAttribute('data-ss-lang-mode')||'',simpLang=document.documentElement.getAttribute('lang')||'';
          var simpDrop=labels();
          document.body.innerHTML='<pre id="audit-output"></pre>';
          document.getElementById('audit-output').textContent='TRAD_MODE='+tradMode+'\nTRAD_LANG='+tradLang+'\nTRAD_DROPDOWN='+tradDrop+'\nTRAD_NAV='+tradNav+'\nTRAD_HEADINGS='+tradHeads+'\n---TRAD---\n'+tradText+'\n---SIMP META---\nSIMP_MODE='+simpMode+'\nSIMP_LANG='+simpLang+'\nSIMP_DROPDOWN='+simpDrop+'\n---SIMP---\n'+simpText;
        },1800);
      },900);
    },1800);
  },1000);
});
</script>'''
    audit_path=ROOT/'runtime-audit.html';dom_path=ROOT/'.runtime-dom.html'
    audit_path.write_text(s.replace('</body>',audit+'\n</body>',1),encoding='utf-8')
    chrome=shutil.which('google-chrome') or shutil.which('chromium') or shutil.which('chromium-browser')
    if not chrome:raise RuntimeError('Chrome not found')
    server=subprocess.Popen([sys.executable,'-m','http.server','8000'],cwd=ROOT,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    try:
        time.sleep(.7)
        with dom_path.open('w',encoding='utf-8') as f:
            subprocess.run([chrome,'--headless','--no-sandbox','--disable-gpu','--window-size=1440,1300','--virtual-time-budget=11000','--dump-dom','http://127.0.0.1:8000/runtime-audit.html'],stdout=f,check=True)
        class P(HTMLParser):
            def __init__(self):super().__init__();self.on=False;self.buf=[]
            def handle_starttag(self,t,a):
                if t=='pre' and dict(a).get('id')=='audit-output':self.on=True
            def handle_endtag(self,t):
                if t=='pre' and self.on:self.on=False
            def handle_data(self,d):
                if self.on:self.buf.append(d)
        parser=P();parser.feed(dom_path.read_text(encoding='utf-8',errors='replace'));text=''.join(parser.buf)
        print(text[:24000])
        if text=='NO DROPDOWN' or 'TRAD_MODE=zhtw' not in text or 'TRAD_LANG=zh-Hant' not in text:raise RuntimeError('Traditional dropdown/mode/lang audit failed')
        if 'SIMP_MODE=zhcn' not in text or 'SIMP_LANG=zh-Hans' not in text:raise RuntimeError('Simplified dropdown/mode/lang audit failed')
        exact='English / 日本語 / 简体中文 / 繁體中文'
        if 'TRAD_DROPDOWN='+exact not in text or 'SIMP_DROPDOWN='+exact not in text:raise RuntimeError('Language dropdown labels changed')
        trad=text.split('---TRAD---\n',1)[1].split('\n---SIMP META---',1)[0]
        simp=text.split('---SIMP---\n',1)[1]
        required=[
            '歡迎來到','公司簡介','亞太經驗','核心市場','全球網絡','東京 / 日本','策略。連結。執行。',
            '致力於促進日本運動與娛樂產業的創新與成長機會。','專注於提升運動商業的連結程度與專業能力。',
            '源自對體育運動的真摯熱愛與尊重，驅動我們所管理的每一項企劃與合作。',
            '打破傳統產業壁壘，開創充滿創意的商業機會與前瞻性策略。',
            '對頂尖表現的技術與工藝抱持高度欣賞，向所有卓越運動員與創作者致敬。',
            '創辦人','總經理','體育行銷主管','日本商務開發總監','世界盃區域銷售與行銷經理',
            '日本體育廳','權利持有方','一級方程式賽車','支付服務','穿戴式裝置','頂尖運動員',
            '收到緊急任務後，在兩小時內完成並交付。','阪神虎','大阪','閱讀完整專欄','聯絡我們','版權所有。'
        ]
        missing=[x for x in required if x not in trad]
        if missing:raise RuntimeError('Missing expected Traditional runtime strings: '+repr(missing))
        # Check the four standardized white headings specifically.
        heading_required=['公司 > 公司簡介','差異 > 核心優勢','職涯 > 專業歷程','網絡 > 廣泛的影響力與資源管道','案例 > 案例研究：Apple']
        head_line=text.split('TRAD_HEADINGS=',1)[1].split('\n',1)[0] if 'TRAD_HEADINGS=' in text else ''
        hm=[x for x in heading_required if x not in head_line]
        if hm:raise RuntimeError('Traditional standardized headings not updated: '+repr(hm))
        nav_line=text.split('TRAD_NAV=',1)[1].split('\n',1)[0]
        for x in ['公司','優勢','創辦人','網絡','案例','洞察']:
            if x not in nav_line:raise RuntimeError('Traditional short navigation missing: '+x)
        cleaned=trad.replace('简体中文','')
        check=OpenCC('s2tw');res=[]
        for line in cleaned.splitlines():
            cv=check.convert(line)
            if cv!=line:res.append((line,cv))
        if res:
            for a,b in res[:50]:print('RUNTIME RESIDUE',repr(a),'=>',repr(b))
            raise RuntimeError('Simplified characters remain in Traditional runtime')
        for x in ['欢迎来到','公司简介','亚太经验','核心市场','全球网络','东京 / 日本']:
            if x not in simp:raise RuntimeError('Simplified mode regression: '+x)
        print('Traditional Chinese runtime verified; Simplified Chinese preserved')
    finally:
        server.terminate()
        try:server.wait(timeout=3)
        except subprocess.TimeoutExpired:server.kill()
        for q in [audit_path,dom_path]:
            if q.exists():q.unlink()


if __name__=='__main__':
    patch_index()
    runtime_audit()
    subprocess.run(['git','diff','--check'],cwd=ROOT,check=True)
