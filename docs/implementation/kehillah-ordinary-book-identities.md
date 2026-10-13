# Ordinary book identities and news

**Status: IMPLEMENTED IN SCRIPT, NOT LIVE-VERIFIED — 2026-10-12.** This is a
follow-up to [v32](../spec/v32-exceptional-sefarim.md), whose exceptional-work
system remains a proposal. ROADMAP is authoritative for shipped status.

`kehillah_book.0007` used the author's `kehillah_book_genre` after the sending
effect had cleared it. Since the recipient event fires 30 days later, its
genre checks fell through to poetry even for a Talmudic or Hashkafa work.
This explains the earlier report of Gaon Sherira's work as a collection of
verse. The event now reads a `kehillah_book_work` flag chosen at completion.
It remains on the author until another writing project begins. The ten-year
decision cooldown keeps those projects well apart from the 30-day news delay.

`kehillah_book_choose_work_effect` selects one of 14 ordinary identities:
three each for Hashkafa, Parshanut, Talmudics, and poetry, plus two Talmudic
studies based on a remembered Bet Din case. The Bet Din cases are selected
only when the author used the special memory inspiration and actually holds
the matching case memory. Other memories use the general Talmudic pool.
The titles include biblical images, named Torah portions, specific sugyot,
and an author-name form in each genre. Each identity has a synopsis of its
contents. The author-facing completion, personal artifact, and recipient news
all use the selected identity. Artifact rarity and modifier selection still
follow the existing quality calculation.

The news is discussion about a named work. It grants the recipient the same
Piety and Learning XP as before and does not add a library flag. The personal
artifact still exists with EP1; the library remains a separate collection.
Only the proposed exceptional works would create new world-work entries.

Source verification: run `ck3-tiger`, check that every work flag has a custom
title, synopsis, artifact name and artifact description, then use console-only
`kehillah_book_news_debug.1` / `.2` to preview Parshanut and a remembered
Bet Din subject in another registered community. A live pass should verify
the event's rendered title/synopsis, artifact title, save/reload stability,
and the absence of a new library row. No live pass is recorded yet.

## Addendum, 2026-10-12: the news is a quiet notice

Daniel decided this after the 62-year soak test (`docs/testing/2026-10-12-balance-soak-test.md`),
which saw this popup 39 times with a single option.

- **No popup.** `kehillah_book_send_copies_effect` no longer fires `kehillah_book.0007` to every
  registered community in the world.
- **Who it reaches:** communities within the author's **diplomatic range**.
- **Effect:** each of those communities' ordained rabbis (the leader if ordained, plus ordained
  courtiers) gains `kehillah_book_news_rabbi_xp` (2) in the work's subject, read from the
  `kehillah_book_work` flag prefix: talm_, parsh_ or hash_. Poetry gives nothing.
- **Notice:** a player leader there gets a quiet Community News feed notice with the work's title
  and synopsis.
- **Removed:** the old Piety and Learning XP for recipient leaders.
- **Still defined:** `.0007` remains, for the preview debug events.
