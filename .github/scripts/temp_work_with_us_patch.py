from pathlib import Path
import re

js_path=Path('assets/site-enhancements.js')
css_path=Path('assets/case-study-split.css')
html_path=Path('index.html')

js=js_path.read_text(encoding='utf-8')

nav_replacements={
    "insights:'INSIGHTS',contact:'CONTACT'":"insights:'INSIGHTS',workWithUs:'WORK WITH US',contact:'CONTACT'",
    "insights:'インサイト',contact:'お問い合わせ'":"insights:'インサイト',workWithUs:'ご相談・協業',contact:'お問い合わせ'",
    "insights:'洞察',contact:'聯絡我們'":"insights:'洞察',workWithUs:'合作洽談',contact:'聯絡我們'",
    "insights:'洞察',contact:'联系我们'":"insights:'洞察',workWithUs:'合作洽谈',contact:'联系我们'",
}
for old,new in nav_replacements.items():
    assert js.count(old)==1, f'nav anchor count for {old!r}: {js.count(old)}'
    js=js.replace(old,new,1)

old_version="var version='20260907-heading-hierarchy-i18n-v4-'+lang;"
new_version="var version='20260907-work-with-us-i18n-v5-'+lang;"
assert js.count(old_version)==1, f'nav version anchor count: {js.count(old_version)}'
js=js.replace(old_version,new_version,1)

old_group="      {href:'#insights',label:c.insights,classes:'nav-level-1'},\n      {href:'#contact',label:c.contact,classes:'nav-level-1 contact-mini'}"
new_group="      {href:'#insights',label:c.insights,classes:'nav-level-1'},\n      {href:'#work-with-us',label:c.workWithUs,classes:'nav-level-1'},\n      {href:'#contact',label:c.contact,classes:'nav-level-1 contact-mini'}"
assert js.count(old_group)==1, f'nav group anchor count: {js.count(old_group)}'
js=js.replace(old_group,new_group,1)

work_function=r'''
function patchWorkWithUs(){
  var contact=document.querySelector('#contact');
  if(!contact)return;

  var lang=currentLanguage();
  var copies={
    en:{
      htmlLang:'en',
      kicker:'WORK WITH US',
      heading:'When to Talk to Sweet Spot',
      intro:'You may want to speak with Sweet Spot if you are:',
      items:[
        'Exploring opportunities in Japan',
        'Looking for the right local partners',
        'Developing a sports or entertainment partnership',
        'Seeking access to relevant industry stakeholders',
        'Evaluating sponsorship strategy or activation',
        'Looking for an experienced local perspective before making a decision'
      ]
    },
    ja:{
      htmlLang:'ja',
      kicker:'ご相談・協業',
      heading:'Sweet Spotにご相談いただきたいとき',
      intro:'以下のようなご要望がある場合は、ぜひ Sweet Spot にご相談ください。',
      items:[
        '日本でのビジネス機会を検討している',
        '最適な現地パートナーを探している',
        'スポーツまたはエンターテインメント分野のパートナーシップを構築したい',
        '関連する業界関係者との接点を求めている',
        'スポンサーシップ戦略やアクティベーションを検討している',
        '意思決定の前に、経験に基づく現地視点を得たい'
      ]
    },
    zhtw:{
      htmlLang:'zh-Hant',
      kicker:'合作洽談',
      heading:'適合與 Sweet Spot 洽談的時機',
      intro:'如果您有以下需求，歡迎與 Sweet Spot 洽談：',
      items:[
        '探索日本市場的商業機會',
        '尋找合適的在地合作夥伴',
        '規劃體育或娛樂領域的合作關係',
        '希望接觸相關產業的關鍵利害關係人',
        '評估贊助策略或贊助活化方案',
        '在做出決策前，希望獲得具經驗的在地觀點'
      ]
    },
    zhcn:{
      htmlLang:'zh-Hans',
      kicker:'合作洽谈',
      heading:'适合与 Sweet Spot 洽谈的时机',
      intro:'如果您有以下需求，欢迎与 Sweet Spot 洽谈：',
      items:[
        '探索日本市场的商业机会',
        '寻找合适的本地合作伙伴',
        '规划体育或娱乐领域的合作关系',
        '希望接触相关行业的关键利益相关方',
        '评估赞助策略或赞助激活方案',
        '在做出决策前，希望获得有经验的本地视角'
      ]
    }
  };
  var copy=copies[lang]||copies.en;

  var section=document.querySelector('#work-with-us');
  if(!section){
    section=document.createElement('section');
    section.id='work-with-us';
    section.className='content-section work-with-us-section';
    section.setAttribute('aria-labelledby','work-with-us-title');
    contact.insertAdjacentElement('beforebegin',section);
  }else if(section.nextElementSibling!==contact){
    contact.insertAdjacentElement('beforebegin',section);
  }

  section.setAttribute('lang',copy.htmlLang);
  if(section.getAttribute('data-ss-work-lang')===lang)return;
  section.setAttribute('data-ss-work-lang',lang);
  section.textContent='';

  var shell=document.createElement('div');
  shell.className='section-shell work-with-us-shell';

  var header=document.createElement('div');
  header.className='work-with-us-heading';

  var eyebrow=document.createElement('p');
  eyebrow.className='eyebrow work-with-us-eyebrow';
  eyebrow.appendChild(document.createElement('span'));
  eyebrow.appendChild(document.createTextNode(copy.kicker));
  header.appendChild(eyebrow);

  var heading=document.createElement('h2');
  heading.id='work-with-us-title';
  heading.textContent=copy.heading;
  header.appendChild(heading);

  var intro=document.createElement('p');
  intro.className='work-with-us-intro';
  intro.textContent=copy.intro;
  header.appendChild(intro);
  shell.appendChild(header);

  var list=document.createElement('ul');
  list.className='work-with-us-list';
  copy.items.forEach(function(text){
    var item=document.createElement('li');
    item.className='work-with-us-item';
    var marker=document.createElement('span');
    marker.className='work-with-us-marker';
    marker.setAttribute('aria-hidden','true');
    var label=document.createElement('span');
    label.className='work-with-us-item-text';
    label.textContent=text;
    item.appendChild(marker);
    item.appendChild(label);
    list.appendChild(item);
  });
  shell.appendChild(list);
  section.appendChild(shell);
}

'''
anchor='function patchFounderIdentity(){'
assert js.count(anchor)==1, f'Work With Us insertion anchor count: {js.count(anchor)}'
assert 'function patchWorkWithUs(){' not in js, 'Work With Us function already present'
js=js.replace(anchor,work_function+anchor,1)

