from pathlib import Path

index_path = Path('index.html')
workflow_path = Path('.github/workflows/validate-heading-integrity.yml')

s = index_path.read_text(encoding='utf-8')

old_maps = """  var mobileLabels={
    en:{company:'Company Features',points:'Points of Difference',founder:'Introducing the Founder',experience:'Career Playbook',network:'Broad Influence and Access',capabilities:'Case Study Apple'},
    ja:{company:'会社の特徴',points:'私たちの強み',founder:'創業者紹介',experience:'キャリア・プレイブック',network:'幅広い影響力とアクセス',capabilities:'ケーススタディ Apple'},
    zh:{company:'公司特色',points:'核心優勢',founder:'創辦人介紹',experience:'職涯軌跡',network:'廣泛的影響力與資源管道',capabilities:'案例研究 Apple'}
  };
  var desktopLabels={
    en:{company:'Company',points:'Difference',founder:'Founder',network:'Network',capabilities:'Cases'},
    ja:{company:'会社',points:'強み',founder:'創業者',network:'ネットワーク',capabilities:'事例'},
    zh:{company:'公司',points:'優勢',founder:'創辦人',network:'資源網絡',capabilities:'案例'}
  };"""
new_maps = """  var navLabels={
    en:{company:'Company Introduction',points:'Points of Difference',founder:'Introducing the Founder',experience:'Professional Journey',network:'Broad Influence and Access',capabilities:'Case Study Apple'},
    ja:{company:'会社紹介',points:'私たちの強み',founder:'創業者紹介',experience:'プロフェッショナル・ジャーニー',network:'幅広い影響力とアクセス',capabilities:'ケーススタディ Apple'},
    zh:{company:'公司簡介',points:'核心優勢',founder:'創辦人介紹',experience:'專業歷程',network:'廣泛的影響力與資源管道',capabilities:'案例研究 Apple'}
  };"""
assert old_maps in s, 'Expected navigation label maps not found'
s = s.replace(old_maps, new_maps, 1)

old_apply = """    if(window.innerWidth<=1050){
      var m=mobileLabels[l];
      Object.keys(m).forEach(function(k){setLabel(links[k],m[k]);});
    }else{
      var d=desktopLabels[l];
      Object.keys(d).forEach(function(k){setLabel(links[k],d[k]);});
    }"""
new_apply = """    var labels=navLabels[l];
    Object.keys(labels).forEach(function(k){setLabel(links[k],labels[k]);});"""
assert old_apply in s, 'Expected responsive navigation label switch not found'
s = s.replace(old_apply, new_apply, 1)

repls = {
"""    en:{
      points:['Difference','Points of Difference',''],""": """    en:{
      company:['Company','Company Introduction',''],
      points:['Difference','Points of Difference',''],""",
"""    ja:{
      points:['差別化','私たちの強み',''],""": """    ja:{
      company:['会社','会社紹介',''],
      points:['差別化','私たちの強み',''],""",
"""    zh:{
      points:['差異','核心優勢',''],""": """    zh:{
      company:['公司','公司簡介',''],
      points:['差異','核心優勢',''],""",
}
for old, new in repls.items():
    assert old in s, f'Expected unified heading language block not found: {old[:24]!r}'
    s = s.replace(old, new, 1)

index_path.write_text(s, encoding='utf-8')

w = workflow_path.read_text(encoding='utf-8')
old_required = """          required=[
            \"points:['Difference','Points of Difference','']\",
            \"experience:['Career','Professional Journey','Built across APAC']\",
            \"network:['Network','Broad Influence and Access','Services rendered to:']\",
            \"capabilities:['Case','Case Study Apple','Demonstrated high-level facilitation capability']\"
          ]"""
new_required = """          required=[
            \"company:['Company','Company Introduction','']\",
            \"company:['会社','会社紹介','']\",
            \"company:['公司','公司簡介','']\",
            \"points:['Difference','Points of Difference','']\",
            \"experience:['Career','Professional Journey','Built across APAC']\",
            \"network:['Network','Broad Influence and Access','Services rendered to:']\",
            \"capabilities:['Case','Case Study Apple','Demonstrated high-level facilitation capability']\",
            \"en:{company:'Company Introduction',points:'Points of Difference',founder:'Introducing the Founder',experience:'Professional Journey',network:'Broad Influence and Access',capabilities:'Case Study Apple'}\",
            \"ja:{company:'会社紹介',points:'私たちの強み',founder:'創業者紹介',experience:'プロフェッショナル・ジャーニー',network:'幅広い影響力とアクセス',capabilities:'ケーススタディ Apple'}\",
            \"zh:{company:'公司簡介',points:'核心優勢',founder:'創辦人介紹',experience:'專業歷程',network:'廣泛的影響力與資源管道',capabilities:'案例研究 Apple'}\"
          ]"""
assert old_required in w, 'Expected integrity required block not found'
w = w.replace(old_required, new_required, 1)
workflow_path.write_text(w, encoding='utf-8')

print('Patched Company Introduction and synchronized navigation labels.')
