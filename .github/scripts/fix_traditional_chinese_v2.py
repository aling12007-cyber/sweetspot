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
START = '<!-- SS TRADITIONAL CHINESE FINALIZER START -->'
END = '<!-- SS TRADITIONAL CHINESE FINALIZER END -->'


def decode_js(body):
    out=[]; i=0
    common={'n':'\n','r':'\r','t':'\t','b':'\b','f':'\f','v':'\v','0':'\0','"':'"',"'":"'",'\\':'\\','/':'/'}
    while i < len(body):
        if body[i] != '\\': out.append(body[i]); i += 1; continue
        if i + 1 >= len(body): out.append('\\'); break
        k=body[i+1]
        if k=='u' and i+5 < len(body) and re.fullmatch(r'[0-9a-fA-F]{4}', body[i+2:i+6]):
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


def patch():
    s=INDEX.read_text(encoding='utf-8')
    before=s
    styles_before=re.findall(r'<style\b[^>]*>.*?</style>',before,re.S|re.I)
    assets_before=sorted(re.findall(r'assets/images/[A-Za-z0-9._-]+',before))
    en_before=re.findall(r'en:"((?:\\.|[^"\\])*)"',before)
    ja_before=re.findall(r'ja:"((?:\\.|[^"\\])*)"',before)

    # Normalize the compiled Chinese source to Traditional wherever it is directly addressable.
    cc=OpenCC('s2tw')
    semantic={
        '公司特色':'公司簡介',
        '案例研究 Apple':'案例研究：Apple',
        '案例研究: Apple':'案例研究：Apple',
        '創始人':'創辦人',
        '2015 FIFA U-20 世界杯區域銷售與行銷經理':'2015 FIFA U-20 世界盃區域銷售與行銷經理',
    }
    counts={'total':0,'changed':0}
    pat=re.compile(r'zh:"((?:\\.|[^"\\])*)"')
    def repl(m):
        counts['total'] += 1
        raw=m.group(1)
        text=decode_js(raw)
        out=cc.convert(text)
        out=semantic.get(out,out)
        enc=json.dumps(out,ensure_ascii=True)[1:-1]
        if enc != raw: counts['changed'] += 1
        return 'zh:"'+enc+'"'
    s=pat.sub(repl,s)
    if counts['total'] < 80 or counts['changed'] < 40:
        raise RuntimeError(f'Unexpected Chinese source coverage: {counts}')

    # Keep the current explicit Chinese title source aligned with the requested copy.
    s=s.replace("capabilities:['案例','案例研究 Apple','展現高水準的協調促成能力']",
                "capabilities:['案例','案例研究：Apple','展現高水準的協調促成能力']",1)
    s=s.replace("capabilities:'案例研究 Apple'","capabilities:'案例研究：Apple'",1)

    # Build a site-local Simplified -> Traditional character map using OpenCC.
    # The existing conversion table contains every Simplified character the site may emit.
    to_m=re.search(r'var to="([^"]*)";',s,re.S)
    if not to_m: raise RuntimeError('Existing Chinese conversion map not found')
    candidates=[]; seen=set()
    for ch in to_m.group(1) + s:
        o=ord(ch)
        if (0x3400<=o<=0x4DBF or 0x4E00<=o<=0x9FFF or 0xF900<=o<=0xFAFF) and ch not in seen:
            seen.add(ch); candidates.append(ch)
    simp=[]; trad=[]
    for ch in candidates:
        converted=cc.convert(ch)
        if len(converted)==1 and converted!=ch:
            simp.append(ch); trad.append(converted)
    simp_js=json.dumps(''.join(simp),ensure_ascii=False)
    trad_js=json.dumps(''.join(trad),ensure_ascii=False)

    finalizer=r'''<script id="ss-traditional-chinese-finalizer">
(function(){
  var from=__SIMP__;
  var to=__TRAD__;
  var map=Object.create(null);
  for(var i=0;i<from.length;i++)map[from.charAt(i)]=to.charAt(i);
  var busy=false,queued=false;
  var phrasePairs=[
    ['坂神虎','阪神虎'],['大坂','大阪'],['世界杯','世界盃'],['營銷','行銷'],['聯繫','聯絡'],
    ['公司特色','公司簡介'],['案例研究 Apple','案例研究：Apple'],['案例研究: Apple','案例研究：Apple']
  ];
  function mode(){return document.documentElement.getAttribute('data-ss-lang-mode')||''}
  function toTraditional(value){
    var s=String(value==null?'':value).replace(/[\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff]/g,function(ch){return map[ch]||ch});
    phrasePairs.forEach(function(p){if(s.indexOf(p[0])>=0)s=s.split(p[0]).join(p[1])});
    return s;
  }
  function skipped(el){return !el||!!el.closest('script,style,noscript,textarea,.lang-switch,[data-ss-no-traditionalize]')}
  function fixText(scope){
    var base=scope&&scope.nodeType?scope:document.body;if(!base)return;
    if(base.nodeType===3){var par=base.parentElement;if(skipped(par))return;var v=toTraditional(base.nodeValue||'');if(v!==base.nodeValue)base.nodeValue=v;return}
    if(base.nodeType!==1&&base.nodeType!==9&&base.nodeType!==11)return;
    var tw=document.createTreeWalker(base,NodeFilter.SHOW_TEXT);var n;
    while((n=tw.nextNode())){if(skipped(n.parentElement))continue;var v=toTraditional(n.nodeValue||'');if(v!==n.nodeValue)n.nodeValue=v}
  }
  function setText(el,value){if(el&&el.textContent!==value)el.textContent=value}
  function fixHeadings(){
    var defs={
      company:['公司','公司簡介',''],
      points:['差異','核心優勢',''],
      founder:['創辦人','Sam L. Pearson',''],
      experience:['職涯','專業歷程','深耕亞太地區'],
      network:['網絡','廣泛的影響力與資源管道','曾服務的對象包括：'],
      capabilities:['案例','案例研究：Apple','展現高水準的協調促成能力'],
      insights:['洞察','洞察與觀點','專家觀點']
    };
    Object.keys(defs).forEach(function(id){
      var h=document.querySelector('#'+id+' .ss-unified-heading');if(!h)return;
      var d=defs[id];setText(h.querySelector('.ss-unified-kicker'),d[0]);setText(h.querySelector('.ss-unified-title'),d[1]);
      var sup=h.querySelector('.ss-unified-support');if(sup){setText(sup,d[2]);sup.style.display=d[2]?'':'none'}
    });
  }
  function fixTopNav(){
    var nav=document.querySelector('.site-header nav');if(!nav)return;
    var labels={'#company':'公司','#points':'優勢','#founder':'創辦人','#network':'網絡','#capabilities':'案例','#insights':'洞察','#contact':'聯絡'};
    Object.keys(labels).forEach(function(href){var a=nav.querySelector('a[href="'+href+'"]');if(a)setText(a,labels[href])});
  }
  function fixHeroCTA(){
    var a=document.querySelector('.hero-cta a.gold-button[href="#company"],a.gold-button[href="#company"]');if(!a)return;
    var spans=a.querySelectorAll('span');if(spans.length)setText(spans[0],'公司簡介');else setText(a,'公司簡介');
  }
  function fixDropdown(){
    var sel=document.querySelector('.lang-dropdown-select');if(!sel||sel.options.length<4)return;
    var labels=['English','日本語','简体中文','繁體中文'];
    for(var i=0;i<4;i++)if(sel.options[i].text!==labels[i])sel.options[i].text=labels[i];
  }
  function run(){
    queued=false;if(busy)return;busy=true;
    try{
      fixDropdown();
      if(mode()!=='zhtw')return;
      if(document.documentElement.getAttribute('lang')!=='zh-Hant')document.documentElement.setAttribute('lang','zh-Hant');
      fixText(document.body);fixHeadings();fixTopNav();fixHeroCTA();fixDropdown();
    }finally{busy=false}
  }
  function queue(){if(queued)return;queued=true;requestAnimationFrame(run)}
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',queue,{once:true});else queue();
  document.addEventListener('click',function(e){if(e.target.closest&&e.target.closest('.lang-switch')){setTimeout(queue,0);setTimeout(queue,80);setTimeout(queue,300)}},true);
  new MutationObserver(function(){if(!busy)queue()}).observe(document.documentElement,{subtree:true,childList:true,characterData:true,attributes:true,attributeFilter:['data-ss-lang-mode','lang']});
})();
</script>'''.replace('__SIMP__',simp_js).replace('__TRAD__',trad_js)
    block=START+'\n'+finalizer+'\n'+END
    if START in s:
        a=s.index(START); b=s.index(END,a)+len(END); s=s[:a]+block+s[b:]
    else:
        if '</body>' not in s: raise RuntimeError('Missing </body>')
        s=s.replace('</body>',block+'\n</body>',1)

    if re.findall(r'<style\b[^>]*>.*?</style>',s,re.S|re.I)!=styles_before: raise RuntimeError('Unexpected CSS change')
    if sorted(re.findall(r'assets/images/[A-Za-z0-9._-]+',s))!=assets_before: raise RuntimeError('Unexpected image asset change')
    if re.findall(r'en:"((?:\\.|[^"\\])*)"',s)!=en_before: raise RuntimeError('Unexpected English bundle change')
    if re.findall(r'ja:"((?:\\.|[^"\\])*)"',s)!=ja_before: raise RuntimeError('Unexpected Japanese bundle change')
    if s.count(START)!=1 or s.count('id="ss-traditional-chinese-finalizer"')!=1: raise RuntimeError('Traditional finalizer duplication')
    INDEX.write_text(s,encoding='utf-8')
    print('Prepared Traditional Chinese source/finalizer',counts,'map chars',len(simp))


