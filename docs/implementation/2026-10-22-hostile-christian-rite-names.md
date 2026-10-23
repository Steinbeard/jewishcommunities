**Status:** implemented 2026-10-22; source and xTiger checked, isolated boot passed, live display pending. This adds to [V39](../spec/v39-pogroms-and-the-popular-crusade.md)'s preacher rite and [V34](../spec/v34-outlook-teachings-and-founding.md)'s popular rising. It does not change [V31](../spec/v31-host-teachings-stances-and-factions.md)'s distinction between a rite's teaching and the violence of a particular mob.

# Names for newly founded exclusionary Christian rites

When a Christian mob preacher or popular rising leader needs an Exclusion rite, the existing path still first looks for a suitable rite in the founder's faith. Only if none exists does it create a dynamic rite. That rite now receives Exclusion during creation and then draws one historical label, according to the founder's location:

| Name | Eligible geography | Selection weight |
|---|---|---:|
| Agobardism | Francia, Germania, Britannia | 4 |
| Amulonianism | Francia, Germania, Britannia | 4 |
| Sisebutianism | Iberia, Italy | 6 |
| Chrysostomianism | Anywhere; preferred in southeastern Europe, Anatolia and the Levant | 3, or 9 in the eastern Mediterranean |

Each label is used once per game. When the local choices are exhausted, CK3's generated name remains. The name is a fictional later rite's invocation of a historical figure, not a claim that the figure founded such a rite. The descriptions make that explicit. The change applies to any Christian faith because it renames the dynamic rite after creation rather than binding a scripted rite type to one faith. Muslim rite creation is unchanged.

Sisebut is a defensible southern label: he ordered forced baptisms in the Visigothic kingdom in the seventh century. An English candidate was considered but not added. Thomas of Monmouth propagated the Norwich ritual murder accusation after 1144; V31 §3 classifies that accusation as an incident and mob pressure, not a rite doctrine. He belongs in an event, not this teaching's name pool.

The console-only `kehillah_hostile_rite_name_debug.1` event creates a preacher at a Kehillah town and exercises the same reuse-or-found path. It is intended for a fresh isolated save and a display check of the rite's name and description. The [isolated live attempt](../testing/2026-10-22-hostile-christian-rite-name-check.md) reached CK3's main menu, but could not enter a campaign through the documented input fallback, so rite behavior and display remain pending.
