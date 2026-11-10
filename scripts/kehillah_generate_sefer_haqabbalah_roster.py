"""Generate the Sefer ha-Qabbalah roster tranche (2026-11-08).

Outputs, all deterministic from the data tables below:
  history/characters/kehillah_sefer_haqabbalah_figures.txt   new historical characters
  history/characters/kehillah_sefer_haqabbalah_wives.txt     invented wives for every father with children
  docs/data/historical-character-tracker.csv                 rows appended (idempotent: HC2xx block replaced)
  scratchpad/title_blocks.txt                                title-history blocks to paste

It also patches existing child records to add `mother = <new wife>` (idempotent).
Rerun after editing the tables; it rewrites its own outputs only.

Dates: office dates for Geonim come from the staged roster
(docs/data/historical-jewish-leadership/*.txt, itself from Daniel's 2026-10-18 seed).
Births are ESTIMATED (office start - 48 unless overridden) and deaths are
ESTIMATED (mid-year of the final office year); every record says so.
"""
import csv
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HIST = ROOT / 'history' / 'characters'
TRACKER = ROOT / 'docs' / 'data' / 'historical-character-tracker.csv'
OUT_CHARS = HIST / 'kehillah_sefer_haqabbalah_figures.txt'
OUT_WIVES = HIST / 'kehillah_sefer_haqabbalah_wives.txt'
TITLE_OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / 'title_blocks.txt'

SURA_COURT = 9000736      # Amram Gaon, 867 holder of d_kehillah_sura
BAGHDAD_COURT = 9001011   # 867 holder of d_kehillah_baghdad

SRC_SEFER = 'https://en.wikipedia.org/wiki/Sefer_ha-Qabbalah'
SRC_SURA = 'https://en.wikipedia.org/wiki/Sura_Academy'
SRC_PUMB = 'https://en.wikipedia.org/wiki/Pumbedita_Academy'
SRC_EXIL = 'https://en.wikipedia.org/wiki/Exilarch'

# ---------------------------------------------------------------------------
# Office tables. (id, name, start, end, extras). start/end are 'Y' or 'Y.M.D'.
# extras: birth, death, father, kohen, levite, note
# ---------------------------------------------------------------------------
SURA = [
    (9000715, 'Hanina', '689', '694', {}),
    (9000716, 'Hillai', '694', '712', {}),
    (9000717, 'Jacob', '712', '730', {}),
    (9000718, 'Samuel', '730', '748', {}),
    (9000719, 'Mari', '748', '756', {'kohen': 1}),
    (9000720, 'Aha', '756', '757', {}),
    (9000721, 'Yehudai', '757', '761', {}),
    (9000722, 'Ahunai', '761', '769', {}),
    (9000723, 'Haninai', '769', '774', {}),
    (9000724, 'Mari', '774', '778', {'levite': 1}),
    (9000725, 'Bebai', '778', '789', {'levite': 1}),
    (9000726, 'Hilai', '789', '798', {}),
    (9000727, 'Jacob', '798', '810', {'kohen': 1}),
    (9000728, 'Zadok', '810', '812', {}),
    (9000729, 'Hilai', '812', '816', {}),
    (9000731, 'Kimoi', '816', '820', {}),
    (9000732, 'Mesharsheya', '820', '830', {}),
    (9000733, 'Kohen Tzedek', '832', '843', {}),
    (9000734, 'Sar Shalom', '843', '853', {}),
    (9000735, 'Natronai', '853', '861', {}),
    (9000737, 'Nahshon', '872', '879', {}),
    (9000738, 'Zemah', '879', '886', {}),
    (9000740, 'Hai', '886', '896', {}),
    (9000741, 'Hilai', '896', '904', {}),
    (9000742, 'Shalom', '904', '911', {}),
    (9000743, 'Jacob', '911', '924', {}),
    (9000744, 'Yom Tov', '924', '928', {}),
    (9000746, 'Zemah', '990', '998', {'note': 'Zemah Tzedek ben Paltoi; the staged roster dates him c. 990-998'}),
    (9000747, 'Samuel', '998', '1013', {'birth': 950, 'death': '1013.7.1', 'note': 'Samuel ben Hophni; 1013 is the conventional death year'}),
    (9000748, 'Dosa', '1013', '1018', {'birth': 938, 'father': 9000224, 'note': 'Dosa ben Saadia; son of Saadia Gaon'}),
    (9000749, 'Israel', '1018', '1033', {'birth': 980, 'father': 9000747, 'kohen': 1, 'note': 'Israel ha-Kohen, son of Samuel ben Hophni'}),
]

