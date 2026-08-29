from pathlib import Path
import re, subprocess, json, html
from urllib.parse import unquote

p=Path('index.html')
s=p.read_text(encoding='utf-8')

# Remove the heading copy accidentally inserted inside the Broad Influence subitem IIFE.
b0=s.find('<!-- Broad Influence framed subitems -->')
b1=s.find('<!-- /Broad Influence framed subitems -->')
if b0<0 or b1<b0: raise SystemExit('Broad Influence block not found')
seg=s[b0:b1]
mis=seg.find('  var ssHeadingCopy={')
q=seg.find('  var queued=false;\n  function queueEnhance')
if mis>=0:
    if q<mis: raise SystemExit('Could not isolate misplaced heading copy')
    seg=seg[:mis]+seg[q:]
    s=s[:b0]+seg+s[b1:]

# Remove legacy heading fallback that can restore older labels after DOM mutations.
s,n=re.subn(r'<!-- Reference major heading fallback START -->.*?<!-- Reference major heading fallback END -->\s*','',s,flags=re.S)
if n>1: raise SystemExit('Duplicate legacy heading fallback blocks')

START='<!-- SS SINGLE UNIFIED SECTION HEADING START -->'
END='<!-- SS SINGLE UNIFIED SECTION HEADING END -->'
a=s.find(START); b=s.find(END)
if a<0 or b<a: raise SystemExit('Unified heading block not found')

