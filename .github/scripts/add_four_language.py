from pathlib import Path
import json
import re
import subprocess

path = Path("index.html")
s = path.read_text(encoding="utf-8")

# Build a compact Traditional -> Simplified character map from ICU.
chars = [chr(i) for i in list(range(0x3400, 0x4DC0)) + list(range(0x4E00, 0xA000)) + list(range(0xF900, 0xFB00))]
proc = subprocess.run(
    ["uconv", "-x", "Hant-Hans"],
    input="\n".join(chars),
    text=True,
    capture_output=True,
    check=True,
)
outs = proc.stdout.split("\n")
pairs = [(a, b) for a, b in zip(chars, outs) if a != b and len(b) == 1]
trad_chars = "".join(a for a, _ in pairs)
simp_chars = "".join(b for _, b in pairs)

block_template = r"""
<!-- SS FOUR LANGUAGE SWITCH START -->
<style id="ss-four-language-style">
.lang-switch.ss-four-language-ready{display:flex!important;align-items:center!important;width:auto!important;max-width:none!important;gap:2px!important;padding:3px!important;border-radius:999px!important;white-space:nowrap!important}
.lang-switch.ss-four-language-ready button{display:inline-flex!important;align-items:center!important;justify-content:center!important;width:auto!important;min-width:0!important;height:26px!important;padding:0 8px!important;border-radius:14px!important;font-size:0!important;line-height:1!important;white-space:nowrap!important}
.lang-switch.ss-four-language-ready button::after{content:attr(data-ss-label)!important;display:block!important;font-family:Arial,Helvetica,sans-serif!important;font-size:9.5px!important;font-weight:800!important;line-height:1!important;letter-spacing:.015em!important;white-space:nowrap!important}
.lang-switch.ss-four-language-ready button.ss-lang-simplified{border:0!important;cursor:pointer!important}
@media(max-width:760px){
  .lang-switch.ss-four-language-ready{gap:1px!important;padding:2px!important}
  .lang-switch.ss-four-language-ready button{height:24px!important;padding:0 5px!important}
  .lang-switch.ss-four-language-ready button::after{font-size:8.5px!important;letter-spacing:0!important}
}
</style>
<script id="ss-four-language-script">
(function(){
  var from=__TRAD__;
  var to=__SIMP__;
  var cmap=Object.create(null);
  for(var i=0;i<from.length;i++)cmap[from.charAt(i)]=to.charAt(i);

  window.__ssToSimplified=function(value){
    return String(value==null?'':value).replace(/[\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff]/g,function(ch){return cmap[ch]||ch});
  };

  var mode='en';
  var internal=false;
  var scheduled=false;
  var translating=false;
  var originals=new WeakMap();
  var attrOriginals=new WeakMap();

  function setMode(next){
    mode=next;
    document.documentElement.setAttribute('data-ss-lang-mode',next);
    document.documentElement.lang=next==='ja'?'ja':next==='zhcn'?'zh-Hans':next==='zhtw'?'zh-Hant':'en';
  }

  function root(){
    return document.querySelector('.lang-switch');
  }

  function baseButtons(){
    var r=root();
    if(!r)return null;
    var list=Array.prototype.filter.call(r.querySelectorAll('button'),function(b){
      return !b.classList.contains('ss-lang-simplified');
    });
    if(list.length<3)return null;
    return {root:r,en:list[0],ja:list[1],zh:list[2]};
  }

  function normalizeBaseButtons(b){
    if(!b)return;
    if((b.en.textContent||'').trim()!=='EN')b.en.textContent='EN';
    if((b.ja.textContent||'').trim()!=='日')b.ja.textContent='日';
    if((b.zh.textContent||'').trim()!=='中')b.zh.textContent='中';

    b.en.dataset.ssLabel='ENG';
    b.en.setAttribute('aria-label','ENG');
    b.en.setAttribute('title','ENG');

    b.ja.dataset.ssLabel='日本語';
    b.ja.setAttribute('aria-label','日本語');
    b.ja.setAttribute('title','日本語');

    b.zh.dataset.ssLabel='繁體中文';
    b.zh.setAttribute('aria-label','繁體中文');
    b.zh.setAttribute('title','繁體中文');
  }

  function ensureUI(){
    var b=baseButtons();
    if(!b)return null;

    normalizeBaseButtons(b);
    b.root.classList.add('ss-four-language-ready');

    var simp=b.root.querySelector('button.ss-lang-simplified');
    if(!simp){
      simp=document.createElement('button');
      simp.type='button';
      simp.className='ss-lang-simplified';
      simp.textContent='中';
      b.root.insertBefore(simp,b.zh);
    }

    simp.dataset.ssLabel='简体中文';
    simp.setAttribute('aria-label','简体中文');
    simp.setAttribute('title','简体中文');

    if(mode==='zhcn'){
      Array.prototype.forEach.call(b.root.querySelectorAll('button'),function(x){x.classList.remove('active')});
      simp.classList.add('active');
    }

    return {root:b.root,en:b.en,ja:b.ja,zh:b.zh,simp:simp};
  }

  function isSkipped(el){
    return !el || !!el.closest('script,style,noscript,textarea,.lang-switch,[data-ss-no-simplify]');
  }

  function simplifyTextNode(node){
    var p=node.parentElement;
    if(isSkipped(p))return;

    var current=node.nodeValue||'';
    var old=originals.get(node);
    var oldSimp=old==null?null:window.__ssToSimplified(old);

    if(old==null || current!==oldSimp){
      old=current;
      originals.set(node,old);
    }

    var next=window.__ssToSimplified(old);
    if(current!==next)node.nodeValue=next;
  }

  function simplifyAttrs(el){
    if(isSkipped(el))return;

    var names=['placeholder','title','aria-label','alt'];
    var store=attrOriginals.get(el)||{};
    var changed=false;

    names.forEach(function(name){
      if(!el.hasAttribute || !el.hasAttribute(name))return;

      var current=el.getAttribute(name)||'';
      var old=store[name];
      var oldSimp=old==null?null:window.__ssToSimplified(old);

      if(old==null || current!==oldSimp){
        old=current;
        store[name]=old;
        changed=true;
      }

      var next=window.__ssToSimplified(old);
      if(current!==next)el.setAttribute(name,next);
    });

    if(changed || Object.keys(store).length)attrOriginals.set(el,store);
  }

  function simplifyTree(scope){
    if(mode!=='zhcn' || translating)return;
    translating=true;

    try{
      var base=scope&&scope.nodeType?scope:document.body;

      if(base.nodeType===3){
        simplifyTextNode(base);
      }else{
        if(base.nodeType===1)simplifyAttrs(base);

        var walker=document.createTreeWalker(base,NodeFilter.SHOW_TEXT|NodeFilter.SHOW_ELEMENT);
        var n;

        while((n=walker.nextNode())){
          if(n.nodeType===3)simplifyTextNode(n);
          else simplifyAttrs(n);
        }
      }
    }finally{
      translating=false;
    }
  }

  function restoreTree(scope){
    if(translating)return;
    translating=true;

    try{
      var base=scope&&scope.nodeType?scope:document.body;

      function restoreNode(n){
        if(n.nodeType===3){
          if(originals.has(n)){
            n.nodeValue=originals.get(n);
            originals.delete(n);
          }
        }else if(n.nodeType===1){
          var store=attrOriginals.get(n);
          if(store){
            Object.keys(store).forEach(function(name){
              if(n.hasAttribute(name))n.setAttribute(name,store[name]);
            });
            attrOriginals.delete(n);
          }
        }
      }

      restoreNode(base);

      if(base.nodeType!==3){
        var walker=document.createTreeWalker(base,NodeFilter.SHOW_TEXT|NodeFilter.SHOW_ELEMENT);
        var n;
        while((n=walker.nextNode()))restoreNode(n);
      }
    }finally{
      translating=false;
    }
  }

  function apply(){
    scheduled=false;
    var ui=ensureUI();
    if(!ui)return;
    if(mode==='zhcn')simplifyTree(document.body);
  }

  function queue(){
    if(scheduled)return;
    scheduled=true;
    requestAnimationFrame(apply);
  }

  document.addEventListener('click',function(event){
    var btn=event.target.closest&&event.target.closest('.lang-switch button');
    if(!btn)return;

    var ui=ensureUI();
    if(!ui)return;

    if(btn.classList.contains('ss-lang-simplified')){
      event.preventDefault();
      event.stopImmediatePropagation();

      if(mode!=='zhcn')restoreTree(document.body);
      setMode('zhcn');

      internal=true;
      try{
        ui.zh.click();
      }finally{
        internal=false;
      }

      setTimeout(queue,0);
      return;
    }

    if(internal)return;

    var token=(btn.textContent||'').trim();

    if(mode==='zhcn')restoreTree(document.body);

    if(token==='日')setMode('ja');
    else if(token==='中')setMode('zhtw');
    else setMode('en');

    Array.prototype.forEach.call(ui.root.querySelectorAll('button'),function(x){x.classList.remove('active')});
    btn.classList.add('active');

    setTimeout(queue,0);
  },true);

  var observer=new MutationObserver(function(mutations){
    if(translating)return;

    if(mode==='zhcn'){
      mutations.forEach(function(m){
        if(m.type==='characterData'){
          simplifyTree(m.target);
        }else{
          Array.prototype.forEach.call(m.addedNodes||[],function(n){simplifyTree(n)});
        }
      });
    }

    queue();
  });

  function start(){
    var ui=ensureUI();

    if(ui){
      if(ui.ja.classList.contains('active'))setMode('ja');
      else if(ui.zh.classList.contains('active'))setMode('zhtw');
      else setMode('en');
    }else{
      setMode('en');
    }

    observer.observe(document.body,{childList:true,subtree:true,characterData:true,attributes:false});
    queue();
  }

  if(document.readyState==='loading'){
    document.addEventListener('DOMContentLoaded',start,{once:true});
  }else{
    start();
  }
})();
</script>
<!-- SS FOUR LANGUAGE SWITCH END -->
"""

