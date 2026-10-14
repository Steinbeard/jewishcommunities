**Status:** built 2026-10-13 (slice 1: the faith's pressure and preaching at court); live test
pending. Daniel: "We should add more interactions that build anti-Jewish pressure ... add more of a
likelihood for the faith to shift in an anti-Jewish direction", and "make personality have a bigger
effect too". This replaces V36c's flat prejudice term (reverted). It follows V31 §9 (incidents) and
§7 (the faction, a later slice).

# V38: Anti-Jewish pressure from the world

## Why

Outlooks and teachings need to move for reasons the player can see: people who preach, accusations,
risings, a faith's mood hardening over the centuries. A flat number does not provide that.

## 1. The faith's pressure (``kehillah_faith_pressure``, on a faith)

- **What builds it:**
  - preaching against the Jews at a court (+1, see 2);
  - an accusation that ends in violence (+2);
  - a rising that turns on a community (+3).
- **Decay:** yearly, by a fifth (``kehillah_faith_pressure_yearly_effect``, on the faith's main rite's
  yearly pulse).
- **What it does** (``kehillah_rite_teaching_yearly_effect``):
  - **The head of faith's mood:** at pressure 10 or more, the head of faith's outlook shifts -1 a year
    (the clergy's mood reaches him). A Protector-minded head resists, but not forever.
  - **Stricter teachings:** the chance of a stricter teaching gains pressure ÷ 4 percentage points.
    It needs no Convinced head, only one who is not a Protector (outlook below 30). With a Convinced
    head, it adds to the old chance.
- **Debug:** ``kehillah_outlook_debug.11`` logs the pressure of the host's faith.

## 2. Preaching at court (``kehillah_court_preaching_yearly_effect``)

- **Who preaches:** a zealous clergyman of the lord's faith. This is his court chaplain, or a zealous
  theocratic vassal (a bishop).
- **The chance, yearly:** 10% under a protective teaching, 25% under a strict one, 40% under an
  exclusionary one.
- **The effect:** the lord's outlook shifts -3 (-5 under a strict or exclusionary teaching), and the
  faith's pressure +1.
- **Who it applies to:** independent Christian or Muslim rulers who host at least one community, so
  the effort goes where Jews live.
- **The player** hears of it: "A Preacher at Court", a feed message with the preacher's portrait, sent
  to communities under that lord.

## 3. Personality (Daniel: "a bigger effect too")

- **Warming:** compassionate +20, just +15, cynical +15, humble +10, trusting +10, forgiving +5,
  generous +5, ambitious +5, greedy without a Jewish debt +5, physician +5.
- **Cooling:** sadistic -25, paranoid -15, callous -10, arrogant -10, wrathful -10, vengeful -10,
  arbitrary -5, and a theologian under a strict or exclusionary teaching -5.

## Later slices

- **Disputation:** the rabbi defends the Talmud before the lord; a learning check.
- **Compelled sermons:** friars in the synagogue; conversions.
- **The vassal faction:** "Petition against the Jews" (V31 §7), after a spike.

## 4. Trimming the warming loop (from the 24-year soak at ``c635592``)

Even with V36c's -15, hosts warmed from an average of +12 to +22 in seven years and never went
Cold. The cause was our own levers acting automatically:
- **Warming sermons:** a learned chaplain under a protective teaching gave +1 a year. Most chaplains
  have learning 15+. It now also needs a compassionate or just chaplain.
- **AI gifts:** they fired whenever the host was below Well-disposed, so several communities gifted
  the same host (the Emperor). They are now a rescue: only for a host already Cold or worse, and
  the AI weight falls from 30 to 20.

The soak also counted 17 favours, 9 invitations (2 answered), 1 rising, and 4 AI foundings in about
24 years.
