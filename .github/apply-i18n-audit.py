from pathlib import Path
import re

js_path = Path('assets/site-enhancements.js')
js = js_path.read_text(encoding='utf-8')

new_navigation = r'''  function patchNavigation(){
    var navs=document.querySelectorAll('.site-header nav');
    if(!navs.length)return;

    var lang=currentLanguage();
    var navCopies={
      en:{home:'HOME',introduction:'INTRODUCTION',foundation:'FOUNDATION / PURPOSE',nameLogo:'NAME / LOGO',standFor:'WHAT WE STAND FOR',difference:'DIFFERENCE',founder:'FOUNDER',career:'CAREER',network:'NETWORK',caseStudy:'CASE',insights:'INSIGHTS',contact:'CONTACT',submenu:' subsections'},
      ja:{home:'ホーム',introduction:'会社紹介',foundation:'創立 / 理念',nameLogo:'名称 / ロゴ',standFor:'私たちの理念',difference:'私たちの強み',founder:'創業者',career:'経歴',network:'ネットワーク',caseStudy:'事例',insights:'インサイト',contact:'お問い合わせ',submenu:'のサブメニュー'},
      zhtw:{home:'首頁',introduction:'公司簡介',foundation:'創立 / 理念',nameLogo:'名稱 / LOGO',standFor:'核心理念',difference:'差異化優勢',founder:'創辦人',career:'職涯',network:'產業網絡',caseStudy:'案例',insights:'洞察',contact:'聯絡我們',submenu:'子選單'},
      zhcn:{home:'首页',introduction:'公司简介',foundation:'创立 / 理念',nameLogo:'名称 / LOGO',standFor:'核心理念',difference:'差异化优势',founder:'创办人',career:'职业经历',network:'行业网络',caseStudy:'案例',insights:'洞察',contact:'联系我们',submenu:'子菜单'}
    };
    var c=navCopies[lang]||navCopies.en;
    var version='20260907-heading-hierarchy-i18n-v3-'+lang;
    var groups=[
      {href:'#home',label:c.home,classes:'nav-home nav-level-1'},
      {href:'#company',label:c.introduction,classes:'nav-level-1 nav-parent',children:[
        {href:'#foundation-purpose',label:c.foundation},
        {href:'#name-logo',label:c.nameLogo},
        {href:'#what-we-stand-for',label:c.standFor},
        {href:'#difference',label:c.difference}
      ]},
      {href:'#founder',label:c.founder,classes:'nav-level-1 nav-parent',children:[
        {href:'#experience',label:c.career}
      ]},
      {href:'#network',label:c.network,classes:'nav-level-1 nav-parent',children:[
        {href:'#capabilities',label:c.caseStudy}
      ]},
      {href:'#insights',label:c.insights,classes:'nav-level-1'},
      {href:'#contact',label:c.contact,classes:'nav-level-1 contact-mini'}
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
        submenu.setAttribute('aria-label',group.label+c.submenu);
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

js, n = re.subn(r"  function patchNavigation\(\)\{.*?\n  \}\n\n  function patchHero\(\)\{", new_navigation + "  function patchHero(){", js, count=1, flags=re.S)
assert n == 1, f'patchNavigation replacement count: {n}'

old_alt = "    image.alt='Apple case study activity';"
new_alt = """    var caseAltLabels={\n      en:'Apple case study activity',\n      ja:'Apple ケーススタディの活動イメージ',\n      zhtw:'Apple 案例研究活動圖片',\n      zhcn:'Apple 案例研究活动图片'\n    };\n    image.alt=caseAltLabels[currentLanguage()]||caseAltLabels.en;"""
assert js.count(old_alt) == 1, 'case study alt target not found once'
js = js.replace(old_alt, new_alt, 1)

# Add localized panel kickers.
repls = {
"        foundationHeading:'Foundation Story and Purpose',": "        foundationKicker:'FOUNDATION / PURPOSE',\n        foundationHeading:'Foundation Story and Purpose',",
"        foundationHeading:'創立ストーリーと理念',": "        foundationKicker:'創立 / 理念',\n        foundationHeading:'創立ストーリーと理念',",
"        foundationHeading:'創立故事與理念',": "        foundationKicker:'創立 / 理念',\n        foundationHeading:'創立故事與理念',",
"        foundationHeading:'创立故事与理念',": "        foundationKicker:'创立 / 理念',\n        foundationHeading:'创立故事与理念',",
"        originHeading:'The Origin of the “Sweet Spot” Name and Logo',": "        originKicker:'NAME / LOGO',\n        originHeading:'The Origin of the “Sweet Spot” Name and Logo',",
"        originHeading:'「Sweet Spot」の名前とロゴの由来',": "        originKicker:'名称 / ロゴ',\n        originHeading:'「Sweet Spot」の名前とロゴの由来',",
"        originHeading:'「Sweet Spot」的名稱和 LOGO 的由來',": "        originKicker:'名稱 / LOGO',\n        originHeading:'「Sweet Spot」的名稱和 LOGO 的由來',",
"        originHeading:'“Sweet Spot”的名称和 LOGO 的由来',": "        originKicker:'名称 / LOGO',\n        originHeading:'“Sweet Spot”的名称和 LOGO 的由来',",
}
for old, new in repls.items():
    assert js.count(old) == 1, f'missing unique target: {old}'
    js = js.replace(old, new, 1)

assert js.count("    foundationKicker.textContent='FOUNDATION / PURPOSE';") == 1
js = js.replace("    foundationKicker.textContent='FOUNDATION / PURPOSE';", "    foundationKicker.textContent=copy.foundationKicker;", 1)
assert js.count("    originKicker.textContent='NAME / LOGO';") == 1
js = js.replace("    originKicker.textContent='NAME / LOGO';", "    originKicker.textContent=copy.originKicker;", 1)

# Refine translations for fidelity and natural business language.
translation_repls = {
"        first:'創業者 Sam は、権利保有者（WTA、FIFA）、エージェンシー（Octagon、CSM）、ブランド（AIG）それぞれの立場で経験を積み、スポーツ業界全体のエコシステムと、各関係者が抱える目標や課題を幅広く理解してきました。特に、AIGで8年間スポーツマーケティング部門を率いた経験を通じ、スポンサーシップの価値を最大化し、具体的なビジネス成果につなげることに注力してきました。',": "        first:'創業者 Sam は、ライツホルダー（WTA、FIFA）、エージェンシー（Octagon、CSM）、ブランド（AIG）での経験を通じて、スポーツ業界のエコシステム全体と、各関係者の目標や課題を包括的に理解してきました。特に、AIG のスポーツマーケティング部門を8年間率いた経験では、スポンサーシップの価値を最大化し、具体的なビジネス成果につなげることに注力しました。',",
"        second:'Sweet Spotは、この課題解決を重視した経験を共有し、さまざまなクライアントに高度な調整・支援を提供するために設立されました。',": "        second:'Sweet Spot は、この課題解決型の経験を共有し、複数のクライアントに高度なファシリテーションを提供するために設立されました。',",
"        logoPrefix:'ロゴは、メキシコの伝統的な ',": "        logoPrefix:'ロゴは、古代の水晶をメキシコの伝統的なサラペ（',",
"        nameSuffix:'（サラペ）の中央に古代の水晶を配したデザインです。',": "        nameSuffix:'）の中央に配置したデザインです。',",
"        first:'創辦人 Sam 曾在權利持有方（WTA、FIFA）、代理商（Octagon、CSM）以及品牌（AIG）累積經驗，使他得以全面理解體育產業生態，以及不同參與者各自的目標與面臨的挑戰。尤其是在 AIG 領導體育行銷業務的八年間，他始終專注於最大化贊助合作的效益，並將其轉化為具體的商業成果。',": "        first:'創辦人 Sam 曾在權利持有方（WTA、FIFA）、代理商（Octagon、CSM）以及品牌（AIG）累積經驗，使他對體育產業生態，以及不同參與方的目標與挑戰，建立了全面的理解。尤其是在 AIG 領導體育行銷部門的八年間，他專注於最大化贊助效益，並將其轉化為具體的商業成果。',",
"        second:'Sweet Spot 的成立，是為了分享這些以解決問題為核心的經驗，並為不同客戶提供高層次的協調與支援。',": "        second:'Sweet Spot 的成立，旨在分享這些以解決方案為導向的經驗，並為多元客戶提供高層次的協調促成服務。',",
"        nameFirst:'「Sweet Spot」這個名稱，代表使用球棒、球拍或球桿的中心部位完美擊中球時，那種令人愉悅的感受。',": "        nameFirst:'「Sweet Spot」這個名稱，代表用球棒、球拍或球桿的中心部位完美擊中球時，那種令人愉悅的手感。',",
"        logoPrefix:'品牌標誌則將一顆古老的石英水晶置於墨西哥傳統 ',": "        logoPrefix:'品牌 LOGO 將一顆古老的石英水晶置於墨西哥傳統 ',",
"        nameSuffix:' 織毯的中央。',": "        nameSuffix:' 織品的中央。',",
"        first:'创办人 Sam 曾在权利持有方（WTA、FIFA）、代理机构（Octagon、CSM）以及品牌（AIG）积累经验，使他得以全面理解体育产业生态，以及不同参与方各自的目标与面临的挑战。尤其是在 AIG 领导体育营销业务的八年间，他始终专注于最大化赞助合作的效益，并将其转化为具体的商业成果。',": "        first:'创办人 Sam 曾在权利持有方（WTA、FIFA）、代理机构（Octagon、CSM）以及品牌（AIG）积累经验，使他对体育产业生态，以及不同参与方的目标与挑战，建立了全面的理解。尤其是在 AIG 领导体育营销部门的八年间，他专注于最大化赞助效益，并将其转化为具体的商业成果。',",
"        second:'Sweet Spot 的成立，是为了分享这些以解决问题为核心的经验，并为不同客户提供高层次的协调与支持。',": "        second:'Sweet Spot 的成立，旨在分享这些以解决方案为导向的经验，并为多元客户提供高层次的协调促成服务。',",
"        nameFirst:'“Sweet Spot”这个名称，代表使用球棒、球拍或球杆的中心部位完美击中球时，那种令人愉悦的感受。',": "        nameFirst:'“Sweet Spot”这个名称，代表用球棒、球拍或球杆的中心部位完美击中球时，那种令人愉悦的手感。',",
"        logoPrefix:'品牌标志则将一颗古老的石英水晶置于墨西哥传统 ',": "        logoPrefix:'品牌 LOGO 将一颗古老的石英水晶置于墨西哥传统 ',",
"        nameSuffix:' 织毯的中央。',": "        nameSuffix:' 织物的中央。',",
}
for old, new in translation_repls.items():
    assert js.count(old) == 1, f'translation target missing or duplicated: {old[:60]}'
    js = js.replace(old, new, 1)

# Localize Introduction subsection labels.
old_intro = """  var introductionLabels={
    en:'Introduction',
    ja:'会社紹介',
    zhtw:'簡介',
    zhcn:'简介'
  };"""
new_intro = """  var introductionLabels={
    en:'Introduction',
    ja:'会社紹介',
    zhtw:'公司簡介',
    zhcn:'公司简介'
  };
  var focusLabels={
    en:'WHAT WE STAND FOR',
    ja:'私たちの理念',
    zhtw:'核心理念',
    zhcn:'核心理念'
  };
  var differenceLabels={
    en:'DIFFERENCE',
    ja:'私たちの強み',
    zhtw:'差異化優勢',
    zhcn:'差异化优势'
  };"""
assert js.count(old_intro) == 1, 'introduction labels target missing'
js = js.replace(old_intro, new_intro, 1)
assert js.count("    focusHeading.textContent='WHAT WE STAND FOR';") == 1
js = js.replace("    focusHeading.textContent='WHAT WE STAND FOR';", "    focusHeading.textContent=focusLabels[lang]||focusLabels.en;", 1)
assert js.count("    differenceHeading.textContent='DIFFERENCE';") == 1
js = js.replace("    differenceHeading.textContent='DIFFERENCE';", "    differenceHeading.textContent=differenceLabels[lang]||differenceLabels.en;", 1)

old_career = """  var labels={
    en:{more:'Read more about the Founder’s career',less:'Hide the Founder’s career'},
    ja:{more:'Founderの職歴をもっと見る',less:'Founderの職歴を閉じる'},
    zhtw:{more:'閱讀更多Founder的職涯',less:'收起Founder的職涯'},
    zhcn:{more:'阅读更多Founder的职业经历',less:'收起Founder的职业经历'}
  };"""
new_career = """  var labels={
    en:{more:'Read more about the Founder’s career',less:'Hide the Founder’s career'},
    ja:{more:'創業者の経歴をもっと見る',less:'創業者の経歴を閉じる'},
    zhtw:{more:'閱讀更多創辦人的職涯',less:'收起創辦人的職涯'},
    zhcn:{more:'阅读更多创办人的职业经历',less:'收起创办人的职业经历'}
  };"""
assert js.count(old_career) == 1, 'career labels target missing'
js = js.replace(old_career, new_career, 1)

# Sanity assertions: no English-only subsection labels remain hardcoded in runtime setters.
assert "focusHeading.textContent='WHAT WE STAND FOR'" not in js
assert "differenceHeading.textContent='DIFFERENCE'" not in js
assert "label:'FUNDATION/PURPOSE'" not in js
assert "foundationKicker.textContent='FOUNDATION / PURPOSE'" not in js
assert "originKicker.textContent='NAME / LOGO'" not in js

js_path.write_text(js, encoding='utf-8')

index_path = Path('index.html')
index = index_path.read_text(encoding='utf-8')
old_src = 'assets/site-enhancements.js?v=navigation-heading-hierarchy-20260907'
new_src = 'assets/site-enhancements.js?v=i18n-audit-20260907'
assert index.count(old_src) == 1, f'cache-buster target count: {index.count(old_src)}'
index = index.replace(old_src, new_src, 1)
index_path.write_text(index, encoding='utf-8')
