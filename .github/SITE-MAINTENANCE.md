# Site maintenance invariants

This repository currently stores the deployed site artifact rather than an unbundled React source project. Preserve the rendered site while maintaining it.

## Do not change without an explicit content/design request

- Visible copy in any language.
- Navigation destinations or interaction behavior.
- Layout, spacing, typography, colors, overlays, or responsive behavior.
- Existing image choices or crop/position settings.
- The Tokyo Tower hero image: `assets/images/site-5fa8ee41a447.webp`.
- The intentionally used Career Playbook stadium texture in `#experience`.

## Hero safeguards

- The retired Unsplash hero stadium image must never be allowed to render behind the Tokyo Tower image.
- `assets/case-study-split.css` neutralizes the legacy `.photo-card::before` background while the bundled source still contains the old declaration.
- `assets/site-enhancements.js` gives the Tokyo Tower image high fetch priority and removes the stale outer accessibility label so the existing Tokyo Tower image alternative text is used.

## Repository hygiene

- `founder.jpg`, `logo.jpg`, and `noop` are retired root-level files and should not be restored.
- Every local `assets/...` reference should resolve to an existing file.
- Run the site-integrity workflow for changes to `index.html`, `assets/**`, or the integrity workflow itself.

## Source-project constraint

There is currently no `src/`, `package.json`, or equivalent unbundled application source on `main`. Do not reverse-engineer or rebuild the React application from the minified bundle when output equivalence is required. If the original source project is recovered later, migrate only with explicit visual, content, responsive, and interaction equivalence checks.