PUMB = [
    (9000819, 'Huna', '689', '700', {}),
    (9000820, 'Hiyya', '700', '710', {}),
    (9000821, 'Rabya', '710', '719', {}),
    (9000822, 'Natronai', '719', '730', {}),
    (9000823, 'Judah', '730', '739', {}),
    (9000824, 'Joseph', '739', '748', {}),
    (9000825, 'Samuel', '748', '755', {}),
    (9000826, 'Natroi', '755', '761', {}),
    (9000827, 'Abraham', '761', '761.7.1', {'birth': 705, 'note': 'Abraham Kahana; the staged roster gives only c. 761, so the year is split with Dodai'}),
    (9000828, 'Dodai', '761.7.1', '767', {'birth': 700}),
    (9000829, 'Hananya', '767', '771', {}),
    (9000830, 'Malka', '771', '773', {}),
    (9000831, 'Rabba', '773', '782', {'father': 9000828}),
    (9000832, 'Shinwai', '782', '782.7.1', {'note': 'staged roster gives only 782; the year is split with Haninai'}),
    (9000833, 'Haninai', '782.7.1', '786', {'father': 9000827}),
    (9000834, 'Huna', '786', '788', {'levite': 1}),
    (9000835, 'Manasseh', '788', '796', {}),
    (9000836, 'Isaiah', '796', '798', {'levite': 1}),
    (9000837, 'Joseph', '798', '804', {}),
    (9000838, 'Kahana', '804', '810', {}),
    (9000839, 'Abumai', '810', '814', {}),
    (9000840, 'Joseph', '814', '816', {}),
    (9000841, 'Abraham', '816', '828', {}),
    (9000842, 'Joseph', '828', '833', {}),
    (9000843, 'Isaac', '833', '839', {}),
    (9000844, 'Joseph', '839', '841', {}),
    (9000845, 'Paltoi', '841', '858', {}),
    (9000846, 'Aha', '858', '858.7.1', {'note': 'staged roster gives only 858; the year is split with Menahem'}),
    (9000847, 'Menahem', '858.7.1', '860', {}),
    (9000848, 'Mattithiah', '860', '869', {'kohen': 1, 'note': 'his title record is cut at 866.12.31 so the 867 bookmark starts with the office vacant'}),
    (9000849, 'Abba', '869', '872', {}),
    (9000850, 'Zemah', '872', '889', {'father': 9000845}),
    (9000851, 'Hai', '889', '896', {'note': 'Hai ben David; the roster gives c. 889/890 and a source inconsistency'}),
    (9000852, 'Kimoi', '896', '905', {'birth': 835}),
    (9000853, 'Mebasser', '905', '917', {'birth': 862, 'father': 9000852}),
    (9000854, 'Kohen Tzedek', '917', '922', {}),
    (9000855, 'Zemah', '935', '937', {}),
    (9000856, 'Hananiah', '937', '943', {'birth': 875}),
    (9000857, 'Aaron', '943', '960', {}),
    (9000858, 'Nehemiah', '960', '968', {'father': 9000854}),
    (9000859, 'Sherira', '968', '1004', {'birth': 906, 'death': '1006.7.1', 'father': 9000856, 'note': 'Sherira, author of the Iggeret; 906-1006 are the conventional dates'}),
    (9000860, 'Hai', '1004', '1038', {'birth': 939, 'death': '1038.7.1', 'father': 9000859, 'note': 'Hai ben Sherira, last great Gaon; 939-1038 are the conventional dates'}),
]

