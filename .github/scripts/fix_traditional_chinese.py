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


def decode_js(body):
    out = []
    i = 0
    common = {'n':'\n','r':'\r','t':'\t','b':'\b','f':'\f','v':'\v','0':'\0','"':'"',"'":"'",'\\':'\\','/':'/'}
    while i < len(body):
        if body[i] != '\\':
            out.append(body[i]); i += 1; continue
        if i + 1 >= len(body):
            out.append('\\'); break
        k = body[i + 1]
        if k == 'u' and i + 5 < len(body) and re.fullmatch(r'[0-9a-fA-F]{4}', body[i+2:i+6]):
            code = int(body[i+2:i+6], 16); i += 6
            if 0xD800 <= code <= 0xDBFF and i + 5 < len(body) and body[i:i+2] == '\\u' and re.fullmatch(r'[0-9a-fA-F]{4}', body[i+2:i+6]):
                low = int(body[i+2:i+6], 16)
                if 0xDC00 <= low <= 0xDFFF:
                    code = 0x10000 + ((code - 0xD800) << 10) + (low - 0xDC00); i += 6
            out.append(chr(code)); continue
        if k == 'x' and i + 3 < len(body) and re.fullmatch(r'[0-9a-fA-F]{2}', body[i+2:i+4]):
            out.append(chr(int(body[i+2:i+4], 16))); i += 4; continue
        out.append(common.get(k, k)); i += 2
    return ''.join(out)


