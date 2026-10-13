# Mo'adim le-Simchah — 2026-10-13

**Status: Feast overlay proposal; holiday-frequency hook source verified, not live tested.** This refines the Jewish tenet proposals in the 2026-10-13 review spreadsheet and depends on the existing holiday calendar described in [jewish-holiday-variety.md](../implementation/jewish-holiday-variety.md). Daniel's 2026-10-13 correction supersedes the earlier Sukkot hospitality decision prototype: festival observance should add Jewish flavor and rewards to vanilla feasts, with no new decision or feast intent. The prototype was removed before commit.

## Tenet identity

**Mo'adim le-Simchah** is a useful player-facing name for the observance theme. The phrase is a festival greeting, especially associated with Pesach and Sukkot, rather than a historical school of Jewish thought. Its description should explain the broader commitment: honoring appointed festivals through household meals, hospitality, and communal celebration. Keep the weekly Shabbat meal in the broader flavor pool without presenting Shabbat as a *mo'ed* or a pilgrimage festival.

Vanilla `tenet_ritual_celebrations` is the mechanical starting point. Samaritanism already has it; Rabbinism does not. Do not change starting rite slots or globally rename the tenet yet: the same vanilla tenet is used by non-Jewish rites. A later Jewish-specific display name or custom tenet can be chosen after the full tenet-pool review.

## One feast overlay

For a Jewish host whose rite has the tenet, an ordinary, successfully completed vanilla feast may gain a Jewish meal theme and a modest bonus. It remains the same feast activity, with its existing cost, guests, intents, and ordinary outcomes. The proposed default is a single flavor beat during the feast or a contextual conclusion line, followed by a small host modifier that improves close-relative opinion, extra Piety from the meal, and, for a Kehillah leader, a small Stability gain. The family effect should favor attending close relatives if the feast system exposes that set cleanly; otherwise a short, modest close-relative-opinion modifier is acceptable. Limit the bonus to once per feast and exclude murder feasts.

Possible themes are **Pesach Seder**, **Sukkot seudah**, **Shavuot seudah**, and **Shabbat seudah**. The Seder is specific enough that it should require an explicit Pesach holiday state, not just a broad spring month. Likewise, do not infer a Shabbat from CK3's month: it is a weekly observance. Until the calendar can mark a suitable date, use a generic Jewish festive meal line rather than falsely naming a specific holiday. A later small state flag from the existing holiday events could mark a nearby Pesach, Sukkot, or Shavuot celebration, allowing a matching feast to pick up that theme. It should not rename every feast in that month or override the shared `activity_feast_name` localization.

Vanilla's `activity_feast` currently excludes the Kehillah custom government from hosting. This overlay therefore reaches landed Jewish hosts first. Giving a Kehillah leader a feast-like activity is a separate access problem; do not create a parallel activity merely to make this tenet function. The existing Jewish holiday events and frequency benefit still reach Kehillah characters.

## Implemented frequency hook

The tenet now halves the quiet-year weight in `jewish_holiday_yearly_pulse`. At the existing 25% evaluation gate, the approximate chance that a Jewish character queues one of the 13 holiday events rises from 11.6% to 15.9% per year. This adds no extra event roll and applies to any Jewish rite taking the vanilla tenet. It does not alter other religions' holiday pools.

`git diff --check` passed. `ck3-tiger` reported only `unknown token rite` for this touched file; installed CK3 1.20.1 vanilla feast scripts use `rite = { rite_has_tenet = tenet_ritual_celebrations }` in character scope, so this is a 1.19-linter mismatch. A live test was attempted but two simultaneous CK3 processes shared the game UI and logs; no reliable behavior check was completed.

The phrase's contemporary use is described by [My Jewish Learning's Sukkot greeting guide](https://www.myjewishlearning.com/article/how-to-greet-someone-on-sukkot/) and [Passover greeting guide](https://www.myjewishlearning.com/article/how-to-greet-people-on-passover/).