block=r'''<!-- SS SINGLE UNIFIED SECTION HEADING START -->
<style id="ss-single-heading-style">
.ss-unified-heading::before,.ss-unified-heading::after,.ss-unified-eyebrow::before,.ss-unified-eyebrow::after,.ss-unified-title::before,.ss-unified-title::after{content:none!important;display:none!important}
.ss-unified-heading svg,.ss-unified-heading i{display:none!important}
</style>
<script id="ss-single-heading-script">
(function(){
  var defs=[
    {id:'company',sels:['.major-insights-title','.section-title']},
    {id:'points',sels:['.section-title']},
    {id:'founder',sels:['.founder-copy .section-title']},
    {id:'experience',sels:['.section-title']},
    {id:'network',sels:['.major-insights-title','.section-title']},
    {id:'capabilities',sels:['.section-title']},
    {id:'insights',sels:['.insight-intro']}
  ];
  var copy={
    en:{
      points:['Difference','Points of Difference',''],
      experience:['Career','Professional Journey','Built across APAC'],
      network:['Network','Broad Influence and Access','Services rendered to:'],
      capabilities:['Case','Case Study Apple','Demonstrated high-level facilitation capability']
    },
    ja:{
      points:['差別化','私たちの強み',''],
      experience:['キャリア','プロフェッショナル・ジャーニー','APACで築いたキャリア'],
      network:['ネットワーク','幅広い影響力とアクセス','サービス提供先：'],
      capabilities:['ケース','ケーススタディ Apple','高水準のファシリテーション能力を実証']
    },
    zh:{
      points:['差異','核心優勢',''],
      experience:['職涯','專業歷程','深耕亞太地區'],
      network:['網絡','廣泛的影響力與資源管道','曾服務的對象包括：'],
      capabilities:['案例','案例研究 Apple','展現高水準的協調促成能力']
    }
  };
  var queued=false;
  function imp(el,map){Object.keys(map).forEach(function(k){el.style.setProperty(k,map[k],'important')})}
  function txt(el){return el?(el.textContent||'').replace(/\s+/g,' ').trim():''}
  function lang(){var a=document.querySelector('.lang-switch button.active'),t=txt(a);if(t==='日')return'ja';if(t==='中')return'zh';var h=(document.documentElement.getAttribute('lang')||'').toLowerCase();return h.indexOf('ja')===0?'ja':h.indexOf('zh')===0?'zh':'en'}
  function applyCopy(d,data){var row=(copy[lang()]||copy.en)[d.id];return row?{kicker:row[0],title:row[1],support:row[2]||''}:data}
  function allSources(section,d){var out=[];d.sels.forEach(function(sel){section.querySelectorAll(sel).forEach(function(el){if(!el.classList.contains('ss-unified-heading')&&out.indexOf(el)<0)out.push(el)})});return out}
  function score(el){var h=el.querySelector('h2'),k=el.querySelector('.heading-ref-row,.major-kicker-row,.hierarchy-kicker-row,.eyebrow,.section-kicker,.major-kicker,.hierarchy-kicker');return(txt(h)?10:0)+(txt(k)?5:0)+(el.dataset.ssHeadingSource==='1'?50:0)}
  function chooseSource(section,d){var a=allSources(section,d);if(!a.length)return null;a.sort(function(x,y){return score(y)-score(x)});var src=a[0];src.dataset.ssHeadingSource='1';a.forEach(function(el){imp(el,{display:'none',visibility:'hidden',height:'0px','min-height':'0px',margin:'0px',padding:'0px',overflow:'hidden'})});return src}
  function extract(src,d){var h=src.querySelector('h2'),k=src.querySelector('.heading-ref-row,.major-kicker-row,.hierarchy-kicker-row,.eyebrow,.section-kicker,.major-kicker,.hierarchy-kicker'),title=txt(h),kicker=txt(k);if(!kicker){var f={company:'Company',points:'Difference',founder:'Founder',experience:'Career',network:'Network',capabilities:'Case',insights:'Insights & Perspectives'};kicker=f[d.id]||''}if(!title)title=kicker;var support='',sup=src.querySelector('.hierarchy-support,.major-support,.founder-name-support');if(sup)support=txt(sup);if(support===title||support===kicker)support='';return{kicker:kicker,title:title,support:support}}
  function make(section,src,d,data){
    var wrap=section.querySelector(':scope .ss-unified-heading[data-ss-section="'+d.id+'"]');
    if(!wrap){wrap=document.createElement('div');wrap.className='ss-unified-heading';wrap.dataset.ssSection=d.id;var eye=document.createElement('div');eye.className='ss-unified-eyebrow';var rule=document.createElement('span');rule.className='ss-unified-rule';rule.setAttribute('aria-hidden','true');var kl=document.createElement('span');kl.className='ss-unified-kicker';eye.appendChild(rule);eye.appendChild(kl);var h=document.createElement('h2');h.className='ss-unified-title';var sp=document.createElement('p');sp.className='ss-unified-support';wrap.appendChild(eye);wrap.appendChild(h);wrap.appendChild(sp);src.parentNode.insertBefore(wrap,src)}
    var eye=wrap.querySelector('.ss-unified-eyebrow'),rule=wrap.querySelector('.ss-unified-rule'),kl=wrap.querySelector('.ss-unified-kicker'),h=wrap.querySelector('.ss-unified-title'),sp=wrap.querySelector('.ss-unified-support');
    if(txt(kl)!==data.kicker)kl.textContent=data.kicker;if(txt(h)!==data.title)h.textContent=data.title;if(txt(sp)!==data.support)sp.textContent=data.support;
    imp(wrap,{position:'relative',display:'block','box-sizing':'border-box',width:'100%','max-width':'760px',margin:'0 0 34px 0',padding:'0','text-align':'left','font-family':'Arial, Helvetica, sans-serif',background:'none',border:'0','box-shadow':'none',transform:'none'});
    imp(eye,{display:'flex','align-items':'center','justify-content':'flex-start',gap:'12px',width:'fit-content','max-width':'100%',margin:'0 0 18px 0',padding:'0','font-family':'Arial, Helvetica, sans-serif','font-size':'11px','font-weight':'900','line-height':'16.5px','letter-spacing':'1.87px',color:'rgb(200, 181, 110)','text-transform':'none','text-align':'left',background:'none',border:'0','box-shadow':'none',transform:'none'});
    imp(rule,{display:'block',width:'28px',height:'1px','min-width':'28px','flex':'0 0 28px',margin:'0',padding:'0',background:'rgb(215, 169, 54)',border:'0','border-radius':'0','box-shadow':'none',transform:'none'});
    imp(kl,{display:'inline',margin:'0',padding:'0','font':'inherit','letter-spacing':'inherit',color:'inherit','text-align':'left','text-transform':'none',background:'none',border:'0','box-shadow':'none'});
    imp(h,{display:'block',width:'fit-content','max-width':'100%',margin:data.support?'0 0 14px 0':'0',padding:'0','font-family':'Arial, Helvetica, sans-serif','font-size':'clamp(34px, 4vw, 58px)','font-weight':'700','line-height':'normal','letter-spacing':'-0.04em',color:'rgb(247, 245, 239)','text-align':'left','text-transform':'none','white-space':'normal',background:'none',border:'0','box-shadow':'none','text-shadow':'none',transform:'none'});
    imp(sp,{display:data.support?'block':'none',width:'100%','max-width':'760px',margin:'0',padding:'0','font-family':'Arial, Helvetica, sans-serif','font-size':'15px','font-weight':'500','line-height':'1.5','letter-spacing':'0',color:'#9da7b4','text-align':'left',background:'none',border:'0','box-shadow':'none'});
  }
  function run(){queued=false;defs.forEach(function(d){var section=document.getElementById(d.id);if(!section)return;var src=chooseSource(section,d);if(!src)return;make(section,src,d,applyCopy(d,extract(src,d)))})}
  function queue(){if(queued)return;queued=true;requestAnimationFrame(run)}
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',queue);else queue();
  new MutationObserver(queue).observe(document.body,{childList:true,subtree:true,characterData:true});
  document.addEventListener('click',function(e){if(e.target.closest&&e.target.closest('.lang-switch'))setTimeout(queue,0)});
})();
</script>
<!-- SS SINGLE UNIFIED SECTION HEADING END -->'''

