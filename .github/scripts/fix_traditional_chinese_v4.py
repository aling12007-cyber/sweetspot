from pathlib import Path
import json,re,shutil,subprocess,sys,time
from html.parser import HTMLParser
from opencc import OpenCC

ROOT=Path(__file__).resolve().parents[2]
INDEX=ROOT/'index.html'

def decode_js(body):
    out=[];i=0;common={'n':'\n','r':'\r','t':'\t','b':'\b','f':'\f','v':'\v','0':'\0','"':'"',"'":"'",'\\':'\\','/':'/'}
    while i<len(body):
        if body[i]!='\\':out.append(body[i]);i+=1;continue
        if i+1>=len(body):out.append('\\');break
        k=body[i+1]
        if k=='u' and i+5<len(body) and re.fullmatch(r'[0-9a-fA-F]{4}',body[i+2:i+6]):
            code=int(body[i+2:i+6],16);i+=6
            if 0xD800<=code<=0xDBFF and i+5<len(body) and body[i:i+2]=='\\u' and re.fullmatch(r'[0-9a-fA-F]{4}',body[i+2:i+6]):
                low=int(body[i+2:i+6],16)
                if 0xDC00<=low<=0xDFFF:code=0x10000+((code-0xD800)<<10)+(low-0xDC00);i+=6
            out.append(chr(code));continue
        if k=='x' and i+3<len(body) and re.fullmatch(r'[0-9a-fA-F]{2}',body[i+2:i+4]):out.append(chr(int(body[i+2:i+4],16)));i+=4;continue
        out.append(common.get(k,k));i+=2
    return ''.join(out)

