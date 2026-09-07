from pathlib import Path

index_path = Path('index.html')
index = index_path.read_text(encoding='utf-8')
index_repls = {
    "      points:['Difference','Points of Difference',''],\n      experience:['Career','Professional Journey','Built across APAC'],": "      points:['Difference','Points of Difference',''],\n      founder:['Founder','Sam L. Pearson',''],\n      experience:['Career','Professional Journey','Built across APAC'],",
    "      points:['差別化','私たちの強み',''],\n      experience:['キャリア','プロフェッショナル・ジャーニー','APACで築いたキャリア'],": "      points:['差別化','私たちの強み',''],\n      founder:['創業者','Sam L. Pearson',''],\n      experience:['キャリア','プロフェッショナル・ジャーニー','APACで築いたキャリア'],",
    "      points:['差異','核心優勢',''],\n      experience:['職涯','專業歷程','深耕亞太地區'],": "      points:['差異','核心優勢',''],\n      founder:['創辦人','Sam L. Pearson',''],\n      experience:['職涯','專業歷程','深耕亞太地區'],",
}
for old, new in index_repls.items():
    assert index.count(old) == 1, f'index target mismatch: {old}'
    index = index.replace(old, new, 1)
index_path.write_text(index, encoding='utf-8')

js_path = Path('assets/site-enhancements.js')
js = js_path.read_text(encoding='utf-8')
anchor = "function patchFounderCareer(){\n"
assert js.count(anchor) == 1, 'patchFounderCareer anchor mismatch'
founder_identity = r'''function patchFounderIdentity(){
  var founder=document.querySelector('#founder');
  if(!founder)return;

  var lang=currentLanguage();
  var labels={
    en:{role:'FOUNDER',location:'Tokyo, Japan'},
    ja:{role:'創業者',location:'東京、日本'},
    zhtw:{role:'創辦人',location:'東京，日本'},
    zhcn:{role:'创办人',location:'东京，日本'}
  };
  var copy=labels[lang]||labels.en;
  var caption=founder.querySelector('.founder-caption');
  if(!caption)return;

  var role=caption.querySelector('span');
  var location=caption.querySelector('small');
  if(role)role.textContent=copy.role;
  if(location)location.textContent=copy.location;
}

'''
js = js.replace(anchor, founder_identity + anchor, 1)
apply_anchor = "      patchIntroduction();\n      patchFounderCareer();"
assert js.count(apply_anchor) == 1, 'apply anchor mismatch'
js = js.replace(apply_anchor, "      patchIntroduction();\n      patchFounderIdentity();\n      patchFounderCareer();", 1)
js_path.write_text(js, encoding='utf-8')

wf_path = Path('.github/workflows/validate-heading-integrity.yml')
wf = wf_path.read_text(encoding='utf-8')
wf_repls = {
    "            \"points:['Difference','Points of Difference','']\",\n            \"experience:['Career','Professional Journey','Built across APAC']\",": "            \"points:['Difference','Points of Difference','']\",\n            \"founder:['Founder','Sam L. Pearson','']\",\n            \"founder:['創業者','Sam L. Pearson','']\",\n            \"founder:['創辦人','Sam L. Pearson','']\",\n            \"experience:['Career','Professional Journey','Built across APAC']\",",
    "            \"創業者の経歴をもっと見る\"": "            \"創業者の経歴をもっと見る\",\n            \"function patchFounderIdentity(){\",\n            \"zhtw:{role:'創辦人',location:'東京，日本'}\",\n            \"zhcn:{role:'创办人',location:'东京，日本'}\"",
}
for old, new in wf_repls.items():
    assert wf.count(old) == 1, f'workflow target mismatch: {old}'
    wf = wf.replace(old, new, 1)
wf_path.write_text(wf, encoding='utf-8')

print('Founder i18n patch applied')
