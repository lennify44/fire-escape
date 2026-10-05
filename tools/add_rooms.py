"""Level-editing helper: load() the rooms in levels.txt, put() one back by index (or append), as a 40x23 grid."""
import json

def load():
    head, rooms = [], []
    for line in open('tools/levels.txt').read().splitlines():
        if line.startswith('= '):
            rooms.append({'head': line[2:], 'rows': [], 'saws': None, 'plats': None, 'via': None})
        elif not rooms:
            head.append(line)
        elif line.startswith(('saws:', 'plats:', 'via:')):
            key, val = line.split(':', 1)
            rooms[-1][key] = json.loads(val)
        elif len(rooms[-1]['rows']) < 23 and (line.strip() or line):
            rooms[-1]['rows'].append(line.ljust(40))
    return head, rooms

def grid(room):
    return [list(r.ljust(40)) for r in room['rows']]

def put(index, header, rows, saws=None, plats=None, via=None):
    rows = [''.join(r) if isinstance(r, list) else r for r in rows]
    for i, r in enumerate(rows):
        assert len(r) == 40, (header, i, len(r), r)
    assert len(rows) == 23, (header, len(rows))
    head, rooms = load()
    entry = {'head': header, 'rows': rows, 'saws': saws, 'plats': plats, 'via': via}
    if index < len(rooms): rooms[index] = entry
    else: rooms.append(entry)
    out = list(head)
    while out and not out[-1].strip(): out.pop()
    for r in rooms:
        out += ['', '= ' + r['head']] + [x.rstrip() if x.strip() else x for x in r['rows']]
        for key in ('saws', 'plats', 'via'):
            if r[key]: out.append(f'{key}: ' + json.dumps(r[key]))
    open('tools/levels.txt', 'w').write('\n'.join(out) + '\n')
