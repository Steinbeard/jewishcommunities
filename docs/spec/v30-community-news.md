**Status:** agreed with Daniel 2026-10-12 and built the same day; live test pending. Follows
[v29 §12](v29-yeshiva.md) (the yeshiva's news), which set the pattern of quiet feed messages.

# V30: Community news

## Why

Daniel asked for side notifications from other systems, so that the wider Jewish world feels
alive. The bar is "notify when something changes your situation, opens a choice, or is rare enough
to be news". Routine background activity, such as every skill check in a Bet Din case, does not
qualify.

## What notifies, and whom

All of these are feed messages: never a banner, never an event. They use their own message
filter, `kehillah_community_news`, which appears as "Community News" in Message Settings and is
separate from "Yeshiva News". "Nearby" means **within the player's diplomatic range**
(vanilla `in_diplomatic_range`). Daniel chose this on 2026-10-12; the first build used the minhag
region. The community
the news is about is never told of itself.

| News | When | Who hears | Hook |
|---|---|---|---|
| Your lord has died | Death of the holder of your community's county, or of that county's top liege. Names the heir. | the player Kehillah leader | `on_death` → `kehillah_on_death_host_news` |
| A charter revised | Names each changed term, old and new, by the charters' own obligation names (custom loc `KehillahCharterChange*`). Fires when an EXISTING charter's terms change: building rights, security, jurisdiction, texts or market access, for example through a settlement-policy change. A first charter, or a new charter after the community passes to a new lord, is NOT reported (Daniel 2026-10-12: "only about charter modifications"). | those in range | `kehillah_refresh_charter_state_cache_effect`, comparing last quarter's terms (`kehillah_charter_terms_signature_value`) |
| New leadership | Someone gains a Kehillah title | those in range | end of `kehillah_on_title_gain`, message only |
| A community in crisis | A pillar falls into the Crisis band | those in range | `kehillah_update_pillar_band_effect` |
| A new yeshiva | Found a Yeshiva | those in range | `kehillah_found_yeshiva_effect` |
| A yeshiva's name grows | Renown reaches Renowned or Illustrious | those in range | `kehillah_yeshiva_check_tier_effect` |
| A Bet Din concludes | The session closes (`kehillah_bet_din.0099`). Says how it went: landmark, strong, adequate or failed. | the region, except the co-judges, who were there | `.0099` immediate |

## Daniel's direction on the Bet Din

Daniel chose "a session concluded" over notable rulings. It is less frequent and more relevant:
someone hosted a Bet Din, and here is how it went.

Daniel also wants the notice to say how the session changed minhag practice, if it did. No such
mechanic exists yet. Takkanot are only proposed, in v25 P7. When sessions can pass them, that line
belongs in this notice; the hook in `.0099` is commented to say so.

## Shared helper

`kehillah_notify_region_players_effect = { TYPE TITLE DESC }`, in
`common/scripted_effects/kehillah_community_news_effects.txt`. Its scope is the leader the news is
about. A character flagged `kehillah_news_skip` is passed over.

## Risk note

`kehillah_on_title_gain` carries the succession code, which is this mod's crash history
(implementation doc §6 and §8). The news call is appended last and sends a message only. Nothing
above it was changed.

## Budget

The aim is a few entries a year. If live play shows more, fold the lower rows into a yearly
"letters from the communities" digest.
