from pathlib import Path
import importlib.util, subprocess
ROOT=Path(__file__).resolve().parents[2]
INDEX=ROOT/'index.html'

spec=importlib.util.spec_from_file_location('v4',ROOT/'.github/scripts/fix_traditional_chinese_v4.py')
v4=importlib.util.module_from_spec(spec);spec.loader.exec_module(v4)
v4.patch_index()

s=INDEX.read_text(encoding='utf-8')
old="function applyCopy(d,data){var row=(copy[lang()]||copy.en)[d.id],out=row?{kicker:row[0],title:row[1],support:row[2]||''}:data;if(document.documentElement.getAttribute('data-ss-lang-mode')==='zhcn'&&window.__ssToSimplified)out={kicker:window.__ssToSimplified(out.kicker),title:window.__ssToSimplified(out.title),support:window.__ssToSimplified(out.support)};return out}"
new="function applyCopy(d,data){var m=document.documentElement.getAttribute('data-ss-lang-mode')||'',code=m==='ja'?'ja':(m==='zhtw'||m==='zhcn'?'zh':lang()),row=(copy[code]||copy.en)[d.id],out=row?{kicker:row[0],title:row[1],support:row[2]||''}:data;if(m==='zhcn'&&window.__ssToSimplified)out={kicker:window.__ssToSimplified(out.kicker),title:window.__ssToSimplified(out.title),support:window.__ssToSimplified(out.support)};return out}"
if old in s:s=s.replace(old,new,1)
elif new not in s:raise RuntimeError('Unified heading applyCopy hook missing')

old="  new MutationObserver(queue).observe(document.body,{childList:true,subtree:true,characterData:true});\n  document.addEventListener('click',function(e){if(e.target.closest&&e.target.closest('.lang-switch'))setTimeout(queue,0)});"
new="  new MutationObserver(queue).observe(document.body,{childList:true,subtree:true,characterData:true});\n  new MutationObserver(queue).observe(document.documentElement,{attributes:true,attributeFilter:['lang','data-ss-lang-mode']});\n  document.addEventListener('click',function(e){if(e.target.closest&&e.target.closest('.lang-switch'))setTimeout(queue,0)});"
if old in s:s=s.replace(old,new,1)
elif new not in s:raise RuntimeError('Unified heading mode observer insertion point missing')

INDEX.write_text(s,encoding='utf-8')
subprocess.run(['git','diff','--check'],cwd=ROOT,check=True)
print('Unified headings now follow explicit Chinese mode')
