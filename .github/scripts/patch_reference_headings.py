from pathlib import Path
import re

p = Path("index.html")
t = p.read_text(encoding="utf-8")

css_start = "/* Reference major heading format START */"
css_end = "/* Reference major heading format END */"
js_start = "<!-- Reference major heading fallback START -->"
js_end = "<!-- Reference major heading fallback END -->"

t = re.sub(re.escape(css_start) + r".*?" + re.escape(css_end), "", t, flags=re.S)
t = re.sub(re.escape(js_start) + r".*?" + re.escape(js_end), "", t, flags=re.S)

css = r'''
/* Reference major heading format START */
/* Match the visual hierarchy used by Insights & Perspectives:
   gold rule + compact gold kicker, then a large white headline. */
#company .section-title,
#points .section-title,
.founder-copy .section-title,
#experience .section-title,
#network .section-title,
#capabilities .section-title{
  display:block!important;
  width:100%!important;
  margin-left:0!important;
  margin-right:0!important;
  margin-bottom:30px!important;
  text-align:left!important;
}

#company .section-title>div:first-child,
#points .section-title>div:first-child,
.founder-copy .section-title>div:first-child,
#experience .section-title>div:first-child,
#network .section-title>div:first-child,
#capabilities .section-title>div:first-child{
  display:flex!important;
  width:100%!important;
  align-items:center!important;
  justify-content:flex-start!important;
  gap:12px!important;
  margin:0 0 24px!important;
  text-align:left!important;
}

#company .section-title>div:first-child::before,
#points .section-title>div:first-child::before,
.founder-copy .section-title>div:first-child::before,
#experience .section-title>div:first-child::before,
#network .section-title>div:first-child::before,
#capabilities .section-title>div:first-child::before{
  content:""!important;
  display:block!important;
  flex:0 0 36px!important;
  width:36px!important;
  height:2px!important;
  background:linear-gradient(90deg,#b77a12,#e5c668)!important;
  box-shadow:0 0 8px rgba(215,169,54,.08)!important;
}

#company .section-title .section-kicker-icon,
#points .section-title .section-kicker-icon,
.founder-copy .section-title .section-kicker-icon,
#experience .section-title .section-kicker-icon,
#network .section-title .section-kicker-icon,
#capabilities .section-title .section-kicker-icon{
  display:none!important;
}

#company .section-title p,
#points .section-title p,
.founder-copy .section-title p,
#experience .section-title p,
#network .section-title p,
#capabilities .section-title p{
  display:block!important;
  width:auto!important;
  margin:0!important;
  padding:0!important;
  color:#c8b56e!important;
  font-family:Arial,Helvetica,sans-serif!important;
  font-size:clamp(11px,.95vw,14px)!important;
  font-weight:900!important;
  line-height:1.35!important;
  letter-spacing:.17em!important;
  text-transform:none!important;
  white-space:normal!important;
  text-align:left!important;
  -webkit-text-stroke:0!important;
  text-shadow:none!important;
}

#company .section-title p::before,
#points .section-title p::before,
.founder-copy .section-title p::before,
#experience .section-title p::before,
#network .section-title p::before,
#capabilities .section-title p::before{
  content:none!important;
  display:none!important;
  background:none!important;
}

#company .section-title .section-heading-row,
#points .section-title .section-heading-row,
.founder-copy .section-title .section-heading-row,
#experience .section-title .section-heading-row,
#network .section-title .section-heading-row,
#capabilities .section-title .section-heading-row{
  display:block!important;
  width:100%!important;
  margin:0!important;
  padding:0!important;
  text-align:left!important;
}

#company .section-title h2,
#points .section-title h2,
.founder-copy .section-title h2,
#experience .section-title h2,
#network .section-title h2,
#capabilities .section-title h2{
  display:block!important;
  width:100%!important;
  max-width:1000px!important;
  margin:0!important;
  padding:0!important;
  color:#f7f5ef!important;
  font-family:Arial,Helvetica,sans-serif!important;
  font-size:clamp(34px,4vw,54px)!important;
  font-weight:800!important;
  line-height:.98!important;
  letter-spacing:-.04em!important;
  text-align:left!important;
  white-space:normal!important;
  -webkit-text-stroke:0!important;
  text-shadow:none!important;
}

#experience.content-section{
  border-top:1px solid var(--line)!important;
}

@media(max-width:760px){
  #company .section-title,
  #points .section-title,
  .founder-copy .section-title,
  #experience .section-title,
  #network .section-title,
  #capabilities .section-title{
    margin-bottom:24px!important;
  }

  #company .section-title>div:first-child,
  #points .section-title>div:first-child,
  .founder-copy .section-title>div:first-child,
  #experience .section-title>div:first-child,
  #network .section-title>div:first-child,
  #capabilities .section-title>div:first-child{
    gap:10px!important;
    margin-bottom:18px!important;
  }

  #company .section-title>div:first-child::before,
  #points .section-title>div:first-child::before,
  .founder-copy .section-title>div:first-child::before,
  #experience .section-title>div:first-child::before,
  #network .section-title>div:first-child::before,
  #capabilities .section-title>div:first-child::before{
    flex-basis:28px!important;
    width:28px!important;
    height:1.5px!important;
  }

  #company .section-title p,
  #points .section-title p,
  .founder-copy .section-title p,
  #experience .section-title p,
  #network .section-title p,
  #capabilities .section-title p{
    font-size:10.5px!important;
    line-height:1.4!important;
    letter-spacing:.145em!important;
  }

  #company .section-title h2,
  #points .section-title h2,
  .founder-copy .section-title h2,
  #experience .section-title h2,
  #network .section-title h2,
  #capabilities .section-title h2{
    display:block!important;
    font-size:clamp(32px,10vw,44px)!important;
    line-height:1!important;
    letter-spacing:-.045em!important;
  }
}
/* Reference major heading format END */
'''

