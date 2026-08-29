from pathlib import Path
import re, subprocess, json, html
from urllib.parse import unquote

p=Path('index.html')
s=p.read_text(encoding='utf-8')

# Remove prior paired heading experiments so they cannot keep fighting the final system.
paired=[
('Reference major heading format START','Reference major heading format END'),
('Heading alignment founder cleanup START','Heading alignment founder cleanup END'),
('Hierarchy heading roles START','Hierarchy heading roles END'),
('Top-level headings — exact Insights pattern START','Top-level headings — exact Insights pattern END'),
('Remaining top-level headings — exact Insights pattern START','Remaining top-level headings — exact Insights pattern END'),
('Exact actual Insights heading reference START','Exact actual Insights heading reference END'),
('Final exact Insights specificity START','Final exact Insights specificity END'),
]
for a,b in paired:
    s=re.sub(r'/\*\s*'+re.escape(a)+r'\s*\*/.*?/\*\s*'+re.escape(b)+r'\s*\*/','',s,flags=re.S)
    s=re.sub(r'<!--\s*'+re.escape(a)+r'\s*-->.*?<!--\s*'+re.escape(b)+r'\s*-->','',s,flags=re.S)

# Remove old standalone injected script blocks that contain the previous heading normalizers.
s=re.sub(r'<script[^>]*>[^<]*(?:Exact actual Insights heading normalizer START|Reference major heading fallback START|Hierarchy heading roles START|Top-level headings — exact Insights pattern START)[\s\S]*?</script>','',s,flags=re.I)

START='<!-- SS SINGLE UNIFIED SECTION HEADING START -->'
END='<!-- SS SINGLE UNIFIED SECTION HEADING END -->'
s=re.sub(re.escape(START)+r'.*?'+re.escape(END),'',s,flags=re.S)

