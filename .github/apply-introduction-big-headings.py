from pathlib import Path
import re

js_path=Path('assets/site-enhancements.js')
js=js_path.read_text(encoding='utf-8')

old_labels="""  var differenceLabels={
    en:'DIFFERENCE',
    ja:'私たちの強み',
    zhtw:'差異化優勢',
    zhcn:'差异化优势'
  };
  var kicker=company.querySelector('.section-title p');
"""
new_labels="""  var differenceLabels={
    en:'DIFFERENCE',
    ja:'私たちの強み',
    zhtw:'差異化優勢',
    zhcn:'差异化优势'
  };
  var focusTitleLabels={
    en:'Our Commitment',
    ja:'私たちのコミットメント',
    zhtw:'我們的承諾',
    zhcn:'我们的承诺'
  };
  var differenceTitleLabels={
    en:'What Sets Sweet Spot Apart',
    ja:'Sweet Spotならではの強み',
    zhtw:'Sweet Spot 的獨特優勢',
    zhcn:'Sweet Spot 的独特优势'
  };
  var kicker=company.querySelector('.section-title p');
"""
assert js.count(old_labels)==1, 'Introduction label insertion target mismatch'
js=js.replace(old_labels,new_labels,1)

old_focus="""  if(focusHeading&&list){
    focusHeading.id='what-we-stand-for';
    focusHeading.textContent=focusLabels[lang]||focusLabels.en;
    list.insertAdjacentElement('beforebegin',focusHeading);
  }

  var points=document.querySelector('#points');
"""
new_focus="""  if(focusHeading&&list){
    focusHeading.id='what-we-stand-for';
    focusHeading.textContent=focusLabels[lang]||focusLabels.en;
    list.insertAdjacentElement('beforebegin',focusHeading);

    var focusTitle=company.querySelector('.introduction-section-heading--focus');
    if(!focusTitle){
      focusTitle=document.createElement('h3');
      focusTitle.className='introduction-section-heading introduction-section-heading--focus';
    }
    focusTitle.textContent=focusTitleLabels[lang]||focusTitleLabels.en;
    list.insertAdjacentElement('beforebegin',focusTitle);
  }

  var points=document.querySelector('#points');
"""
assert js.count(old_focus)==1, 'Focus heading target mismatch'
js=js.replace(old_focus,new_focus,1)

old_difference="""    differenceHeading.id='difference';
    differenceHeading.textContent=differenceLabels[lang]||differenceLabels.en;
    grid.insertAdjacentElement('beforebegin',differenceHeading);
  }

  if(points){
"""
new_difference="""    differenceHeading.id='difference';
    differenceHeading.textContent=differenceLabels[lang]||differenceLabels.en;
    grid.insertAdjacentElement('beforebegin',differenceHeading);

    var differenceTitle=company.querySelector('.introduction-section-heading--difference');
    if(!differenceTitle){
      differenceTitle=document.createElement('h3');
      differenceTitle.className='introduction-section-heading introduction-section-heading--difference';
    }
    differenceTitle.textContent=differenceTitleLabels[lang]||differenceTitleLabels.en;
    grid.insertAdjacentElement('beforebegin',differenceTitle);
  }

  if(points){
"""
assert js.count(old_difference)==1, 'Difference heading target mismatch'
js=js.replace(old_difference,new_difference,1)
js_path.write_text(js,encoding='utf-8')

css_path=Path('assets/case-study-split.css')
css=css_path.read_text(encoding='utf-8')
marker='/* Introduction major subsection headings */'
assert marker not in css, 'Introduction major heading CSS already exists'
css += r'''

/* Introduction major subsection headings */
#company .introduction-section-heading{
  position:relative;
  z-index:2;
  width:min(100%,1040px);
  margin:0 auto 20px;
  color:#fff;
  font-size:clamp(27px,3vw,38px);
  font-weight:850;
  line-height:1.14;
  letter-spacing:-.035em;
}

@media(max-width:760px){
  #company .introduction-section-heading{
    max-width:88%;
    margin-bottom:17px;
    font-size:24px;
    line-height:1.2;
  }
}
'''
css_path.write_text(css,encoding='utf-8')

index_path=Path('index.html')
index=index_path.read_text(encoding='utf-8')
index,n_css=re.subn(r'assets/case-study-split\.css(?:\?v=[^"\']+)?','assets/case-study-split.css?v=intro-big-headings-20260907',index,count=1)
index,n_js=re.subn(r'assets/site-enhancements\.js(?:\?v=[^"\']+)?','assets/site-enhancements.js?v=intro-big-headings-20260907',index,count=1)
assert n_css==1, f'CSS asset reference count: {n_css}'
assert n_js==1, f'JS asset reference count: {n_js}'
index_path.write_text(index,encoding='utf-8')

print('Introduction major headings patch applied')
