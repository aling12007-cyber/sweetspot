from pathlib import Path
import re

js_path=Path('assets/site-enhancements.js')
js=js_path.read_text(encoding='utf-8')

repls={
"""    var foundationIndex=document.createElement('span');
    foundationIndex.className='company-story-index';
    foundationIndex.textContent='01';
""":"",
"""    foundationEyebrow.appendChild(foundationIndex);
""":"",
"""    var originIndex=document.createElement('span');
    originIndex.className='company-story-index';
    originIndex.textContent='02';
""":"",
"""    originEyebrow.appendChild(originIndex);
""":"",
}
for old,new in repls.items():
    assert js.count(old)==1, f'JS target mismatch: {old!r}'
    js=js.replace(old,new,1)
js_path.write_text(js,encoding='utf-8')

css_path=Path('assets/case-study-split.css')
css=css_path.read_text(encoding='utf-8')
marker='/* Story subsection headings — match Introduction small headings */'
assert marker not in css, 'Story subhead override already exists'
css += r'''

/* Story subsection headings — match Introduction small headings */
#company .company-story-panel::after{
  content:none!important;
  display:none!important;
}

#company .company-story-index{
  display:none!important;
}

#company .company-story-eyebrow{
  position:relative;
  z-index:2;
  display:flex;
  align-items:center;
  gap:12px;
  width:100%;
  margin:0 0 16px;
  color:#c8b56e;
  font-size:11px;
  line-height:1.4;
  font-weight:900;
  letter-spacing:.17em;
  text-transform:uppercase;
}

#company .company-story-eyebrow::before{
  content:"";
  display:block;
  width:28px;
  height:1px;
  flex:0 0 28px;
  background:var(--gold);
}

#company .company-story-kicker{
  color:inherit;
  font-size:inherit;
  line-height:inherit;
  font-weight:inherit;
  letter-spacing:inherit;
}

@media(max-width:760px){
  #company .company-story-eyebrow{
    gap:10px;
    margin-bottom:13px;
    font-size:10px;
    letter-spacing:.145em;
  }

  #company .company-story-eyebrow::before{
    width:22px;
    flex-basis:22px;
  }
}
'''
css_path.write_text(css,encoding='utf-8')

index_path=Path('index.html')
index=index_path.read_text(encoding='utf-8')
index,n_css=re.subn(r'assets/case-study-split\.css(?:\?v=[^"\']+)?','assets/case-study-split.css?v=story-subheads-20260907',index,count=1)
index,n_js=re.subn(r'assets/site-enhancements\.js(?:\?v=[^"\']+)?','assets/site-enhancements.js?v=story-subheads-20260907',index,count=1)
assert n_css==1, f'CSS asset reference count: {n_css}'
assert n_js==1, f'JS asset reference count: {n_js}'
index_path.write_text(index,encoding='utf-8')

print('Story subsection heading style patch applied')
