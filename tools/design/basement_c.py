"""Basement floors B9-B12 (rooms 21-24). Run from the repo root: python3 tools/design/basement_c.py"""
import sys; sys.path.insert(0, 'tools')
from add_rooms import put

def G(): return [[' '] * 40 for _ in range(23)]
def f(g, c0, c1, r0, r1, ch='#'):
    for r in range(r0, r1 + 1):
        for c in range(c0, c1 + 1): g[r][c] = ch
def frame(g, bottom=True):
    f(g, 0, 39, 0, 1); f(g, 0, 1, 0, 22); f(g, 38, 39, 0, 22)
    if bottom: f(g, 0, 39, 22, 22)
def pit(g, r, c0, c1):
    f(g, c0, c1, r, r, ' '); f(g, c0, c1, r + 1, r + 1, '^')

# B9 Server Room: belts drag you back while breaker walls cycle; tile floors that flicker
g = G(); frame(g)
f(g, 2, 37, 20, 21); g[19][3] = 'S'
f(g, 5, 20, 20, 20, '{'); f(g, 5, 20, 8, 16)
f(g, 10, 10, 17, 19, 'R'); f(g, 15, 15, 17, 19, 'B')
pit(g, 20, 23, 31); g[17][27] = '*'
g[19][34] = 'C'
f(g, 2, 31, 8, 15); f(g, 32, 37, 2, 19, ' ')
f(g, 35, 36, 16, 16, 'B'); f(g, 32, 33, 13, 13, 'R'); f(g, 35, 36, 10, 10, 'B')
f(g, 2, 31, 7, 7); f(g, 20, 31, 7, 7, '}')
pit(g, 7, 12, 18)
for i, c in enumerate(range(12, 19)): g[7][c] = 'R' if i % 2 == 0 else 'B'
f(g, 12, 18, 8, 8, '^')
g[6][29] = 'C'; g[5][2] = g[6][2] = 'E'
f(g, 2, 31, 2, 2, 'v'); f(g, 2, 9, 2, 2, ' ')
f(g, 21, 31, 12, 15, ' '); f(g, 21, 31, 11, 11, 'v')
g[14][26] = 'K'
put(20, 'B9 | Server Room | The belt drags you back while you wait for the next beat.', g,
    via=[[20, 18], [34, 18], [34, 9], [25, 6], [10, 6]])

# B10 Sewer Access: lifts over nothing, and an updraft that carries you towards spikes
g = G(); frame(g, bottom=False)
f(g, 2, 5, 12, 22); g[11][3] = 'S'
g[22][18] = 'F'; f(g, 16, 20, 2, 2, 'v')
f(g, 22, 23, 13, 13); g[12][22] = 'C'
f(g, 33, 37, 8, 22); g[6][37] = g[7][37] = 'E'
f(g, 6, 15, 2, 2, 'v'); f(g, 21, 32, 2, 2, 'v')
g[4][18] = 'K'
put(21, 'B10 | Sewer Access | The updraft does not stop at the spikes. You have to.', g,
    saws=[{"o": [27, 11], "rad": 2, "t": 120, "n": 2}],
    plats=[{"a": [7, 12], "b": [14, 12], "t": 240}, {"a": [20, 16], "b": [20, 6], "t": 240}, {"a": [24, 6], "b": [29, 6], "t": 240}],
    via=[[10, 11], [18, 14], [22, 12], [21, 5], [27, 5], [35, 7]])

# B11 Pump Station: everything at once
g = G(); frame(g)
f(g, 2, 37, 20, 21); g[19][3] = 'S'
f(g, 4, 12, 20, 20, '}'); f(g, 13, 13, 17, 19, 'R')
pit(g, 20, 15, 29); g[21][16] = 'F'; f(g, 18, 19, 16, 16, '=')
f(g, 2, 31, 8, 13); f(g, 4, 31, 14, 14, 'v'); f(g, 14, 18, 14, 14, ' ')
g[20][35] = 'F'; g[19][33] = 'C'
f(g, 32, 37, 2, 2, 'v')
f(g, 2, 31, 7, 7); f(g, 19, 27, 7, 7, '{')
pit(g, 7, 8, 16); f(g, 9, 10, 7, 7, '='); f(g, 13, 14, 7, 7, '=')
g[6][29] = 'C'; g[5][2] = g[6][2] = 'E'
g[18][37] = 'K'
put(22, 'B11 | Pump Station | Belts, breakers, fans, lifts and saws, all on one floor.', g,
    saws=[{"a": [5, 4], "b": [28, 4], "t": 240}],
    plats=[{"a": [21, 18], "b": [27, 18], "t": 240}],
    via=[[11, 18], [16, 15], [18, 15], [24, 17], [33, 19], [35, 5], [28, 6], [5, 6]])

# B12 Outfall: three tiers to the river
g = G(); frame(g)
f(g, 2, 37, 15, 17); f(g, 2, 37, 7, 9)                         # floors between tiers, three tiles thick
g[20][3] = 'S'
f(g, 4, 10, 21, 21, '}'); g[20][8] = 'o'
pit(g, 21, 12, 20); g[20][14] = '='; g[20][18] = '='
f(g, 22, 24, 21, 21, ' '); g[22][22] = g[22][24] = '^'; g[22][23] = 'F'
f(g, 30, 30, 18, 20, 'B'); f(g, 33, 33, 18, 20, 'R')
g[20][36] = 'C'
f(g, 35, 37, 15, 17, ' '); g[16][35] = '>'                      # chimney up to tier 2
pit(g, 15, 8, 30)
g[14][4] = 'C'
f(g, 2, 3, 7, 9, ' ')                                          # chimney up to tier 3
f(g, 7, 37, 2, 2, 'v')
g[6][12] = 'T'; pit(g, 7, 13, 31); g[4][17] = '*'; g[4][23] = '*'; f(g, 27, 28, 7, 7, 'R')
g[5][37] = g[6][37] = 'E'
g[11][20] = 'K'
put(23, 'B12 | Outfall | The river is on the other side. One more floor.', g,
    saws=[{"o": [19, 11], "rad": 1.5, "t": 120, "n": 2}],
    plats=[{"a": [27, 15], "b": [9, 15], "t": 240, "w": 3}],
    via=[[10, 20], [23, 19], [36, 20], [36, 13], [18, 14], [4, 14], [3, 5], [12, 5], [24, 5], [35, 6]])
