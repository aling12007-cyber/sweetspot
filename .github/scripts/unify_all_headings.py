from pathlib import Path
import re
import subprocess
import json
import html as htmlmod
from urllib.parse import unquote

path = Path('index.html')
text = path.read_text(encoding='utf-8')

style_id = 'unified-insights-heading-final'
style_re = re.compile(r'<style id=["\']' + re.escape(style_id) + r'["\']>.*?</style>\s*', re.S)
text = style_re.sub('', text)

css = r'''
<style id="unified-insights-heading-final">
/* One heading system for all six requested sections. */
#company .major-insights-title,
#network .major-insights-title,
#points .section-title.hierarchy-applied,
.founder-copy .section-title.hierarchy-applied,
#experience .section-title.hierarchy-applied,
#capabilities .section-title.hierarchy-applied{
  position:relative!important;
  z-index:20!important;
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
#company .major-insights-title *,
#network .major-insights-title *,
#points .section-title.hierarchy-applied *,
.founder-copy .section-title.hierarchy-applied *,
#experience .section-title.hierarchy-applied *,
#capabilities .section-title.hierarchy-applied *{
  box-sizing:border-box!important;
  text-align:left!important;
}

/* Completely suppress legacy square/icon markers. */
#company .major-insights-title::before,
#company .major-insights-title::after,
#network .major-insights-title::before,
#network .major-insights-title::after,
#points .section-title.hierarchy-applied::before,
#points .section-title.hierarchy-applied::after,
.founder-copy .section-title.hierarchy-applied::before,
.founder-copy .section-title.hierarchy-applied::after,
#experience .section-title.hierarchy-applied::before,
#experience .section-title.hierarchy-applied::after,
#capabilities .section-title.hierarchy-applied::before,
#capabilities .section-title.hierarchy-applied::after,
#points .hierarchy-kicker::before,
#points .hierarchy-kicker::after,
.founder-copy .hierarchy-kicker::before,
.founder-copy .hierarchy-kicker::after,
#experience .hierarchy-kicker::before,
#experience .hierarchy-kicker::after,
#capabilities .hierarchy-kicker::before,
#capabilities .hierarchy-kicker::after{
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
  box-shadow:none!important;
}

/* Gold kicker row: exactly the Insights pattern. */
#company .major-insights-title .major-kicker-row,
#network .major-insights-title .major-kicker-row,
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
#company .major-insights-title .major-kicker-line,
#network .major-insights-title .major-kicker-line,
#points .section-title.hierarchy-applied .hierarchy-kicker-row::before,
.founder-copy .section-title.hierarchy-applied .hierarchy-kicker-row::before,
#experience .section-title.hierarchy-applied .hierarchy-kicker-row::before,
#capabilities .section-title.hierarchy-applied .hierarchy-kicker-row::before{
  content:""!important;
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

#company .major-insights-title .major-kicker,
#network .major-insights-title .major-kicker,
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

#company .major-insights-title h2,
#network .major-insights-title h2,
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

/* Keep these two supporting lines visibly subordinate. */
#network .hierarchy-support,
#capabilities .hierarchy-support{
  display:block!important;
  width:100%!important;
  max-width:920px!important;
  margin:28px 0 0!important;
  padding:0!important;
  color:#9da7b4!important;
  font-family:Arial,Helvetica,sans-serif!important;
  font-size:clamp(14px,1.25vw,18px)!important;
  font-weight:500!important;
  line-height:1.45!important;
  letter-spacing:0!important;
  text-align:left!important;
}

@media(max-width:760px){
  #company .major-insights-title,
  #network .major-insights-title,
  #points .section-title.hierarchy-applied,
  .founder-copy .section-title.hierarchy-applied,
  #experience .section-title.hierarchy-applied,
  #capabilities .section-title.hierarchy-applied{
    margin-bottom:28px!important;
    text-align:left!important;
  }
  #company .major-insights-title .major-kicker-row,
  #network .major-insights-title .major-kicker-row,
  #points .section-title.hierarchy-applied .hierarchy-kicker-row,
  .founder-copy .section-title.hierarchy-applied .hierarchy-kicker-row,
  #experience .section-title.hierarchy-applied .hierarchy-kicker-row,
  #capabilities .section-title.hierarchy-applied .hierarchy-kicker-row{
    gap:16px!important;
    margin-bottom:24px!important;
  }
  #company .major-insights-title .major-kicker-line,
  #network .major-insights-title .major-kicker-line,
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
  #company .major-insights-title .major-kicker,
  #network .major-insights-title .major-kicker,
  #points .section-title.hierarchy-applied .hierarchy-kicker,
  .founder-copy .section-title.hierarchy-applied .hierarchy-kicker,
  #experience .section-title.hierarchy-applied .hierarchy-kicker,
  #capabilities .section-title.hierarchy-applied .hierarchy-kicker{
    font-size:clamp(14px,4.4vw,18px)!important;
    letter-spacing:.16em!important;
  }
  #company .major-insights-title h2,
  #network .major-insights-title h2,
  #points .section-title.hierarchy-applied .hierarchy-heading,
  .founder-copy .section-title.hierarchy-applied .hierarchy-heading,
  #experience .section-title.hierarchy-applied .hierarchy-heading,
  #capabilities .section-title.hierarchy-applied .hierarchy-heading{
    max-width:100%!important;
    font-size:clamp(42px,13vw,62px)!important;
    line-height:.98!important;
    letter-spacing:-.052em!important;
    text-align:left!important;
  }
  #network .hierarchy-support,
  #capabilities .hierarchy-support{
    margin-top:22px!important;
    max-width:100%!important;
    font-size:clamp(13px,3.8vw,15px)!important;
  }
  .founder-copy .section-title.hierarchy-applied .founder-name-support{
    display:none!important;
  }
}
</style>
'''

