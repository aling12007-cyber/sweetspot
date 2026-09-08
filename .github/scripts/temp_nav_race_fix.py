from pathlib import Path

index = Path('index.html')
js = Path('assets/site-enhancements.js')

# Keep the visible Japanese top-nav label concise and remove the exact text
# mismatch that caused the legacy short-label observer and enhanced nav
# observer to rewrite the navigation back and forth.
j = js.read_text(encoding='utf-8')
old = "ja:{home:'ホーム',introduction:'会社紹介',foundation:'創立 / 理念'"
new = "ja:{home:'ホーム',introduction:'会社',foundation:'創立 / 理念'"
assert j.count(old) == 1, 'Japanese navigation label source mismatch'
j = j.replace(old, new, 1)
old = "var version='20260908-nav-hierarchy-v8-'+lang;"
new = "var version='20260908-nav-hierarchy-v9-'+lang;"
assert j.count(old) == 1, 'navigation version source mismatch'
j = j.replace(old, new, 1)
js.write_text(j, encoding='utf-8')

# Stop the old short-label observer from touching a navigation that is
# already owned by site-enhancements.js. This prevents future label changes
# from reintroducing a DOM rewrite loop.
s = index.read_text(encoding='utf-8')
old = 'function a(){var h=document.querySelector("header");if(!h)return;h.querySelectorAll("a,button").forEach(r);}'
new = 'function a(){var h=document.querySelector("header"),nav=h&&h.querySelector("nav");if(!h)return;if(nav&&nav.hasAttribute("data-ss-nav-version"))return;h.querySelectorAll("a,button").forEach(r);}'
assert s.count(old) == 1, 'legacy top-navigation short-label function mismatch'
s = s.replace(old, new, 1)

# Force a fresh enhancement script after the root-cause fix.
old = 'assets/site-enhancements.js?v=ja-nav-welcome-20260908'
new = 'assets/site-enhancements.js?v=ja-nav-stable-20260908'
assert s.count(old) == 1, 'site-enhancements cache-buster source mismatch'
s = s.replace(old, new, 1)
index.write_text(s, encoding='utf-8')

assert "introduction:'会社'" in js.read_text(encoding='utf-8')
assert "nav-hierarchy-v9" in js.read_text(encoding='utf-8')
assert 'nav.hasAttribute("data-ss-nav-version")' in index.read_text(encoding='utf-8')
assert 'site-enhancements.js?v=ja-nav-stable-20260908' in index.read_text(encoding='utf-8')
