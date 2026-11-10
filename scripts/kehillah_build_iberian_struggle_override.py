"""Build the mod's override of vanilla iberian_struggle_script.txt.
argv[1]: vanilla file, argv[2]: output file. Re-run after a CK3 patch."""
import sys, re

RUIN = [  # toward a worse phase
    ('catalyst_kehillah_crisis', 'medium_struggle_catalyst_gain'),
    ('catalyst_kehillah_lost', 'major_struggle_catalyst_gain'),
    ('catalyst_kehillah_charter_worsened', 'minor_struggle_catalyst_gain'),
]
FLOURISH = [  # toward a better phase
    ('catalyst_kehillah_founded', 'medium_struggle_catalyst_gain'),
    ('catalyst_kehillah_flourishing', 'minor_struggle_catalyst_gain'),
    ('catalyst_kehillah_charter_improved', 'medium_struggle_catalyst_gain'),
    ('catalyst_kehillah_nagid_named', 'medium_struggle_catalyst_gain'),
    ('catalyst_kehillah_court_service', 'minor_struggle_catalyst_gain'),
]
HEADER = """# =====================================================================
# JEWISH COMMUNITIES -- FULL OVERRIDE of vanilla
# common/struggle/struggles/iberian_struggle_script.txt (CK3 1.20.1),
# 2026-11-09. Copied verbatim; the only change is the mod's own catalysts
# appended to the five catalyst lists (search "Jewish Communities"):
#   toward a worse phase  (Opportunity->Hostility, Compromise->Opportunity,
#                          Conciliation->Compromise): %s
#   toward a better phase (Opportunity->Conciliation, Hostility->Compromise):
#                          %s
# Why an override: a struggle's catalyst lists cannot be extended from
# another file, and borrowing vanilla catalysts would make the struggle's
# own notice call a community crisis "Converted". See docs/spec/v53-
# sepharad-and-the-iberian-struggle.md section 6b. REFRESH THIS FILE when
# a CK3 patch changes the vanilla one: re-run
# scripts/kehillah_build_iberian_struggle_override.py, or diff and re-append by hand. Loads harmlessly without
# The Fate of Iberia: vanilla only starts the struggle with the DLC.
# =====================================================================
""" % (', '.join(c for c, _ in RUIN), ', '.join(c for c, _ in FLOURISH))

src, dst = sys.argv[1], sys.argv[2]
raw = open(src, 'rb').read()
crlf = b'\r\n' in raw
lines = raw.decode('utf-8-sig').replace('\r\n', '\n').split('\n')
out, nr, nf = [], 0, 0
for ln in lines:
    out.append(ln)
    m = re.match(r'^(\t+)catalyst_broke_truce_against_important_character = massive_struggle_catalyst_gain', ln)
    if m:
        nr += 1
        out.append(m.group(1) + "# Jewish Communities (2026-11-09): a community's ruin hardens the struggle.")
        out += [m.group(1) + '%s = %s' % c for c in RUIN]
    m = re.match(r'^(\t+)catalyst_release_important = massive_struggle_catalyst_gain', ln)
    if m:
        nf += 1
        out.append(m.group(1) + "# Jewish Communities (2026-11-09): a community's flourishing eases the struggle.")
        out += [m.group(1) + '%s = %s' % c for c in FLOURISH]
assert (nr, nf) == (3, 2), (nr, nf)
text = HEADER + '\n'.join(out)
if crlf:
    text = text.replace('\n', '\r\n')
open(dst, 'w', encoding='utf-8-sig', newline='').write(text)
print('built', dst, nr, nf)
