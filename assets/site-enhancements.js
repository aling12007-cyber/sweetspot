/* Sweet Spot — requested CTA and Case Study enhancements */
(function(){
  var applying=false;

  function currentLanguage(){
    var lang=(document.documentElement.lang||'en').toLowerCase();
    if(lang.indexOf('ja')===0)return 'ja';
    if(lang.indexOf('zh')===0)return 'zh';
    return 'en';
  }

  function patchHeroCTA(){
    var cta=document.querySelector('#home .hero-cta a');
    if(!cta)return;

    var labels={
      en:"Let's Connect",
      ja:'お問い合わせ',
      zh:'聯絡我們'
    };
    var label=labels[currentLanguage()];

    if(cta.getAttribute('href')!=='#contact')cta.setAttribute('href','#contact');

    var textNode=null;
    for(var i=0;i<cta.childNodes.length;i++){
      if(cta.childNodes[i].nodeType===Node.TEXT_NODE){
        textNode=cta.childNodes[i];
        break;
      }
    }

    if(textNode){
      if((textNode.nodeValue||'').trim()!==label)textNode.nodeValue=label;
    }else if(!cta.textContent.includes(label)){
      cta.insertBefore(document.createTextNode(label),cta.firstChild);
    }
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
      patchHeroCTA();
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