def patch_index():
    s=INDEX.read_text(encoding='utf-8');before=s
    styles_before=re.findall(r'<style\b[^>]*>.*?</style>',s,re.S|re.I)
    assets_before=sorted(re.findall(r'assets/images/[A-Za-z0-9._-]+',s))
    en_before=re.findall(r'en:"((?:\\.|[^"\\])*)"',s)
    ja_before=re.findall(r'ja:"((?:\\.|[^"\\])*)"',s)

    cc=OpenCC('s2twp');pat=re.compile(r'zh:"((?:\\.|[^"\\])*)"');count=0;total=0
    semantic={
      '公司特色':'公司簡介','案例研究 Apple':'案例研究：Apple','案例研究: Apple':'案例研究：Apple',
      '創始人':'創辦人','世界杯':'世界盃','營銷':'行銷','聯繫我們':'聯絡我們','聯繫 Sam':'聯絡 Sam',
      '團隊聯繫':'團隊聯絡','網路':'網絡'
    }
    def repl(m):
        nonlocal count,total
        total+=1;raw=m.group(1);txt=decode_js(raw);new=cc.convert(txt)
        for a,b in semantic.items():new=new.replace(a,b)
        enc=json.dumps(new,ensure_ascii=True)[1:-1]
        if enc!=raw:count+=1
        return 'zh:"'+enc+'"'
    s=pat.sub(repl,s)
    if total<90 or count<75:raise RuntimeError(f'Unexpected zh coverage total={total} changed={count}')

    old="capabilities:['案例','案例研究 Apple','展現高水準的協調促成能力']";new="capabilities:['案例','案例研究：Apple','展現高水準的協調促成能力']"
    if old in s:s=s.replace(old,new,1)
    elif new not in s:raise RuntimeError('Unified heading Chinese source missing')

    old="function lang(){var a=document.querySelector('.lang-switch button.active'),t=txt(a);if(t==='日')return'ja';if(t==='中')return'zh';var h=(document.documentElement.getAttribute('lang')||'').toLowerCase();return h.indexOf('ja')===0?'ja':h.indexOf('zh')===0?'zh':'en'}"
    new="function lang(){var m=document.documentElement.getAttribute('data-ss-lang-mode')||'';if(m==='zhtw'||m==='zhcn')return'zh';if(m==='ja')return'ja';var a=document.querySelector('.lang-switch button.active'),t=txt(a);if(t==='日')return'ja';if(t==='中')return'zh';var h=(document.documentElement.getAttribute('lang')||'').toLowerCase();return h.indexOf('ja')===0?'ja':h.indexOf('zh')===0?'zh':'en'}"
    if old in s:s=s.replace(old,new,1)
    elif new not in s:raise RuntimeError('Unified heading language detector missing')

    old='onClick:()=>{t(n),document.documentElement.lang=n}'
    new='onClick:()=>{t(n),document.documentElement.lang=n==="zh"?(document.documentElement.getAttribute("data-ss-lang-mode")==="zhcn"?"zh-Hans":"zh-Hant"):n}'
    if old in s:s=s.replace(old,new,1)
    elif new not in s:raise RuntimeError('React language setter missing')

    # Always clear any stale Simplified mutations before choosing a base language.
    old="    if(mode==='zhcn')restoreTree(document.body);\n\n    if(token==='日')setMode('ja');"
    new="    restoreTree(document.body);\n\n    if(token==='日')setMode('ja');"
    if old in s:s=s.replace(old,new,1)
    elif new not in s:raise RuntimeError('Four-language restore hook missing')

    # Keep the language dropdown labels immutable in both Chinese modes.
    marker="  function apply(){\n    scheduled=false;\n    var ui=ensureUI();"
    inject="  function normalizeDropdownLabels(){\n    var select=document.querySelector('.lang-dropdown-select');\n    if(!select||select.options.length<4)return;\n    var labels=['English','日本語','简体中文','繁體中文'];\n    for(var i=0;i<4;i++)if(select.options[i].text!==labels[i])select.options[i].text=labels[i];\n  }\n\n  function apply(){\n    scheduled=false;\n    var ui=ensureUI();"
    if marker in s:s=s.replace(marker,inject,1)
    elif 'function normalizeDropdownLabels()' not in s:raise RuntimeError('Dropdown normalization insertion point missing')

    old="    if(!ui)return;\n    if(mode==='zhcn')simplifyTree(document.body);\n  }"
    new="    if(!ui)return;\n    if(mode==='zhcn')simplifyTree(document.body);\n    else if(mode==='zhtw')restoreTree(document.body);\n    normalizeDropdownLabels();\n  }"
    if old in s:s=s.replace(old,new,1)
    elif new not in s:raise RuntimeError('Four-language apply hook missing')

    # Fix nav language detection for the separate Simplified button.
    old="    var active=document.querySelector('.lang-switch button.active');\n    var x=(active&&active.textContent||'EN').trim();\n    return x==='日'?'ja':x==='中'?'zh':'en';"
    new="    var m=document.documentElement.getAttribute('data-ss-lang-mode')||'';\n    if(m==='zhtw'||m==='zhcn')return'zh';\n    if(m==='ja')return'ja';\n    var active=document.querySelector('.lang-switch button.active');\n    var x=(active&&active.textContent||'EN').trim();\n    return x==='日'?'ja':x==='中'?'zh':'en';"
    if old in s:s=s.replace(old,new,1)
    elif new not in s:raise RuntimeError('Navigation language detector missing')

    residues=[];check=OpenCC('s2tw')
    for m in pat.finditer(s):
        txt=decode_js(m.group(1));cv=check.convert(txt)
        if cv!=txt:residues.append((txt,cv))
    if residues:raise RuntimeError('Simplified characters remain in compiled zh source: '+repr(residues[:10]))
    if re.findall(r'<style\b[^>]*>.*?</style>',s,re.S|re.I)!=styles_before:raise RuntimeError('CSS changed')
    if sorted(re.findall(r'assets/images/[A-Za-z0-9._-]+',s))!=assets_before:raise RuntimeError('Assets changed')
    if re.findall(r'en:"((?:\\.|[^"\\])*)"',s)!=en_before:raise RuntimeError('English changed')
    if re.findall(r'ja:"((?:\\.|[^"\\])*)"',s)!=ja_before:raise RuntimeError('Japanese changed')
    INDEX.write_text(s,encoding='utf-8')
    print('Patched zh source',total,count,'without CSS/assets/EN/JA changes')

