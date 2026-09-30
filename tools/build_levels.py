"""Turn tools/levels.txt into the LEVELS block of index.html."""
import json, pathlib, re, sys

root = pathlib.Path(__file__).resolve().parent.parent
rooms, cur = [], None
for n, line in enumerate((root / 'tools/levels.txt').read_text().splitlines(), 1):
    if line.startswith('#') and cur is None or not line.strip() and (cur is None or len(cur['map']) in (0, 23)):
        continue
    if line.startswith('= '):
        floor, name, hint, *flags = [s.strip() for s in line[2:].split('|')]
        cur = {'floor': floor, 'name': name, 'hint': hint, 'map': []}
        if 'nodash' in flags:
            cur['dash'] = False
        rooms.append(cur)
    elif line.startswith('saws:'):
        cur['saws'] = json.loads(line[5:])
    else:
        if len(line) > 40:
            sys.exit(f'levels.txt:{n}: row is {len(line)} wide')
        cur['map'].append(line.ljust(40))
    if cur and len(cur['map']) == 23 and not line.startswith(('saws', '=')):
        cur = cur  # room complete; header or saws may follow
for r in rooms:
    if len(r['map']) != 23:
        sys.exit(f"room {r['name']}: {len(r['map'])} rows")
    text = ''.join(r['map'])
    if text.count('S') != 1 or 'E' not in text:
        sys.exit(f"room {r['name']}: needs one S and an E")

body = 'const LEVELS = [\n' + ',\n'.join(
    '  { floor: %s, name: %s, hint: %s,%s\n    map: [\n%s\n    ] }' % (
        json.dumps(r['floor']), json.dumps(r['name']), json.dumps(r['hint']),
        (' dash: false,' if r.get('dash') is False else '') + ((' saws: ' + json.dumps(r['saws'], separators=(',', ':')) + ',') if 'saws' in r else ''),
        ',\n'.join('      ' + json.dumps(row) for row in r['map']))
    for r in rooms) + '\n];\n'
html = (root / 'index.html').read_text()
html = re.sub(r'/\*LEVELS\*/.*?/\*END LEVELS\*/', lambda m: '/*LEVELS*/\n' + body + '/*END LEVELS*/', html, flags=re.S)
(root / 'index.html').write_text(html)
print(f'{len(rooms)} rooms written')
