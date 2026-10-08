"""Turn tools/levels.txt into the LEVELS block of index.html."""
import json, pathlib, re, sys

root = pathlib.Path(__file__).resolve().parent.parent
rooms, cur = [], None
for n, line in enumerate((root / 'tools/levels.txt').read_text().splitlines(), 1):
    if cur is None and (line.startswith('#') or not line.strip()):
        continue
    if line.startswith('= '):
        floor, name, hint, *flags = [s.strip() for s in line[2:].split('|')]
        cur = {'floor': floor, 'name': name, 'hint': hint, 'map': []}
        if 'nodash' in flags:
            cur['dash'] = False
        for fl in flags:
            if fl.startswith('par='):
                cur['par'] = float(fl[4:])
        rooms.append(cur)
    elif line.startswith(('saws:', 'plats:', 'via:')):
        key, val = line.split(':', 1)
        cur[key] = json.loads(val)
    elif len(cur['map']) < 23:
        if len(line) > 40:
            sys.exit(f'levels.txt:{n}: row is {len(line)} wide')
        cur['map'].append(line.ljust(40))
    elif line.strip():
        sys.exit(f'levels.txt:{n}: unexpected line after the 23 map rows')
for r in rooms:
    if len(r['map']) != 23:
        sys.exit(f"room {r['name']}: {len(r['map'])} rows")
    text = ''.join(r['map'])
    if text.count('S') != 1 or 'E' not in text or text.count('K') > 1:
        sys.exit(f"room {r['name']}: needs one S, an E and at most one K")

def extras(r):
    out = ' dash: false,' if r.get('dash') is False else ''
    if 'par' in r:
        out += ' par: %s,' % r['par']
    for key in ('saws', 'plats', 'via'):
        if key in r:
            out += f' {key}: ' + json.dumps(r[key], separators=(',', ':')) + ','
    return out

body = 'const LEVELS = [\n' + ',\n'.join(
    '  { floor: %s, name: %s, hint: %s,%s\n    map: [\n%s\n    ] }' % (
        json.dumps(r['floor']), json.dumps(r['name']), json.dumps(r['hint']), extras(r),
        ',\n'.join('      ' + json.dumps(row) for row in r['map']))
    for r in rooms) + '\n];\n'
html = (root / 'index.html').read_text()
html = re.sub(r'/\*LEVELS\*/.*?/\*END LEVELS\*/', lambda m: '/*LEVELS*/\n' + body + '/*END LEVELS*/', html, flags=re.S)
(root / 'index.html').write_text(html)
print(f'{len(rooms)} rooms written')