def runtime_audit():
    s=INDEX.read_text(encoding='utf-8')
    audit=r'''<script>
window.addEventListener('load',function(){setTimeout(function(){
 var sel=document.querySelector('.lang-dropdown-select');if(!sel||sel.options.length<4){document.body.innerHTML='<pre id="audit-output">NO DROPDOWN</pre>';return;}
 function labels(){return [].slice.call(sel.options).map(function(o){return o.text}).join(' / ')}
 function snap(tag,next){setTimeout(function(){
   var body=(document.body.innerText||'').replace(/\u00a0/g,' ');var mode=document.documentElement.getAttribute('data-ss-lang-mode')||'';var lang=document.documentElement.getAttribute('lang')||'';
   window.__aud=(window.__aud||[]).concat([tag+'_MODE='+mode,tag+'_LANG='+lang,tag+'_DROP='+labels(),tag+'_BODY='+body]);if(next)next();
 },1400)}
 sel.value='3';sel.dispatchEvent(new Event('change',{bubbles:true}));snap('TRAD',function(){sel=document.querySelector('.lang-dropdown-select');sel.value='2';sel.dispatchEvent(new Event('change',{bubbles:true}));snap('SIMP',function(){document.body.innerHTML='<pre id="audit-output"></pre>';document.getElementById('audit-output').textContent=window.__aud.join('\n');});});
},900)});
</script>'''
    audit_path=ROOT/'runtime-audit.html';dom_path=ROOT/'.runtime-dom.html';audit_path.write_text(s.replace('</body>',audit+'\n</body>',1),encoding='utf-8')
    chrome=shutil.which('google-chrome') or shutil.which('chromium') or shutil.which('chromium-browser')
    if not chrome:raise RuntimeError('Chrome not found')
    server=subprocess.Popen([sys.executable,'-m','http.server','8000'],cwd=ROOT,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    try:
        time.sleep(.7)
        with dom_path.open('w',encoding='utf-8') as f:subprocess.run([chrome,'--headless','--no-sandbox','--disable-gpu','--window-size=1440,1300','--virtual-time-budget=8000','--dump-dom','http://127.0.0.1:8000/runtime-audit.html'],stdout=f,check=True)
        class P(HTMLParser):
            def __init__(self):super().__init__();self.on=False;self.buf=[]
            def handle_starttag(self,t,a):
                if t=='pre' and dict(a).get('id')=='audit-output':self.on=True
            def handle_endtag(self,t):
                if t=='pre' and self.on:self.on=False
            def handle_data(self,d):
                if self.on:self.buf.append(d)
        p=P();p.feed(dom_path.read_text(encoding='utf-8',errors='replace'));text=''.join(p.buf);print(text[:26000])
        if 'TRAD_MODE=zhtw' not in text or 'TRAD_LANG=zh-Hant' not in text:raise RuntimeError('Traditional mode/lang failed')
        if 'SIMP_MODE=zhcn' not in text or 'SIMP_LANG=zh-Hans' not in text:raise RuntimeError('Simplified mode/lang failed')
        exact='English / 日本語 / 简体中文 / 繁體中文'
        if 'TRAD_DROP='+exact not in text or 'SIMP_DROP='+exact not in text:raise RuntimeError('Dropdown labels changed')
        trad=text.split('TRAD_BODY=',1)[1].split('\nSIMP_MODE=',1)[0];simp=text.split('SIMP_BODY=',1)[1]
        required=['歡迎來到','公司簡介','亞太經驗','核心市場','全球網絡','東京 / 日本','策略。連結。執行。','創辦人','專業歷程','廣泛的影響力與資源管道','案例研究：Apple','聯絡我們']
        miss=[x for x in required if x not in trad]
        if miss:raise RuntimeError('Traditional missing '+repr(miss))
        for x in ['欢迎来到','公司简介','亚太经验','核心市场','全球网络','东京 / 日本']:
            if x not in simp:raise RuntimeError('Simplified missing '+x)
        residue=[];check=OpenCC('s2tw')
        for line in trad.replace('简体中文','').splitlines():
            cv=check.convert(line)
            if cv!=line:residue.append((line,cv))
        if residue:raise RuntimeError('Traditional runtime residues '+repr(residue[:20]))
        print('Traditional and Simplified runtime verified')
    finally:
        server.terminate()
        try:server.wait(timeout=3)
        except subprocess.TimeoutExpired:server.kill()
        for q in (audit_path,dom_path):
            if q.exists():q.unlink()

if __name__=='__main__':
    patch_index();runtime_audit();subprocess.run(['git','diff','--check'],cwd=ROOT,check=True)
