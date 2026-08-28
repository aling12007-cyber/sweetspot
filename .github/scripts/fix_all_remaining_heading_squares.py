from pathlib import Path
import re, subprocess, json
from urllib.parse import unquote

path = Path('index.html')
text = path.read_text(encoding='utf-8')

start = '/* Remaining top-level headings — exact Insights pattern START */'
end = '/* Remaining top-level headings — exact Insights pattern END */'

css = r'''/* Remaining top-level headings — exact Insights pattern START */
#points .section-title.hierarchy-applied,
.founder-copy .section-title.hierarchy-applied,
#experience .section-title.hierarchy-applied,
#capabilities .section-title.hierarchy-applied{
  position:relative!important;
  z-index:6!important;
  display:block!important;
  width:100%!important;
  max-width:none!important;
  box-sizing:border-box!important;
  margin:0 0 36px 0!important;
  padding:0!important;
  text-align:left!important;
  justify-items:start!important;
  align-items:start!important;
}
#points .section-title.hierarchy-applied *,
.founder-copy .section-title.hierarchy-applied *,
#experience .section-title.hierarchy-applied *,
#capabilities .section-title.hierarchy-applied *{
  box-sizing:border-box!important;
  text-align:left!important;
}
/* Kill every legacy square / icon / decorative marker in these headings. */
#points .section-title.hierarchy-applied::before,
#points .section-title.hierarchy-applied::after,
.founder-copy .section-title.hierarchy-applied::before,
.founder-copy .section-title.hierarchy-applied::after,
#experience .section-title.hierarchy-applied::before,
#experience .section-title.hierarchy-applied::after,
#capabilities .section-title.hierarchy-applied::before,
#capabilities .section-title.hierarchy-applied::after,
#points .section-title.hierarchy-applied .hierarchy-kicker::before,
#points .section-title.hierarchy-applied .hierarchy-kicker::after,
.founder-copy .section-title.hierarchy-applied .hierarchy-kicker::before,
.founder-copy .section-title.hierarchy-applied .hierarchy-kicker::after,
#experience .section-title.hierarchy-applied .hierarchy-kicker::before,
#experience .section-title.hierarchy-applied .hierarchy-kicker::after,
#capabilities .section-title.hierarchy-applied .hierarchy-kicker::before,
#capabilities .section-title.hierarchy-applied .hierarchy-kicker::after{
  content:none!important;
  display:none!important;
  width:0!important;
  height:0!important;
  min-width:0!important;
  min-height:0!important;
  margin:0!important;
  padding:0!important;
  border:0!important;
  background:none!important;
  background-image:none!important;
  box-shadow:none!important;
}
#points .section-title.hierarchy-applied .section-kicker-icon,
#points .section-title.hierarchy-applied .section-sport-icon,
#points .section-title.hierarchy-applied svg,
#points .section-title.hierarchy-applied i,
.founder-copy .section-title.hierarchy-applied .section-kicker-icon,
.founder-copy .section-title.hierarchy-applied .section-sport-icon,
.founder-copy .section-title.hierarchy-applied svg,
.founder-copy .section-title.hierarchy-applied i,
#experience .section-title.hierarchy-applied .section-kicker-icon,
#experience .section-title.hierarchy-applied .section-sport-icon,
#experience .section-title.hierarchy-applied svg,
#experience .section-title.hierarchy-applied i,
#capabilities .section-title.hierarchy-applied .section-kicker-icon,
#capabilities .section-title.hierarchy-applied .section-sport-icon,
#capabilities .section-title.hierarchy-applied svg,
#capabilities .section-title.hierarchy-applied i{
  display:none!important;
  visibility:hidden!important;
  width:0!important;
  height:0!important;
  min-width:0!important;
  min-height:0!important;
  margin:0!important;
  padding:0!important;
  border:0!important;
  background:none!important;
  background-image:none!important;
  box-shadow:none!important;
}
#points .section-title.hierarchy-applied .hierarchy-kicker-row,
.founder-copy .section-title.hierarchy-applied .hierarchy-kicker-row,
#experience .section-title.hierarchy-applied .hierarchy-kicker-row,
#capabilities .section-title.hierarchy-applied .hierarchy-kicker-row{
  display:flex!important;
  align-items:center!important;
  justify-content:flex-start!important;
  gap:28px!important;
  width:100%!important;
  margin:0 0 38px 0!important;
  padding:0!important;
  text-align:left!important;
}
#points .section-title.hierarchy-applied .hierarchy-kicker-row::before,
.founder-copy .section-title.hierarchy-applied .hierarchy-kicker-row::before,
#experience .section-title.hierarchy-applied .hierarchy-kicker-row::before,
#capabilities .section-title.hierarchy-applied .hierarchy-kicker-row::before{
  content:''!important;
  display:block!important;
  flex:0 0 84px!important;
  width:84px!important;
  min-width:84px!important;
  max-width:84px!important;
  height:3px!important;
  min-height:3px!important;
  max-height:3px!important;
  margin:0!important;
  padding:0!important;
  border:0!important;
  border-radius:0!important;
  background:#c99b35!important;
  background-image:none!important;
  box-shadow:none!important;
  transform:none!important;
}
#points .section-title.hierarchy-applied .hierarchy-kicker-row::after,
.founder-copy .section-title.hierarchy-applied .hierarchy-kicker-row::after,
#experience .section-title.hierarchy-applied .hierarchy-kicker-row::after,
#capabilities .section-title.hierarchy-applied .hierarchy-kicker-row::after{
  content:none!important;
  display:none!important;
}
#points .section-title.hierarchy-applied .hierarchy-kicker,
.founder-copy .section-title.hierarchy-applied .hierarchy-kicker,
#experience .section-title.hierarchy-applied .hierarchy-kicker,
#capabilities .section-title.hierarchy-applied .hierarchy-kicker{
  display:block!important;
  margin:0!important;
  padding:0!important;
  color:#c8b56e!important;
  background:none!important;
  background-image:none!important;
  border:0!important;
  border-radius:0!important;
  box-shadow:none!important;
  font-family:Arial,Helvetica,sans-serif!important;
  font-size:clamp(17px,2vw,30px)!important;
  font-weight:800!important;
  line-height:1.15!important;
  letter-spacing:.18em!important;
  text-transform:none!important;
  white-space:normal!important;
}
#points .section-title.hierarchy-applied .hierarchy-heading,
.founder-copy .section-title.hierarchy-applied .hierarchy-heading,
#experience .section-title.hierarchy-applied .hierarchy-heading,
#capabilities .section-title.hierarchy-applied .hierarchy-heading{
  display:block!important;
  width:100%!important;
  max-width:1120px!important;
  margin:0!important;
  padding:0!important;
  color:#f7f5ef!important;
  background:none!important;
  background-image:none!important;
  border:0!important;
  box-shadow:none!important;
  font-family:Arial,Helvetica,sans-serif!important;
  font-size:clamp(54px,7vw,96px)!important;
  font-weight:800!important;
  line-height:.98!important;
  letter-spacing:-.055em!important;
  text-align:left!important;
  white-space:normal!important;
  -webkit-text-stroke:0!important;
  text-shadow:none!important;
}
.founder-copy .section-title.hierarchy-applied .hierarchy-support,
#capabilities .section-title.hierarchy-applied .hierarchy-support{
  display:block!important;
  width:100%!important;
  max-width:920px!important;
  margin:28px 0 0!important;
  padding:0!important;
  color:#9da7b4!important;
  background:none!important;
  font-family:Arial,Helvetica,sans-serif!important;
  font-size:clamp(15px,1.45vw,20px)!important;
  font-weight:500!important;
  line-height:1.45!important;
  letter-spacing:0!important;
  text-align:left!important;
}
@media(max-width:760px){
  #points .section-title.hierarchy-applied,
  .founder-copy .section-title.hierarchy-applied,
  #experience .section-title.hierarchy-applied,
  #capabilities .section-title.hierarchy-applied{margin-bottom:28px!important}
  #points .section-title.hierarchy-applied .hierarchy-kicker-row,
  .founder-copy .section-title.hierarchy-applied .hierarchy-kicker-row,
  #experience .section-title.hierarchy-applied .hierarchy-kicker-row,
  #capabilities .section-title.hierarchy-applied .hierarchy-kicker-row{
    gap:16px!important;
    margin-bottom:24px!important;
  }
  #points .section-title.hierarchy-applied .hierarchy-kicker-row::before,
  .founder-copy .section-title.hierarchy-applied .hierarchy-kicker-row::before,
  #experience .section-title.hierarchy-applied .hierarchy-kicker-row::before,
  #capabilities .section-title.hierarchy-applied .hierarchy-kicker-row::before{
    flex-basis:48px!important;
    width:48px!important;
    min-width:48px!important;
    max-width:48px!important;
    height:2px!important;
    min-height:2px!important;
    max-height:2px!important;
  }
  #points .section-title.hierarchy-applied .hierarchy-kicker,
  .founder-copy .section-title.hierarchy-applied .hierarchy-kicker,
  #experience .section-title.hierarchy-applied .hierarchy-kicker,
  #capabilities .section-title.hierarchy-applied .hierarchy-kicker{
    font-size:clamp(14px,4.4vw,18px)!important;
    letter-spacing:.16em!important;
  }
  #points .section-title.hierarchy-applied .hierarchy-heading,
  .founder-copy .section-title.hierarchy-applied .hierarchy-heading,
  #experience .section-title.hierarchy-applied .hierarchy-heading,
  #capabilities .section-title.hierarchy-applied .hierarchy-heading{
    max-width:100%!important;
    font-size:clamp(42px,13vw,62px)!important;
    line-height:.98!important;
    letter-spacing:-.052em!important;
  }
  .founder-copy .section-title.hierarchy-applied .hierarchy-support,
  #capabilities .section-title.hierarchy-applied .hierarchy-support{
    margin-top:22px!important;
    max-width:100%!important;
    font-size:clamp(13px,4vw,16px)!important;
    line-height:1.45!important;
  }
  .founder-copy .section-title.hierarchy-applied .founder-name-support{display:none!important}
}
/* Remaining top-level headings — exact Insights pattern END */'''

