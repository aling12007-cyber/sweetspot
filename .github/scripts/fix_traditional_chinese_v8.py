from pathlib import Path
import importlib.util, subprocess
ROOT=Path(__file__).resolve().parents[2]
INDEX=ROOT/'index.html'

spec=importlib.util.spec_from_file_location('v7',ROOT/'.github/scripts/fix_traditional_chinese_v7.py')
v7=importlib.util.module_from_spec(spec);spec.loader.exec_module(v7)
# v7 executes the complete localization patch at import time.

s=INDEX.read_text(encoding='utf-8')

marker="  function simplifyTree(scope){\n    if(mode!=='zhcn' || translating)return;"
insert="  function resetLanguageDropdownLabels(){\n    var select=document.querySelector('.lang-dropdown-select');\n    if(!select||select.options.length<4)return;\n    var labels=['English','日本語','简体中文','繁體中文'];\n    for(var i=0;i<4;i++)if(select.options[i].text!==labels[i])select.options[i].text=labels[i];\n  }\n\n  function simplifyTree(scope){\n    if(mode!=='zhcn' || translating)return;"
if marker in s:s=s.replace(marker,insert,1)
elif 'function resetLanguageDropdownLabels()' not in s:raise RuntimeError('simplifyTree insertion point missing')

old="    }finally{\n      translating=false;\n    }\n  }\n\n  function restoreTree(scope){"
new="    }finally{\n      resetLanguageDropdownLabels();\n      translating=false;\n    }\n  }\n\n  function restoreTree(scope){"
if old in s:s=s.replace(old,new,1)
elif 'resetLanguageDropdownLabels();\n      translating=false;' not in s:raise RuntimeError('simplifyTree finalizer missing')

INDEX.write_text(s,encoding='utf-8')
subprocess.run(['git','diff','--check'],cwd=ROOT,check=True)
print('Simplified conversion now restores immutable language dropdown labels')
