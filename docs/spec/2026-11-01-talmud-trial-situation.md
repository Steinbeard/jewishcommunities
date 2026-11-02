**Status:** built 2026-11-01, not live-tested. Daniel: "let's build out the non-violent crisis situations like Talmud trials too". This is the build design for §3.2 of [Crisis situations as the mechanic](2026-11-01-crisis-situations-as-the-mechanic.md). It follows that spec's race addendum and supersedes §3.2 where they differ: the phase list, the hearing (a three-way race, not a deadline draw), and "Copying anew", which is deferred. The attack's patterns are reused: the window ([three standing actions](2026-11-01-three-standing-actions.md)), the announcements and the monthly toasts.

# The Talmud trial as a situation

## What it replaces

The incident director's Talmud pick (`kehillah_incident.0001`, V41 step 4b) decided everything in one event: a duel, a bribe, hiding the books, or the Shtadlan, and the verdict on the spot. Now the same pick starts a situation that lasts months. Its gates (a Christian host, from `kehillah_incident_christian_late_year`, a community with the Talmud, the 30-year cooldown) are unchanged. `kehillah_incident.0001` is no longer fired, and is kept for saves that scheduled it.

Assumption, recorded because §9 decision 4 was never answered: §3.2 suggested gating a full trial at 1236 and keeping a lighter form earlier. There is now one form only, at the director's existing gate.

## The situation: `kehillah_talmud_trial`

Its display name is "The Talmud on Trial in X". It uses the crisis window (`kehillah_crisis_situation_window`) and the attack's announcement and toast message types.

**Participants**, refreshed monthly:
- **the defence:** the community's leader;
- **the accuser:** the baptized former student who denounced the books (Donin);
- **the judges:** the sovereign.

**One crisis at a time.** A trial does not start while the community has an attack running or another trial.

## Phases

| Phase | How it ends | Next |
| --- | --- | --- |
| **Denunciation** | A race to 100. A hidden 180-day backstop takes the leader. | **The books are seized**, or **Quashed** (the lord lets it drop) |
| **The books are seized** | 60 days | **The hearing**, always |
| **The hearing** | A three-way race to 100. A hidden 90-day backstop takes the leader. | **Acquittal**, **Expurgation**, or **Condemnation** |
| **A verdict** | 30 days | Closed: the situation ends |

**Denunciation.**
- **Seizure pressure:** the opening push, then every month the accuser's pressure. It is larger under a hostile lord or a strict teaching, and smaller under a protective one.
- **Quashed** only grows from what the community does: pleading, silver, a written answer to the articles, a letter from the head of the faith.

**The books are seized.** The library's Talmud is in the lord's hands; the books are not lost unless the verdict burns them. Nothing races here: the community prepares. Each preparation is remembered on the title and counts once when the hearing opens:
- **a disputant prepared:** the leader, the Dayyan or a scholar spends the time studying the articles;
- **a letter:** from the head of the faith, or from a protective bishop;
- **books hidden:** some volumes never reached the lord's men. If the hiding is discovered, Condemnation gains points instead.

**The hearing.** Three sessions, about 30 days apart. Each is a Learning duel between the disputant and the accuser:
- **Answer boldly:** a win adds a lot to Acquittal; a loss adds a lot to Condemnation, and the lord takes offence (his outlook falls). This is Nahmanides' price.
- **Answer cautiously:** a win adds a little to Acquittal and a little to Expurgation; a loss adds mostly to Expurgation and a little to Condemnation.

Every month, the judges lean on the scale by their outlook on the Jews:
- protective or well-disposed: toward Acquittal;
- indifferent or cold: toward Expurgation;
- hostile: toward Condemnation.

## Verdicts

- **Acquittal:** the books come back, and Greatness rises (`kehillah_talmud_acquitted_greatness`).
- **Expurgation:** the books come back with passages struck out. Greatness takes a moderate loss, and the charter's text is censored (`kehillah_charter_censor_text_effect`).
- **Condemnation:** the books are burned (`kehillah_talmud_burned_effect`). If some were hidden, the burning is only partly a loss: the community keeps its library, with the same Greatness loss as an expurgation.
- **Quashed:** the books come back. The fear lingers: a minor Stability penalty.

## Actions

Three situation decisions, in the attack's pattern; each opens a scene whose options are the sub-actions:
- **Prepare the Defence:**
  - choose the disputant and study the articles (seizure);
  - in Denunciation, answer the articles in writing (a Learning duel: Quashed, or more Seizure).
- **Seek Protection:**
  - plead with the lord (a diplomacy roll by the Shtadlan, or the leader);
  - silver for the lord;
  - a letter to the head of the faith or a protective bishop.
- **Save the Books:**
  - hide the books (an intrigue duel against the accuser, who knows which houses keep them);
  - copy the rarest volumes (gold for scribes: whatever is burned, a copy remains).

Each sub-action counts once per trial. Its points are shown through the native catalyst tooltip, never in prose.

## Not built

- Copying anew: the recovery decisions after a burning. The existing sefarim acquisition covers it meanwhile.
- The disputant's emigration after a condemnation (Yehiel to Acre).
- A judge-specific hearing event: the judges act through the monthly lean only.

## Console

- `event kehillah_trial_debug.10`: start a trial now, ignoring chance and cooldown.
- `kehillah_trial_debug.11`: log the trial's state.
