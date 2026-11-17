# Bookmark portraits captured from the game

**Status: Built 2026-11-16; live-verified (867, 1066 and 1178 boots), xTiger clean.**
Supersedes the portrait notes in [v51-bookmark-rosters.md](../spec/v51-bookmark-rosters.md)
("Portraits are copies of vanilla bookmark portraits", and "Faces, dress and expressions" in 0b).
That doc already named this as the better fix.

## Problem

The start-screen cards did not show the characters as the game draws them.

- 13 of the 16 mod characters on the three Kehillah start screens had no `dna`, so the game
  gave them a new random face every game. Their cards held a face copied from an unrelated
  vanilla portrait.
- Isaac, Rashi and Joseph had DNA, but their cards were hand-dressed (scholar's or vizier's
  dress, chosen beards). The game dresses them by its own portrait rules, so the clothes and
  hair differed.
- Maimonides (`maimonides_1`) and Khagan Manasseh (74025) are vanilla characters without DNA.

## What changed

- **`common/dna_data/kehillah_bookmark_dna.txt`** (new): 14 DNA entries,
  `kehillah_dna_bookmark_<card>`. Each is the face from the card's old portrait, without
  clothing and props. The faces stay the same; they are now fixed in the game too.
- **History:** the 12 DNA-less mod characters get `dna =`. The Rif (9001101) uses the roster's
  existing `kehillah_dna_isaac_alfasi`, so he has the same face as 9002023 (see below).
- **Vanilla characters:** two template characters, 9001190 and 9001191 (born 700, died 760,
  in `kehillah_v51_bookmark_characters.txt`), carry the Maimonides and Khagan DNA.
  `kehillah_on_game_start` copies it with `copy_inheritable_appearance_from`. This avoids
  overriding vanilla history files. The dumps confirm it works: their in-game genes equal the
  template DNA.
- **Cards:** all 18 entries in `kehillah_bookmark_portraits.txt` are now the game's own
  `dump_bookmark_portraits` output, from a game started at each bookmark date. They show the
  in-game face, age, hair, beard and clothes.
- **`scripts/kehillah_import_bookmark_dumps.py`** (new): copies `bookmark_kehillah_*.txt` dumps
  into the portrait file by key. The steps are in the portrait file's header.

## What the game shows (and now the cards)

The game's dress, not the earlier hand-chosen dress. For example, Isaac and Rashi wear Western
commoner clothes. Bavli and Sephardi characters wear Byzantine commoner clothes. Eldad has no
beard, and the Khagan wears steppe royal headgear. If a character should look different in
game, change the DNA or the portrait modifiers, then dump the card again. Do not hand-edit the
card.

## Repeatability

A second 867 game produced identical faces, hair, beards and clothes. Only body shape (weight)
and the expression and wrinkle genes differed: the game sets those from per-game state, and the
bookmark's own `animation` sets the pose on the card anyway.

## Found, not fixed

The Rif exists twice in a 1066 game: the bookmark's 9001101 (Fez) and 9002023 in
`kehillah_historical_families_1066.txt` (born 1013, at court 155015). They now share a face,
which makes the duplicate easy to spot. Choosing which one stays needs a decision.
