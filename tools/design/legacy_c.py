"""Legacy floors L9-L12 (rooms 33-36). Run from the repo root: python3 tools/design/legacy_c.py"""
import sys; sys.path.insert(0, 'tools')
from add_rooms import put

def G(): return [[' '] * 40 for _ in range(23)]
def f(g, c0, c1, r0, r1, ch='#'):
    for r in range(r0, r1 + 1):
        for c in range(c0, c1 + 1): g[r][c] = ch
def frame(g, bottom=True):
    f(g, 0, 39, 0, 1); f(g, 0, 1, 0, 22); f(g, 38, 39, 0, 22)
    if bottom: f(g, 0, 39, 22, 22)
def pit(g, r, c0, c1):  # gap in a floor at row r with spikes in the tile below
    f(g, c0, c1, r, r, ' '); f(g, c0, c1, r + 1, r + 1, '^')

# L9 Old Generator: breaker stones around a rotor of saws; the hat sits on the hub
g = G(); frame(g)
f(g, 2, 6, 20, 21); g[19][3] = 'S'
pit(g, 20, 7, 32); f(g, 33, 37, 20, 21); g[19][35] = 'C'
f(g, 7, 37, 2, 2, 'v')
for c0, r, ch in ((8, 18, 'R'), (12, 19, 'B'), (16, 19, 'R'), (21, 19, 'B'), (25, 19, 'R'), (29, 18, 'B')):
    f(g, c0, c0 + 1, r, r, ch)
f(g, 35, 36, 15, 15, 'R'); f(g, 32, 33, 12, 12, 'B'); f(g, 35, 36, 9, 9, 'R')
for c0, r, ch in ((28, 6, 'B'), (23, 6, 'R'), (17, 6, 'B'), (11, 6, 'R')):
    f(g, c0, c0 + 1, r, r, ch)
f(g, 2, 6, 6, 6); g[4][2] = g[5][2] = 'E'
g[10][8] = 'K'
put(32, 'L9 | Old Generator | The rotor never stops. The blocks around it keep their own time.', g,
    saws=[{"o": [20, 11], "rad": 4.5, "t": 240, "n": 3}],
    via=[[9, 17], [17, 18], [26, 18], [35, 19], [35, 8], [28, 5], [17, 5], [4, 5]],
    hatvia=[[9, 17], [17, 18], [26, 18], [35, 19], [35, 8], [28, 5], [17, 5], [11, 5], [8, 10], [4, 5]])

# L10 Overflow: a lift, two rotten planks and an updraft between saws, then down past a spinning pair
g = G(); frame(g)
f(g, 2, 37, 21, 21, '^'); f(g, 2, 37, 2, 2, 'v')
f(g, 2, 4, 14, 21); g[13][3] = 'S'
f(g, 15, 16, 11, 11, '='); f(g, 19, 20, 12, 12, '=')
g[21][23] = 'F'
f(g, 30, 31, 9, 9); g[8][30] = 'C'
f(g, 34, 37, 17, 21); g[15][37] = g[16][37] = 'E'
g[4][30] = 'K'
put(33, 'L10 | Overflow | Planks, air, a lift and saws. Nothing here holds still.', g,
    saws=[{"a": [22, 8], "b": [24, 8], "t": 50}, {"o": [33, 13], "rad": 2, "t": 120, "n": 3},
          {"a": [27, 3], "b": [34, 3], "t": 140}],
    plats=[{"a": [5, 14], "b": [12, 14], "t": 200}, {"a": [26, 18], "b": [26, 7], "t": 240}],
    via=[[8, 13], [15, 10], [19, 11], [23, 10], [27, 8], [30, 8], [33, 16], [36, 16]])

# L11 Spillway: everything, twice. Belt into a breaker gate, fan, planks, a spring under a lid, a lift,
# then up a scaffold shaft and back over belts, breakers and a long gap
g = G(); frame(g)
f(g, 2, 37, 7, 21); f(g, 2, 31, 14, 19, ' '); f(g, 5, 31, 14, 14, 'v')
g[19][3] = 'S'
f(g, 4, 9, 20, 20, '}'); f(g, 11, 11, 15, 19, 'R')
pit(g, 20, 12, 30); g[21][14] = 'F'
f(g, 17, 18, 17, 17, '=')
f(g, 20, 21, 18, 18, 'B')
f(g, 32, 37, 3, 19, ' '); g[19][34] = 'C'
for r, c0 in ((16, 36), (13, 32), (10, 36)): f(g, c0, c0 + 1, r, r, '-')
f(g, 2, 31, 3, 6, ' '); f(g, 2, 37, 2, 2, 'v')
f(g, 24, 29, 7, 7, '{'); pit(g, 7, 10, 23)
for c in (21, 18, 15): g[7][c] = 'R' if c != 18 else 'B'
g[4][12] = '*'
g[6][30] = 'C'; g[5][2] = g[6][2] = 'E'
g[17][26] = 'K'
put(34, 'L11 | Spillway | Everything from the tower and the basement, twice over.', g,
    saws=[{"a": [32, 7], "b": [37, 7], "t": 90}, {"a": [10, 4], "b": [20, 4], "t": 160}],
    plats=[{"a": [23, 18], "b": [29, 18], "t": 200}],
    via=[[10, 19], [14, 16], [17, 16], [20, 17], [24, 17], [34, 18], [34, 9], [30, 5], [16, 5], [3, 6]])

# L12 Daylight: three tiers to the surface. The door at the top is the last one.
g = G(); frame(g)
f(g, 2, 37, 15, 17); f(g, 2, 37, 7, 9)                         # floors between tiers
g[20][3] = 'S'; f(g, 2, 3, 21, 21)
f(g, 4, 9, 21, 21, '{'); g[19][8] = 'o'
pit(g, 21, 10, 21); g[20][13] = '='; g[20][18] = '='
f(g, 22, 24, 21, 21)
pit(g, 21, 25, 32); g[19][28] = '*'
f(g, 33, 37, 21, 21); f(g, 33, 33, 18, 20, 'B')
g[20][36] = 'C'
f(g, 35, 37, 15, 17, ' '); g[16][35] = '>'                      # chimney up to tier 2
pit(g, 15, 6, 19); pit(g, 15, 23, 25); f(g, 4, 34, 10, 10, 'v')   # lift pit, then a hop under rotor 2
g[14][4] = 'C'
f(g, 2, 3, 7, 9, ' ')                                          # chimney up to tier 3
f(g, 6, 37, 2, 2, 'v')
g[6][8] = 'T'; pit(g, 7, 9, 33); g[4][13] = '*'; g[5][20] = '*'; g[4][27] = '*'
g[7][17] = '='; g[7][24] = '='
f(g, 34, 37, 7, 7); g[5][37] = g[6][37] = 'E'
g[12][12] = 'K'
put(35, 'L12 | Daylight | Three more levels of the old works, then the surface.', g,
    saws=[{"o": [16, 11], "rad": 1.5, "t": 100, "n": 2}, {"o": [24, 11], "rad": 1.5, "t": 100, "n": 2, "ccw": 1}],
    plats=[{"a": [17, 15], "b": [6, 15], "t": 300, "w": 3}],
    via=[[9, 20], [24, 19], [36, 20], [36, 13], [24, 14], [4, 14], [3, 5], [12, 5], [24, 5], [36, 6]],
    hatvia=[[9, 20], [24, 19], [36, 20], [36, 13], [24, 14], [12, 12], [4, 14], [3, 5], [12, 5], [24, 5], [36, 6]])
