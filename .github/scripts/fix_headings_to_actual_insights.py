from pathlib import Path
import re, subprocess, json, html
from urllib.parse import unquote

path=Path('index.html')
text=path.read_text(encoding='utf-8')

css_start='/* Exact actual Insights heading reference START */'
css_end='/* Exact actual Insights heading reference END */'
css=r'''/* Exact actual Insights heading reference START */
/* Use the ACTUAL Insights typography, not the previous oversized approximation. */
#company .exact-insights-heading,
#points .exact-insights-heading,
.founder-copy .exact-insights-heading,
#experience .exact-insights-heading,
#network .exact-insights-heading,
#capabilities .exact-insights-heading{
  position:relative!important;
  display:block!important;
  box-sizing:border-box!important;
  width:100%!important;
  max-width:760px!important;
  margin:0 0 24px 0!important;
  padding:0!important;
  text-align:left!important;
}
#company .exact-insights-heading *,
#points .exact-insights-heading *,
.founder-copy .exact-insights-heading *,
#experience .exact-insights-heading *,
#network .exact-insights-heading *,
#capabilities .exact-insights-heading *{text-align:left!important;box-sizing:border-box!important}

/* Remove every legacy square/icon/pseudo-marker from the six title blocks. */
#company .exact-insights-heading::before,#company .exact-insights-heading::after,
#points .exact-insights-heading::before,#points .exact-insights-heading::after,
.founder-copy .exact-insights-heading::before,.founder-copy .exact-insights-heading::after,
#experience .exact-insights-heading::before,#experience .exact-insights-heading::after,
#network .exact-insights-heading::before,#network .exact-insights-heading::after,
#capabilities .exact-insights-heading::before,#capabilities .exact-insights-heading::after,
#company .heading-ref-row::before,#company .heading-ref-row::after,
#points .heading-ref-row::before,#points .heading-ref-row::after,
.founder-copy .heading-ref-row::before,.founder-copy .heading-ref-row::after,
#experience .heading-ref-row::before,#experience .heading-ref-row::after,
#network .heading-ref-row::before,#network .heading-ref-row::after,
#capabilities .heading-ref-row::before,#capabilities .heading-ref-row::after{
  content:none!important;display:none!important;width:0!important;height:0!important;
  margin:0!important;padding:0!important;border:0!important;background:none!important;
  background-image:none!important;box-shadow:none!important;
}
#company .exact-insights-heading .section-kicker-icon,#company .exact-insights-heading .section-sport-icon,#company .exact-insights-heading svg,#company .exact-insights-heading i,
#points .exact-insights-heading .section-kicker-icon,#points .exact-insights-heading .section-sport-icon,#points .exact-insights-heading svg,#points .exact-insights-heading i,
.founder-copy .exact-insights-heading .section-kicker-icon,.founder-copy .exact-insights-heading .section-sport-icon,.founder-copy .exact-insights-heading svg,.founder-copy .exact-insights-heading i,
#experience .exact-insights-heading .section-kicker-icon,#experience .exact-insights-heading .section-sport-icon,#experience .exact-insights-heading svg,#experience .exact-insights-heading i,
#network .exact-insights-heading .section-kicker-icon,#network .exact-insights-heading .section-sport-icon,#network .exact-insights-heading svg,#network .exact-insights-heading i,
#capabilities .exact-insights-heading .section-kicker-icon,#capabilities .exact-insights-heading .section-sport-icon,#capabilities .exact-insights-heading svg,#capabilities .exact-insights-heading i{display:none!important;visibility:hidden!important;width:0!important;height:0!important;margin:0!important;padding:0!important}

/* The kicker is rebuilt as the same .eyebrow structure used by Insights. */
#company .heading-ref-row,#points .heading-ref-row,.founder-copy .heading-ref-row,
#experience .heading-ref-row,#network .heading-ref-row,#capabilities .heading-ref-row{
  display:flex!important;align-items:center!important;justify-content:flex-start!important;
  gap:12px!important;width:fit-content!important;max-width:100%!important;
  margin:0 0 18px 0!important;padding:0!important;
  font-family:inherit!important;font-size:11px!important;font-weight:900!important;
  line-height:16.5px!important;letter-spacing:1.87px!important;color:rgb(200,181,110)!important;
  text-transform:none!important;white-space:normal!important;text-align:left!important;
  background:none!important;border:0!important;border-radius:0!important;box-shadow:none!important;
}
/* Preserve the real Insights line by using its actual .eyebrow > span rule; only neutralize old transforms. */
#company .heading-ref-row>span,#points .heading-ref-row>span,.founder-copy .heading-ref-row>span,
#experience .heading-ref-row>span,#network .heading-ref-row>span,#capabilities .heading-ref-row>span{
  transform:none!important;border-radius:0!important;box-shadow:none!important;
}

/* Exact responsive main-title typography measured from Expert Commentary. */
#company .exact-insights-heading h2,
#points .exact-insights-heading h2,
.founder-copy .exact-insights-heading h2,
#experience .exact-insights-heading h2,
#network .exact-insights-heading h2,
#capabilities .exact-insights-heading h2{
  display:block!important;
  width:fit-content!important;max-width:100%!important;
  margin:0 0 14px 0!important;padding:0!important;
  font-family:inherit!important;
  font-size:clamp(34px,4vw,58px)!important;
  font-weight:700!important;
  line-height:normal!important;
  letter-spacing:-.04em!important;
  color:rgb(247,245,239)!important;
  text-align:left!important;
  text-transform:none!important;
  white-space:normal!important;
  background:none!important;border:0!important;box-shadow:none!important;text-shadow:none!important;
  -webkit-text-stroke:0!important;
}

/* Requested support lines stay subordinate. */
#network .exact-insights-heading .hierarchy-support,
#network .exact-insights-heading .major-support,
#capabilities .exact-insights-heading .hierarchy-support{
  display:block!important;width:100%!important;max-width:760px!important;
  margin:0!important;padding:0!important;
  font-family:inherit!important;font-size:15px!important;font-weight:500!important;
  line-height:1.5!important;letter-spacing:0!important;color:#9da7b4!important;text-align:left!important;
}

/* Keep the requested mobile Founder placement rule; only title position differs by device. */
@media(max-width:760px){
  #company .exact-insights-heading,#points .exact-insights-heading,.founder-copy .exact-insights-heading,
  #experience .exact-insights-heading,#network .exact-insights-heading,#capabilities .exact-insights-heading{
    max-width:760px!important;margin-bottom:24px!important;
  }
  .founder-copy .exact-insights-heading .founder-name-support{display:none!important}
  #network .exact-insights-heading .hierarchy-support,#network .exact-insights-heading .major-support,
  #capabilities .exact-insights-heading .hierarchy-support{font-size:14px!important}
}
/* Exact actual Insights heading reference END */'''
pat=re.escape(css_start)+r'.*?'+re.escape(css_end)
if re.search(pat,text,re.S):
    text=re.sub(pat,css,text,count=1,flags=re.S)