# Exilarchs of the Geonic age (Baghdad). Dates beyond the Hezekiah line are
# reconstructions; the staged roster supplies the order and the descent.
EXIL = [
    (9000597, 'David', '921', '940', {'birth': 890, 'dynasty': 9000064, 'note': 'David ben Zakkai, who clashed with Saadia Gaon'}),
    (9000599, 'Judah', None, None, {'birth': 920, 'death': '975.7.1', 'father': 9000597, 'dynasty': 9000064}),
    (9000603, 'David', None, None, {'birth': 958, 'death': '1017.7.1', 'father': 9000599, 'dynasty': 9000064,
                                    'note': 'the generation the staged roster omits between Judah and Hezekiah; Hezekiah is named "ben David ben Judah"'}),
]
HEZEKIAH = 9002053  # existing live character; gets father = 9000603 and holds Baghdad/Pumbedita 1038-1040

# Standalone figures: id, name, culture, birth, death, extras, role text
OTHERS = [
    (9003001, 'Gershom', 'ashkenazi', 960, 1028, {'note': 'Rabbenu Gershom Me\'or ha-Golah; Mainz academy c. 1000 (estimated start)'}, 'Mainz', 'Rabbenu Gershom, "Light of the Exile"'),
    (9003002, 'Simeon', 'ashkenazi', 988, 1010, {'father': 9003001, 'note': 'son who left the faith in the traditional account; Gershom mourned him'}, 'Mainz', 'Gershom\'s son Simeon'),
    (9003003, 'Eliezer', 'ashkenazi', 992, 1055, {'father': 9003001}, 'Mainz', 'Gershom\'s son Eliezer'),
    (9003004, 'Jacob', 'ashkenazi', 990, 1064, {'note': 'Jacob ben Yakar, Rashi\'s teacher; his successor at Worms is Isaac ha-Levi (9000002)'}, 'Worms', 'Jacob ben Yakar, teacher of Rashi'),
    (9003005, 'Menahem', 'sephardi', 910, 970, {'note': 'Menahem ben Saruq, secretary to Hasdai ibn Shaprut and author of the Mahberet'}, 'Cordoba', 'Menahem ben Saruq'),
    (9003006, 'Dunash', 'sephardi', 920, 990, {'note': 'Dunash ibn Labrat, poet and grammarian who answered Menahem'}, 'Cordoba', 'Dunash ibn Labrat'),
    (9003007, 'Judah', 'sephardi', 945, 1000, {'note': 'Judah ben David Hayyuj, founder of Hebrew grammar by the triliteral root'}, 'Cordoba', 'Judah Hayyuj'),
    (9003008, 'Jonah', 'sephardi', 990, 1050, {'note': 'Jonah ibn Janah, grammarian and physician'}, 'Zaragoza', 'Jonah ibn Janah'),
    (9003009, 'Joseph', 'sephardi', 930, 1010, {'note': 'Joseph ibn Abitur, who left Merida for the east'}, 'Cordoba', 'Joseph ibn Abitur'),
]

# Existing characters the Sefer chain needs, for the tracker and the title blocks only.
EXISTING_NAMES = {9000224: 'Saadia', 9000736: 'Amram', 9002053: 'Hezekiah ben David', 9002077: 'Hasdai ibn Shaprut',
                  9002021: 'Enoch ben Moses', 9000230: 'Samuel ha-Nagid', 9000216: 'Joseph ibn Naghrilla'}

TRAITS_M = [
    ('calm', 'honest', 'diligent'), ('patient', 'just', 'stubborn'), ('humble', 'diligent', 'temperate'),
    ('zealous', 'just', 'honest'), ('content', 'generous', 'patient'), ('shy', 'honest', 'diligent'),
    ('ambitious', 'diligent', 'just'), ('calm', 'compassionate', 'humble'), ('temperate', 'patient', 'content'),
    ('stubborn', 'diligent', 'honest'),
]
TRAITS_F = [
    ('compassionate', 'patient', 'content'), ('generous', 'gregarious', 'trusting'), ('calm', 'patient', 'forgiving'),
    ('honest', 'diligent', 'humble'), ('content', 'generous', 'compassionate'), ('patient', 'shy', 'honest'),
]
FEMALE_NAMES = ['Hannah', 'Rachel', 'Miriam', 'Sarah', 'Rivka', 'Leah', 'Esther', 'Tamar', 'Yocheved', 'Devorah',
                'Naomi', 'Dinah', 'Shifra', 'Abigail', 'Zipporah']


