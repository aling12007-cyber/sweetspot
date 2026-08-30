/* Sweet Spot — requested Hero, navigation and Case Study enhancements */
(function(){
  var applying=false;

  function currentLanguage(){
    var lang=(document.documentElement.lang||'en').toLowerCase();
    if(lang.indexOf('ja')===0)return 'ja';
    if(lang.indexOf('zh')===0)return 'zh';
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

  function patchNavigation(){
    var navs=document.querySelectorAll('.site-header nav');
    if(!navs.length)return;

    var homeLabels={
      en:'Home',
      ja:'ホーム',
      zh:'首頁'
    };
    var label=homeLabels[currentLanguage()];

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

    var primary=ctaWrap.querySelector('a:not(.hero-company-cta)');
    if(primary){
      var contactLabels={
        en:"Let's Connect",
        ja:'お問い合わせ',
        zh:'聯絡我們'
      };
      if(primary.getAttribute('href')!=='#contact')primary.setAttribute('href','#contact');
      setLinkLabel(primary,contactLabels[currentLanguage()]);
    }

    var tagline=home.querySelector('.hero-bridge-line');
    if(!tagline){
      tagline=document.createElement('p');
      tagline.className='hero-bridge-line';
      ctaWrap.parentNode.insertBefore(tagline,ctaWrap);
    }
    tagline.textContent='Bridging Japan and the world through sports, business and culture.';

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
      zh:'公司介紹'
    };
    if(secondary.getAttribute('href')!=='#company')secondary.setAttribute('href','#company');
    setLinkLabel(secondary,companyLabels[currentLanguage()]);
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
    if(e.target.closest&&e.target.closest('.lang-switch'))setTimeout(apply,0);
  });
})();
