from pathlib import Path

css_path = Path('assets/case-study-split.css')
css = css_path.read_text(encoding='utf-8')
marker = '/* Desktop navigation hover/click reliability — 20260908 */'
if marker not in css:
    css += r'''

/* Desktop navigation hover/click reliability — 20260908 */
@media(min-width:1051px){
  /* Keep top-level navigation labels clickable above decorative/hover layers. */
  .site-header nav,
  .site-header nav a.nav-level-1{
    position:relative;
  }
  .site-header nav a.nav-level-1{
    z-index:3;
    pointer-events:auto!important;
  }

  /* Bridge the visual gap so the submenu stays open while the pointer moves into it. */
  .site-header nav .ss-nav-group::after{
    content:"";
    position:absolute;
    left:0;
    right:0;
    top:100%;
    height:13px;
    z-index:1;
  }

  .site-header nav .ss-nav-group>.nav-parent{
    z-index:3;
    pointer-events:auto!important;
  }

  .site-header nav .ss-nav-submenu{
    top:calc(100% + 8px)!important;
    z-index:90!important;
  }

  .site-header nav .ss-nav-submenu .nav-level-2{
    position:relative;
    z-index:91;
    pointer-events:auto!important;
  }
}
'''
    css_path.write_text(css, encoding='utf-8')

index_path = Path('index.html')
html = index_path.read_text(encoding='utf-8')
old = 'assets/case-study-split.css?v=mobile-reading-density-20260908'
new = 'assets/case-study-split.css?v=desktop-nav-hover-fix-20260908'
if old in html:
    html = html.replace(old, new, 1)
    index_path.write_text(html, encoding='utf-8')
elif new not in html:
    raise SystemExit('Expected stylesheet cache reference not found')

assert marker in css
assert '.ss-nav-group::after' in css
assert 'pointer-events:auto!important' in css
assert 'overflow-x:hidden' in html