def year(text):
    return int(str(text).split('.')[0])


def date(text, default_md='1.1'):
    text = str(text)
    return text if text.count('.') == 2 else f'{text}.{default_md}'


class Person:
    def __init__(self, ident, name, culture):
        self.id, self.name, self.culture = ident, name, culture
        self.female = False
        self.birth = None      # int year
        self.death = None      # 'Y.M.D'
        self.father = None
        self.mother = None
        self.spouse = None     # husband id for wives
        self.marriage = None
        self.dynasty = None
        self.kohen = self.levite = False
        self.learning = 3
        self.edu = 'learning'
        self.note = ''
        self.court = None
        self.office = []
        self.est = True

    def death_year(self):
        return year(self.death)


people = {}


def add(person):
    people[person.id] = person
    return person


def geonic(table, court, kind):
    for ident, name, start, end, ex in table:
        p = Person(ident, name, 'bavlim')
        p.birth = ex.get('birth', year(start) - 48)
        p.death = ex.get('death') or f'{max(year(end), p.birth + 55)}.7.1'
        p.father = ex.get('father')
        p.kohen = bool(ex.get('kohen'))
        p.levite = bool(ex.get('levite'))
        p.dynasty = 9000062 if p.kohen else None
        p.learning = 4
        p.note = ex.get('note', '')
        p.court = court
        p.office = [(kind, date(start), date(end))]
        p.kind = kind
        add(p)


geonic(SURA, SURA_COURT, 'sura')
geonic(PUMB, BAGHDAD_COURT, 'pumbedita')

for ident, name, start, end, ex in EXIL:
    p = Person(ident, name, 'bavlim')
    p.birth = ex['birth']
    p.death = ex.get('death') or f'{p.birth + 50}.7.1'
    if start:
        p.death = ex.get('death') or f'{year(end)}.7.1'
    p.father = ex.get('father')
    p.dynasty = ex.get('dynasty')
    p.edu = 'stewardship'
    p.learning = 3
    p.note = ex.get('note', '')
    p.court = BAGHDAD_COURT
    p.kind = 'exilarch'
    p.office = [('baghdad', date(start), date(end))] if start else []
    add(p)

for ident, name, culture, birth, death, ex, place, role in OTHERS:
    p = Person(ident, name, culture)
    p.birth, p.death = birth, f'{death}.7.1'
    p.father = ex.get('father')
    p.note = ex.get('note', '')
    p.learning = 3 if ident != 9003002 else 2
    p.place, p.role = place, role
    p.kind = 'other'
    add(p)
people[9003001].office = [('mainz', '1000.1.1', '1028.1.1')]

# Fixed existing parents/children whose records live elsewhere.
EXTERNAL = {  # id -> (birth, death) of existing characters used as parents
    9000224: (882, 942),
    HEZEKIAH: (1000, 1045),
}


def read_existing():
    ents = {}
    for path in HIST.glob('*.txt'):
        if path in (OUT_CHARS, OUT_WIVES):
            continue
        text = path.read_text(encoding='utf-8-sig')
        for match in re.finditer(r'(?m)^\s*(\d{4,7})\s*=\s*\{', text):
            depth = 0
            for pos in range(match.end() - 1, len(text)):
                depth += (text[pos] == '{') - (text[pos] == '}')
                if depth == 0:
                    ents[int(match.group(1))] = (path, text[match.end():pos + 1])
                    break
    return ents


def field(body, key):
    m = re.search(r'\b' + key + r'\s*=\s*"?(\w+)', body)
    return m.group(1) if m else None


def byear(body):
    m = re.search(r'\bbirth\s*=\s*"?(\d{3,4})\.', body)
    return int(m.group(1)) if m else None


def dyear(body):
    m = re.search(r'\bdeath\s*=\s*"?(\d{3,4})\.', body)
    return int(m.group(1)) if m else None