block=r'''<!-- SS SINGLE UNIFIED SECTION HEADING START -->
<style id="ss-single-heading-style">
.ss-unified-heading::before,.ss-unified-heading::after,
.ss-unified-eyebrow::before,.ss-unified-eyebrow::after,
.ss-unified-title::before,.ss-unified-title::after{content:none!important;display:none!important}
.ss-unified-heading svg,.ss-unified-heading i{display:none!important}
</style>
<script id="ss-single-heading-script">
(function(){
  var defs=[
    {id:'company', sels:['.major-insights-title','.section-title']},
    {id:'points', sels:['.section-title']},
    {id:'founder', sels:['.founder-copy .section-title']},
    {id:'experience', sels:['.section-title']},
    {id:'network', sels:['.major-insights-title','.section-title']},
    {id:'capabilities', sels:['.section-title']},
    {id:'insights', sels:['.insight-intro']}
  ];
  var queued=false;
  function imp(el,map){Object.keys(map).forEach(function(k){el.style.setProperty(k,map[k],'important')})}
  function txt(el){return el?(el.textContent||'').replace(/\s+/g,' ').trim():''}
  function allSources(section,d){
    var out=[];
    d.sels.forEach(function(sel){section.querySelectorAll(sel).forEach(function(el){if(!el.classList.contains('ss-unified-heading')&&out.indexOf(el)<0)out.push(el)})});
    return out;
  }
  function score(el){
    var h=el.querySelector('h2');
    var k=el.querySelector('.heading-ref-row,.major-kicker-row,.hierarchy-kicker-row,.eyebrow,.section-kicker,.major-kicker,.hierarchy-kicker');
    return (txt(h)?10:0)+(txt(k)?5:0)+(el.dataset.ssHeadingSource==='1'?50:0);
  }
  function chooseSource(section,d){
    var a=allSources(section,d); if(!a.length)return null;
    a.sort(function(x,y){return score(y)-score(x)});
    var src=a[0]; src.dataset.ssHeadingSource='1';
    a.forEach(function(el){imp(el,{display:'none',visibility:'hidden',height:'0px','min-height':'0px',margin:'0px',padding:'0px',overflow:'hidden'})});
    return src;
  }
  function extract(src,d){
    var h=src.querySelector('h2');
    var k=src.querySelector('.heading-ref-row,.major-kicker-row,.hierarchy-kicker-row,.eyebrow,.section-kicker,.major-kicker,.hierarchy-kicker');
    var title=txt(h);
    var kicker=txt(k);
    if(!kicker){
      var fallback={company:'Company Introduction',points:'Points of Difference',founder:'Introducing the Founder',experience:'Career',network:'Broad Influence and Access',capabilities:'Case Study Apple',insights:'Insights & Perspectives'};
      kicker=fallback[d.id]||'';
    }
    if(!title) title=kicker;
    var support='';
    var sup=src.querySelector('.hierarchy-support,.major-support,.founder-name-support');
    if(sup) support=txt(sup);
    if(support===title||support===kicker) support='';
    return {kicker:kicker,title:title,support:support};
  }
  function make(section,src,d,data){
    var wrap=section.querySelector(':scope .ss-unified-heading[data-ss-section="'+d.id+'"]');
    if(!wrap){
      wrap=document.createElement('div'); wrap.className='ss-unified-heading'; wrap.dataset.ssSection=d.id;
      var eye=document.createElement('div'); eye.className='ss-unified-eyebrow';
      var rule=document.createElement('span'); rule.className='ss-unified-rule'; rule.setAttribute('aria-hidden','true');
      var kl=document.createElement('span'); kl.className='ss-unified-kicker';
      eye.appendChild(rule); eye.appendChild(kl);
      var h=document.createElement('h2'); h.className='ss-unified-title';
      var sp=document.createElement('p'); sp.className='ss-unified-support';
      wrap.appendChild(eye); wrap.appendChild(h); wrap.appendChild(sp);
      src.parentNode.insertBefore(wrap,src);
    }
    var eye=wrap.querySelector('.ss-unified-eyebrow'), rule=wrap.querySelector('.ss-unified-rule'), kl=wrap.querySelector('.ss-unified-kicker'), h=wrap.querySelector('.ss-unified-title'), sp=wrap.querySelector('.ss-unified-support');
    if(txt(kl)!==data.kicker)kl.textContent=data.kicker;
    if(txt(h)!==data.title)h.textContent=data.title;
    if(txt(sp)!==data.support)sp.textContent=data.support;
    imp(wrap,{position:'relative',display:'block','box-sizing':'border-box',width:'100%','max-width':'760px',margin:'0 0 34px 0',padding:'0','text-align':'left','font-family':'Arial, Helvetica, sans-serif',background:'none',border:'0','box-shadow':'none',transform:'none'});
    imp(eye,{display:'flex','align-items':'center','justify-content':'flex-start',gap:'12px',width:'fit-content','max-width':'100%',margin:'0 0 18px 0',padding:'0','font-family':'Arial, Helvetica, sans-serif','font-size':'11px','font-weight':'900','line-height':'16.5px','letter-spacing':'1.87px',color:'rgb(200, 181, 110)','text-transform':'none','text-align':'left',background:'none',border:'0','box-shadow':'none',transform:'none'});
    imp(rule,{display:'block',width:'28px',height:'1px','min-width':'28px','flex':'0 0 28px',margin:'0',padding:'0',background:'rgb(215, 169, 54)',border:'0','border-radius':'0','box-shadow':'none',transform:'none'});
    imp(kl,{display:'inline',margin:'0',padding:'0','font':'inherit','letter-spacing':'inherit',color:'inherit','text-align':'left','text-transform':'none',background:'none',border:'0','box-shadow':'none'});
    imp(h,{display:'block',width:'fit-content','max-width':'100%',margin:'0 0 14px 0',padding:'0','font-family':'Arial, Helvetica, sans-serif','font-size':'clamp(34px, 4vw, 58px)','font-weight':'700','line-height':'normal','letter-spacing':'-0.04em',color:'rgb(247, 245, 239)','text-align':'left','text-transform':'none','white-space':'normal',background:'none',border:'0','box-shadow':'none','text-shadow':'none',transform:'none'});
    imp(sp,{display:data.support?'block':'none',width:'100%','max-width':'760px',margin:'0',padding:'0','font-family':'Arial, Helvetica, sans-serif','font-size':'15px','font-weight':'500','line-height':'1.5','letter-spacing':'0',color:'#9da7b4','text-align':'left',background:'none',border:'0','box-shadow':'none'});
  }
  function run(){
    queued=false;
    defs.forEach(function(d){
      var section=document.getElementById(d.id); if(!section)return;
      var src=chooseSource(section,d); if(!src)return;
      make(section,src,d,extract(src,d));
    });
  }
  function queue(){if(queued)return;queued=true;requestAnimationFrame(run)}
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',queue);else queue();
  new MutationObserver(queue).observe(document.body,{childList:true,subtree:true,characterData:true});
  document.addEventListener('click',function(e){if(e.target.closest&&e.target.closest('.lang-switch'))setTimeout(queue,0)});
})();
</script>
<!-- SS SINGLE UNIFIED SECTION HEADING END -->'''
if '</body>' not in s: raise SystemExit('missing body')
s=s.replace('</body>',block+'\n</body>',1)
p.write_text(s,encoding='utf-8')

