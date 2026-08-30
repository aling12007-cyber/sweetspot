/* Sweet Spot — requested Hero, navigation and Case Study enhancements */
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

    var homeLabels={
      en:'Home',
      ja:'ホーム',
      zhtw:'首頁',
      zhcn:'首页'
    };
    var label=homeLabels[currentLanguage()]||homeLabels.en;

    navs.forEach(function(nav){
      var homeLink=nav.querySelector('a.nav-home[href="#home"]');
      if(!homeLink){
        homeLink=document.createElement('a');
        homeLink.className='nav-home nav-level-1';
        homeLink.href='#home';
        nav.insertBefore(homeLink,nav.firstElementChild);
      }
      setLinkLabel(homeLink,label);
    });
  }

  function patchHero(){
    var home=document.querySelector('#home');
    if(!home)return;

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
    image.alt='Apple case study activity';

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
      patchCaseStudy();
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
