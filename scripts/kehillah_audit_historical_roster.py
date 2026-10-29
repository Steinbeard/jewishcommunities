"""Audit the authored Kehillah roster and its CSV index before shipping."""
import csv
import re
from pathlib import Path

root = Path(__file__).resolve().parents[1]
history = root / 'history' / 'characters'
entries = {}
duplicates = []

for path in history.glob('*.txt'):
    source = path.read_text(encoding='utf-8-sig')
    for match in re.finditer(r'(?m)^\s*(9\d{6})\s*=\s*\{', source):
        ident = int(match.group(1))
        depth = 0
        end = None
        for pos in range(match.end() - 1, len(source)):
            depth += (source[pos] == '{') - (source[pos] == '}')
            if depth == 0:
                end = pos + 1
                break
        if end is None:
            raise SystemExit(f'unclosed character: {ident} in {path}')
        if ident in entries:
            duplicates.append((ident, path, entries[ident][0]))
        entries[ident] = (path, source[match.end():end])

with (root / 'docs' / 'data' / 'historical-character-tracker.csv').open(encoding='utf-8-sig', newline='') as stream:
    rows = list(csv.DictReader(stream))
tracker_ids = {int(row['history_id']) for row in rows if row['history_id'].isdigit()}
issues = [f'duplicate character ID {ident}: {left} and {right}' for ident, left, right in duplicates]

def birth(ident):
    if ident not in entries:
        return None
    match = re.search(r'\bbirth\s*=\s*"?(\d{3,4})\.', entries[ident][1])
    return int(match.group(1)) if match else None

for ident, (path, body) in entries.items():
    if ident < 9002000:
        continue
    if ident not in tracker_ids:
        issues.append(f'{ident} missing from historical-character-tracker.csv')
    born = birth(ident)
    for parent in ('father', 'mother'):
        match = re.search(rf'\b{parent}\s*=\s*(\d+)', body)
        if not match:
            continue
        parent_id = int(match.group(1))
        parent_born = birth(parent_id)
        if parent_born is None:
            issues.append(f'{ident} references {parent} {parent_id} without mod history/birth')
        elif born is not None and born - parent_born < 16:
            issues.append(f'{ident} has {parent} {parent_id} aged {born - parent_born} at birth')

roster = (root / 'common' / 'scripted_effects' / 'kehillah_historical_roster_effects.txt').read_text(encoding='utf-8-sig')
for match in re.finditer(r'PERSON = character:(\d+)', roster):
    ident = int(match.group(1))
    if ident not in entries:
        issues.append(f'recruited character {ident} has no history')

if issues:
    print('\n'.join(issues))
    raise SystemExit(1)
print(f'Audited {sum(ident >= 9002000 for ident in entries)} roster characters, {len(rows)} tracker rows, and {len(re.findall(r"PERSON = character:", roster))} court placements.')
