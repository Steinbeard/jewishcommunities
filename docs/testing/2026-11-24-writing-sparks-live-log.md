# Writing sparks v2: first live UI check

**Status: 2026-11-24, done by a Sonnet test agent through the xTiger MCP tools. Screenshots are in [screenshots/2026-11-24-writing-sparks/](screenshots/2026-11-24-writing-sparks/).** Feature: [the v2 spec](../spec/2026-11-24-writing-sparks-v2.md).

## Method

- Booted `bm_1066_kehillah_worms` as `d_kehillah_worms` (Rav Isaac) through `ck3_run_start`. The agent closed its own game afterwards (PID 35168).
- Set up through `ck3_script`:
  - gave mastery of a few works;
  - filled slots with the pool effects (which choose a random form, so "Order of Prayer, from Bavli Nezikin" is a setup artefact);
  - raised tiers and refreshed paths;
  - viewed Rashi by setting `kehillah_learning_view = character:9000201`;
  - fired `kehillah_spark.0001` and `.0002`.
- Downscaled screenshots to 1280×720.

## Results

| Check | Result |
|---|---|
| Empty cards (01) | Pass: dimmed icon, "Master a work of X to spark an idea." |
| Insight cards (02) | Pass: name, "From <book>", one star, four routes with ✗ and aptitude *39 / 44* |
| Chiddush cards (03, 03b) | Pass: two stars. Generic forms show "No unwritten landmark is open"; Torah Commentary shows the eight-line historical path plus the *before 1160* and *before 1268* paths |
| Viewed character, Rashi (04) | Pass: card renders and the Write button is hidden. His shortcut lines show ✗ correctly, since a 1066 Rashi has Learning 12 and no Parshanut experience yet |
| Write a Sefer event (05, 05b) | Pass: options read *Torah Commentary (Chiddush)*; tooltip is tier, used-up line and AI weight (debug mode) |
| Competing Idea event (06) | Pass: names the source, the new form and the held spark with its tier. "Pursue" not clicked |
| Intrigue writing entry (07) | Pass: *Writing a Sefer: Torah Commentary* with icon. The scheme starts one day after the choice, by design (`kehillah_writing.0010`) |
| Top-bar suggestion (08) | Pass: *An Idea to Write* listed when no writing scheme runs |

## Bugs

- **Fixed:** `gui/kehillah_scheme_widget.gui` used `margin_left` on the two spark `icon`s. The game does not handle that property, and it logged `Property 'margin_left' not handled` plus `Error setting properties` once each. Removed from the GUI and from `scripts/kehillah_scheme_widget_sparks.py`.
- **Pre-existing, not sparks:**
  - The Learning window's intro text overlaps the band art and is clipped.
  - For the player it reads "your Learning" / "The works you has mastered" (the name concatenation in `KEHILLAH_LEARNING_INTRO_*`).
- No floods from `Character.Custom`, `IsLocalPlayer` or the `GetList` datamodel.

## Not covered

- The Studying Torah spark icon.
- Scrolling to the third card and the lower path lines; the agent had no scroll tool.
- The competing idea's "Pursue" option.
- Hovering the Write button and the stars.
- A real study-to-spark cycle without script setup.