else:
    if '</style>' not in text: raise SystemExit('missing </style>')
    text=text.replace('</style>',css+'\n</style>',1)

js_start='/* Exact actual Insights heading normalizer START */'
js_end='/* Exact actual Insights heading normalizer END */'
js=r'''/* Exact actual Insights heading normalizer START */
(function(){
  var defs=[
    ['#company','.major-insights-title'],
    ['#points','.section-title.hierarchy-applied'],
    ['#founder','.founder-copy .section-title.hierarchy-applied'],
    ['#experience','.section-title.hierarchy-applied'],
    ['#network','.major-insights-title'],
    ['#capabilities','.section-title.hierarchy-applied']
  ];
  var busy=false;
  function visible(el){if(!el)return false;var s=getComputedStyle(el),r=el.getBoundingClientRect();return s.display!=='none'&&s.visibility!=='hidden'&&r.width>0&&r.height>0}
  function normalizeOne(sectionSel,wrapSel){
    var section=document.querySelector(sectionSel); if(!section)return;
    var wraps=[].slice.call(section.querySelectorAll(wrapSel));
    var wrap=wraps.find(visible)||wraps[0]; if(!wrap)return;
    wrap.classList.add('exact-insights-heading','insight-intro');
    var row=wrap.querySelector('.heading-ref-row,.major-kicker-row,.hierarchy-kicker-row'); if(!row)return;
    var labelEl=row.querySelector('.major-kicker,.hierarchy-kicker');
    var label=(labelEl?labelEl.textContent:row.textContent||'').trim();
    if(!label && row.dataset.headingLabel) label=row.dataset.headingLabel;
    if(!label)return;
    row.dataset.headingLabel=label;
    if(!row.classList.contains('heading-ref-row') || row.childNodes.length!==2 || !row.firstElementChild){
      row.textContent='';
      var line=document.createElement('span'); line.setAttribute('aria-hidden','true');
      row.appendChild(line); row.appendChild(document.createTextNode(label));
    }else{
      var current=(row.textContent||'').trim();
      if(current!==label){row.lastChild.nodeValue=label;}
    }
    row.classList.add('eyebrow','heading-ref-row');
  }
  function run(){ if(busy)return; busy=true; requestAnimationFrame(function(){busy=false;defs.forEach(function(d){normalizeOne(d[0],d[1])})}) }
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',run);else run();
  new MutationObserver(run).observe(document.body,{childList:true,subtree:true,characterData:true});
  document.addEventListener('click',function(e){if(e.target.closest&&e.target.closest('.lang-switch'))setTimeout(run,0)});
})();
/* Exact actual Insights heading normalizer END */'''
patjs=re.escape(js_start)+r'.*?'+re.escape(js_end)
if re.search(patjs,text,re.S): text=re.sub(patjs,js,text,count=1,flags=re.S)
else: text=text.replace('</body>','<script>'+js+'</script>\n</body>',1)
path.write_text(text,encoding='utf-8')

