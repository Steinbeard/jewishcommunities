# Player wiki

**Status:** IMPLEMENTED 2026-11-25; initial local build validates 24 pages, 95 named book entries, and all local links/anchors. GitHub publication is blocked by the current connection's read-only integration access. Intended for the existing `https://steinbeard.github.io/jewishcommunities/` address, not a separate GitHub Wiki repository. Browser review and live deployment remain pending.

This is the player-facing wiki. Keep internal specifications and test logs in their existing locations and link to them as evidence. `articles.json` contains authored guide pages, grouped navigation, summaries, and repository source paths. Its `body` fields are trusted, reviewed HTML fragments. The builder generates a shared layout, section anchors, search, and two reference pages directly from the mod's book catalog, English localization, and building definitions.

## Build and review

```powershell
python scripts/kehillah_build_wiki.py --output C:/Users/Daniel/AppData/Local/Temp/kehillah-wiki
```

Open the generated `index.html`. Python 3.12 and the standard library are sufficient; no package install or game launch is needed. Search is embedded in each page so it also works when opening local files. Article links, image links, fragment IDs, source-file existence, and duplicate IDs are checked by the builder. Generated output should not be committed. Build metadata explicitly marks previews containing uncommitted source changes.

The book page excludes empty procedural slots. Bookmark columns compare configured dates only; they do not simulate ownership, authority, dynamic authorship, or discovery. The building reference deliberately labels retained legacy definitions and does not claim that all definitions are currently constructible. Historical metadata is attributed to the mod rather than presented as newly verified research.

## Publish to the existing Pages address

1. Review the generated site and confirm it is to replace the present Pages presentation. The existing live site's contents and Pages settings could not be retrieved in this session; its current presentation was not copied or deleted.
2. Merge a focused wiki PR to `master` with these files and the roadmap entry. Do not include unrelated uncommitted game changes.
3. In repository Settings → Pages, select **GitHub Actions** as the build source if it is not already selected. This is an owner/admin setting, not an operation performed by the builder.
4. Run or inspect **Build and publish the player wiki**. PRs build an artifact; only `master` deploys. Verify the deploy job and the existing public URL.

The workflow publishes only generated wiki pages, four existing public-facing screenshots, and the wiki's assets. It does not publish the whole development documentation tree. Source/test records remain linked on GitHub. Once publication succeeds, add a prominent wiki link to the repository README.

## Maintain with feature changes

- Update the relevant article and its source links in the same PR as a player-visible change. Read status lines and superseding addenda before summarizing a specification.
- Keep source-built, live-tested, and proposed work distinct. Avoid hardcoded balance numbers unless useful to players and verified against the current source.
- Change `REVIEWED` in the builder when performing a new editorial review.
- Catalog/localization changes rebuild the references automatically. Guide prose still needs editorial review.
- Keep page slugs stable so external links continue to work. Add redirects if a slug must change.

## Validation limits

The builder checks generated documents and local links. It does not establish that external URLs are reachable, that all descriptions match engine behaviour, or that the site renders correctly in every browser. A live Pages deployment and browser review remain separate checks. No CK3 scripts, localization, GUI, succession, or title history are changed by this unit.
