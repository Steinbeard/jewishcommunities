# Sefer shelf and Jewish tenet UI — 2026-10-15

**Status: Live visual checks passed; feast event behavior pending.** Tested the Codex worktree in its isolated CK3 `-userdir` profile on the primary display at Daniel's request. The normal primary checkout was not edited or mounted. The tested game is CK3 1.20.1; `ck3-tiger` is still targeted at 1.19.0.

## Source and static checks

- `ck3-tiger` exited 0 with no findings in the changed tenet, library GUI, or localization files. Its known global findings from the version mismatch remain.
- `git diff --check` passed. The new localization has UTF-8 BOM.
- Installed vanilla `window_faith.gui` displays a tenet's base name on faith cards. `TenetType.GetName( Rite.Self )` is used elsewhere, but using it on these cards would require a full GUI-file fork. The shared Religious Legal Pronouncements ID already supplies the Jewish tooltip name Halakha. The shared Ritual Celebrations ID is now given a Jewish dynamic name/description while preserving its vanilla mechanics and ID.

## Live run

The fresh isolated process reached the main menu and a playable Worms 1066 start as Rav Isaac. Rabbinism's cards read Legalism, Religious Law, and Talmud Torah. Religious Law's Jewish tooltip read **Halakha**. The Talmud Torah tooltip displayed the Learning-8 mastery rule, Piety and Learning lifestyle rewards, Rabbi field XP, and **Monthly Learning Lifestyle Experience +10%**. The earlier **Religious Scholar Trait Experience +10%** line was absent, confirming the modifier correction.

The Jewish Quarter Books tab showed a two-column shelf with five Worms works. Selecting a card opened its title, detail, mastery status, and **Donate this copy** action. The first screenshot was saved outside the repo at `C:\Users\Daniel\.codex\ck3-test\festival-observance\library-qa.png`. The initial vanilla `artifact_book.dds` choice appeared as narrow repeated spines because it is a four-frame texture strip. After switching to the single-image `artifact_chronicle.dds`, the final screenshot at `C:\Users\Daniel\.codex\ck3-test\festival-observance\book-icons-final.png` showed clear open-book icons, and card selection still worked.

Isaac's Rabbi trait showed the custom gold/blue icon and its three named tracks. Opening the track tooltip in the first pass caused three missing-texture errors for `parshanut.dds`, `talmudics.dds`, and `hashkafa.dds`. Three 60×60 vanilla trait-track icons were supplied under those required names. The second live run displayed a book, patterned tile, and ornamental emblem for the tracks and logged no missing track textures. The Levite icon was not tested because Isaac did not have that trait.

A final fresh Worms game opened Samaritanism's shared Ritual Celebrations tenet. Its card and tooltip heading still read **Ritual Celebrations**, while the Jewish tooltip subtitle directly beneath read **Mo'adim le-Simchah**. The description mentioned increased Jewish holiday moments, feast Piety, and goodwill from attending family; vanilla effects still listed Feast/Festival Piety and +5 vassal/courtier opinion. No Mo'adim localization or festival-override errors appeared in the fresh log. The feast event itself was not played through in this session.

The new festival override initially produced one UTF-8-BOM warning despite loading. After correcting its encoding, the second startup had no warning for that file. Two existing files still had BOM warnings (`kehillah_inheritance_actions_override.txt` and `kehillah_bet_din_sources_events.txt`). Other observed log entries included pre-existing succession/bookmark/localization problems and a missing `Labrat` history-name localization, unrelated to this UI patch. The isolated CK3 process was left running and visible on the primary monitor.