if '</head>' not in text:
    raise SystemExit('No </head> found')
text = text.replace('</head>', css + '\n</head>', 1)
path.write_text(text, encoding='utf-8')

# Browser audit: all six headings must use the same left-aligned line+kicker+white-title pattern.
verify_js = r'''<script>
setTimeout(function(){
  var targets={
    company:{root:'#company .major-insights-title',row:'.major-kicker-row',line:'.major-kicker-line',kicker:'.major-kicker',heading:'h2'},
    points:{root:'#points .section-title.hierarchy-applied',row:'.hierarchy-kicker-row',kicker:'.hierarchy-kicker',heading:'.hierarchy-heading'},
    founder:{root:'.founder-copy .section-title.hierarchy-applied',row:'.hierarchy-kicker-row',kicker:'.hierarchy-kicker',heading:'.hierarchy-heading'},
    experience:{root:'#experience .section-title.hierarchy-applied',row:'.hierarchy-kicker-row',kicker:'.hierarchy-kicker',heading:'.hierarchy-heading'},
    network:{root:'#network .major-insights-title',row:'.major-kicker-row',line:'.major-kicker-line',kicker:'.major-kicker',heading:'h2'},
    capabilities:{root:'#capabilities .section-title.hierarchy-applied',row:'.hierarchy-kicker-row',kicker:'.hierarchy-kicker',heading:'.hierarchy-heading'}
  };
  var out={};
  Object.keys(targets).forEach(function(key){
    var t=targets[key],root=document.querySelector(t.root);
    if(!root){out[key]={ok:false,reason:'root missing'};return;}
    var row=root.querySelector(t.row),kick=root.querySelector(t.kicker),head=root.querySelector(t.heading);
    if(!row||!kick||!head){out[key]={ok:false,reason:'piece missing'};return;}
    var rs=getComputedStyle(row), hs=getComputedStyle(head), roots=getComputedStyle(root);
    var rr=row.getBoundingClientRect(), hr=head.getBoundingClientRect();
    var lineEl=t.line?root.querySelector(t.line):null;
    var lineStyle=lineEl?getComputedStyle(lineEl):getComputedStyle(row,'::before');
    var lineW=parseFloat(lineStyle.width)||0, lineH=parseFloat(lineStyle.height)||0;
    var icons=[].slice.call(root.querySelectorAll('.section-kicker-icon,.section-sport-icon,svg,i'));
    var iconsHidden=icons.every(function(el){var s=getComputedStyle(el);return s.display==='none'||s.visibility==='hidden';});
    var rb=getComputedStyle(root,'::before'), ra=getComputedStyle(root,'::after'), kb=getComputedStyle(kick,'::before');
    var noSquare=iconsHidden && (rb.display==='none'||rb.content==='none') && (ra.display==='none'||ra.content==='none') && (kb.display==='none'||kb.content==='none');
    var ok=roots.textAlign==='left' && rs.display==='flex' && rs.justifyContent==='flex-start' &&
      hs.textAlign==='left' && Math.abs(rr.left-hr.left)<3 && noSquare && lineW>=40 && lineW>lineH*10 && lineH<=4;
    out[key]={ok:ok,kicker:kick.textContent.trim(),title:head.textContent.trim(),rootAlign:roots.textAlign,
      rowDisplay:rs.display,rowJustify:rs.justifyContent,headingAlign:hs.textAlign,lineWidth:lineStyle.width,
      lineHeight:lineStyle.height,noSquare:noSquare,leftDelta:Math.abs(rr.left-hr.left)};
  });
  document.body.setAttribute('data-all-heading-audit',encodeURIComponent(JSON.stringify(out)));
},1400);
</script>'''

verify_text = text.replace('</body>', verify_js + '\n</body>', 1)
verify_path = Path('.verify-all-headings.html')
verify_path.write_text(verify_text, encoding='utf-8')
chrome = '/usr/bin/google-chrome'
if not Path(chrome).exists(): chrome = '/usr/bin/chromium-browser'
if not Path(chrome).exists(): chrome = '/usr/bin/chromium'
if not Path(chrome).exists(): raise SystemExit('Chrome/Chromium missing')

for width in (1280,390):
    res = subprocess.run([
        chrome,'--headless=new','--no-sandbox','--disable-gpu','--allow-file-access-from-files',
        '--virtual-time-budget=6000',f'--window-size={width},900','--dump-dom',verify_path.resolve().as_uri()
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    m = re.search(r'data-all-heading-audit="([^"]+)"', res.stdout)
    if not m:
        raise SystemExit(f'Heading audit marker missing at width {width}')
    audit = json.loads(unquote(htmlmod.unescape(m.group(1))))
    print('WIDTH', width, json.dumps(audit, ensure_ascii=False))
    bad = {k:v for k,v in audit.items() if not v.get('ok')}
    if bad:
        raise SystemExit('Heading audit failed: ' + json.dumps(bad, ensure_ascii=False))

verify_path.unlink(missing_ok=True)
print('ALL SIX HEADING AUDITS PASSED')
