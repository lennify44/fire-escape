"""Small helpers for building 40x23 rooms in Python. Rows are 0..22, columns 0..39."""
import sys; sys.path.insert(0, 'tools')
from add_rooms import put, load

def G(): return [[' '] * 40 for _ in range(23)]
def f(g, c0, c1, r0, r1, ch='#'):
    for r in range(r0, r1 + 1):
        for c in range(c0, c1 + 1): g[r][c] = ch
def frame(g, bottom=True):
    f(g, 0, 39, 0, 1); f(g, 0, 1, 0, 22); f(g, 38, 39, 0, 22)
    if bottom: f(g, 0, 39, 22, 22)
def pit(g, r, c0, c1):  # gap in a floor at row r with spikes in the tile below
    f(g, c0, c1, r, r, ' '); f(g, c0, c1, r + 1, r + 1, '^')

def room_index(label):
    """Index of the room with this floor label, or the next free index to append it."""
    _, rooms = load()
    for i, r in enumerate(rooms):
        if r['head'].split('|')[0].strip() == label: return i
    return len(rooms)

def night(label, name, hint, g, par=None, **kw):
    """Write a Night Shift run; keeps the par time already in levels.txt unless one is given."""
    i = room_index(label)
    _, rooms = load()
    if par is None and i < len(rooms):
        for fl in rooms[i]['head'].split('|')[3:]:
            if fl.strip().startswith('par='): par = float(fl.strip()[4:])
    put(i, f'{label} | {name} | {hint}' + (f' | par={par}' if par else ''), g, kw.get('saws'), kw.get('plats'), kw.get('via'))
