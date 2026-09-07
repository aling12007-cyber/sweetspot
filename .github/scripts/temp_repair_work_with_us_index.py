from pathlib import Path
import subprocess

main_html=subprocess.check_output(['git','show','origin/main:index.html'],text=True)
old_css='assets/case-study-split.css?v=intro-big-headings-20260907'
new_css='assets/case-study-split.css?v=work-with-us-20260907'
old_js='assets/site-enhancements.js?v=heading-consistency-i18n-20260907'
new_js='assets/site-enhancements.js?v=work-with-us-20260907'
assert main_html.count(old_css)==1, f'css ref count: {main_html.count(old_css)}'
assert main_html.count(old_js)==1, f'js ref count: {main_html.count(old_js)}'
html=main_html.replace(old_css,new_css,1).replace(old_js,new_js,1)
Path('index.html').write_text(html,encoding='utf-8')