apply_anchor='      patchIntroduction();\n      patchFounderIdentity();'
apply_new='      patchIntroduction();\n      patchWorkWithUs();\n      patchFounderIdentity();'
assert js.count(apply_anchor)==1, f'apply anchor count: {js.count(apply_anchor)}'
js=js.replace(apply_anchor,apply_new,1)
js_path.write_text(js,encoding='utf-8')

css=css_path.read_text(encoding='utf-8')
assert '/* Work With Us conversion section */' not in css, 'Work With Us CSS already present'
css += r'''

/* Work With Us conversion section */
#work-with-us{
  scroll-margin-top:96px;
}
.work-with-us-section{
  overflow:hidden;
  background:
    radial-gradient(circle at 84% 18%,rgba(215,169,54,.085),transparent 30%),
    linear-gradient(180deg,#0a0f16 0%,#080c12 100%);
}
.work-with-us-shell{
  position:relative;
  z-index:1;
}
.work-with-us-heading{
  max-width:860px;
  margin-bottom:clamp(30px,4vw,46px);
}
.work-with-us-eyebrow{
  margin-bottom:18px;
}
.work-with-us-heading h2{
  margin:0;
  color:#fff;
  font-size:clamp(36px,5vw,64px);
  font-weight:950;
  line-height:.98;
  letter-spacing:-.05em;
}
.work-with-us-intro{
  max-width:720px;
  margin:22px 0 0;
  color:#aeb7c3;
  font-size:clamp(15px,1.2vw,17px);
  line-height:1.7;
}
.work-with-us-list{
  display:grid;
  grid-template-columns:repeat(2,minmax(0,1fr));
  gap:1px;
  margin:0;
  padding:1px;
  list-style:none;
  background:rgba(255,255,255,.12);
}
.work-with-us-item{
  position:relative;
  display:flex;
  align-items:flex-start;
  gap:18px;
  min-height:112px;
  padding:26px 28px;
  background:linear-gradient(145deg,rgba(255,255,255,.038),rgba(255,255,255,.015));
}
.work-with-us-marker{
  display:block;
  width:24px;
  height:1px;
  flex:0 0 24px;
  margin-top:.72em;
  background:var(--gold);
  box-shadow:8px 0 18px rgba(215,169,54,.18);
}
.work-with-us-item-text{
  color:#f1f3f6;
  font-size:clamp(15px,1.25vw,18px);
  font-weight:720;
  line-height:1.5;
}
@media(max-width:760px){
  .work-with-us-heading{
    margin-bottom:26px;
  }
  .work-with-us-eyebrow{
    margin-bottom:14px;
  }
  .work-with-us-heading h2{
    font-size:clamp(34px,10.5vw,46px);
    line-height:1.02;
  }
  .work-with-us-intro{
    margin-top:18px;
    font-size:15px;
    line-height:1.65;
  }
  .work-with-us-list{
    grid-template-columns:1fr;
  }
  .work-with-us-item{
    min-height:0;
    gap:14px;
    padding:21px 18px;
  }
  .work-with-us-marker{
    width:20px;
    flex-basis:20px;
  }
  .work-with-us-item-text{
    font-size:15px;
    line-height:1.55;
  }
}
'''
css_path.write_text(css,encoding='utf-8')

html=html_path.read_text(encoding='utf-8')
html,n_js=re.subn(r"assets/site-enhancements\.js(?:\?v=[^\"']+)?",'assets/site-enhancements.js?v=work-with-us-20260907',html,count=1)
assert n_js==1, f'site-enhancements cache-bust replacements: {n_js}'
html,n_css=re.subn(r"assets/case-study-split\.css(?:\?v=[^\"']+)?",'assets/case-study-split.css?v=work-with-us-20260907',html,count=1)
assert n_css==1, f'case-study CSS cache-bust replacements: {n_css}'
html_path.write_text(html,encoding='utf-8')
