from pathlib import Path

css_path = Path('assets/case-study-split.css')
css = css_path.read_text(encoding='utf-8')
marker = '/* Mobile Name / Logo square-image safeguard — 20260908 */'
if marker not in css:
    css += r'''

/* Mobile Name / Logo square-image safeguard — 20260908 */
#company .company-story-origin-layout .company-story-logo-stage{
  min-height:0!important;
  height:auto!important;
}
#company .company-story-origin-layout .company-story-logo{
  display:block!important;
  width:clamp(150px,16vw,205px)!important;
  height:clamp(150px,16vw,205px)!important;
  max-width:100%!important;
  aspect-ratio:1 / 1!important;
  object-fit:contain!important;
  object-position:center!important;
}
@media(max-width:760px){
  #company .company-story-origin-layout .company-story-logo-stage{
    min-height:0!important;
    height:auto!important;
    margin:0 0 18px!important;
  }
  #company .company-story-origin-layout .company-story-logo{
    width:min(50vw,174px)!important;
    height:min(50vw,174px)!important;
    max-width:174px!important;
    max-height:174px!important;
    aspect-ratio:1 / 1!important;
    object-fit:contain!important;
  }
}
'''
    css_path.write_text(css, encoding='utf-8')

index_path = Path('index.html')
html = index_path.read_text(encoding='utf-8')
old = 'assets/case-study-split.css?v=contact-heading-135-20260908'
new = 'assets/case-study-split.css?v=mobile-logo-square-20260908'
if old in html:
    html = html.replace(old, new, 1)
    index_path.write_text(html, encoding='utf-8')
elif new not in html:
    raise SystemExit('Expected stylesheet cache reference not found')

assert "logo.src='assets/images/site-e8a84d6c8ba9.webp'" in Path('assets/site-enhancements.js').read_text(encoding='utf-8')