def patch_index():
    s = INDEX.read_text(encoding='utf-8')
    before = s
    styles_before = re.findall(r'<style\b[^>]*>.*?</style>', before, re.S | re.I)
    assets_before = sorted(re.findall(r'assets/images/[A-Za-z0-9._-]+', before))
    en_before = re.findall(r'en:"((?:\\.|[^"\\])*)"', before)
    ja_before = re.findall(r'ja:"((?:\\.|[^"\\])*)"', before)

    cc = OpenCC('s2tw')
    semantic = {
        '公司特色': '公司簡介',
        '案例研究 Apple': '案例研究：Apple',
        '案例研究: Apple': '案例研究：Apple',
        '創始人': '創辦人',
        '2015 FIFA U-20 世界杯區域銷售與行銷經理': '2015 FIFA U-20 世界盃區域銷售與行銷經理',
    }
    counts = {'total': 0, 'changed': 0}
    pat = re.compile(r'zh:"((?:\\.|[^"\\])*)"')

    def zh_repl(m):
        counts['total'] += 1
        raw = m.group(1)
        text = decode_js(raw)
        converted = cc.convert(text)
        converted = semantic.get(converted, converted)
        enc = json.dumps(converted, ensure_ascii=True)[1:-1]
        if enc != raw:
            counts['changed'] += 1
        return 'zh:"' + enc + '"'

    s = pat.sub(zh_repl, s)
    if counts['total'] < 80 or counts['changed'] < 40:
        raise RuntimeError(f'Unexpected Chinese localization coverage: {counts}')

    start = '<!-- SS FOUR LANGUAGE SWITCH START -->'
    end = '<!-- SS FOUR LANGUAGE SWITCH END -->'
    if s.count(start) != 1 or s.count(end) != 1:
        raise RuntimeError('Four-language controller markers are not unique')
    a = s.index(start)
    b = s.index(end, a) + len(end)
    old_block = s[a:b]
    style_m = re.search(r'<style id="ss-four-language-style">.*?</style>', old_block, re.S)
    from_m = re.search(r'var from="([^"]*)";', old_block, re.S)
    to_m = re.search(r'var to="([^"]*)";', old_block, re.S)
    if not (style_m and from_m and to_m):
        raise RuntimeError('Could not recover current four-language style/map')
    style = style_m.group(0)
    from_js = json.dumps(from_m.group(1), ensure_ascii=False)
    to_js = json.dumps(to_m.group(1), ensure_ascii=False)

    controller = r'''<script id="ss-four-language-script">
(function(){
  var from=__FROM__;
  var to=__TO__;
  var cmap=Object.create(null);
  for(var i=0;i<from.length;i++)cmap[from.charAt(i)]=to.charAt(i);
  window.__ssToSimplified=function(value){
    return String(value==null?'':value).replace(/[\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff]/g,function(ch){return cmap[ch]||ch});
  };

  var mode='en';
  var internal=false;
  var scheduled=false;
  var translating=false;
  var originals=new WeakMap();
  var attrOriginals=new WeakMap();

  function desiredLang(){return mode==='ja'?'ja':mode==='zhcn'?'zh-Hans':mode==='zhtw'?'zh-Hant':'en'}
  function enforceLang(){var v=desiredLang();if(document.documentElement.getAttribute('lang')!==v)document.documentElement.setAttribute('lang',v)}
  function setMode(next){mode=next;document.documentElement.setAttribute('data-ss-lang-mode',next);enforceLang()}
  function root(){return document.querySelector('.lang-switch')}
  function baseButtons(){
    var r=root();if(!r)return null;
    var list=Array.prototype.filter.call(r.querySelectorAll('button'),function(btn){return !btn.classList.contains('ss-lang-simplified')});
    if(list.length<3)return null;
    return {root:r,en:list[0],ja:list[1],zh:list[2]};
  }
  function normalizeBaseButtons(b){
    if(!b)return;
    if((b.en.textContent||'').trim()!=='EN')b.en.textContent='EN';
    if((b.ja.textContent||'').trim()!=='日')b.ja.textContent='日';
    if((b.zh.textContent||'').trim()!=='中')b.zh.textContent='中';
    b.en.dataset.ssLabel='EN';b.en.setAttribute('aria-label','EN');b.en.setAttribute('title','EN');
    b.ja.dataset.ssLabel='日';b.ja.setAttribute('aria-label','日');b.ja.setAttribute('title','日');
    b.zh.dataset.ssLabel='繁';b.zh.setAttribute('aria-label','繁');b.zh.setAttribute('title','繁');
  }
  function ensureUI(){
    var b=baseButtons();if(!b)return null;
    normalizeBaseButtons(b);b.root.classList.add('ss-four-language-ready');
    var simp=b.root.querySelector('button.ss-lang-simplified');
    if(!simp){simp=document.createElement('button');simp.type='button';simp.className='ss-lang-simplified';simp.textContent='中';b.root.insertBefore(simp,b.zh)}
    simp.dataset.ssLabel='简';simp.setAttribute('aria-label','简');simp.setAttribute('title','简');
    if(mode==='zhcn'){
      Array.prototype.forEach.call(b.root.querySelectorAll('button'),function(x){x.classList.remove('active')});
      simp.classList.add('active');
    }
    return {root:b.root,en:b.en,ja:b.ja,zh:b.zh,simp:simp};
  }
  function isSkipped(el){return !el||!!el.closest('script,style,noscript,textarea,.lang-switch,[data-ss-no-simplify]')}
  function simplifyTextNode(node){
    var p=node.parentElement;if(isSkipped(p))return;
    var current=node.nodeValue||'';
    var old=originals.get(node);
    if(old==null){old=current;originals.set(node,old)}
    else{
      var oldSimp=window.__ssToSimplified(old);
      if(current!==old&&current!==oldSimp){old=current;originals.set(node,old)}
    }
    var next=window.__ssToSimplified(old);if(current!==next)node.nodeValue=next;
  }
  function simplifyAttrs(el){
    if(isSkipped(el)||!el.getAttribute)return;
    var names=['title','aria-label','alt','placeholder'];
    var store=attrOriginals.get(el)||{};
    names.forEach(function(name){
      if(!el.hasAttribute(name))return;
      var current=el.getAttribute(name)||'';var old=store[name];
      if(old==null){old=current;store[name]=old}
      else{var oldSimp=window.__ssToSimplified(old);if(current!==old&&current!==oldSimp){old=current;store[name]=old}}
      var next=window.__ssToSimplified(old);if(current!==next)el.setAttribute(name,next);
    });
    attrOriginals.set(el,store);
  }
  function simplifyTree(scope){
    if(mode!=='zhcn'||translating)return;
    translating=true;
    try{
      var base=scope&&scope.nodeType?scope:document.body;
      if(base.nodeType===3){simplifyTextNode(base);return}
      if(base.nodeType!==1&&base.nodeType!==9&&base.nodeType!==11)return;
      if(base.nodeType===1)simplifyAttrs(base);
      var tw=document.createTreeWalker(base,NodeFilter.SHOW_TEXT);var n;while((n=tw.nextNode()))simplifyTextNode(n);
      if(base.querySelectorAll)Array.prototype.forEach.call(base.querySelectorAll('*'),simplifyAttrs);
    }finally{translating=false}
  }
  function restoreTree(scope){
    if(translating)return;translating=true;
    try{
      var base=scope&&scope.nodeType?scope:document.body;var nodes=[];
      if(base.nodeType===3)nodes=[base];
      else if(base.nodeType===1||base.nodeType===9||base.nodeType===11){var tw=document.createTreeWalker(base,NodeFilter.SHOW_TEXT);var n;while((n=tw.nextNode()))nodes.push(n)}
      nodes.forEach(function(node){var old=originals.get(node);if(old!=null&&node.nodeValue!==old)node.nodeValue=old});
      var els=[];if(base.nodeType===1)els.push(base);if(base.querySelectorAll)els=els.concat(Array.prototype.slice.call(base.querySelectorAll('*')));
      els.forEach(function(el){var store=attrOriginals.get(el);if(!store)return;Object.keys(store).forEach(function(name){if(el.getAttribute(name)!==store[name])el.setAttribute(name,store[name])})});
    }finally{translating=false}
  }
  function apply(){scheduled=false;var ui=ensureUI();if(!ui)return;enforceLang();if(mode==='zhcn')simplifyTree(document.body)}
  function queue(){if(scheduled)return;scheduled=true;requestAnimationFrame(apply)}

  document.addEventListener('click',function(event){
    var btn=event.target.closest&&event.target.closest('.lang-switch button');if(!btn)return;
    var ui=ensureUI();if(!ui)return;
    if(btn.classList.contains('ss-lang-simplified')){
      event.preventDefault();event.stopImmediatePropagation();
      setMode('zhcn');
      internal=true;try{ui.zh.click()}finally{internal=false}
      Array.prototype.forEach.call(ui.root.querySelectorAll('button'),function(x){x.classList.remove('active')});ui.simp.classList.add('active');
      setTimeout(queue,0);setTimeout(queue,80);setTimeout(queue,260);return;
    }
    if(internal)return;
    if(mode==='zhcn')restoreTree(document.body);
    var token=(btn.textContent||'').trim();
    if(token==='日')setMode('ja');else if(token==='中')setMode('zhtw');else setMode('en');
    Array.prototype.forEach.call(ui.root.querySelectorAll('button'),function(x){x.classList.remove('active')});btn.classList.add('active');
    setTimeout(queue,0);setTimeout(queue,100);
  },true);

  var observer=new MutationObserver(function(mutations){
    if(translating)return;enforceLang();
    if(mode==='zhcn')mutations.forEach(function(m){if(m.type==='characterData')simplifyTree(m.target);else Array.prototype.forEach.call(m.addedNodes||[],function(n){simplifyTree(n)})});
    queue();
  });
  function start(){
    var ui=ensureUI();
    if(ui){if(ui.ja.classList.contains('active'))setMode('ja');else if(ui.zh.classList.contains('active'))setMode('zhtw');else setMode('en')}else setMode('en');
    observer.observe(document.documentElement,{childList:true,subtree:true,characterData:true,attributes:true,attributeFilter:['lang']});queue();
  }
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',start,{once:true});else start();
})();
</script>'''.replace('__FROM__', from_js).replace('__TO__', to_js)
    new_block = start + '\n' + style + '\n' + controller + '\n' + end
    s = s[:a] + new_block + s[b:]

    old = "    return x==='日'?'ja':x==='中'?'zh':'en';"
    new = "    var mode=document.documentElement.getAttribute('data-ss-lang-mode')||'';\n    if(mode==='zhtw'||mode==='zhcn')return 'zh';\n    if(mode==='ja')return 'ja';\n    return x==='日'?'ja':x==='中'?'zh':'en';"
    if old not in s: raise RuntimeError('Section navigation language detector not found')
    s = s.replace(old, new, 1)
    s = s.replace("capabilities:'案例研究 Apple'", "capabilities:'案例研究：Apple'", 1)

    old = "function lang(){var a=document.querySelector('.lang-switch button.active'),t=txt(a);if(t==='日')return'ja';if(t==='中')return'zh';var h=(document.documentElement.getAttribute('lang')||'').toLowerCase();return h.indexOf('ja')===0?'ja':h.indexOf('zh')===0?'zh':'en'}"
    new = "function lang(){var m=document.documentElement.getAttribute('data-ss-lang-mode')||'';if(m==='zhtw'||m==='zhcn')return'zh';if(m==='ja')return'ja';var a=document.querySelector('.lang-switch button.active'),t=txt(a);if(t==='日')return'ja';if(t==='中')return'zh';var h=(document.documentElement.getAttribute('lang')||'').toLowerCase();return h.indexOf('ja')===0?'ja':h.indexOf('zh')===0?'zh':'en'}"
    if old not in s: raise RuntimeError('Unified heading language detector not found')
    s = s.replace(old, new, 1)

    old = """    zh:{
      company:['公司','公司簡介',''],
      points:['差異','核心優勢',''],
      experience:['職涯','專業歷程','深耕亞太地區'],
      network:['網絡','廣泛的影響力與資源管道','曾服務的對象包括：'],
      capabilities:['案例','案例研究 Apple','展現高水準的協調促成能力']
    }"""
    new = """    zh:{
      company:['公司','公司簡介',''],
      points:['差異','核心優勢',''],
      founder:['創辦人','Sam L. Pearson',''],
      experience:['職涯','專業歷程','深耕亞太地區'],
      network:['網絡','廣泛的影響力與資源管道','曾服務的對象包括：'],
      capabilities:['案例','案例研究：Apple','展現高水準的協調促成能力'],
      insights:['洞察','洞察與觀點','專家觀點']
    }"""
    if old not in s: raise RuntimeError('Unified Chinese heading map not found')
    s = s.replace(old, new, 1)

    if re.findall(r'<style\b[^>]*>.*?</style>', s, re.S | re.I) != styles_before:
        raise RuntimeError('Unexpected CSS/style change')
    if sorted(re.findall(r'assets/images/[A-Za-z0-9._-]+', s)) != assets_before:
        raise RuntimeError('Unexpected image asset change')
    if re.findall(r'en:"((?:\\.|[^"\\])*)"', s) != en_before:
        raise RuntimeError('Unexpected English bundle change')
    if re.findall(r'ja:"((?:\\.|[^"\\])*)"', s) != ja_before:
        raise RuntimeError('Unexpected Japanese bundle change')
    if s.count(start) != 1 or s.count('id="ss-four-language-script"') != 1:
        raise RuntimeError('Language controller duplication detected')

    INDEX.write_text(s, encoding='utf-8')
    print(f'Patched Chinese localization {counts}; CSS/assets/EN/JA unchanged')


