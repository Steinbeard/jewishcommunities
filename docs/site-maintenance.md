# Player wiki site maintenance

**Status:** GitHub Pages setup, 2026-11-16. The public site uses the repository's `docs/` folder and Jekyll's built-in GitHub Pages build.

The public URL is <https://steinbeard.github.io/jewishcommunities/>. The source is `docs/index.html`, `docs/_layouts/default.html`, `docs/assets/site.css`, the five pages under `docs/wiki/`, and the curated images under `docs/images/`. Edit those files in this repository; the Markdown guides remain readable on GitHub. GitHub Pages' built-in relative-links plugin changes guide links ending in `.md` to the rendered pages.

On 2026-11-16 the home page and shared layout were revised as documentation: overview of the playable community, first steps, a comparison of the three 1066 starts, a Domain walkthrough, a system index, and an explicit pre-alpha status section. The old library screenshot was removed from the public README and feature guide. New user-supplied images can be added beside the relevant guide text, with a caption identifying the screen, version, and what it demonstrates.

While [PR #71](https://github.com/Steinbeard/jewishcommunities/pull/71) is under review, Pages publishes from branch `docs/prealpha-readme-wiki-20261116`, folder `/docs`. **After that PR merges**, switch the Pages source to `master`, folder `/docs` under repository Settings → Pages. This avoids publishing an old branch after the review branch has been merged. Subsequent edits to `docs/` on `master` will then publish automatically. Keep this note current when the source changes.

To check a change, open the site on desktop and mobile widths, follow the four navigation links, and verify the real game images and relative guide links. The site is informational; its external Google Fonts may fall back to system fonts when blocked.

Initial deployment was verified on 2026-11-16: [the GitHub Pages build and deploy run](https://github.com/Steinbeard/jewishcommunities/actions/runs/44016089072) completed successfully for commit `167d84e`; six pages and eleven linked local assets returned HTTP 200, with no missing internal anchors. The home page and three-start guide were reviewed in desktop and 390-pixel mobile views, and the guide's Markdown links resolved to the rendered HTML pages. The repository's homepage field points to the public wiki.
