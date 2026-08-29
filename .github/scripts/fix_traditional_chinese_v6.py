from pathlib import Path
import importlib.util, subprocess
ROOT=Path(__file__).resolve().parents[2]
INDEX=ROOT/'index.html'

spec=importlib.util.spec_from_file_location('v5',ROOT/'.github/scripts/fix_traditional_chinese_v5.py')
v5=importlib.util.module_from_spec(spec);spec.loader.exec_module(v5)
# v5 executes its patch at import time.

s=INDEX.read_text(encoding='utf-8')

# Keep a direct, mode-aware refresh function inside the existing unified heading controller.
old="  function run(){queued=false;defs.forEach(function(d){var section=document.getElementById(d.id);if(!section)return;var src=chooseSource(section,d);if(!src)return;make(section,src,d,applyCopy(d,extract(src,d)))})}\n  function queue(){if(queued)return;queued=true;requestAnimationFrame(run)}"
new="  function run(){queued=false;defs.forEach(function(d){var section=document.getElementById(d.id);if(!section)return;var src=chooseSource(section,d);if(!src)return;make(section,src,d,applyCopy(d,extract(src,d)))})}\n  window.__ssRefreshUnifiedHeadings=run;\n  function queue(){if(queued)return;queued=true;requestAnimationFrame(run)}"
if old in s:s=s.replace(old,new,1)
elif 'window.__ssRefreshUnifiedHeadings=run;' not in s:raise RuntimeError('Unified heading run hook missing')

# Invoke the existing unified heading renderer only after the language mode is settled.
old="  function setMode(next){\n    mode=next;\n    document.documentElement.setAttribute('data-ss-lang-mode',next);\n    document.documentElement.lang=next==='ja'?'ja':next==='zhcn'?'zh-Hans':next==='zhtw'?'zh-Hant':'en';\n  }"
new="  function setMode(next){\n    mode=next;\n    document.documentElement.setAttribute('data-ss-lang-mode',next);\n    document.documentElement.lang=next==='ja'?'ja':next==='zhcn'?'zh-Hans':next==='zhtw'?'zh-Hant':'en';\n    setTimeout(function(){if(window.__ssRefreshUnifiedHeadings)window.__ssRefreshUnifiedHeadings();},0);\n    setTimeout(function(){if(window.__ssRefreshUnifiedHeadings)window.__ssRefreshUnifiedHeadings();},80);\n  }"
if old in s:s=s.replace(old,new,1)
elif new not in s:raise RuntimeError('setMode hook missing')

INDEX.write_text(s,encoding='utf-8')
subprocess.run(['git','diff','--check'],cwd=ROOT,check=True)
print('Language mode now refreshes the existing unified heading renderer directly')
