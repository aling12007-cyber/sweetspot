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

- The retired Unsplash Hero stadium URL has been removed from `index.html` and must not be restored.
- `assets/case-study-split.css` continues to suppress the legacy `.photo-card::before` layer while preserving the current Tokyo Tower composition.
- `index.html` statically preloads the Tokyo Tower image with high fetch priority.
- `assets/site-enhancements.js` keeps the rendered Tokyo Tower image at high fetch priority and removes the stale outer accessibility label so the existing Tokyo Tower image alternative text is used.

## Repository hygiene

- `founder.jpg`, `logo.jpg`, and `noop` are retired root-level files and should not be restored.
- Every local `assets/...` reference should resolve to an existing file.
- Run the site-integrity workflow for changes to `index.html`, `assets/**`, `favicon.svg`, `robots.txt`, `sitemap.xml`, or the integrity workflow itself.
- Remove merged or abandoned maintenance branches after their work is complete.

## Pull request safeguards

- The default branch is protected by an active repository ruleset.
- All changes to `main` should go through a pull request.
- The required checks are `integrity` and `validate`.
- Both required workflows run on every pull request so required checks cannot remain pending because of path filters.
- `Validate site integrity` can also be run manually with `workflow_dispatch`.
- Dependabot checks GitHub Actions dependencies weekly and should update them through normal pull requests and required checks.

## Source-project constraint

There is currently no `src/`, `package.json`, or equivalent unbundled application source on `main`. Do not reverse-engineer or rebuild the React application from the minified bundle when output equivalence is required. If the original source project is recovered later, migrate only with explicit visual, content, responsive, and interaction equivalence checks.
