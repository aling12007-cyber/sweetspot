from pathlib import Path
import shutil,subprocess,sys,time
from html.parser import HTMLParser
from opencc import OpenCC

ROOT=Path(__file__).resolve().parents[2]
INDEX=ROOT/'index.html'

class PreParser(HTMLParser):
    def __init__(self):super().__init__();self.on=False;self.buf=[]
    def handle_starttag(self,t,a):
        if t=='pre' and dict(a).get('id')=='audit-output':self.on=True
    def handle_endtag(self,t):
        if t=='pre' and self.on:self.on=False
    def handle_data(self,d):
        if self.on:self.buf.append(d)

def run_mode(value,name):
    s=INDEX.read_text(encoding='utf-8')
    audit=f'''<script>
window.addEventListener('load',function(){{setTimeout(function(){{
 var sel=document.querySelector('.lang-dropdown-select');
 if(!sel||sel.options.length<4){{document.body.innerHTML='<pre id="audit-output">NO DROPDOWN</pre>';return;}}
 sel.value='{value}';sel.dispatchEvent(new Event('change',{{bubbles:true}}));
 setTimeout(function(){{
   var labels=[].slice.call(sel.options).map(function(o){{return o.text}}).join(' / ');
   var mode=document.documentElement.getAttribute('data-ss-lang-mode')||'';
   var lang=document.documentElement.getAttribute('lang')||'';
   var hero=((document.querySelector('.hero-copy h2')||{{}}).textContent||'').trim();
   var stat=((document.querySelector('.stats span')||{{}}).textContent||'').trim();
   var heads=[].slice.call(document.querySelectorAll('.ss-unified-heading')).map(function(h){{return ((h.querySelector('.ss-unified-kicker')||{{}}).textContent||'').trim()+' > '+((h.querySelector('.ss-unified-title')||{{}}).textContent||'').trim()+' > '+((h.querySelector('.ss-unified-support')||{{}}).textContent||'').trim()}}).join(' || ');
   var body=(document.body.innerText||'').replace(/\\u00a0/g,' ');
   document.body.innerHTML='<pre id="audit-output"></pre>';
   document.getElementById('audit-output').textContent='MODE='+mode+'\\nLANG='+lang+'\\nDROP='+labels+'\\nHERO='+hero+'\\nSTAT='+stat+'\\nHEADINGS='+heads+'\\nBODY='+body;
 }},1700);
}},900)}});
</script>'''
    html_path=ROOT/f'audit-{name}.html';dom_path=ROOT/f'.dom-{name}.html'
    html_path.write_text(s.replace('</body>',audit+'\n</body>',1),encoding='utf-8')
    chrome=shutil.which('google-chrome') or shutil.which('chromium') or shutil.which('chromium-browser')
    if not chrome:raise RuntimeError('Chrome not found')
    server=subprocess.Popen([sys.executable,'-m','http.server','8000'],cwd=ROOT,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    try:
        time.sleep(.6)
        with dom_path.open('w',encoding='utf-8') as f:
            subprocess.run([chrome,'--headless','--no-sandbox','--disable-gpu','--window-size=1440,1300','--virtual-time-budget=7000','--dump-dom',f'http://127.0.0.1:8000/{html_path.name}'],stdout=f,check=True)
        p=PreParser();p.feed(dom_path.read_text(encoding='utf-8',errors='replace'));text=''.join(p.buf)
        print(f'--- {name.upper()} ---\n'+text[:24000])
        return text
    finally:
        server.terminate()
        try:server.wait(timeout=3)
        except subprocess.TimeoutExpired:server.kill()
        for q in (html_path,dom_path):
            if q.exists():q.unlink()

def main():
    trad_drop='English / 日本語 / 简体中文 / 繁體中文'
    simp_drop='English / 日本语 / 简体中文 / 繁体中文'
    trad=run_mode('3','trad')
    if 'MODE=zhtw' not in trad or 'LANG=zh-Hant' not in trad:raise RuntimeError('Traditional mode/lang failed')
    if 'DROP='+trad_drop not in trad:raise RuntimeError('Traditional dropdown changed')
    required=['歡迎來到','公司簡介','亞太經驗','核心市場','全球網絡','東京 / 日本','策略。連結。執行。','創辦人','聯絡我們']
    miss=[x for x in required if x not in trad]
    if miss:raise RuntimeError('Traditional missing '+repr(miss))
    heading_required=['公司 > 公司簡介','差異 > 核心優勢','職涯 > 專業歷程','網絡 > 廣泛的影響力與資源管道','案例 > 案例研究：Apple']
    hm=[x for x in heading_required if x not in trad]
    if hm:raise RuntimeError('Traditional headings missing '+repr(hm))
    cleaned=trad.replace('简体中文','')
    residues=[];cc=OpenCC('s2tw')
    for line in cleaned.splitlines():
        cv=cc.convert(line)
        if cv!=line:residues.append((line,cv))
    if residues:raise RuntimeError('Traditional runtime residues '+repr(residues[:20]))

    simp=run_mode('2','simp')
    if 'MODE=zhcn' not in simp or 'LANG=zh-Hans' not in simp:raise RuntimeError('Simplified mode/lang failed')
    if 'DROP='+simp_drop not in simp:raise RuntimeError('Simplified dropdown changed')
    for x in ['欢迎来到','公司简介','亚太经验','核心市场','全球网络','东京 / 日本']:
        if x not in simp:raise RuntimeError('Simplified missing '+x)
    for x in ['公司 > 公司简介','差异 > 核心优势','职涯 > 专业历程','网络 > 广泛的影响力与资源管道','案例 > 案例研究：Apple']:
        if x not in simp:raise RuntimeError('Simplified heading missing '+x)
    print('Isolated Traditional and Simplified runtime verification passed')

if __name__=='__main__':main()
