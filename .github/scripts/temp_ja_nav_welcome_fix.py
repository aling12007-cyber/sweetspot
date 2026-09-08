from pathlib import Path

index = Path('index.html')
js = Path('assets/site-enhancements.js')
css = Path('assets/case-study-split.css')

s = index.read_text(encoding='utf-8')
old = 'assets/case-study-split.css?v=desktop-nav-hover-fix-20260908'
new = 'assets/case-study-split.css?v=ja-nav-welcome-20260908'
assert s.count(old) == 1, 'CSS cache-buster source mismatch'
s = s.replace(old, new, 1)
old = 'assets/site-enhancements.js?v=contact-simple-20260908'
new = 'assets/site-enhancements.js?v=ja-nav-welcome-20260908'
assert s.count(old) == 1, 'JS cache-buster source mismatch'
s = s.replace(old, new, 1)
index.write_text(s, encoding='utf-8')

j = js.read_text(encoding='utf-8')
marker = "  document.addEventListener('click',function(e){\n"
insert = """  /* Desktop anchor fallback: handle section navigation before legacy React handlers can swallow Japanese/localized clicks. */
  document.addEventListener('click',function(e){
    if(!window.matchMedia||!window.matchMedia('(min-width:1051px)').matches)return;
    if(e.button!==0||e.metaKey||e.ctrlKey||e.shiftKey||e.altKey)return;
    var link=e.target.closest&&e.target.closest('.site-header nav a[href^=\"#\"]');
    if(!link)return;
    var href=link.getAttribute('href');
    if(!href||href.charAt(0)!=='#')return;
    var target=document.querySelector(href);
    if(!target)return;
    e.preventDefault();
    e.stopPropagation();
    target.scrollIntoView({behavior:'smooth',block:'start'});
    if(window.history&&history.replaceState)history.replaceState(null,'',href);
  },true);

  document.addEventListener('click',function(e){
"""
assert 'Desktop anchor fallback:' not in j, 'desktop anchor fallback already present'
assert j.count(marker) == 1, 'click listener insertion point mismatch'
j = j.replace(marker, insert, 1)
js.write_text(j, encoding='utf-8')

c = css.read_text(encoding='utf-8')
assert 'Desktop localized navigation hardening + company welcome sheen — 20260908' not in c, 'CSS enhancement already present'
c += r'''

/* Desktop localized navigation hardening + company welcome sheen — 20260908 */
@media(min-width:1051px){
  .site-header{
    z-index:500!important;
  }
  .site-header::before,
  .site-header::after{
    pointer-events:none!important;
  }
  .site-header nav{
    position:relative!important;
    z-index:501!important;
    pointer-events:auto!important;
  }
  .site-header nav .ss-nav-group{
    position:relative!important;
    z-index:502!important;
    pointer-events:auto!important;
  }
  .site-header nav a{
    position:relative!important;
    z-index:503!important;
    pointer-events:auto!important;
    cursor:pointer!important;
  }
  .site-header nav .ss-nav-submenu{
    z-index:510!important;
    pointer-events:auto!important;
  }
}

#company .company-story-welcome{
  color:transparent!important;
  -webkit-text-fill-color:transparent;
  background:linear-gradient(100deg,#b77a12 0%,#f3d777 26%,#fff2a7 44%,#d7a936 62%,#fff8c5 80%,#b77a12 100%);
  background-size:220% 100%;
  background-clip:text;
  -webkit-background-clip:text;
  animation:ss-company-welcome-sheen 6.5s ease-in-out infinite;
  filter:drop-shadow(0 0 18px rgba(215,169,54,.10));
}

#company .company-story-welcome::after{
  content:"";
  display:block;
  width:clamp(76px,8vw,122px);
  height:1px;
  margin-top:clamp(15px,1.8vw,22px);
  background:linear-gradient(90deg,var(--gold),rgba(215,169,54,.15),transparent);
  transform-origin:left center;
  animation:ss-company-welcome-line 3.8s ease-in-out infinite alternate;
}

@keyframes ss-company-welcome-sheen{
  0%,20%{background-position:0% 50%}
  55%,100%{background-position:100% 50%}
}

@keyframes ss-company-welcome-line{
  from{transform:scaleX(.72);opacity:.55}
  to{transform:scaleX(1);opacity:1}
}

@media(prefers-reduced-motion:reduce){
  #company .company-story-welcome,
  #company .company-story-welcome::after{
    animation:none!important;
  }
}
'''
css.write_text(c, encoding='utf-8')

assert 'ja-nav-welcome-20260908' in index.read_text(encoding='utf-8')
assert 'Desktop anchor fallback:' in js.read_text(encoding='utf-8')
assert 'ss-company-welcome-sheen' in css.read_text(encoding='utf-8')