def render_and_verify():
    s = INDEX.read_text(encoding='utf-8')
    audit = r'''<script>
window.addEventListener('load',function(){
  setTimeout(function(){
    var buttons=[].slice.call(document.querySelectorAll('.lang-switch button'));
    var trad=buttons.find(function(b){return !b.classList.contains('ss-lang-simplified')&&(b.textContent||'').trim()==='中'});
    if(trad)trad.click();
    setTimeout(function(){
      var toggle=document.querySelector('.career-toggle');if(toggle&&toggle.getAttribute('aria-expanded')!=='true')toggle.click();
      setTimeout(function(){
        var tradText=(document.body.innerText||'').replace(/\u00a0/g,' ').replace(/[ \t]+\n/g,'\n').replace(/\n{3,}/g,'\n\n').trim();
        var tradMode=document.documentElement.getAttribute('data-ss-lang-mode')||'';
        var tradLang=document.documentElement.getAttribute('lang')||'';
        var simp=document.querySelector('.ss-lang-simplified');if(simp)simp.click();
        setTimeout(function(){
          var simpText=(document.body.innerText||'').replace(/\u00a0/g,' ').replace(/[ \t]+\n/g,'\n').replace(/\n{3,}/g,'\n\n').trim();
          var simpMode=document.documentElement.getAttribute('data-ss-lang-mode')||'';
          var simpLang=document.documentElement.getAttribute('lang')||'';
          document.body.innerHTML='<pre id="audit-output"></pre>';
          document.getElementById('audit-output').textContent='TRAD_MODE='+tradMode+'\nTRAD_LANG='+tradLang+'\n---TRAD---\n'+tradText+'\n---SIMP META---\nSIMP_MODE='+simpMode+'\nSIMP_LANG='+simpLang+'\n---SIMP---\n'+simpText;
        },1800);
      },1000);
    },1800);
  },1000);
});
</script>'''
    audit_path = ROOT / 'runtime-audit.html'
    audit_path.write_text(s.replace('</body>', audit + '\n</body>', 1), encoding='utf-8')
    chrome = shutil.which('google-chrome') or shutil.which('chromium') or shutil.which('chromium-browser')
    if not chrome:
        raise RuntimeError('Chrome not found')
    server = subprocess.Popen([sys.executable, '-m', 'http.server', '8000'], cwd=ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        time.sleep(0.6)
        dom_path = ROOT / '.runtime-dom.html'
        with dom_path.open('w', encoding='utf-8') as f:
            subprocess.run([chrome, '--headless', '--no-sandbox', '--disable-gpu', '--window-size=1440,1300', '--virtual-time-budget=11000', '--dump-dom', 'http://127.0.0.1:8000/runtime-audit.html'], stdout=f, check=True)
        class P(HTMLParser):
            def __init__(self): super().__init__(); self.on=False; self.buf=[]
            def handle_starttag(self, tag, attrs):
                if tag == 'pre' and dict(attrs).get('id') == 'audit-output': self.on=True
            def handle_endtag(self, tag):
                if tag == 'pre' and self.on: self.on=False
            def handle_data(self, data):
                if self.on: self.buf.append(data)
        parser=P(); parser.feed(dom_path.read_text(encoding='utf-8', errors='replace'))
        text=''.join(parser.buf)
        print(text[:18000])
        if 'TRAD_MODE=zhtw' not in text or 'TRAD_LANG=zh-Hant' not in text:
            raise RuntimeError('Traditional mode/lang failed')
        if 'SIMP_MODE=zhcn' not in text or 'SIMP_LANG=zh-Hans' not in text:
            raise RuntimeError('Simplified mode/lang failed')
        trad=text.split('---TRAD---\n',1)[1].split('\n---SIMP META---',1)[0]
        simp=text.split('---SIMP---\n',1)[1]
        required=[
            '公司簡介','亞太經驗','核心市場','全球網絡','東京 / 日本',
            '源自對體育運動的真摯熱愛與尊重，驅動我們所管理的每一項企劃與合作。',
            '打破傳統產業壁壘，開創充滿創意的商業機會與前瞻性策略。',
            '對頂尖表現的技術與工藝抱持高度欣賞，向所有卓越運動員與創作者致敬。',
            '創辦人','總經理','體育行銷主管','日本商務開發總監','世界盃區域銷售與行銷經理',
            '公司\n公司簡介','差異\n核心優勢','職涯\n專業歷程','網絡\n廣泛的影響力與資源管道','案例\n案例研究：Apple','洞察\n洞察與觀點',
            '閱讀完整專欄','聯絡我們','立即聯絡我們','版權所有。'
        ]
        missing=[x for x in required if x not in trad]
        if missing:
            raise RuntimeError('Missing expected Traditional strings: '+repr(missing))
        cleaned=trad.replace('简体中文','')
        cc=OpenCC('s2tw')
        suspects=[]
        for line in cleaned.splitlines():
            converted=cc.convert(line)
            if converted != line:
                suspects.append((line, converted))
        if suspects:
            for old,new in suspects[:50]: print('SIMPLIFIED RESIDUE:',old,'=>',new)
            raise RuntimeError('Simplified characters remain in Traditional runtime')
        for x in ['公司简介','亚太经验','核心市场','全球网络','东京 / 日本']:
            if x not in simp:
                raise RuntimeError('Simplified mode regression: '+x)
        for label in ['English','日本語','简体中文','繁體中文']:
            if label not in trad or label not in simp:
                raise RuntimeError('Language dropdown label regression: '+label)
        print('Traditional and Simplified runtime localization verified')
    finally:
        server.terminate()
        try: server.wait(timeout=3)
        except subprocess.TimeoutExpired: server.kill()
        for q in [audit_path, ROOT/'.runtime-dom.html']:
            if q.exists(): q.unlink()


if __name__ == '__main__':
    patch_index()
    render_and_verify()
    subprocess.run(['git','diff','--check'], cwd=ROOT, check=True)