# Browser verification: all seven visible heading blocks must have identical computed formatting.
probe=r'''<script>
setTimeout(function(){
 var ids=['company','points','founder','experience','network','capabilities','insights'];
 function pick(id){return document.querySelector('#'+id+' .ss-unified-heading[data-ss-section="'+id+'"]')}
 function snap(id){
  var w=pick(id),e=w&&w.querySelector('.ss-unified-eyebrow'),r=w&&w.querySelector('.ss-unified-rule'),h=w&&w.querySelector('.ss-unified-title');
  if(!w||!e||!r||!h)return {ok:false,missing:true};
  var ws=getComputedStyle(w),es=getComputedStyle(e),rs=getComputedStyle(r),hs=getComputedStyle(h),wr=w.getBoundingClientRect(),er=e.getBoundingClientRect(),hr=h.getBoundingClientRect();
  return {ok:true,w:{display:ws.display,maxWidth:ws.maxWidth,mb:ws.marginBottom,ta:ws.textAlign,ff:ws.fontFamily},e:{display:es.display,gap:es.gap,mb:es.marginBottom,fs:es.fontSize,fw:es.fontWeight,lh:es.lineHeight,ls:es.letterSpacing,c:es.color,ff:es.fontFamily},r:{w:rs.width,h:rs.height,bg:rs.backgroundColor},h:{fs:hs.fontSize,fw:hs.fontWeight,lh:hs.lineHeight,ls:hs.letterSpacing,c:hs.color,mb:hs.marginBottom,ff:hs.fontFamily,ta:hs.textAlign},left:Math.abs(er.left-hr.left)<1,title:(h.textContent||'').trim().length>0};
 }
 var out={};ids.forEach(function(id){out[id]=snap(id)});
 var ref=JSON.stringify(out.company);var keys=['points','founder','experience','network','capabilities','insights'];
 var base=out.company;var same=function(a,b){return JSON.stringify(a.w)===JSON.stringify(b.w)&&JSON.stringify(a.e)===JSON.stringify(b.e)&&JSON.stringify(a.r)===JSON.stringify(b.r)&&JSON.stringify(a.h)===JSON.stringify(b.h)&&a.left&&b.left&&a.title&&b.title};
 out.ALL=base.ok&&base.left&&base.title&&keys.every(function(k){return out[k].ok&&same(base,out[k])});
 document.body.setAttribute('data-ss-unified-audit',encodeURIComponent(JSON.stringify(out)));
},2200);
</script>'''
verify=s.replace('</body>',probe+'\n</body>',1)
vp=Path('.ss-unified-verify.html');vp.write_text(verify,encoding='utf-8')
chrome='/usr/bin/google-chrome'
if not Path(chrome).exists(): chrome='/usr/bin/chromium'
if not Path(chrome).exists(): raise SystemExit('Chrome not found')
for width in (1280,390):
    res=subprocess.run([chrome,'--headless=new','--no-sandbox','--disable-gpu','--allow-file-access-from-files','--virtual-time-budget=7000',f'--window-size={width},1400','--dump-dom',vp.resolve().as_uri()],capture_output=True,text=True)
    m=re.search(r'data-ss-unified-audit="([^"]+)"',res.stdout)
    if not m: raise SystemExit('audit missing at width %s'%width)
    data=json.loads(unquote(html.unescape(m.group(1))))
    print('UNIFIED',width,json.dumps(data,ensure_ascii=False))
    if not data.get('ALL'): raise SystemExit('headings not identical at width %s'%width)
vp.unlink(missing_ok=True)
print('ALL SEVEN SECTION HEADINGS USE ONE IDENTICAL FORMAT')
