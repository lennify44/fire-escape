"""Scratch helper for level editing: put(index, header, rows, saws) replaces or appends one room in levels.txt."""
import json

def load():
    lines = open('tools/levels.txt').read().splitlines()
    head, rooms = [], []
    for line in lines:
        if line.startswith('= '):
            rooms.append([line[2:], [], None])
        elif not rooms:
            head.append(line)
        elif line.startswith('saws:'):
            rooms[-1][2] = json.loads(line[5:])
        elif line.strip() or len(rooms[-1][1]) < 23 and line:
            rooms[-1][1].append(line.ljust(40))
    return head, rooms

def put(index, header, rows, saws=None):
    for i, r in enumerate(rows):
        assert len(r) == 40, (header, i, len(r), r)
    assert len(rows) == 23, (header, len(rows))
    head, rooms = load()
    entry = [header, rows, saws]
    if index < len(rooms): rooms[index] = entry
    else: rooms.append(entry)
    out = list(head)
    while out and not out[-1].strip(): out.pop()
    for h, rs, sw in rooms:
        out += ['', '= ' + h] + [r.rstrip() if r.strip() else r for r in rs]
        if sw: out.append('saws: ' + json.dumps(sw))
    open('tools/levels.txt', 'w').write('\n'.join(out) + '\n')
