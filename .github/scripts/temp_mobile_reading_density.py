from pathlib import Path

css_path = Path('assets/case-study-split.css')
css = css_path.read_text(encoding='utf-8')
marker = '/* Mobile reading-density refinement — 20260908 */'
if marker not in css:
    css += r'''

/* Mobile reading-density refinement — 20260908 */
@media(max-width:760px){
  /* Give content more usable width without affecting desktop. */
  .section-shell{
    width:calc(100% - 30px)!important;
  }
  .content-section{
    padding-block:68px!important;
  }

  /* Improve mobile reading size and line rhythm. */
  #home .hero-bridge-line{
    max-width:100%!important;
    font-size:15px!important;
    line-height:1.6!important;
    letter-spacing:.025em!important;
  }
  .hero-lede,
  #company .company-foundation-story p,
  #company .company-story-origin-layout .company-story-origin-copy,
  .founder-copy>p,
  .feature-card p,
  #network .network-grid p,
  .capability-grid p,
  .solutions-grid p,
  .insight-card p,
  #experience .timeline p{
    font-size:16px!important;
    line-height:1.68!important;
  }

  /* Let Introduction content use the available mobile width. */
  #company .company-foundation-story{
    width:100%!important;
    gap:14px!important;
    margin-top:26px!important;
  }
  #company .company-story-panel{
    padding:22px 16px 24px!important;
  }
  #company .company-foundation-story h3,
  #company .introduction-section-heading{
    max-width:100%!important;
    font-size:26px!important;
    line-height:1.16!important;
  }
  #company .company-story-intro{
    font-size:18px!important;
    line-height:1.56!important;
  }
  #company .company-story-eyebrow,
  #company .introduction-subhead,
  .eyebrow{
    font-size:11px!important;
  }

  /* Reduce card padding so text does not feel boxed into a narrow column. */
  .feature-card,
  #network .network-grid article,
  .capability-grid article,
  .solutions-grid article,
  .insight-card{
    padding-left:20px!important;
    padding-right:20px!important;
  }
  .feature-card{
    min-height:0!important;
    padding-top:24px!important;
    padding-bottom:24px!important;
  }
  .card-top{
    margin-bottom:34px!important;
  }
  #capabilities .case-study-split{
    padding:16px!important;
    gap:18px!important;
  }

  /* One clear mobile title scale below section-level headings. */
  .feature-card h3,
  #network .network-grid h3,
  .capability-grid h3,
  .solutions-grid h3{
    font-size:20px!important;
    line-height:1.28!important;
  }
  #experience .timeline h3{
    font-size:19px!important;
    line-height:1.3!important;
  }
  #experience .timeline time{
    font-size:11px!important;
  }

  /* Make mobile actions easier to read and tap. */
  .button{
    min-height:48px!important;
    font-size:12px!important;
  }
  #home .hero-company-cta{
    min-height:44px!important;
    font-size:12px!important;
  }
  #founder .founder-career-disclosure{
    min-height:52px!important;
    font-size:13px!important;
  }
}
'''
    css_path.write_text(css, encoding='utf-8')

index_path = Path('index.html')
html = index_path.read_text(encoding='utf-8')
old = 'assets/case-study-split.css?v=mobile-logo-square-20260908'
new = 'assets/case-study-split.css?v=mobile-reading-density-20260908'
if old in html:
    html = html.replace(old, new, 1)
    index_path.write_text(html, encoding='utf-8')
elif new not in html:
    raise SystemExit('Expected stylesheet cache reference not found')

# Keep prior safeguards intact.
assert '/* Mobile Name / Logo square-image safeguard — 20260908 */' in css
assert 'overflow-x:hidden' in html
