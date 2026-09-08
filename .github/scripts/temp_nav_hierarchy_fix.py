from pathlib import Path

path = Path('assets/site-enhancements.js')
s = path.read_text(encoding='utf-8')

old = """      en:{home:'HOME',introduction:'INTRODUCTION',foundation:'FOUNDATION / PURPOSE',nameLogo:'NAME / LOGO',standFor:'WHAT WE STAND FOR',difference:'DIFFERENCE',founder:'FOUNDER',career:'CAREER',network:'NETWORK',caseStudy:'CASE STUDY',insights:'INSIGHTS',contact:'CONTACT',submenu:' subsections'},
      ja:{home:'ホーム',introduction:'会社紹介',foundation:'創立 / 理念',nameLogo:'名称 / ロゴ',standFor:'私たちの理念',difference:'私たちの強み',founder:'創業者',career:'経歴',network:'ネットワーク',caseStudy:'ケーススタディ',insights:'インサイト',contact:'お問い合わせ',submenu:'のサブメニュー'},
      zhtw:{home:'首頁',introduction:'公司簡介',foundation:'創立 / 理念',nameLogo:'名稱 / LOGO',standFor:'核心理念',difference:'差異化優勢',founder:'創辦人',career:'職涯',network:'產業網絡',caseStudy:'案例研究',insights:'洞察',contact:'聯絡我們',submenu:'子選單'},
      zhcn:{home:'首页',introduction:'公司简介',foundation:'创立 / 理念',nameLogo:'名称 / LOGO',standFor:'核心理念',difference:'差异化优势',founder:'创办人',career:'职业经历',network:'行业网络',caseStudy:'案例研究',insights:'洞察',contact:'联系我们',submenu:'子菜单'}
"""
new = """      en:{home:'HOME',introduction:'INTRODUCTION',foundation:'FOUNDATION / PURPOSE',nameLogo:'NAME / LOGO',standFor:'WHAT WE STAND FOR',difference:'DIFFERENCE',founder:'FOUNDER',network:'NETWORK',industryAccess:'INDUSTRY ACCESS',caseStudy:'CASE STUDY',insights:'INSIGHTS',contact:'CONTACT',submenu:' subsections'},
      ja:{home:'ホーム',introduction:'会社紹介',foundation:'創立 / 理念',nameLogo:'名称 / ロゴ',standFor:'私たちの理念',difference:'私たちの強み',founder:'創業者',network:'ネットワーク',industryAccess:'業界アクセス',caseStudy:'ケーススタディ',insights:'インサイト',contact:'お問い合わせ',submenu:'のサブメニュー'},
      zhtw:{home:'首頁',introduction:'公司簡介',foundation:'創立 / 理念',nameLogo:'名稱 / LOGO',standFor:'核心理念',difference:'差異化優勢',founder:'創辦人',network:'產業網絡',industryAccess:'產業資源與連結',caseStudy:'案例研究',insights:'洞察',contact:'聯絡我們',submenu:'子選單'},
      zhcn:{home:'首页',introduction:'公司简介',foundation:'创立 / 理念',nameLogo:'名称 / LOGO',standFor:'核心理念',difference:'差异化优势',founder:'创办人',network:'行业网络',industryAccess:'行业资源与连接',caseStudy:'案例研究',insights:'洞察',contact:'联系我们',submenu:'子菜单'}
"""
assert s.count(old) == 1, 'nav copy block mismatch'
s = s.replace(old, new, 1)

old = "var version='20260908-contact-simple-v7-'+lang;"
new = "var version='20260908-nav-hierarchy-v8-'+lang;"
assert s.count(old) == 1, 'nav version mismatch'
s = s.replace(old, new, 1)

old = """      {href:'#founder',label:c.founder,classes:'nav-level-1 nav-parent',children:[
        {href:'#experience',label:c.career}
      ]},
      {href:'#network',label:c.network,classes:'nav-level-1 nav-parent',children:[
        {href:'#capabilities',label:c.caseStudy}
      ]},
"""
new = """      {href:'#founder',label:c.founder,classes:'nav-level-1'},
      {href:'#network',label:c.network,classes:'nav-level-1 nav-parent',children:[
        {href:'#network-access',label:c.industryAccess},
        {href:'#capabilities',label:c.caseStudy}
      ]},
"""
assert s.count(old) == 1, 'navigation groups mismatch'
s = s.replace(old, new, 1)

old = "nav.querySelectorAll('.ss-nav-group').length===3&&"
new = "nav.querySelectorAll('.ss-nav-group').length===2&&"
assert s.count(old) == 1, 'group count mismatch'
s = s.replace(old, new, 1)

needle = """  function patchNavigation(){
"""
insert = """  function patchNetworkAccessAnchor(){
    var network=document.querySelector('#network');
    if(!network)return;
    if(network.querySelector('#network-access'))return;

    var heading=network.querySelector('.ss-unified-heading[data-ss-section=\"network\"], .major-insights-title, .section-title');
    if(heading&&!heading.id){
      heading.id='network-access';
      heading.style.scrollMarginTop='96px';
      return;
    }

    var anchor=document.createElement('span');
    anchor.id='network-access';
    anchor.setAttribute('aria-hidden','true');
    anchor.style.cssText='display:block;height:0;scroll-margin-top:96px;';
    network.insertBefore(anchor,network.firstChild);
  }

  function patchNavigation(){
"""
assert s.count(needle) == 1, 'patchNavigation insertion point mismatch'
s = s.replace(needle, insert, 1)

old = """      patchNavigation();
      patchHero();
"""
new = """      patchNetworkAccessAnchor();
      patchNavigation();
      patchHero();
"""
assert s.count(old) == 1, 'apply block mismatch'
s = s.replace(old, new, 1)

path.write_text(s, encoding='utf-8')

assert "label:c.career" not in s
assert "INDUSTRY ACCESS" in s
assert "href:'#network-access'" in s
assert "length===2&&" in s
