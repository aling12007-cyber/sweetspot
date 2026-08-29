from pathlib import Path
import subprocess, json, re, html

src = Path('index.html').read_text(encoding='utf-8')
probe = r'''<script>
setTimeout(function(){
  function visibleExact(text){
    var els=[].slice.call(document.querySelectorAll('body *')).filter(function(el){
      var t=(el.textContent||'').trim();
      if(t!==text) return false;
      var s=getComputedStyle(el), r=el.getBoundingClientRect();
      return s.display!=='none' && s.visibility!=='hidden' && r.width>0 && r.height>0;
    });
    els.sort(function(a,b){return parseFloat(getComputedStyle(b).fontSize)-parseFloat(getComputedStyle(a).fontSize)});
    return els[0]||null;
  }
  function style(el){
    if(!el) return null;
    var s=getComputedStyle(el), r=el.getBoundingClientRect();
    return {
      tag:el.tagName, cls:el.className, id:el.id, text:(el.textContent||'').trim(),
      fontSize:s.fontSize,fontWeight:s.fontWeight,lineHeight:s.lineHeight,letterSpacing:s.letterSpacing,
      color:s.color,textAlign:s.textAlign,display:s.display,position:s.position,
      margin:s.margin,padding:s.padding,width:s.width,maxWidth:s.maxWidth,
      left:r.left,top:r.top,right:r.right,bottom:r.bottom,height:r.height,
      bg:s.background, border:s.border, transform:s.transform
    };
  }
  function pseudo(el,p){
    if(!el) return null; var s=getComputedStyle(el,p); return {content:s.content,display:s.display,width:s.width,height:s.height,background:s.background,margin:s.margin,border:s.border};
  }
  var texts=['Insights & Perspectives','Expert Commentary','Company Features','Points of Difference','Introducing the Founder','Career Playbook','Broad Influence and Access','Case Study Apple'];
  var out={};
  texts.forEach(function(t){
    var el=visibleExact(t); var arr=[]; var n=el;
    for(var i=0;i<5 && n;i++,n=n.parentElement){arr.push(style(n));}
    out[t]={self:style(el),before:pseudo(el,'::before'),after:pseudo(el,'::after'),chain:arr,outer:el?el.outerHTML.slice(0,1500):null};
  });
  document.body.setAttribute('data-audit',encodeURIComponent(JSON.stringify(out)));
},1200);
</script>'''
page = src.replace('</body>', probe+'\n</body>',1)
Path('.audit.html').write_text(page,encoding='utf-8')
chrome='/usr/bin/google-chrome'
if not Path(chrome).exists(): chrome='/usr/bin/chromium'
for width in (1280,390):
    res=subprocess.run([chrome,'--headless=new','--no-sandbox','--disable-gpu','--allow-file-access-from-files','--virtual-time-budget=5000',f'--window-size={width},1200','--dump-dom',Path('.audit.html').resolve().as_uri()],capture_output=True,text=True)
    m=re.search(r'data-audit="([^"]+)"',res.stdout)
    if not m:
        print('NO AUDIT',width,res.stderr[-2000:]); continue
    data=json.loads(html.unescape(__import__('urllib.parse').parse.unquote(m.group(1))))
    print('=== WIDTH',width,'===')
    print(json.dumps(data,ensure_ascii=False,indent=2))
Path('.audit.html').unlink(missing_ok=True)
