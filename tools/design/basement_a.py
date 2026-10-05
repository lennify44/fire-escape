"""Basement floors B1-B4 (rooms 13-16). Run from the repo root: python3 tools/design/basement_a.py"""
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

# B1 Loading Dock: conveyor belts
g = G(); frame(g)
f(g, 2, 33, 5, 21)                       # mass; carve out below
f(g, 2, 37, 13, 19, ' ')                 # bottom hall
f(g, 2, 37, 2, 4, ' ')                   # top corridor
f(g, 34, 37, 5, 19, ' ')                 # shaft on the right
f(g, 2, 37, 20, 21)                      # bottom floor
f(g, 7, 14, 20, 20, '}'); pit(g, 20, 15, 19); f(g, 20, 27, 20, 20, '{'); pit(g, 20, 28, 30)
f(g, 6, 29, 13, 13, 'v')                 # spikes under the hall ceiling
g[19][3] = 'S'; g[19][32] = 'C'
for r, c0 in ((17, 36), (14, 34), (11, 36), (8, 34)): f(g, c0, c0 + 1, r, r)
f(g, 6, 12, 5, 5, '}'); pit(g, 5, 13, 16); f(g, 17, 24, 5, 5, '{'); pit(g, 5, 25, 28)
f(g, 14, 27, 2, 2, 'v')
g[4][31] = 'C'; g[3][2] = g[4][2] = 'E'
g[15][17] = 'K'
put(12, 'B1 | Loading Dock | The street door is chained shut. Down through the basement. Belts push you around while you stand on them.', g)

# B2 Parking Level: moving platforms over a drop
g = G(); frame(g, bottom=False)
f(g, 2, 5, 18, 22); g[17][3] = 'S'
f(g, 23, 25, 9, 10); g[8][24] = 'C'
f(g, 35, 37, 9, 22); g[7][37] = g[8][37] = 'E'
f(g, 6, 34, 2, 2, 'v')
f(g, 9, 13, 21, 22, '^'); f(g, 9, 13, 22, 22, '#')
g[4][20] = 'K'
put(13, 'B2 | Parking Level | Ride the yellow lifts. You can jump up through them.', g,
    plats=[{"a": [7, 17], "b": [14, 17], "t": 240}, {"a": [18, 18], "b": [18, 7], "t": 240, "ph": 0.5},
           {"a": [27, 9], "b": [31, 9], "t": 240}],
    via=[[10, 16], [19, 10], [24, 8], [29, 8], [36, 8]])

# B3 Boiler Room: fans
g = G(); frame(g)
f(g, 2, 37, 20, 21)                      # bottom floor
f(g, 2, 29, 9, 12)                       # mass between the levels
f(g, 2, 30, 5, 8)                        # top floor block
f(g, 2, 30, 2, 4, ' ')
pit(g, 20, 7, 9); g[21][8] = 'F'
f(g, 11, 14, 15, 16)                     # ledge after fan 1
pit(g, 20, 16, 18); g[21][17] = 'F'
f(g, 20, 23, 14, 15)                     # ledge after fan 2
g[13][21] = 'C'
pit(g, 20, 25, 29)
f(g, 31, 37, 13, 21, ' '); f(g, 30, 30, 13, 21); f(g, 30, 30, 18, 19, ' '); f(g, 31, 37, 21, 21); g[21][33] = 'F'; g[21][34] = 'F'
f(g, 31, 31, 15, 16, '>'); f(g, 37, 37, 10, 11, '<'); f(g, 31, 31, 6, 7, '>')
f(g, 31, 37, 2, 12, ' ')
pit(g, 5, 23, 25); g[6][24] = 'F'; f(g, 22, 26, 2, 2, 'v')
pit(g, 5, 12, 14); g[6][13] = 'F'; f(g, 11, 15, 2, 2, 'v')
g[4][28] = 'C'; g[3][2] = g[4][2] = 'E'
g[19][3] = 'S'
g[13][4] = 'K'
put(14, 'B3 | Boiler Room | Fans blow you up. Dash across an updraft before it lifts you into trouble.', g)

# B4 Breaker Room: blocks that swap
g = G(); frame(g)
f(g, 2, 5, 19, 21); g[18][3] = 'S'
pit(g, 21, 6, 31); f(g, 6, 31, 20, 20, ' ')
for c0, r, ch in ((8, 18, 'R'), (13, 17, 'B'), (18, 16, 'R'), (23, 15, 'B'), (28, 14, 'R')): f(g, c0, c0 + 1, r, r, ch)
f(g, 32, 37, 13, 21)
f(g, 2, 31, 6, 9)                        # top block
f(g, 32, 37, 2, 12, ' ')
f(g, 35, 36, 10, 10, 'B'); f(g, 33, 34, 7, 7, 'R')
g[12][34] = 'C'
pit(g, 5, 7, 9); pit(g, 5, 14, 16); pit(g, 5, 21, 23)
f(g, 2, 31, 5, 5); pit(g, 5, 7, 9); pit(g, 5, 14, 16); pit(g, 5, 21, 23)
f(g, 26, 26, 2, 4, 'R'); f(g, 19, 19, 2, 4, 'B'); f(g, 12, 12, 2, 4, 'R')
g[4][29] = 'C'; g[3][2] = g[4][2] = 'E'
g[11][36] = 'K'
put(15, 'B4 | Breaker Room | Pink and blue blocks take turns being solid. Listen for the click.', g)
