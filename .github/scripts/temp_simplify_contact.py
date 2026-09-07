from pathlib import Path
import re

js = Path('assets/site-enhancements.js')
s = js.read_text(encoding='utf-8')
s = s.replace("var version='20260908-contact-work-with-us-i18n-v6-'+lang;", "var version='20260908-contact-simple-v7-'+lang;")
old_body = """    var bodyLabels={
      en:'Whether you’re exploring the market, looking for the right partner or need a local perspective, let’s start a conversation!',
      ja:'市場進出を検討している方も、最適なパートナーを探している方も、現地の視点が必要な方も、まずは気軽にお話ししましょう！',
      zhtw:'無論您正在探索市場、尋找合適的合作夥伴，或需要在地觀點，都歡迎與我們聊聊！',
      zhcn:'无论您正在探索市场、寻找合适的合作伙伴，或需要本地视角，都欢迎与我们聊聊！'
    };"""
new_body = """    var bodyLabels={
      en:'If you’re exploring opportunities in Japan, building partnerships or looking for an experienced local perspective, let’s start a conversation.',
      ja:'日本でのビジネス機会を検討している方、パートナーシップの構築を進めている方、または経験に基づく現地の視点を求めている方は、ぜひお話ししましょう。',
      zhtw:'如果您正在探索日本市場的機會、建立合作夥伴關係，或尋求具經驗的在地觀點，歡迎與我們聊聊。',
      zhcn:'如果您正在探索日本市场的机会、建立合作伙伴关系，或寻求有经验的本地视角，欢迎与我们聊聊。'
    };"""
assert old_body in s, 'Current Contact body labels not found'
s = s.replace(old_body, new_body)
cleanup = """function patchWorkWithUs(){
  var legacy=document.querySelector('#work-with-us');
  if(legacy)legacy.remove();
  document.querySelectorAll('#contact .work-with-us-inline').forEach(function(block){block.remove();});
}
"""
pattern = r"function patchWorkWithUs\(\)\{.*?\n\}\n\nfunction patchFounderIdentity\(\)\{"
s, n = re.subn(pattern, cleanup + "\nfunction patchFounderIdentity(){", s, flags=re.S)
assert n == 1, f'patchWorkWithUs replacement count: {n}'
js.write_text(s, encoding='utf-8')

css = Path('assets/case-study-split.css')
c = css.read_text(encoding='utf-8')
new_css = """/* Simplified Contact conversion copy */
#contact .contact-inner > p:not(.eyebrow){
  max-width:880px;
  margin-left:auto;
  margin-right:auto;
  color:#c2cad4;
  font-size:clamp(20px,1.75vw,24px);
  line-height:1.6;
}
@media(max-width:760px){
  #contact .contact-inner > p:not(.eyebrow){
    max-width:100%;
    font-size:18px;
    line-height:1.55;
  }
}
"""
c, n = re.subn(r"/\* Work With Us content merged into Contact \*/.*\Z", new_css, c, flags=re.S)
assert n == 1, f'Contact CSS replacement count: {n}'
css.write_text(c, encoding='utf-8')

idx = Path('index.html')
h = idx.read_text(encoding='utf-8')
assert 'assets/case-study-split.css?v=contact-work-with-us-20260908' in h
assert 'assets/site-enhancements.js?v=contact-work-with-us-20260908' in h
h = h.replace('assets/case-study-split.css?v=contact-work-with-us-20260908', 'assets/case-study-split.css?v=contact-simple-20260908')
h = h.replace('assets/site-enhancements.js?v=contact-work-with-us-20260908', 'assets/site-enhancements.js?v=contact-simple-20260908')
idx.write_text(h, encoding='utf-8')
