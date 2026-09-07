from pathlib import Path
import re

js_path = Path('assets/site-enhancements.js')
js = js_path.read_text(encoding='utf-8')

new_nav = """  function patchNavigation(){
    var navs=document.querySelectorAll('.site-header nav');
    if(!navs.length)return;

    var version='20260907-heading-hierarchy';
    var items=[
      {href:'#home',label:'HOME',classes:'nav-home nav-level-1'},
      {href:'#company',label:'INTRODUCTION',classes:'nav-level-1 nav-parent'},
      {href:'#foundation-purpose',label:'FUNDATION/PURPOSE',classes:'nav-level-2'},
      {href:'#name-logo',label:'NAME/LOGO',classes:'nav-level-2'},
      {href:'#what-we-stand-for',label:'WHAT WE STAND FOR',classes:'nav-level-2'},
      {href:'#difference',label:'DIFFERENCE',classes:'nav-level-2'},
      {href:'#founder',label:'FOUNDER',classes:'nav-level-1 nav-parent'},
      {href:'#experience',label:'CAREER',classes:'nav-level-2'},
      {href:'#network',label:'NETWORK',classes:'nav-level-1 nav-parent'},
      {href:'#capabilities',label:'CASE',classes:'nav-level-2'},
      {href:'#insights',label:'INSIGHTS',classes:'nav-level-1'},
      {href:'#contact',label:'CONTACT',classes:'nav-level-1 contact-mini'}
    ];

    navs.forEach(function(nav){
      var current=Array.prototype.slice.call(nav.querySelectorAll('a[href^="#"]'));
      var ready=nav.getAttribute('data-ss-nav-version')===version&&
        current.length===items.length&&
        items.every(function(item,index){
          var link=current[index];
          if(!link)return false;
          return link.getAttribute('href')===item.href&&
            (link.textContent||'').trim()===item.label&&
            item.classes.split(' ').every(function(name){return link.classList.contains(name);});
        });
      if(ready)return;

      var byHref={};
      current.forEach(function(link){
        var href=link.getAttribute('href');
        if(href&&!byHref[href])byHref[href]=link;
      });

      var ordered=items.map(function(item){
        var link=byHref[item.href]||document.createElement('a');
        var wasActive=link.classList.contains('is-active');
        link.setAttribute('href',item.href);
        link.className=item.classes+(wasActive?' is-active':'');
        link.textContent=item.label;
        return link;
      });

      current.forEach(function(link){link.remove();});
      ordered.forEach(function(link){nav.appendChild(link);});
      nav.setAttribute('data-ss-nav-version',version);
    });
  }
"""

nav_pattern = re.compile(r"  function patchNavigation\(\)\{\n.*?\n  \}\n\n  function patchHero\(\)\{", re.S)
matches = nav_pattern.findall(js)
if len(matches) != 1:
    raise SystemExit(f'Expected exactly one patchNavigation function boundary, found {len(matches)}')
js = nav_pattern.sub(new_nav + "\n  function patchHero(){", js, count=1)

replacements = [
    ("    foundation.className='company-story-panel company-story-foundation';\n", "    foundation.className='company-story-panel company-story-foundation';\n    foundation.id='foundation-purpose';\n"),
    ("    origin.className='company-story-panel company-story-origin';\n", "    origin.className='company-story-panel company-story-origin';\n    origin.id='name-logo';\n"),
    ("    focusHeading.textContent='WHAT WE STAND FOR';\n", "    focusHeading.id='what-we-stand-for';\n    focusHeading.textContent='WHAT WE STAND FOR';\n"),
    ("    differenceHeading.textContent='DIFFERENCE';\n", "    differenceHeading.id='difference';\n    differenceHeading.textContent='DIFFERENCE';\n"),
]
for old, new in replacements:
    if new in js:
        continue
    if js.count(old) != 1:
        raise SystemExit(f'Expected exactly one target: {old!r}; found {js.count(old)}')
    js = js.replace(old, new, 1)

required = [
    "label:'HOME'",
    "label:'INTRODUCTION'",
    "label:'FUNDATION/PURPOSE'",
    "label:'NAME/LOGO'",
    "label:'WHAT WE STAND FOR'",
    "label:'DIFFERENCE'",
    "label:'FOUNDER'",
    "label:'CAREER'",
    "label:'NETWORK'",
    "label:'CASE'",
    "label:'INSIGHTS'",
    "label:'CONTACT'",
    "foundation.id='foundation-purpose'",
    "origin.id='name-logo'",
    "focusHeading.id='what-we-stand-for'",
    "differenceHeading.id='difference'",
]
for token in required:
    if token not in js:
        raise SystemExit(f'Missing required token after patch: {token}')

js_path.write_text(js, encoding='utf-8')

index_path = Path('index.html')
index = index_path.read_text(encoding='utf-8')
pattern = r'assets/site-enhancements\.js\?v=[A-Za-z0-9._-]+'
matches = re.findall(pattern, index)
if len(matches) != 1:
    raise SystemExit(f'Expected exactly one site-enhancements cache key, found {len(matches)}: {matches}')
index = re.sub(pattern, 'assets/site-enhancements.js?v=navigation-heading-hierarchy-20260907', index, count=1)
index_path.write_text(index, encoding='utf-8')