# Hezekiah's father link (existing record) goes in first so he counts as a child of 9000603.
_hz = HIST / 'kehillah_historical_families_1066.txt'
_text = _hz.read_text(encoding='utf-8-sig')
_m = re.search(r'(?m)^' + str(HEZEKIAH) + r' = \{[^\n]*', _text)
if _m and 'father =' not in _m.group(0):
    _text = _text.replace(_m.group(0), _m.group(0).replace('rite = "rabbinism"', 'rite = "rabbinism" father = 9000603', 1), 1)
    _hz.write_bytes(b'\xef\xbb\xbf' + _text.encode('utf-8'))
    print('Hezekiah father link added')

existing = read_existing()
problems = []

# ---- Wives ---------------------------------------------------------------
wife_ids = iter(range(9003101, 9003400))
wives = {}


def mother_free(body):
    m = field(body, 'mother')
    return not m or 9003101 <= int(m) < 9003400


def children_of(father_id):
    kids = []
    for p in people.values():
        if p.father == father_id:
            kids.append((p.birth, p.id, 'new'))
    for ident, (path, body) in existing.items():
        if field(body, 'father') == str(father_id) and ident not in people:
            if mother_free(body):
                kids.append((byear(body), ident, 'existing'))
    return sorted(kids)


def father_info(fid):
    if fid in people:
        p = people[fid]
        return p.birth, p.death_year(), p.culture
    if fid in EXTERNAL:
        b, d = EXTERNAL[fid]
        return b, d, 'bavlim'
    path, body = existing[fid]
    return byear(body), dyear(body) or 9999, field(body, 'culture')


def father_court_1066(fid):
    """Return (alive_at_1066, employer_id_or_self)."""
    if fid in people:
        return False, None
    path, body = existing[fid]
    d = dyear(body)
    alive = d is None or d > 1066
    if not alive:
        return False, None
    m = re.search(r'1066\.\d+\.\d+\s*=\s*\{[^}]*employer\s*=\s*(\d+)', body)
    return True, int(m.group(1)) if m else fid


# New fathers with children among the new people, plus existing fathers lacking wives.
father_ids = set(p.father for p in people.values() if p.father)
# Gershom's wife is added explicitly through children; Dunash gets a wife and son below.
dunash_son = Person(9003010, 'Isaac', 'sephardi')
dunash_son.birth, dunash_son.death, dunash_son.father = 950, '1015.7.1', 9003006
dunash_son.note = 'son named in Dunash\'s wife\'s poem; his name is invented'
dunash_son.learning, dunash_son.kind = 2, 'other'
dunash_son.place, dunash_son.role = 'Cordoba', 'Dunash\'s son'
add(dunash_son)
father_ids.add(9003006)

# Existing fathers with kids lacking a mother and no spouse recorded.
spouse_of = defaultdict(set)
for ident, (path, body) in existing.items():
    for m in re.finditer(r'add_spouse\s*=\s*(\d+)', body):
        spouse_of[ident].add(int(m.group(1)))
        spouse_of[int(m.group(1))].add(ident)
retro_fathers = []
for ident, (path, body) in existing.items():
    f = field(body, 'father')
    if f and f.isdigit() and mother_free(body):
        fid = int(f)
        if fid in existing and not spouse_of[fid] and fid not in retro_fathers:
            retro_fathers.append(fid)
retro_fathers.sort()

patch_children = {}  # child id -> wife id (existing child records to patch)

for index, fid in enumerate(sorted(father_ids | set(retro_fathers))):
    kids = children_of(fid)
    if not kids:
        continue
    first, last = kids[0][0], kids[-1][0]
    fb, fd, culture = father_info(fid)
    wid = next(wife_ids)
    w = Person(wid, FEMALE_NAMES[(wid * 7 + index) % len(FEMALE_NAMES)], culture if culture in ('bavlim', 'sephardi', 'ashkenazi', 'italki', 'romaniote', 'radhanite') else 'bavlim')
    w.female = True
    w.birth = max(first - 24, (fb or first - 24) - 6)
    if first - w.birth < 18:
        w.birth = first - 22
    w.marriage = first - 3
    # Wife outlives the last child's infancy and dies close to her husband.
    cap = w.birth + 68
    floor = last + 20
    w.death = f'{min(max((fd or floor) - 2, floor), max(cap, floor))}.7.1'
    alive_1066, court_1066 = father_court_1066(fid)
    if alive_1066 and year(w.death) <= 1066:
        w.death = '1067.7.1'
    w.spouse = fid
    w.learning = 0
    w.note = 'invented wife of ' + (people[fid].name if fid in people else field(existing[fid][1], 'name') or str(fid))
    w.alive_1066_court = court_1066 if alive_1066 else None
    wives[wid] = w
    for _, kid, kind in kids:
        if kind == 'new':
            people[kid].mother = wid
        else:
            patch_children[kid] = wid
    w.kids = [k[1] for k in kids]
    w.husband_court = people[fid].court if fid in people else None
    if fid in people:
        people[fid].wife = wid

