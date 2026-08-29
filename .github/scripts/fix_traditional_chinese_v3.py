from pathlib import Path
import importlib.util
import subprocess

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
V2=HERE/'fix_traditional_chinese_v2.py'
spec=importlib.util.spec_from_file_location('ss_trad_v2',V2)
mod=importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

# First apply the verified source-normalization/finalizer patch.
mod.patch()

p=ROOT/'index.html'
s=p.read_text(encoding='utf-8')
old="""  var busy=false,queued=false;
  var phrasePairs=["""
new="""  var busy=false,queued=false;
  var realSimplify=typeof window.__ssToSimplified==='function'?window.__ssToSimplified:null;
  function identitySimplify(value){return String(value==null?'':value)}
  var phrasePairs=["""
if old not in s:
    raise RuntimeError('Traditional finalizer state marker not found')
s=s.replace(old,new,1)

old="""  function run(){
    queued=false;if(busy)return;busy=true;
    try{
      fixDropdown();
      if(mode()!=='zhtw')return;
      if(document.documentElement.getAttribute('lang')!=='zh-Hant')document.documentElement.setAttribute('lang','zh-Hant');
      fixText(document.body);fixHeadings();fixTopNav();fixHeroCTA();fixDropdown();
    }finally{busy=false}
  }"""
new="""  function run(){
    queued=false;if(busy)return;busy=true;
    try{
      var m=mode();fixDropdown();
      if(!realSimplify&&typeof window.__ssToSimplified==='function'&&window.__ssToSimplified!==identitySimplify)realSimplify=window.__ssToSimplified;
      if(m==='zhtw'){
        if(window.__ssToSimplified!==identitySimplify)window.__ssToSimplified=identitySimplify;
        if(document.documentElement.getAttribute('lang')!=='zh-Hant')document.documentElement.setAttribute('lang','zh-Hant');
        fixText(document.body);fixHeadings();fixTopNav();fixHeroCTA();fixDropdown();
      }else{
        if(realSimplify&&window.__ssToSimplified!==realSimplify)window.__ssToSimplified=realSimplify;
        var desired=m==='zhcn'?'zh-Hans':m==='ja'?'ja':m==='en'?'en':'';
        if(desired&&document.documentElement.getAttribute('lang')!==desired)document.documentElement.setAttribute('lang',desired);
        fixDropdown();
      }
    }finally{busy=false}
  }"""
if old not in s:
    raise RuntimeError('Traditional finalizer run block not found')
s=s.replace(old,new,1)
p.write_text(s,encoding='utf-8')

# Reuse the full browser audit from v2 after blocking the conflicting simplifier in Traditional mode.
mod.audit()
subprocess.run(['git','diff','--check'],cwd=ROOT,check=True)
print('Traditional finalizer verified with Simplified override disabled only in zhtw mode')
