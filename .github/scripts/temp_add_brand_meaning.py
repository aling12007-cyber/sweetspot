from pathlib import Path
import re
import subprocess

js_path = Path('assets/site-enhancements.js')
js = js_path.read_text(encoding='utf-8')

replacements = [
    (
        "        nameSuffix:'.',\n        closing:'Welcome to the Sweet Spot!'",
        "        nameSuffix:'.',\n        summary:'Together, they reflect Sweet Spot’s belief in bringing the right people and opportunities together to create meaningful partnerships in sport and business.',\n        closing:'Welcome to the Sweet Spot!'"
    ),
    (
        "        nameSuffix:'）の中央に配置したデザインです。',\n        closing:'Sweet Spotへようこそ！'",
        "        nameSuffix:'）の中央に配置したデザインです。',\n        summary:'この二つには、スポーツとビジネスにおいて適切な人と機会を結びつけ、意義あるパートナーシップを生み出すという Sweet Spot の信念が込められています。',\n        closing:'Sweet Spotへようこそ！'"
    ),
    (
        "        nameSuffix:' 織品的中央。',\n        closing:'歡迎來到 Sweet Spot！'",
        "        nameSuffix:' 織品的中央。',\n        summary:'兩者共同體現了 Sweet Spot 的信念：連結合適的人與機會，在運動與商業領域創造有意義的合作夥伴關係。',\n        closing:'歡迎來到 Sweet Spot！'"
    ),
    (
        "        nameSuffix:' 织物的中央。',\n        closing:'欢迎来到 Sweet Spot！'",
        "        nameSuffix:' 织物的中央。',\n        summary:'两者共同体现了 Sweet Spot 的信念：连接合适的人与机会，在体育与商业领域创造有意义的合作伙伴关系。',\n        closing:'欢迎来到 Sweet Spot！'"
    ),
]

for old, new in replacements:
    count = js.count(old)
    assert count == 1, f'Expected exactly one copy block match, found {count}: {old[:40]}'
    js = js.replace(old, new, 1)

old_render = "    originCopy.appendChild(logoParagraph);\n    originLayout.appendChild(originCopy);"
new_render = "    originCopy.appendChild(logoParagraph);\n\n    var summaryParagraph=appendStoryParagraph(originCopy,copy.summary);\n    summaryParagraph.className='company-story-origin-copy';\n\n    originLayout.appendChild(originCopy);"
assert js.count(old_render) == 1, 'Origin copy render anchor not found exactly once'
js = js.replace(old_render, new_render, 1)

js_path.write_text(js, encoding='utf-8')
subprocess.run(['node', '--check', str(js_path)], check=True)

index_path = Path('index.html')
index = index_path.read_text(encoding='utf-8')
index, count = re.subn(r'assets/site-enhancements\.js\?v=[^\"\']+', 'assets/site-enhancements.js?v=brand-meaning-20260908', index)
assert count == 1, f'Expected exactly one site-enhancements cache reference, found {count}'
index_path.write_text(index, encoding='utf-8')

assert 'Together, they reflect Sweet Spot’s belief in bringing the right people and opportunities together to create meaningful partnerships in sport and business.' in js
assert "appendStoryParagraph(originCopy,copy.summary)" in js
print('Brand meaning summary added in all four languages and JS cache key updated.')