# ---- validation ----------------------------------------------------------
for p in list(people.values()):
    if p.father:
        fb, fd, _ = father_info(p.father)
        if p.birth - fb < 18:
            problems.append(f'{p.id} {p.name} born {p.birth}, father {p.father} born {fb}')
        if fd < p.birth:
            problems.append(f'{p.id} father {p.father} dead {fd} before birth {p.birth}')
for w in wives.values():
    for kid in w.kids:
        kb = people[kid].birth if kid in people else byear(existing[kid][1])
        if kb - w.birth < 16:
            problems.append(f'wife {w.id} too young for {kid}')
        if year(w.death) < kb:
            problems.append(f'wife {w.id} dies {w.death} before child {kid} born {kb}')
if problems:
    print('PROBLEMS')
    print('\n'.join(problems))
    sys.exit(1)

# ---- trait assignment -----------------------------------------------------
def traits(p, i):
    if p.female:
        t = TRAITS_F[i % len(TRAITS_F)]
        return list(t)
    t = list(TRAITS_M[i % len(TRAITS_M)])
    edu = {'learning': 'education_learning_', 'stewardship': 'education_stewardship_'}[p.edu]
    out = [edu + str(p.learning)]
    if p.edu == 'learning':
        out.append('kehillah_rabbi_trait')
    if p.kohen:
        out.append('kohen')
    if p.levite:
        out.append('levite')
    return out + t


def alive_at(p, y, md):
    return p.birth <= y and (year(p.death) > y or p.death.startswith(f'{y}.') and False)


def alive_867(p):
    return p.birth < 867 and year(p.death) >= 867 and not (year(p.death) == 867 and False)


def line(p, i, comment='', extra_events=()):
    parts = ['disallow_random_traits = yes', f'name = "{p.name}"']
    if p.female:
        parts.append('female = yes')
    if p.dynasty:
        parts.append(f'dynasty = {p.dynasty}')
    parts += ['rite = "rabbinism"', f'culture = "{p.culture}"']
    if p.father:
        parts.append(f'father = {p.father}')
    if p.mother:
        parts.append(f'mother = {p.mother}')
    parts += [f'trait = {t}' for t in traits(p, i)]
    events = [(p.birth, f'{p.birth}.1.1 = {{ birth = "{p.birth}.1.1" }}')]
    if p.marriage:
        events.append((p.marriage, f'{p.marriage}.1.1 = {{ add_spouse = {p.spouse} }}'))
    if p.court and alive_867(p):
        events.append((867, f'867.1.1 = {{ employer = {p.court} }}'))
    events += list(extra_events)
    events.append((year(p.death), f'{p.death} = {{ death = "{p.death}" }}'))
    events.sort(key=lambda e: e[0])
    parts += [e[1] for e in events]
    tail = f' # {comment}' if comment else ''
    return f'{p.id} = {{ {" ".join(parts)} }}{tail}'


def describe(p):
    bits = []
    for kind, s, e in p.office:
        bits.append(f'{kind} {s}-{e}')
    return ('; '.join(bits) + ('. ' if bits else '') + (p.note + '. ' if p.note else '') + 'Birth and death ESTIMATED unless conventional.').strip()


