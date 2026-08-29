from pathlib import Path
import importlib.util, subprocess
ROOT=Path(__file__).resolve().parents[2]
INDEX=ROOT/'index.html'

spec=importlib.util.spec_from_file_location('v6',ROOT/'.github/scripts/fix_traditional_chinese_v6.py')
v6=importlib.util.module_from_spec(spec);spec.loader.exec_module(v6)
# v6 executes the complete localization patch at import time.

s=INDEX.read_text(encoding='utf-8')
old='      select.className="lang-dropdown-select";\n      select.setAttribute("aria-label","Language");'
new='      select.className="lang-dropdown-select";\n      select.setAttribute("aria-label","Language");\n      select.setAttribute("data-ss-no-simplify","1");'
if old in s:s=s.replace(old,new,1)
elif 'select.setAttribute("data-ss-no-simplify","1");' not in s:raise RuntimeError('Dropdown creation hook missing')

# Also protect an already-created select whenever the dropdown controller reapplies.
old='    rebuild(select,buttons);\n    select.value=String(activeIndex(buttons));\n    box.classList.add("lang-dropdown-ready");'
new='    select.setAttribute("data-ss-no-simplify","1");\n    rebuild(select,buttons);\n    select.value=String(activeIndex(buttons));\n    box.classList.add("lang-dropdown-ready");'
if old in s:s=s.replace(old,new,1)
elif 'select.setAttribute("data-ss-no-simplify","1");\n    rebuild(select,buttons);' not in s:raise RuntimeError('Dropdown apply hook missing')

INDEX.write_text(s,encoding='utf-8')
subprocess.run(['git','diff','--check'],cwd=ROOT,check=True)
print('Language dropdown labels protected from Simplified conversion')