block = block_template.replace("__TRAD__", json.dumps(trad_chars, ensure_ascii=False)).replace("__SIMP__", json.dumps(simp_chars, ensure_ascii=False))

old_set = "function setLabel(a,v){if(a&&a.textContent!==v)a.textContent=v;}"
new_set = "function setLabel(a,v){if(document.documentElement.getAttribute('data-ss-lang-mode')==='zhcn'&&window.__ssToSimplified)v=window.__ssToSimplified(v);if(a&&a.textContent!==v)a.textContent=v;}"

old_apply = "function applyCopy(d,data){var row=(copy[lang()]||copy.en)[d.id];return row?{kicker:row[0],title:row[1],support:row[2]||''}:data}"
new_apply = "function applyCopy(d,data){var row=(copy[lang()]||copy.en)[d.id],out=row?{kicker:row[0],title:row[1],support:row[2]||''}:data;if(document.documentElement.getAttribute('data-ss-lang-mode')==='zhcn'&&window.__ssToSimplified)out={kicker:window.__ssToSimplified(out.kicker),title:window.__ssToSimplified(out.title),support:window.__ssToSimplified(out.support)};return out}"

if new_set not in s:
    assert old_set in s, "Navigation setLabel hook not found"
    s = s.replace(old_set, new_set, 1)

if new_apply not in s:
    assert old_apply in s, "Unified heading applyCopy hook not found"
    s = s.replace(old_apply, new_apply, 1)

marker = "<!-- SS FOUR LANGUAGE SWITCH START -->"
if marker not in s:
    insert_marker = "<!-- Section hierarchy navigation -->"
    assert insert_marker in s, "Navigation marker not found"
    s = s.replace(insert_marker, block + "\n\n" + insert_marker, 1)

assert s.count("<!-- SS FOUR LANGUAGE SWITCH START -->") == 1
assert s.count("<!-- SS FOUR LANGUAGE SWITCH END -->") == 1
for token in ["简体中文", "繁體中文", "window.__ssToSimplified", "data-ss-lang-mode"]:
    assert token in s, f"Missing token: {token}"

path.write_text(s, encoding="utf-8")

# Syntax-check the injected runtime.
m = re.search(r'<script id="ss-four-language-script">(.*?)</script>', s, re.S)
assert m, "Four-language runtime missing"
check = Path(".ss-four-language-check.js")
check.write_text(m.group(1), encoding="utf-8")
subprocess.run(["node", "--check", str(check)], check=True)
check.unlink()

print(f"Installed four-language switch with {len(pairs)} Traditional->Simplified character mappings.")
