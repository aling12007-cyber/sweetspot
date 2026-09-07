from pathlib import Path
import re

css_path = Path('assets/case-study-split.css')
css = css_path.read_text(encoding='utf-8')
marker = '/* Contact heading emphasis — 35% above main heading scale */'
if marker not in css:
    css += '''\n\n/* Contact heading emphasis — 35% above main heading scale */\n#contact .contact-inner h2{\n  font-size:clamp(46px,5.4vw,78px)!important;\n}\n@media(max-width:760px){\n  #contact .contact-inner h2{\n    font-size:46px!important;\n  }\n}\n'''
    css_path.write_text(css, encoding='utf-8')

idx_path = Path('index.html')
idx = idx_path.read_text(encoding='utf-8')
pattern = r'assets/case-study-split\.css\?v=[^"\']+'
replacement = 'assets/case-study-split.css?v=contact-heading-135-20260908'
new_idx, count = re.subn(pattern, replacement, idx, count=1)
if count == 1:
    idx_path.write_text(new_idx, encoding='utf-8')
elif replacement not in idx:
    raise SystemExit(f'Expected one case-study stylesheet cache reference, found {count}')