header_figs = '''# 2026-11-08: the Sefer ha-Qabbalah tranche. Geonic heads of Sura and Pumbedita, three
# generations of the exilarchal house, and the grammarians, Rhineland masters and Spanish
# scholars of Ibn Daud's wider tradition. GENERATED by
# scripts/kehillah_generate_sefer_haqabbalah_roster.py - edit the tables there, not here.
# Geonic IDs are the staged IDs of docs/data/historical-jewish-leadership (moved here).
# Office dates are the staged roster's; births are ESTIMATED as office start minus 48
# unless a conventional date is known, and deaths are ESTIMATED as mid-year of the final
# office year. Wives are invented wherever a father has attested children
# (kehillah_sefer_haqabbalah_wives.txt). Anyone alive at the 867 bookmark is employed by
# Amram (Sura) or the Baghdad leader, so nobody starts courtless.
# See docs/implementation/2026-11-08-sefer-haqabbalah-roster.md.
'''
with OUT_CHARS.open('w', encoding='utf-8-sig', newline='\n') as out:
    out.write(header_figs)
    sections = [('# --- Sura: Geonim (title: d_kehillah_sura) ---', [p for p in people.values() if getattr(p, 'kind', '') == 'sura']),
                ('# --- Pumbedita: Geonim (title: d_kehillah_pumbedita_academy) ---', [p for p in people.values() if getattr(p, 'kind', '') == 'pumbedita']),
                ('# --- Exilarchal house (title: d_kehillah_baghdad) ---', [p for p in people.values() if getattr(p, 'kind', '') == 'exilarch']),
                ('# --- Rhineland, Spain and the grammarians ---', [p for p in people.values() if getattr(p, 'kind', '') == 'other'])]
    n = 0
    for title, group in sections:
        out.write('\n' + title + '\n')
        for p in sorted(group, key=lambda q: q.id):
            out.write(line(p, n, describe(p)) + '\n')
            n += 1

with OUT_WIVES.open('w', encoding='utf-8-sig', newline='\n') as out:
    out.write('# 2026-11-08: invented wives, one for every father with attested children in the\n'
              '# Sefer ha-Qabbalah tranche and in the earlier 1066 roster. GENERATED by\n'
              '# scripts/kehillah_generate_sefer_haqabbalah_roster.py. Names, birth years and\n'
              '# marriages are inventions; only the children are the record. Wives alive at the\n'
              '# 1066 bookmark join their husband\'s court; wives alive in 867 join the husband\'s.\n\n')
    for n, w in enumerate(wives.values()):
        extra = []
        court = None
        if w.husband_court and alive_867(w):
            court = w.husband_court
        p = w
        # reuse line() with a temporary court
        w.court = court
        extra_events = []
        if getattr(w, 'alive_1066_court', None):
            extra_events.append((1066, f'1066.9.15 = {{ employer = {w.alive_1066_court} }}'))
        text = line(w, n, w.note, extra_events)
        out.write(text + '\n')

# ---- patch existing child records -----------------------------------------
patched = 0
for kid, wid in patch_children.items():
    path, body = existing[kid]
    text = path.read_text(encoding='utf-8-sig')
    bom = path.read_bytes().startswith(b'\xef\xbb\xbf')
    block = re.search(rf'(?m)^\s*{kid}\s*=\s*\{{', text)
    start = block.start()
    seg_end = block.end()
    depth = 1
    while depth:
        seg_end += 1
        depth += (text[seg_end] == '{') - (text[seg_end] == '}')
    seg = text[start:seg_end + 1]
    if re.search(r'\bmother\s*=', seg):
        continue
    new = re.sub(r'\bfather\s*=\s*(\d+)', rf'mother = {wid} father = \1', seg, count=1)
    text = text[:start] + new + text[seg_end + 1:]
    path.write_bytes((b'\xef\xbb\xbf' if bom else b'') + text.encode('utf-8'))
    patched += 1
print('patched child records:', patched)

# ---- tracker --------------------------------------------------------------
cols = ['key', 'bookmark', 'place', 'character', 'role_or_hook', 'relationships', 'history_id', 'status', 'evidence',
        'gameplay_option', 'accuracy_caveat', 'source_1', 'source_2', 'profile_tag', 'presence_1066']
rows = list(csv.DictReader(TRACKER.open(encoding='utf-8-sig', newline='')))
rows = [r for r in rows if not r['key'].startswith('HC2')]
seq = 200