def audit():
    s=INDEX.read_text(encoding='utf-8')
    audit_js=r'''<script>
window.addEventListener('load',function(){
 setTimeout(function(){
  var buttons=[].slice.call(document.querySelectorAll('.lang-switch button'));
  var trad=buttons.find(function(b){return !b.classList.contains('ss-lang-simplified')&&(b.textContent||'').trim()==='中'});if(trad)trad.click();
  setTimeout(function(){
   var toggle=document.querySelector('.career-toggle');if(toggle&&toggle.getAttribute('aria-expanded')!=='true')toggle.click();
   setTimeout(function(){
    var tradText=(document.body.innerText||'').replace(/\u00a0/g,' ').replace(/[ \t]+\n/g,'\n').replace(/\n{3,}/g,'\n\n').trim();
    var tradMode=document.documentElement.getAttribute('data-ss-lang-mode')||'',tradLang=document.documentElement.getAttribute('lang')||'';
    var simp=document.querySelector('.ss-lang-simplified');if(simp)simp.click();
    setTimeout(function(){
     var simpText=(document.body.innerText||'').replace(/\u00a0/g,' ').replace(/[ \t]+\n/g,'\n').replace(/\n{3,}/g,'\n\n').trim();
     var simpMode=document.documentElement.getAttribute('data-ss-lang-mode')||'',simpLang=document.documentElement.getAttribute('lang')||'';
     document.body.innerHTML='<pre id="audit-output"></pre>';
     document.getElementById('audit-output').textContent='TRAD_MODE='+tradMode+'\nTRAD_LANG='+tradLang+'\n---TRAD---\n'+tradText+'\n---SIMP META---\nSIMP_MODE='+simpMode+'\nSIMP_LANG='+simpLang+'\n---SIMP---\n'+simpText;
    },1900);
   },1200);
  },2100);
 },1000);
});
</script>'''
    ap=ROOT/'runtime-audit.html'; dp=ROOT/'.runtime-dom.html'
    ap.write_text(s.replace('</body>',audit_js+'\n</body>',1),encoding='utf-8')
    chrome=shutil.which('google-chrome') or shutil.which('chromium') or shutil.which('chromium-browser')
    if not chrome: raise RuntimeError('Chrome not found')
    server=subprocess.Popen([sys.executable,'-m','http.server','8000'],cwd=ROOT,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    try:
        time.sleep(.7)
        with dp.open('w',encoding='utf-8') as f:
            subprocess.run([chrome,'--headless','--no-sandbox','--disable-gpu','--window-size=1440,1300','--virtual-time-budget=12000','--dump-dom','http://127.0.0.1:8000/runtime-audit.html'],stdout=f,check=True)
        class P(HTMLParser):
            def __init__(self):super().__init__();self.on=False;self.buf=[]
            def handle_starttag(self,t,a):
                if t=='pre' and dict(a).get('id')=='audit-output':self.on=True
            def handle_endtag(self,t):
                if t=='pre' and self.on:self.on=False
            def handle_data(self,d):
                if self.on:self.buf.append(d)
        parser=P();parser.feed(dp.read_text(encoding='utf-8',errors='replace'));text=''.join(parser.buf)
        print(text[:20000])
        if 'TRAD_MODE=zhtw' not in text or 'TRAD_LANG=zh-Hant' not in text: raise RuntimeError('Traditional mode/lang failed')
        if 'SIMP_MODE=zhcn' not in text or 'SIMP_LANG=zh-Hans' not in text: raise RuntimeError('Simplified mode/lang failed')
        trad=text.split('---TRAD---\n',1)[1].split('\n---SIMP META---',1)[0]
        simp=text.split('---SIMP---\n',1)[1]
        required=['公司簡介','亞太經驗','核心市場','全球網絡','東京 / 日本','源自對體育運動的真摯熱愛與尊重，驅動我們所管理的每一項企劃與合作。','打破傳統產業壁壘，開創充滿創意的商業機會與前瞻性策略。','對頂尖表現的技術與工藝抱持高度欣賞，向所有卓越運動員與創作者致敬。','創辦人','總經理','體育行銷主管','日本商務開發總監','世界盃區域銷售與行銷經理','公司\n公司簡介','差異\n核心優勢','職涯\n專業歷程','網絡\n廣泛的影響力與資源管道','案例\n案例研究：Apple','洞察\n洞察與觀點','閱讀完整專欄','聯絡我們','立即聯絡我們','版權所有。','阪神虎','大阪']
        missing=[x for x in required if x not in trad]
        if missing: raise RuntimeError('Missing Traditional strings: '+repr(missing))
        cc=OpenCC('s2tw'); cleaned=trad.replace('简体中文','')
        suspects=[]
        for line in cleaned.splitlines():
            cv=cc.convert(line)
            if cv!=line:suspects.append((line,cv))
        if suspects:
            for a,b in suspects[:60]:print('RESIDUE',a,'=>',b)
            raise RuntimeError('Simplified characters remain in Traditional mode')
        for bad in ['公司简介','亚太经验','核心市场','全球网络','东京 / 日本','版权所有','日本语','繁体中文']:
            if bad in trad: raise RuntimeError('Traditional mode still contains: '+bad)
        for x in ['公司简介','亚太经验','核心市场','全球网络','东京 / 日本']:
            if x not in simp: raise RuntimeError('Simplified mode regression: '+x)
        for label in ['English','日本語','简体中文','繁體中文']:
            if label not in trad or label not in simp: raise RuntimeError('Dropdown label regression: '+label)
        print('Traditional Chinese runtime verified; Simplified mode preserved')
    finally:
        server.terminate()
        try:server.wait(timeout=3)
        except subprocess.TimeoutExpired:server.kill()
        for q in [ap,dp]:
            if q.exists():q.unlink()


if __name__=='__main__':
    patch();audit();subprocess.run(['git','diff','--check'],cwd=ROOT,check=True)
