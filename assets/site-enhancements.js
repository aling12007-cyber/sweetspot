/* Sweet Spot — requested Hero, navigation, Contact and Case Study enhancements */
(function(){
  var applying=false;
  function currentLanguage(){
    var mode=(document.documentElement.getAttribute('data-ss-lang-mode')||'').toLowerCase();
    if(mode==='ja')return 'ja';
    if(mode==='zhtw')return 'zhtw';
    if(mode==='zhcn')return 'zhcn';

    var lang=(document.documentElement.lang||'en').toLowerCase();
    if(lang.indexOf('ja')===0)return 'ja';
    if(lang.indexOf('zh-hans')===0||lang.indexOf('zh-cn')===0)return 'zhcn';
    if(lang.indexOf('zh')===0)return 'zhtw';
    return 'en';
  }

  function setLinkLabel(link,label){
    var textNode=null;
    for(var i=0;i<link.childNodes.length;i++){
      if(link.childNodes[i].nodeType===Node.TEXT_NODE){
        textNode=link.childNodes[i];
        break;
      }
    }

    if(textNode){
      if((textNode.nodeValue||'').trim()!==label)textNode.nodeValue=label;
    }else if(!link.textContent.includes(label)){
      link.insertBefore(document.createTextNode(label),link.firstChild);
    }
  }

  function ensureCompanyArrow(link){
    var arrow=link.querySelector('.hero-company-arrow');
    if(arrow)return;

    var ns='http://www.w3.org/2000/svg';
    arrow=document.createElementNS(ns,'svg');
    arrow.setAttribute('class','hero-company-arrow');
    arrow.setAttribute('viewBox','0 0 18 18');
    arrow.setAttribute('aria-hidden','true');
    arrow.setAttribute('focusable','false');
    arrow.setAttribute('fill','none');
    arrow.setAttribute('stroke','currentColor');
    arrow.setAttribute('stroke-width','1.25');
    arrow.setAttribute('stroke-linecap','round');
    arrow.setAttribute('stroke-linejoin','round');

    var path=document.createElementNS(ns,'path');
    path.setAttribute('d','M9 2.5v12M5 10.5l4 4 4-4');
    arrow.appendChild(path);
    link.appendChild(arrow);
  }

  function patchNavigation(){
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

  function patchHero(){
    var home=document.querySelector('#home');
    if(!home)return;

    var heroVisual=home.querySelector('.hero-visual');
    if(heroVisual&&heroVisual.getAttribute('aria-label')==='A stadium under lights'){
      heroVisual.removeAttribute('aria-label');
    }

    var cityImage=home.querySelector('.hero-city-image');
    if(cityImage&&cityImage.getAttribute('fetchpriority')!=='high'){
      cityImage.setAttribute('fetchpriority','high');
    }

    var ctaWrap=home.querySelector('.hero-cta');
    if(!ctaWrap)return;

    var lang=currentLanguage();
    var primary=ctaWrap.querySelector('a:not(.hero-company-cta)');
    if(primary){
      var contactLabels={
        en:"Let's Connect",
        ja:'お問い合わせ',
        zhtw:'聯絡我們',
        zhcn:'联系我们'
      };
      if(primary.getAttribute('href')!=='#contact')primary.setAttribute('href','#contact');
      setLinkLabel(primary,contactLabels[lang]||contactLabels.en);
    }

    var tagline=home.querySelector('.hero-bridge-line');
    if(!tagline){
      tagline=document.createElement('p');
      tagline.className='hero-bridge-line';
      ctaWrap.parentNode.insertBefore(tagline,ctaWrap);
    }
    var taglineLabels={
      en:'Bridging Japan and the world through sports, business and culture.',
      ja:'スポーツ、ビジネス、カルチャーを通じて、日本と世界をつなぐ。',
      zhtw:'透過運動、商業與文化，連結日本與世界。',
      zhcn:'通过体育、商业与文化，连接日本与世界。'
    };
    tagline.textContent=taglineLabels[lang]||taglineLabels.en;

    var secondary=ctaWrap.querySelector('.hero-company-cta');
    if(!secondary){
      secondary=document.createElement('a');
      secondary.className='hero-company-cta';
      secondary.href='#company';
      ctaWrap.appendChild(secondary);
    }

    var companyLabels={
      en:'Company Introduction',
      ja:'会社紹介',
      zhtw:'公司簡介',
      zhcn:'公司简介'
    };
    if(secondary.getAttribute('href')!=='#company')secondary.setAttribute('href','#company');
    setLinkLabel(secondary,companyLabels[lang]||companyLabels.en);
    ensureCompanyArrow(secondary);
  }

  function patchContact(){
    var contact=document.querySelector('#contact');
    if(!contact)return;

    var lang=currentLanguage();
    var heading=contact.querySelector('.contact-inner h2');
    var body=contact.querySelector('.contact-inner > p:not(.eyebrow)');
    if(!heading||!body)return;

    var headingLabels={
      en:'Let’s connect!',
      ja:'ぜひお話ししましょう！',
      zhtw:'來聊聊吧！',
      zhcn:'来聊聊吧！'
    };
    var bodyLabels={
      en:'Whether you’re exploring the market, looking for the right partner or need a local perspective, let’s start a conversation!',
      ja:'市場進出を検討している方も、最適なパートナーを探している方も、現地の視点が必要な方も、まずは気軽にお話ししましょう！',
      zhtw:'無論您正在探索市場、尋找合適的合作夥伴，或需要在地觀點，都歡迎與我們聊聊！',
      zhcn:'无论您正在探索市场、寻找合适的合作伙伴，或需要本地视角，都欢迎与我们聊聊！'
    };

    heading.textContent=headingLabels[lang]||headingLabels.en;
    body.textContent=bodyLabels[lang]||bodyLabels.en;
  }

  function patchCaseStudy(){
    var scope=document.querySelector('#capabilities');
    if(!scope||scope.querySelector('.case-study-split'))return;

    var heading=scope.querySelector('.ss-unified-heading[data-ss-section="capabilities"], .section-title');
    if(!heading)return;

    var image=scope.querySelector('img[data-case-study-activity="1"]');
    if(!image){
      image=document.createElement('img');
      image.src='assets/case-study-activity.webp';
      image.loading='lazy';
      image.setAttribute('data-case-study-activity','1');
    }
    var caseAltLabels={
      en:'Apple case study activity',
      ja:'Apple ケーススタディの活動イメージ',
      zhtw:'Apple 案例研究活動圖片',
      zhcn:'Apple 案例研究活动图片'
    };
    image.alt=caseAltLabels[currentLanguage()]||caseAltLabels.en;

    var split=document.createElement('div');
    split.className='case-study-split';

    var copy=document.createElement('div');
    copy.className='case-study-copy';

    var media=document.createElement('figure');
    media.className='case-study-media';

    heading.parentNode.insertBefore(split,heading);
    copy.appendChild(heading);
    media.appendChild(image);
    split.appendChild(copy);
    split.appendChild(media);
  }

  function appendStoryParagraph(container,text){
    var paragraph=document.createElement('p');
    paragraph.textContent=text;
    container.appendChild(paragraph);
    return paragraph;
  }

  function patchFoundationStory(){
    var company=document.querySelector('#company');
    if(!company)return;

    var lang=currentLanguage();
    var copies={
      en:{
        htmlLang:'en',
        foundationKicker:'FOUNDATION / PURPOSE',
        foundationHeading:'Foundation Story and Purpose',
        first:'Founder Sam’s experience across rights holders (WTA, FIFA), agencies (Octagon, CSM) and brands (AIG) has provided a comprehensive appreciation of the sports ecosystem and objectives and challenges across the various parties. In particular, the 8 years leading AIG’s sports marketing function ensured a focus on maximizing sponsorship benefits to achieve tangible business results.',
        second:'Sweet Spot was founded to share this solution-focused experience and offer high level facilitation to multiple clients.',
        originKicker:'NAME / LOGO',
        originHeading:'The Origin of the “Sweet Spot” Name and Logo',
        logoAlt:'Sweet Spot logo',
        nameFirst:'The name represents the sweet feeling when perfectly hitting a ball with the middle part of the bat, racquet or club.',
        logoPrefix:'The logo brings together an ancient quartz crystal in the center of a traditional Mexican ',
        nameTerm:'serape',
        nameSuffix:'.',
        closing:'Welcome to the Sweet Spot!'
      },
      ja:{
        htmlLang:'ja',
        foundationKicker:'創立 / 理念',
        foundationHeading:'創立ストーリーと理念',
        first:'創業者 Sam は、ライツホルダー（WTA、FIFA）、エージェンシー（Octagon、CSM）、ブランド（AIG）での経験を通じて、スポーツ業界のエコシステム全体と、各関係者の目標や課題を包括的に理解してきました。特に、AIG のスポーツマーケティング部門を8年間率いた経験では、スポンサーシップの価値を最大化し、具体的なビジネス成果につなげることに注力しました。',
        second:'Sweet Spot は、この課題解決型の経験を共有し、複数のクライアントに高度なファシリテーションを提供するために設立されました。',
        originKicker:'名称 / ロゴ',
        originHeading:'「Sweet Spot」の名前とロゴの由来',
        logoAlt:'Sweet Spot ロゴ',
        nameFirst:'「Sweet Spot」という名前は、バット、ラケット、クラブの芯でボールを完璧に捉えたときに感じる心地よさを表しています。',
        logoPrefix:'ロゴは、古代の水晶をメキシコの伝統的なサラペ（',
        nameTerm:'serape',
        nameSuffix:'）の中央に配置したデザインです。',
        closing:'Sweet Spotへようこそ！'
      },
      zhtw:{
        htmlLang:'zh-Hant',
        foundationKicker:'創立 / 理念',
        foundationHeading:'創立故事與理念',
        first:'創辦人 Sam 曾在權利持有方（WTA、FIFA）、代理商（Octagon、CSM）以及品牌（AIG）累積經驗，使他對體育產業生態，以及不同參與方的目標與挑戰，建立了全面的理解。尤其是在 AIG 領導體育行銷部門的八年間，他專注於最大化贊助效益，並將其轉化為具體的商業成果。',
        second:'Sweet Spot 的成立，旨在分享這些以解決方案為導向的經驗，並為多元客戶提供高層次的協調促成服務。',
        originKicker:'名稱 / LOGO',
        originHeading:'「Sweet Spot」的名稱和 LOGO 的由來',
        logoAlt:'Sweet Spot 品牌 LOGO',
        nameFirst:'「Sweet Spot」這個名稱，代表用球棒、球拍或球桿的中心部位完美擊中球時，那種令人愉悅的手感。',
        logoPrefix:'品牌 LOGO 將一顆古老的石英水晶置於墨西哥傳統 ',
        nameTerm:'serape',
        nameSuffix:' 織品的中央。',
        closing:'歡迎來到 Sweet Spot！'
      },
      zhcn:{
        htmlLang:'zh-Hans',
        foundationKicker:'创立 / 理念',
        foundationHeading:'创立故事与理念',
        first:'创办人 Sam 曾在权利持有方（WTA、FIFA）、代理机构（Octagon、CSM）以及品牌（AIG）积累经验，使他对体育产业生态，以及不同参与方的目标与挑战，建立了全面的理解。尤其是在 AIG 领导体育营销部门的八年间，他专注于最大化赞助效益，并将其转化为具体的商业成果。',
        second:'Sweet Spot 的成立，旨在分享这些以解决方案为导向的经验，并为多元客户提供高层次的协调促成服务。',
        originKicker:'名称 / LOGO',
        originHeading:'“Sweet Spot”的名称和 LOGO 的由来',
        logoAlt:'Sweet Spot 品牌 LOGO',
        nameFirst:'“Sweet Spot”这个名称，代表用球棒、球拍或球杆的中心部位完美击中球时，那种令人愉悦的手感。',
        logoPrefix:'品牌 LOGO 将一颗古老的石英水晶置于墨西哥传统 ',
        nameTerm:'serape',
        nameSuffix:' 织物的中央。',
        closing:'欢迎来到 Sweet Spot！'
      }
    };
    var copy=copies[lang]||copies.en;

    var list=company.querySelector('.company-intro-list');
    if(!list)return;

    var story=company.querySelector('.company-foundation-story');
    if(!story){
      story=document.createElement('div');
      story.className='company-foundation-story';
      story.setAttribute('aria-labelledby','company-foundation-story-title');
      list.insertAdjacentElement('afterend',story);
    }

    story.hidden=false;
    var needsRebuild=story.getAttribute('data-ss-story-lang')!==lang;
    story.setAttribute('lang',copy.htmlLang);

    if(needsRebuild){
      story.setAttribute('data-ss-story-lang',lang);
      story.textContent='';

    var foundation=document.createElement('section');
    foundation.className='company-story-panel company-story-foundation';
    foundation.id='foundation-purpose';

    var foundationEyebrow=document.createElement('div');
    foundationEyebrow.className='company-story-eyebrow';
    var foundationIndex=document.createElement('span');
    foundationIndex.className='company-story-index';
    foundationIndex.textContent='01';
    var foundationKicker=document.createElement('span');
    foundationKicker.className='company-story-kicker';
    foundationKicker.textContent=copy.foundationKicker;
    foundationEyebrow.appendChild(foundationIndex);
    foundationEyebrow.appendChild(foundationKicker);
    foundation.appendChild(foundationEyebrow);

    var heading=document.createElement('h3');
    heading.id='company-foundation-story-title';
    heading.textContent=copy.foundationHeading;
    foundation.appendChild(heading);

    appendStoryParagraph(foundation,copy.first);
    appendStoryParagraph(foundation,copy.second);
    story.appendChild(foundation);

    var origin=document.createElement('section');
    origin.className='company-story-panel company-story-origin';
    origin.id='name-logo';

    var originEyebrow=document.createElement('div');
    originEyebrow.className='company-story-eyebrow';
    var originIndex=document.createElement('span');
    originIndex.className='company-story-index';
    originIndex.textContent='02';
    var originKicker=document.createElement('span');
    originKicker.className='company-story-kicker';
    originKicker.textContent=copy.originKicker;
    originEyebrow.appendChild(originIndex);
    originEyebrow.appendChild(originKicker);
    origin.appendChild(originEyebrow);

    var originHeading=document.createElement('h3');
    originHeading.className='company-story-origin-title';
    originHeading.textContent=copy.originHeading;
    origin.appendChild(originHeading);

    var originLayout=document.createElement('div');
    originLayout.className='company-story-origin-layout';

    var logoStage=document.createElement('div');
    logoStage.className='company-story-logo-stage';
    var logo=document.createElement('img');
    logo.className='company-story-logo';
    logo.src='assets/images/site-e8a84d6c8ba9.webp';
    logo.alt=copy.logoAlt;
    logo.loading='lazy';
    logo.decoding='async';
    logoStage.appendChild(logo);
    originLayout.appendChild(logoStage);

    var originCopy=document.createElement('div');
    originCopy.className='company-story-origin-copy-group';

    var nameParagraph=appendStoryParagraph(originCopy,copy.nameFirst);
    nameParagraph.className='company-story-origin-copy';

    var logoParagraph=document.createElement('p');
    logoParagraph.className='company-story-origin-copy';
    logoParagraph.appendChild(document.createTextNode(copy.logoPrefix));
    var serape=document.createElement('em');
    serape.textContent=copy.nameTerm;
    logoParagraph.appendChild(serape);
    logoParagraph.appendChild(document.createTextNode(copy.nameSuffix));
    originCopy.appendChild(logoParagraph);
    originLayout.appendChild(originCopy);
    origin.appendChild(originLayout);
    story.appendChild(origin);
    }

    // Requested reading order: Foundation, logo origin, company statements, welcome.
    story.insertAdjacentElement('afterend',list);

    var welcome=company.querySelector('.company-story-welcome');
    if(!welcome){
      welcome=document.createElement('p');
      welcome.className='company-story-welcome';
    }
    welcome.setAttribute('lang',copy.htmlLang);
    welcome.textContent=copy.closing;
    var mergedDifference=company.querySelector('.difference-grid[data-ss-merged-introduction="1"]');
    if(mergedDifference)mergedDifference.insertAdjacentElement('afterend',welcome);
    else list.insertAdjacentElement('afterend',welcome);
  }


function patchIntroduction(){
  var company=document.querySelector('#company');
  if(!company)return;

  var lang=currentLanguage();
  var introductionLabels={
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
  };
  var kicker=company.querySelector('.section-title p');
  if(kicker)kicker.textContent=introductionLabels[lang]||introductionLabels.en;

  var list=company.querySelector('.company-intro-list');
  var focusHeading=company.querySelector('.introduction-subhead--focus');
  if(!focusHeading&&list){
    focusHeading=document.createElement('div');
    focusHeading.className='introduction-subhead introduction-subhead--focus';
  }
  if(focusHeading&&list){
    focusHeading.id='what-we-stand-for';
    focusHeading.textContent=focusLabels[lang]||focusLabels.en;
    list.insertAdjacentElement('beforebegin',focusHeading);
  }

  var points=document.querySelector('#points');
  var grid=company.querySelector('.difference-grid[data-ss-merged-introduction="1"]');
  if(!grid&&points)grid=points.querySelector('.difference-grid');
  if(grid){
    grid.setAttribute('data-ss-merged-introduction','1');
    var welcome=company.querySelector('.company-story-welcome');
    if(welcome)welcome.insertAdjacentElement('beforebegin',grid);
    else company.appendChild(grid);

    var differenceHeading=company.querySelector('.introduction-subhead--difference');
    if(!differenceHeading){
      differenceHeading=document.createElement('div');
      differenceHeading.className='introduction-subhead introduction-subhead--difference';
    }
    differenceHeading.id='difference';
    differenceHeading.textContent=differenceLabels[lang]||differenceLabels.en;
    grid.insertAdjacentElement('beforebegin',differenceHeading);
  }

  if(points){
    points.hidden=true;
    points.setAttribute('aria-hidden','true');
  }
}

function patchFounderIdentity(){
  var founder=document.querySelector('#founder');
  if(!founder)return;

  var lang=currentLanguage();
  var labels={
    en:{role:'FOUNDER',location:'Tokyo, Japan'},
    ja:{role:'創業者',location:'東京、日本'},
    zhtw:{role:'創辦人',location:'東京，日本'},
    zhcn:{role:'创办人',location:'东京，日本'}
  };
  var copy=labels[lang]||labels.en;
  var caption=founder.querySelector('.founder-caption');
  if(!caption)return;

  var role=caption.querySelector('span');
  var location=caption.querySelector('small');
  if(role)role.textContent=copy.role;
  if(location)location.textContent=copy.location;
}

function patchFounderCareer(){
  var founder=document.querySelector('#founder');
  var experience=document.querySelector('#experience');
  if(!founder||!experience)return;

  if(experience.parentElement!==founder)founder.appendChild(experience);
  experience.setAttribute('data-ss-founder-career','1');

  var grid=founder.querySelector('.founder-grid');
  if(!grid)return;

  var wrap=founder.querySelector('.founder-career-disclosure-wrap');
  var button=wrap&&wrap.querySelector('.founder-career-disclosure');
  if(!wrap){
    wrap=document.createElement('div');
    wrap.className='founder-career-disclosure-wrap';
    button=document.createElement('button');
    button.className='founder-career-disclosure';
    button.type='button';
    button.setAttribute('aria-controls','experience');
    wrap.appendChild(button);
    grid.insertAdjacentElement('afterend',wrap);
    button.addEventListener('click',function(){
      var isOpen=founder.getAttribute('data-ss-career-open')==='true';
      founder.setAttribute('data-ss-career-open',isOpen?'false':'true');
      patchFounderCareer();
    });
  }

  if(!founder.hasAttribute('data-ss-career-open'))founder.setAttribute('data-ss-career-open','false');
  var isOpen=founder.getAttribute('data-ss-career-open')==='true';
  experience.hidden=!isOpen;

  var lang=currentLanguage();
  var labels={
    en:{more:'Read more about the Founder’s career',less:'Hide the Founder’s career'},
    ja:{more:'創業者の経歴をもっと見る',less:'創業者の経歴を閉じる'},
    zhtw:{more:'閱讀更多創辦人的職涯',less:'收起創辦人的職涯'},
    zhcn:{more:'阅读更多创办人的职业经历',less:'收起创办人的职业经历'}
  };
  var copy=labels[lang]||labels.en;
  button.textContent=isOpen?copy.less:copy.more;
  button.setAttribute('aria-expanded',isOpen?'true':'false');
}

  function patchEmptySemantics(){
  document.querySelectorAll('.hero-lede,.hero-note,.section-title h2').forEach(function(element){
    if((element.textContent||'').trim()===''){
      element.setAttribute('aria-hidden','true');
    }else if(element.getAttribute('aria-hidden')==='true'){
      element.removeAttribute('aria-hidden');
    }
  });
}

  function closeMobileMenu(){
    if(window.matchMedia&&!window.matchMedia('(max-width:1050px)').matches)return;

    var nav=document.querySelector('.site-header nav.is-open');
    if(!nav)return;

    var toggle=document.querySelector('.site-header .menu-toggle[aria-expanded="true"]');
    if(toggle){
      toggle.click();
      return;
    }

    nav.classList.remove('is-open');
    var fallback=document.querySelector('.site-header .menu-toggle.is-open');
    if(fallback)fallback.classList.remove('is-open');
  }

  function apply(){
    if(applying)return;
    applying=true;
    try{
      patchNavigation();
      patchHero();
      patchContact();
      patchCaseStudy();
      patchFoundationStory();
      patchIntroduction();
      patchFounderIdentity();
      patchFounderCareer();
      patchEmptySemantics();
    }finally{
      applying=false;
    }
  }

  var queued=false;
  function queue(){
    if(queued)return;
    queued=true;
    setTimeout(function(){queued=false;apply();},0);
  }

  if(document.readyState==='loading'){
    document.addEventListener('DOMContentLoaded',apply,{once:true});
  }else{
    apply();
  }

  new MutationObserver(queue).observe(document.documentElement,{
    subtree:true,
    childList:true,
    attributes:true,
    attributeFilter:['lang','href','data-ss-lang-mode']
  });

  document.addEventListener('click',function(e){
    if(e.target.closest&&e.target.closest('.site-header nav a, .site-header nav button')){
      setTimeout(closeMobileMenu,0);
    }
    if(e.target.closest&&e.target.closest('.lang-switch'))setTimeout(apply,0);
  });
})();