t = t.replace("</style>", css + "\n</style>", 1)

js = r'''
<!-- Reference major heading fallback START -->
<script>
(function(){
  var labels = {
    company: { en: "Company", ja: "会社", zh: "公司" },
    points: { en: "Difference", ja: "強み", zh: "優勢" }
  };

  function applyReferenceHeadingFallbacks(){
    ["company","points"].forEach(function(id){
      var section = document.getElementById(id);
      if(!section) return;
      var title = section.querySelector(".section-title");
      if(!title) return;
      var kicker = title.querySelector("p");
      var headline = title.querySelector("h2");
      if(!kicker || !headline) return;

      if(!(headline.textContent || "").trim()){
        var original = (kicker.textContent || "").trim();
        if(original){
          headline.textContent = original;
          var lang = (document.documentElement.lang || "en").toLowerCase();
          var shortLabel = (labels[id] && labels[id][lang]) || (labels[id] && labels[id].en);
          if(shortLabel) kicker.textContent = shortLabel;
        }
      }
    });
  }

  var queued = false;
  function queueReferenceHeadingFallbacks(){
    if(queued) return;
    queued = true;
    requestAnimationFrame(function(){
      queued = false;
      applyReferenceHeadingFallbacks();
    });
  }

  if(document.readyState === "loading"){
    document.addEventListener("DOMContentLoaded", queueReferenceHeadingFallbacks, {once:true});
  } else {
    queueReferenceHeadingFallbacks();
  }

  new MutationObserver(queueReferenceHeadingFallbacks).observe(document.body, {
    childList:true,
    subtree:true,
    characterData:true
  });
  document.addEventListener("click", function(event){
    if(event.target.closest && event.target.closest(".lang-switch")){
      setTimeout(queueReferenceHeadingFallbacks, 0);
    }
  });
})();
</script>
<!-- Reference major heading fallback END -->
'''

t = t.replace("</body>", js + "\n</body>", 1)
p.write_text(t, encoding="utf-8")