s=s[:a]+block+s[b+len(END):]
p.write_text(s,encoding='utf-8')
out=p.read_text(encoding='utf-8')
assert out.count(START)==1 and out.count(END)==1
assert 'Reference major heading fallback START' not in out
assert 'var ssHeadingCopy={' not in out
required=["points:['Difference','Points of Difference','']","experience:['Career','Professional Journey','Built across APAC']","network:['Network','Broad Influence and Access','Services rendered to:']","capabilities:['Case','Case Study Apple','Demonstrated high-level facilitation capability']"]
for x in required:
    if x not in out: raise SystemExit('Missing required heading copy: '+x)

m=re.search(r'<script id="ss-single-heading-script">(.*?)</script>',out,re.S)
if not m: raise SystemExit('Unified heading script missing')
t=Path('.heading-check.js');t.write_text(m.group(1),encoding='utf-8');subprocess.run(['node','--check',str(t)],check=True);t.unlink()

probe=r'''<script>setTimeout(function(){var e={points:['Difference','Points of Difference',''],experience:['Career','Professional Journey','Built across APAC'],network:['Network','Broad Influence and Access','Services rendered to:'],capabilities:['Case','Case Study Apple','Demonstrated high-level facilitation capability']},r={};Object.keys(e).forEach(function(id){var w=document.querySelector('#'+id+' .ss-unified-heading[data-ss-section="'+id+'"]'),k=w&&w.querySelector('.ss-unified-kicker'),h=w&&w.querySelector('.ss-unified-title'),p=w&&w.querySelector('.ss-unified-support'),v=[k&&k.textContent.trim(),h&&h.textContent.trim(),p&&p.textContent.trim()],ps=p&&getComputedStyle(p);r[id]={v:v,ok:!!w&&JSON.stringify(v)===JSON.stringify(e[id]),left:!!h&&getComputedStyle(h).textAlign==='left',support:e[id][2]?ps.display!=='none':ps.display==='none'}});r.ALL=Object.keys(e).every(function(id){return r[id].ok&&r[id].left&&r[id].support});document.body.setAttribute('data-ss-heading-probe',encodeURIComponent(JSON.stringify(r)))},2600)</script>'''
v=Path('.heading-verify.html');v.write_text(out.replace('</body>',probe+'\n</body>',1),encoding='utf-8')
chrome='/usr/bin/google-chrome' if Path('/usr/bin/google-chrome').exists() else '/usr/bin/chromium'
res=subprocess.run([chrome,'--headless=new','--no-sandbox','--disable-gpu','--allow-file-access-from-files','--virtual-time-budget=7000','--window-size=1280,1400','--dump-dom',v.resolve().as_uri()],capture_output=True,text=True)
mm=re.search(r'data-ss-heading-probe="([^"]+)"',res.stdout)
if not mm: raise SystemExit('Runtime probe missing')
data=json.loads(unquote(html.unescape(mm.group(1))))
print('HEADING_RUNTIME',json.dumps(data,ensure_ascii=False))
if not data.get('ALL'): raise SystemExit('Runtime heading verification failed')
v.unlink()

wf=Path('.github/workflows/validate-heading-integrity.yml')
wf.parent.mkdir(parents=True,exist_ok=True)
wf.write_text('''name: Validate heading integrity\non:\n  push:\n    branches: [main]\n    paths:\n      - index.html\n      - .github/workflows/validate-heading-integrity.yml\n  workflow_dispatch:\npermissions:\n  contents: read\njobs:\n  validate:\n    runs-on: ubuntu-latest\n    steps:\n      - uses: actions/checkout@v4\n      - name: Check single heading source of truth\n        shell: bash\n        run: |\n          python - <<'PY'\n          from pathlib import Path\n          import re, subprocess\n          s=Path('index.html').read_text(encoding='utf-8')\n          start='<!-- SS SINGLE UNIFIED SECTION HEADING START -->'; end='<!-- SS SINGLE UNIFIED SECTION HEADING END -->'\n          assert s.count(start)==1 and s.count(end)==1, 'Unified heading block must exist exactly once'\n          assert 'Reference major heading fallback START' not in s, 'Legacy heading fallback returned'\n          assert 'var ssHeadingCopy={' not in s, 'Misplaced legacy heading copy returned'\n          a=s.index(start); b=s.index(end,a); block=s[a:b]\n          for x in [\"points:['Difference','Points of Difference','']\",\"experience:['Career','Professional Journey','Built across APAC']\",\"network:['Network','Broad Influence and Access','Services rendered to:']\",\"capabilities:['Case','Case Study Apple','Demonstrated high-level facilitation capability']\"]:\n              assert x in block, 'Required heading copy missing: '+x\n          m=re.search(r'<script id=\\\"ss-single-heading-script\\\">(.*?)</script>',block,re.S); assert m, 'Unified heading script missing'\n          t=Path('.heading-check.js'); t.write_text(m.group(1),encoding='utf-8'); subprocess.run(['node','--check',str(t)],check=True); t.unlink()\n          print('Heading integrity check passed')\n          PY\n''',encoding='utf-8')
print('Stabilized heading controller and installed regression guard.')