def row(p, role, place, rel, evidence, profile, caveat, s1, s2):
    global seq
    seq += 1
    return {
        'key': f'HC{seq}', 'bookmark': '867/1066 history-only' if p.birth < 1066 else '1066', 'place': place,
        'character': p.name, 'role_or_hook': role, 'relationships': rel, 'history_id': p.id,
        'status': 'implemented', 'evidence': evidence,
        'gameplay_option': 'History-only holder of a community or academy title [Built: history/characters/kehillah_sefer_haqabbalah_figures.txt]'
        if p.office else 'Dead historical figure whose record anchors a family or a library credit [Built: history/characters/kehillah_sefer_haqabbalah_figures.txt]',
        'accuracy_caveat': caveat, 'source_1': s1, 'source_2': s2, 'profile_tag': profile, 'presence_1066': 'history_only'}


def rel_text(p):
    out = []
    if p.father:
        fn = people[p.father].name if p.father in people else EXISTING_NAMES.get(p.father, str(p.father))
        out.append(f'son/daughter of {fn} ({p.father})')
    if p.mother:
        out.append(f'mother {p.mother} (invented)')
    if getattr(p, 'spouse', None):
        out.append(f'wife of {p.spouse}')
    return '; '.join(out)


for p in sorted(people.values(), key=lambda q: q.id):
    if p.kind in ('sura', 'pumbedita', 'exilarch'):
        kind = {'sura': 'Gaon of Sura', 'pumbedita': 'Gaon of Pumbedita', 'exilarch': 'Exilarch (Reish Galuta)'}[p.kind]
        office = '; '.join(f'{s}-{e}' for _, s, e in p.office)
        role = f'{kind}' + (f' {office}' if office else ' (family link, no term recorded)')
        rows.append(row(p, role, 'Babylonia', rel_text(p),
                        'office term from the staged roster (Sherira and Ibn Daud tradition)',
                        'known_figure', 'Birth and death are estimates; ' + (p.note or 'office order follows the roster'),
                        SRC_SEFER, {'sura': SRC_SURA, 'pumbedita': SRC_PUMB, 'exilarch': SRC_EXIL}[p.kind]))
    else:
        rows.append(row(p, p.role, p.place, rel_text(p), 'named in the standard sources',
                        'known_figure' if p.id != 9003010 else 'invented',
                        'Conventional dates are approximate; ' + (p.note or ''),
                        SRC_SEFER, 'https://www.jewishencyclopedia.com/'))
for w in wives.values():
    husband = people[w.spouse].name if w.spouse in people else (field(existing[w.spouse][1], 'name') or str(w.spouse))
    rows.append(row(w, 'Invented wife of ' + husband, 'wife', f'wife of {w.spouse}; mother of ' + ', '.join(str(k) for k in w.kids),
                    'name and dates invented; the children are attested', 'invented',
                    'Wife added so the attested children have a mother; no source names her',
                    'https://www.jewishencyclopedia.com/', ''))
for r in rows:
    r.setdefault('presence_1066', '')
with TRACKER.open('w', encoding='utf-8-sig', newline='') as f:
    wr = csv.DictWriter(f, fieldnames=cols, lineterminator='\n')
    wr.writeheader()
    for r in rows:
        wr.writerow({c: r.get(c, '') for c in cols})

# ---- title blocks ---------------------------------------------------------
def entry(d, holder):
    return f'\t{d} = {{ liege = 0 holder = {holder} government = kehillah_government }}'


def seq_entries(table, kind, gaps):
    lines = []
    prev_end = None
    for ident, name, start, end, ex in table:
        s, e = date(start), date(end)
        if prev_end and year(s) - year(prev_end) >= 2:
            lines.append(f'\t{prev_end} = {{ holder = 0 }}')
        lines.append(entry(s, ident))
        prev_end = e
    return lines, prev_end


sura_lines, _ = seq_entries(SURA, 'sura', None)
pumb_lines, _ = seq_entries(PUMB, 'pumbedita', None)
with TITLE_OUT.open('w', encoding='utf-8', newline='\n') as out:
    out.write('# SURA (insert after 499.1.1 holder = 0; replace 867/900 entries as documented)\n')
    out.write('\n'.join(sura_lines) + '\n\n# PUMBEDITA\n' + '\n'.join(pumb_lines) + '\n')
print('people', len(people), 'wives', len(wives), 'rows', len(rows))