# Browser-level comparison against the ACTUAL Insights reference.
probe=r'''<script>
setTimeout(function(){
 function cs(el){return getComputedStyle(el)}
 function pick(section,sel){var a=[].slice.call(document.querySelectorAll(section+' '+sel));return a.find(function(e){var s=cs(e),r=e.getBoundingClientRect();return s.display!=='none'&&s.visibility!=='hidden'&&r.width>0&&r.height>0})||a[0]}
 var rk=document.querySelector('#insights .eyebrow'), rh=document.querySelector('#insights .insight-intro h2'), rl=document.querySelector('#insights .eyebrow span');
 var rks=cs(rk), rhs=cs(rh), rls=cs(rl);
 var defs={company:['#company','.exact-insights-heading'],points:['#points','.exact-insights-heading'],founder:['#founder','.exact-insights-heading'],experience:['#experience','.exact-insights-heading'],network:['#network','.exact-insights-heading'],capabilities:['#capabilities','.exact-insights-heading']};
 var out={reference:{kicker:{fontSize:rks.fontSize,fontWeight:rks.fontWeight,lineHeight:rks.lineHeight,letterSpacing:rks.letterSpacing,color:rks.color,marginBottom:rks.marginBottom,fontFamily:rks.fontFamily},h2:{fontSize:rhs.fontSize,fontWeight:rhs.fontWeight,lineHeight:rhs.lineHeight,letterSpacing:rhs.letterSpacing,color:rhs.color,marginBottom:rhs.marginBottom,fontFamily:rhs.fontFamily},line:{width:rls.width,height:rls.height,background:rls.background}}};
 Object.keys(defs).forEach(function(key){
   var wrap=pick(defs[key][0],defs[key][1]), k=wrap&&wrap.querySelector('.heading-ref-row'), h=wrap&&wrap.querySelector('h2'), l=k&&k.querySelector(':scope>span');
   if(!wrap||!k||!h||!l){out[key]={ok:false,reason:'missing pieces'};return}
   var ks=cs(k),hs=cs(h),ls=cs(l),wr=wrap.getBoundingClientRect(),kr=k.getBoundingClientRect(),hr=h.getBoundingClientRect();
   var matchK=['fontSize','fontWeight','lineHeight','letterSpacing','color','marginBottom','fontFamily'].every(function(p){return ks[p]===rks[p]});
   var matchH=['fontSize','fontWeight','lineHeight','letterSpacing','color','marginBottom','fontFamily'].every(function(p){return hs[p]===rhs[p]});
   var matchL=['width','height','background'].every(function(p){return ls[p]===rls[p]});
   var pseudo=[cs(wrap,'::before'),cs(wrap,'::after'),cs(k,'::before'),cs(k,'::after')];
   var noSquare=pseudo.every(function(s){return s.content==='none'||s.display==='none'});
   var left=ks.textAlign==='left'&&hs.textAlign==='left'&&Math.abs(kr.left-hr.left)<1;
   out[key]={ok:matchK&&matchH&&matchL&&noSquare&&left,matchK:matchK,matchH:matchH,matchL:matchL,noSquare:noSquare,left:left,kicker:{fontSize:ks.fontSize,fontWeight:ks.fontWeight,lineHeight:ks.lineHeight,letterSpacing:ks.letterSpacing,color:ks.color,marginBottom:ks.marginBottom,fontFamily:ks.fontFamily},h2:{fontSize:hs.fontSize,fontWeight:hs.fontWeight,lineHeight:hs.lineHeight,letterSpacing:hs.letterSpacing,color:hs.color,marginBottom:hs.marginBottom,fontFamily:hs.fontFamily},line:{width:ls.width,height:ls.height,background:ls.background}};
 });
 document.body.setAttribute('data-exact-heading-audit',encodeURIComponent(JSON.stringify(out)));
},1600);
</script>'''
verify=text.replace('</body>',probe+'\n</body>',1)
vp=Path('.exact-heading-verify.html');vp.write_text(verify,encoding='utf-8')
chrome='/usr/bin/google-chrome'
if not Path(chrome).exists(): chrome='/usr/bin/chromium'
if not Path(chrome).exists(): raise SystemExit('Chrome not found')
for width in (1280,390):
    res=subprocess.run([chrome,'--headless=new','--no-sandbox','--disable-gpu','--allow-file-access-from-files','--virtual-time-budget=6000',f'--window-size={width},1200','--dump-dom',vp.resolve().as_uri()],capture_output=True,text=True)
    m=re.search(r'data-exact-heading-audit="([^"]+)"',res.stdout)
    if not m: raise SystemExit('No exact audit at width %s: %s'%(width,res.stderr[-1500:]))
    data=json.loads(unquote(html.unescape(m.group(1))))
    print('WIDTH',width,json.dumps(data,ensure_ascii=False))
    bad=[k for k,v in data.items() if k!='reference' and not v.get('ok')]
    if bad: raise SystemExit('Mismatch vs actual Insights at width %s: %s'%(width,bad))
vp.unlink(missing_ok=True)
print('ALL SIX EXACTLY MATCH ACTUAL INSIGHTS TYPOGRAPHY')