pattern = re.escape(start) + r'.*?' + re.escape(end)
if re.search(pattern, text, flags=re.S):
    text = re.sub(pattern, css, text, count=1, flags=re.S)
else:
    if '</style>' not in text:
        raise SystemExit('No </style> found')
    text = text.replace('</style>', css + '\n</style>', 1)
path.write_text(text, encoding='utf-8')

# Verify actual rendered CSS in Chromium at desktop and mobile widths.
verify_js = r'''<script>
setTimeout(function(){
  var targets={
    points:'#points .section-title.hierarchy-applied',
    founder:'.founder-copy .section-title.hierarchy-applied',
    experience:'#experience .section-title.hierarchy-applied',
    capabilities:'#capabilities .section-title.hierarchy-applied'
  };
  var out={};
  Object.keys(targets).forEach(function(key){
    var title=document.querySelector(targets[key]);
    if(!title){out[key]={ok:false,reason:'missing title'};return;}
    var row=title.querySelector('.hierarchy-kicker-row');
    var kicker=title.querySelector('.hierarchy-kicker');
    var heading=title.querySelector('.hierarchy-heading');
    if(!row||!kicker||!heading){out[key]={ok:false,reason:'missing pieces'};return;}
    var titleBefore=getComputedStyle(title,'::before');
    var titleAfter=getComputedStyle(title,'::after');
    var kickerBefore=getComputedStyle(kicker,'::before');
    var rowBefore=getComputedStyle(row,'::before');
    var rs=getComputedStyle(row), hs=getComputedStyle(heading), ts=getComputedStyle(title);
    var rr=row.getBoundingClientRect(), hr=heading.getBoundingClientRect();
    var icons=[].slice.call(title.querySelectorAll('.section-kicker-icon,.section-sport-icon,svg,i'));
    var iconsHidden=icons.every(function(el){return getComputedStyle(el).display==='none'||getComputedStyle(el).visibility==='hidden';});
    var lineW=parseFloat(rowBefore.width)||0, lineH=parseFloat(rowBefore.height)||0;
    var noSquare=(titleBefore.display==='none'||titleBefore.content==='none') &&
                 (titleAfter.display==='none'||titleAfter.content==='none') &&
                 (kickerBefore.display==='none'||kickerBefore.content==='none') && iconsHidden;
    var ok=ts.textAlign==='left' && rs.display==='flex' && rs.justifyContent==='flex-start' &&
           hs.textAlign==='left' && Math.abs(rr.left-hr.left)<3 && noSquare &&
           lineW>=40 && lineW>lineH*10 && lineH<=4;
    out[key]={ok:ok,noSquare:noSquare,lineWidth:rowBefore.width,lineHeight:rowBefore.height,leftDelta:Math.abs(rr.left-hr.left),titleAlign:ts.textAlign,headingAlign:hs.textAlign};
  });
  document.body.setAttribute('data-heading-verify',encodeURIComponent(JSON.stringify(out)));
},1200);
</script>'''
verify_text = text.replace('</body>', verify_js + '\n</body>', 1)
verify_path = Path('.heading-verify.html')
verify_path.write_text(verify_text, encoding='utf-8')

chrome = '/usr/bin/google-chrome'
if not Path(chrome).exists(): chrome='/usr/bin/chromium-browser'
if not Path(chrome).exists(): chrome='/usr/bin/chromium'
if not Path(chrome).exists(): raise SystemExit('Chrome/Chromium not found')

for width in (1280, 390):
    res=subprocess.run([chrome,'--headless=new','--no-sandbox','--disable-gpu','--allow-file-access-from-files','--virtual-time-budget=5000',f'--window-size={width},900','--dump-dom',verify_path.resolve().as_uri()],stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
    if res.returncode != 0:
        raise SystemExit(f'Chromium failed at {width}: {res.stderr[-1000:]}')
    m=re.search(r'data-heading-verify="([^"]+)"',res.stdout)
    if not m:
        raise SystemExit(f'No verification data at width {width}')
    report=json.loads(unquote(m.group(1)))
    print(width, json.dumps(report, ensure_ascii=False, indent=2))
    bad=[k for k,v in report.items() if not v.get('ok')]
    if bad:
        raise SystemExit(f'Heading verification failed at width {width}: {bad}')

verify_path.unlink(missing_ok=True)
print('Verified all four headings: left aligned, gold line present, no gold square, desktop + mobile.')
