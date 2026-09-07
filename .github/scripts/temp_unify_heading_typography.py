from pathlib import Path

css = Path('assets/case-study-split.css')
c = css.read_text(encoding='utf-8')
marker = '/* Unified heading typography hierarchy — 20260908 */'
if marker not in c:
    c += '''

/* Unified heading typography hierarchy — 20260908 */
:root{
  --ss-heading-main:clamp(34px,4vw,58px);
  --ss-heading-sub:clamp(27px,3vw,38px);
  --ss-heading-card:21px;
  --ss-heading-item:19px;
}

/* Main section titles: match Company / Founder / Career / Network / Case Study / Insights. */
#contact .contact-inner h2{
  font-size:var(--ss-heading-main)!important;
  font-weight:700!important;
  line-height:normal!important;
  letter-spacing:-.04em!important;
}

/* Introduction subsection titles and Insights content headline share one secondary scale. */
#company .company-foundation-story h3,
#company .introduction-section-heading,
.insight-card h2{
  font-size:var(--ss-heading-sub)!important;
}
#company .company-foundation-story h3,
#company .introduction-section-heading{
  font-weight:850!important;
  line-height:1.14!important;
  letter-spacing:-.035em!important;
}
.insight-card h2{
  font-weight:800!important;
  line-height:1.12!important;
  letter-spacing:-.035em!important;
}

/* Card titles use one consistent scale across Difference, Network and Case Study cards. */
.feature-card h3,
#network .network-grid h3,
.capability-grid h3,
.solutions-grid h3{
  font-size:var(--ss-heading-card)!important;
  line-height:1.25!important;
}

/* Timeline item titles remain one step below card titles. */
#experience .timeline h3{
  font-size:var(--ss-heading-item)!important;
  line-height:1.25!important;
}

@media(max-width:760px){
  #contact .contact-inner h2{
    font-size:34px!important;
    line-height:1.05!important;
  }
  #company .company-foundation-story h3,
  #company .introduction-section-heading,
  .insight-card h2{
    font-size:24px!important;
  }
  .feature-card h3,
  #network .network-grid h3,
  .capability-grid h3,
  .solutions-grid h3{
    font-size:19px!important;
  }
  #experience .timeline h3{
    font-size:18px!important;
  }
}
'''
    css.write_text(c, encoding='utf-8')

idx = Path('index.html')
h = idx.read_text(encoding='utf-8')
old = 'assets/case-study-split.css?v=contact-simple-20260908'
new = 'assets/case-study-split.css?v=heading-type-scale-20260908'
if old in h:
    h = h.replace(old, new)
    idx.write_text(h, encoding='utf-8')
elif new not in h:
    raise SystemExit('Expected current case-study stylesheet cache version not found')
