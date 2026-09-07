from pathlib import Path
import re

js_path = Path('assets/site-enhancements.js')
js = js_path.read_text(encoding='utf-8')

new_nav = r'''  function patchNavigation(){
    var navs=document.querySelectorAll('.site-header nav');
    if(!navs.length)return;

    var version='20260907-heading-hierarchy-v2';
    var groups=[
      {href:'#home',label:'HOME',classes:'nav-home nav-level-1'},
      {href:'#company',label:'INTRODUCTION',classes:'nav-level-1 nav-parent',children:[
        {href:'#foundation-purpose',label:'FUNDATION/PURPOSE'},
        {href:'#name-logo',label:'NAME/LOGO'},
        {href:'#what-we-stand-for',label:'WHAT WE STAND FOR'},
        {href:'#difference',label:'DIFFERENCE'}
      ]},
      {href:'#founder',label:'FOUNDER',classes:'nav-level-1 nav-parent',children:[
        {href:'#experience',label:'CAREER'}
      ]},
      {href:'#network',label:'NETWORK',classes:'nav-level-1 nav-parent',children:[
        {href:'#capabilities',label:'CASE'}
      ]},
      {href:'#insights',label:'INSIGHTS',classes:'nav-level-1'},
      {href:'#contact',label:'CONTACT',classes:'nav-level-1 contact-mini'}
    ];
    var flat=[];
    groups.forEach(function(group){
      flat.push({href:group.href,label:group.label,classes:group.classes});
      (group.children||[]).forEach(function(child){
        flat.push({href:child.href,label:child.label,classes:'nav-level-2'});
      });
    });

    navs.forEach(function(nav){
      var current=Array.prototype.slice.call(nav.querySelectorAll('a[href^="#"]'));
      var ready=nav.getAttribute('data-ss-nav-version')===version&&
        current.length===flat.length&&
        nav.querySelectorAll('.ss-nav-group').length===3&&
        flat.every(function(item,index){
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

      function prepareLink(item,extraClass){
        var link=byHref[item.href]||document.createElement('a');
        var wasActive=link.classList.contains('is-active');
        link.setAttribute('href',item.href);
        link.className=(extraClass||item.classes)+(wasActive?' is-active':'');
        link.textContent=item.label;
        return link;
      }

      current.forEach(function(link){link.remove();});
      nav.querySelectorAll('.ss-nav-group').forEach(function(group){group.remove();});

      groups.forEach(function(group){
        var parent=prepareLink(group);
        if(!group.children){
          nav.appendChild(parent);
          return;
        }

        var wrap=document.createElement('div');
        wrap.className='ss-nav-group';
        wrap.appendChild(parent);

        var submenu=document.createElement('div');
        submenu.className='ss-nav-submenu';
        submenu.setAttribute('aria-label',group.label+' subsections');
        group.children.forEach(function(child){
          submenu.appendChild(prepareLink(child,'nav-level-2'));
        });
        wrap.appendChild(submenu);
        nav.appendChild(wrap);
      });

      nav.setAttribute('data-ss-nav-version',version);
    });
  }
'''

nav_pattern = re.compile(r"  function patchNavigation\(\)\{\n.*?\n  \}\n\n  function patchHero\(\)\{", re.S)
if len(nav_pattern.findall(js)) != 1:
    raise SystemExit('Could not uniquely locate patchNavigation')
js = nav_pattern.sub(new_nav + "\n  function patchHero(){", js, count=1)
js_path.write_text(js, encoding='utf-8')

