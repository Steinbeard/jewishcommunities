**Status: Built 2026-11-16; source and xTiger checked; isolated boot passed database initialization, live claim transfer pending.**

# David ben Hezekiah and the Baghdad claim

This user-directed slice revises the 1066 Seljuk Mesopotamian Jewish political
map. It supersedes the 1066 Baghdad/Pumbedita relationship in
`docs/spec/v29-yeshiva.md` and the David duplicate in
`docs/implementation/2026-11-08-sefer-haqabbalah-roster.md`. The older
records remain as design history. It leaves the Muslim caliph and Seljuk
rulers in vanilla's title histories.

## Historical basis and choices

- [Encyclopaedia Judaica on Hezekiah](https://www.encyclopedia.com/religion/encyclopedias-almanacs-transcripts-and-maps/hezekiah-ben-david)
  describes him as Exilarch and Gaon, dying around 1058; sources disagree
  with the older account of his death following his fall around 1040.
  The model now ends his **Pumbedita Gaonate** in 1040 but his separate
  **Exilarchate** at his modeled 1058 death. Both dates are approximate.
- [Encyclopaedia Judaica on David](https://www.encyclopedia.com/religion/encyclopedias-almanacs-transcripts-and-maps/david-ben-hezekiah)
  describes Hezekiah's son as an exilarch who later returned to Baghdad,
  whereas the [older exile account](https://www.jewishencyclopedia.com/articles/12364-princes-of-the-captivity)
  sends two sons to Joseph ha-Nagid in Spain. The bookmark chooses the exile
  story for David, records a reconstructed 1058–1060 office term, and gives
  him a playable route to regain recognition. His brother Yitzhak remains
  at Joseph's court; his name and dates are conjectural.
- Joseph's historical shelter of the sons and poem to their father support
  a close relationship, but David's individual friendship with Joseph is
  an inferred scenario choice.
- [Research on Seljuk Baghdad](https://jscholarship.library.jhu.edu/server/api/core/bitstreams/5ef45d46-ddf3-449e-b6af-02967aa8d8c7/content)
  reports the Jewish banker Ibn Fadlan's role in a disputed exilarch
  selection in 1068. He replaces the invented Baghdad steward. His
  given name and dates are unknown, and placing him in 1066 is an inference.
  Baghdad's Parnas Ezra and the Sura and Pumbedita scholars remain explicitly
  invented representatives; nobody is presented as an attested 1066 holder.
- [The account of Isaac b. Moses b. Sakri](https://www.encyclopedia.com/religion/encyclopedias-almanacs-transcripts-and-maps/gaon)
  places his arrival in Baghdad around 1070. A [modern study](https://jscholarship.library.jhu.edu/bitstream/1774.2/60908/1/GRAYSON-DISSERTATION-2017.pdf)
  observes that no surviving Baghdad manuscript attests his gaonate. His
  1066 service as David's camp Dayyan is deliberate scenario fiction, not a
  historical claim. His father Moses is named by the patronymic; the father's
  life dates are estimated.

## In-game structure

The bookmark David `9001102` is now the only live David ben Hezekiah.
The duplicate courtier `9002054` is removed; David gains his existing
Hezekiah/Naomi parent links and Ben David trait. Joseph `9000216` is his
friend. Isaac `9003160` is at his camp and receives the new Dayyan court
position at start. His father is `9003161`.

Baghdad, Sura, and Pumbedita are three playable community titles. The
Pumbedita community is at `c_anbar` as a map proxy for the old Fallujah
site. The historical Pumbedita academy title remains separate, with the
Geonim's earlier holder history. Reviving a community at the old site in
1066 is a flavor liberty: the working academy had moved to Baghdad.

`d_kehillah_exilarchate` is a separate titular duchy, modeled on vanilla's
landless `d_samaritan` office and `d_sunni` Caliphate. It is **not** the
religious head title and gives no Gaonate powers. The title histories link
the dated David ben Zakkai → Judah → David → Hezekiah → David family chain
where parentage is actually recorded. The office title records David ben
Zakkai and Hezekiah, and David's brief reconstructed term. The older
exilarchs remain in `docs/data/historical-jewish-leadership`: their
continuous parentage and lifespans cannot be established, so moving them
into live CK3 history would falsely manufacture dates and kinship.

The **Press the Claim to the Exilarchate** decision is David's separate
route, independent of Weigh Their Seat and appointment succession. He must
travel to Baghdad, have at least -10 opinion from its leader and -25 from
the local top liege, and spend 100 gold and 150 prestige. Its effect gives
him the existing Baghdad community, destroys his old camp title, grants the
separate Exilarchate, and seats Isaac as the community Dayyan if he still
serves David. The separate title is lifetime recognition and lapses at
succession; a new claimant requires recognition rather than automatically
becoming Exilarch solely by taking Baghdad. This transfer is the risky
engine step that needs a Luna live probe.

## Verification

- xTiger: 0 fatal, 17 errors, 124 warnings, 38 untidy and 44 tips,
  **identical to a fresh `origin/master` baseline**. No new diagnostic.
- Source audit: unique live IDs for David and Isaac; family links resolve;
  title histories, community registry, and start effects reference all three
  separate Mesopotamian seats.
- Luna's [isolated boot log](../testing/2026-11-16-exilarch-claim-live-log.md)
  confirms content and bookmark database initialization. Council position,
  title transfer, quarter continuity, player continuation, and save/reload
  remain unrun because the CK3 probe tools were unavailable.
