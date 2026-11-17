# Player wiki site maintenance

**Status:** GitHub Pages setup, 2026-11-16. The public site uses the repository's `docs/` folder and Jekyll's built-in GitHub Pages build.

The public URL is <https://steinbeard.github.io/jewishcommunities/>. The source is `docs/index.html`, `docs/_layouts/default.html`, `docs/assets/site.css`, the five pages under `docs/wiki/`, and the curated images under `docs/images/`. Edit those files in this repository; the Markdown guides remain readable on GitHub. GitHub Pages' built-in relative-links plugin changes guide links ending in `.md` to the rendered pages.

While [PR #71](https://github.com/Steinbeard/jewishcommunities/pull/71) is under review, Pages publishes from branch `docs/prealpha-readme-wiki-20261116`, folder `/docs`. **After that PR merges**, switch the Pages source to `master`, folder `/docs` under repository Settings → Pages. This avoids publishing an old branch after the review branch has been merged. Subsequent edits to `docs/` on `master` will then publish automatically. Keep this note current when the source changes.

To check a change, open the site on desktop and mobile widths, follow the four navigation links, and verify the real game images and relative guide links. The site is informational; its external Google Fonts may fall back to system fonts when blocked.