css_path = Path('assets/case-study-split.css')
css = css_path.read_text(encoding='utf-8')
marker = '/* Requested navigation heading hierarchy — desktop + mobile */'
if marker not in css:
    css += r'''

/* Requested navigation heading hierarchy — desktop + mobile */
#foundation-purpose,
#name-logo,
#what-we-stand-for,
#difference,
#experience,
#capabilities{
  scroll-margin-top:96px;
}

@media(min-width:1051px){
  .site-header nav .ss-nav-group{
    position:relative;
    display:flex;
    align-items:center;
  }

  .site-header nav .ss-nav-group>.nav-parent{
    position:relative;
    padding-right:13px;
  }

  .site-header nav .ss-nav-group>.nav-parent::before{
    content:"";
    position:absolute;
    right:1px;
    top:50%;
    width:4px;
    height:4px;
    margin-top:-3px;
    border-right:1px solid currentColor;
    border-bottom:1px solid currentColor;
    transform:rotate(45deg);
    opacity:.72;
  }

  .site-header nav .ss-nav-submenu{
    position:absolute;
    z-index:90;
    top:calc(100% + 11px);
    left:0;
    display:flex;
    min-width:228px;
    flex-direction:column;
    gap:2px;
    padding:9px;
    border:1px solid rgba(215,169,54,.24);
    background:rgba(7,9,13,.98);
    box-shadow:0 18px 48px rgba(0,0,0,.42);
    opacity:0;
    visibility:hidden;
    transform:translateY(-5px);
    pointer-events:none;
    transition:opacity .18s ease,transform .18s ease,visibility .18s ease;
  }

  .site-header nav .ss-nav-group:hover>.ss-nav-submenu,
  .site-header nav .ss-nav-group:focus-within>.ss-nav-submenu{
    opacity:1;
    visibility:visible;
    transform:translateY(0);
    pointer-events:auto;
  }

  .site-header nav .ss-nav-submenu .nav-level-2{
    display:block;
    width:100%;
    padding:9px 11px;
    color:#aeb7c3;
    font-size:10px;
    font-weight:800;
    line-height:1.3;
    letter-spacing:.075em;
    white-space:nowrap;
  }

  .site-header nav .ss-nav-submenu .nav-level-2:hover,
  .site-header nav .ss-nav-submenu .nav-level-2:focus-visible{
    color:#fff;
    background:rgba(215,169,54,.09);
  }
}

@media(max-width:1050px){
  .site-header nav .ss-nav-group{
    display:block;
    width:100%;
  }

  .site-header nav .ss-nav-submenu{
    display:flex;
    width:100%;
    flex-direction:column;
    gap:1px;
  }

  .site-header nav .ss-nav-group>.nav-level-1{
    display:block;
    width:100%!important;
  }
}
'''
    css_path.write_text(css, encoding='utf-8')

index_path = Path('index.html')
index = index_path.read_text(encoding='utf-8')

legacy_pattern = re.compile(r'<!-- Section hierarchy navigation -->\s*<script>.*?</script>\s*<!-- /Section hierarchy navigation -->', re.S)
legacy_matches = legacy_pattern.findall(index)
if len(legacy_matches) != 1:
    raise SystemExit(f'Expected one legacy hierarchy navigation block, found {len(legacy_matches)}')
index = legacy_pattern.sub('<!-- Section hierarchy navigation is handled by assets/site-enhancements.js -->', index, count=1)

css_pattern = r'assets/case-study-split\.css\?v=[A-Za-z0-9._-]+'
css_matches = re.findall(css_pattern, index)
if len(css_matches) != 1:
    raise SystemExit(f'Expected one case-study CSS cache key, found {len(css_matches)}')
index = re.sub(css_pattern, 'assets/case-study-split.css?v=navigation-heading-hierarchy-20260907', index, count=1)

js_pattern = r'assets/site-enhancements\.js\?v=[A-Za-z0-9._-]+'
js_matches = re.findall(js_pattern, index)
if len(js_matches) != 1:
    raise SystemExit(f'Expected one site-enhancements JS cache key, found {len(js_matches)}')
index = re.sub(js_pattern, 'assets/site-enhancements.js?v=navigation-heading-hierarchy-20260907', index, count=1)
index_path.write_text(index, encoding='utf-8')

for token in [
    "label:'HOME'", "label:'INTRODUCTION'", "label:'FUNDATION/PURPOSE'",
    "label:'NAME/LOGO'", "label:'WHAT WE STAND FOR'", "label:'DIFFERENCE'",
    "label:'FOUNDER'", "label:'CAREER'", "label:'NETWORK'", "label:'CASE'",
    "label:'INSIGHTS'", "label:'CONTACT'", "ss-nav-submenu"
]:
    if token not in js:
        raise SystemExit(f'Missing JS token: {token}')
if marker not in css:
    raise SystemExit('Missing navigation CSS marker')
if 'Section hierarchy navigation is handled by assets/site-enhancements.js' not in index:
    raise SystemExit('Legacy navigation script was not neutralized')
