"""Legacy floors L5-L8 (rooms 29-32). Run from the repo root: python3 tools/design/legacy_b.py"""
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

# L5 Cooling Tunnel: breaker stepping stones under a spiked ceiling, a breaker shaft, then a flickering floor
g = G(); frame(g)
f(g, 2, 37, 2, 21)
f(g, 2, 37, 14, 19, ' '); f(g, 5, 31, 14, 14, 'v')            # low tunnel
g[19][3] = 'S'
pit(g, 20, 5, 31)
for c0, r, ch in ((7, 18, 'R'), (11, 17, 'B'), (15, 18, 'R'), (19, 17, 'B'), (23, 18, 'R'), (27, 17, 'B')):
    f(g, c0, c0 + 1, r, r, ch)
g[19][34] = 'C'
f(g, 32, 37, 2, 19, ' ')                                       # shaft
f(g, 35, 36, 16, 16, 'B'); f(g, 32, 33, 13, 13, 'R'); f(g, 35, 36, 10, 10, 'B'); f(g, 32, 33, 7, 7, 'R')
f(g, 37, 37, 11, 14, '<'); f(g, 37, 37, 4, 8, '<')
f(g, 2, 31, 2, 5, ' '); f(g, 8, 30, 2, 2, 'v')                  # top corridor
f(g, 23, 30, 6, 6, '}'); pit(g, 6, 9, 22)
for i, c in enumerate(range(9, 23)): g[6][c] = 'R' if (c // 2) % 2 == 0 else 'B'
g[5][31] = 'C'; g[4][2] = g[5][2] = 'E'
g[19][13] = 'K'
put(28, 'L5 | Cooling Tunnel | Be in the air when the beat changes. Never on the block that leaves.', g,
    via=[[8, 16], [20, 15], [28, 15], [34, 18], [35, 9], [32, 5], [16, 5], [3, 5]])

# L6 Kiln: never touch the floor. Springs, rotten planks and a dash refill between them
g = G(); frame(g)
f(g, 2, 5, 20, 21); g[19][3] = 'S'
pit(g, 20, 6, 33); f(g, 6, 33, 2, 2, 'v')
g[20][9] = '#'; g[19][9] = 'T'
g[13][13] = '='; f(g, 11, 19, 7, 8); f(g, 11, 19, 9, 9, 'v')  # a spiked slab caps the first spring
f(g, 17, 18, 16, 16); g[15][17] = 'C'
g[20][22] = '#'; g[19][22] = 'T'
g[9][24] = '*'
g[14][27] = '='
f(g, 30, 31, 10, 10, '=')
f(g, 34, 37, 8, 21); g[6][37] = g[7][37] = 'E'
g[11][20] = 'K'
put(29, 'L6 | Kiln | The floor is not an option. Planks hold for half a second.', g,
    via=[[9, 15], [13, 12], [17, 15], [22, 15], [27, 13], [30, 9], [36, 7]])

# L7 Rolling Mill: belts drive you into saws; long gaps want a super, the low top corridor wants a hyper
g = G(); frame(g)
f(g, 2, 37, 7, 21); f(g, 2, 33, 15, 19, ' '); f(g, 4, 31, 15, 15, 'v')
g[19][3] = 'S'
f(g, 6, 12, 20, 20, '{'); pit(g, 20, 13, 20); f(g, 21, 25, 20, 20, '}'); pit(g, 20, 26, 31)
f(g, 34, 37, 3, 19, ' ')
for r, c0 in ((16, 34), (13, 36), (10, 34)): f(g, c0, c0 + 1, r, r, '-')
g[19][35] = 'C'
f(g, 2, 33, 3, 6, ' '); f(g, 2, 37, 2, 2, 'v')
f(g, 24, 31, 7, 7, '}'); pit(g, 7, 15, 23); f(g, 8, 14, 7, 7, '}'); pit(g, 7, 5, 7)
g[6][32] = 'C'; g[5][2] = g[6][2] = 'E'
g[17][17] = 'K'
put(30, 'L7 | Rolling Mill | Dash, then jump while the dash is still going. The belts will not help.', g,
    saws=[{"a": [7, 19], "b": [11, 19], "t": 100}, {"a": [21, 19], "b": [25, 19], "t": 100, "ph": 0.5},
          {"a": [34, 7], "b": [37, 7], "t": 80}, {"a": [9, 4], "b": [14, 4], "t": 120}],
    via=[[12, 18], [22, 18], [35, 18], [35, 9], [32, 6], [20, 5], [10, 6], [3, 6]])

# L8 Sluice: climb three spiked chimneys; the fans help, the crumbling ledges do not wait
g = G(); frame(g)
f(g, 2, 37, 2, 21)
f(g, 2, 7, 15, 20, ' '); g[20][3] = 'S'                        # start room
f(g, 8, 11, 4, 20, ' '); g[21][9] = g[21][10] = 'F'            # chimney 1 with a fan
f(g, 8, 8, 5, 9, '>'); f(g, 11, 11, 14, 18, '<'); f(g, 8, 11, 3, 3, 'v')
f(g, 12, 16, 5, 6, ' '); f(g, 12, 16, 7, 7)                     # door to chimney 2
f(g, 17, 20, 5, 20, ' ')                                        # chimney 2, wall jumps down then up
f(g, 17, 17, 9, 13, '>'); f(g, 20, 20, 7, 10, '<'); f(g, 17, 20, 21, 21, '^')
f(g, 18, 19, 15, 15, '='); g[14][18] = 'C'
f(g, 21, 25, 17, 19, ' ')                                       # door to chimney 3
f(g, 26, 29, 3, 19, ' '); g[20][27] = g[20][28] = 'F'
f(g, 26, 26, 5, 9, '>'); f(g, 29, 29, 12, 15, '<'); f(g, 26, 29, 2, 2, 'v')
f(g, 30, 37, 5, 6, ' '); g[5][37] = g[6][37] = 'E'
f(g, 30, 33, 6, 6, '^')
f(g, 3, 6, 10, 13, ' '); g[11][4] = 'K'; f(g, 7, 7, 11, 12, ' ')
put(31, 'L8 | Sluice | Up the chimneys. Kick off the clean wall, never the rusty one.', g,
    via=[[5, 19], [9, 12], [14, 6], [18, 10], [18, 14], [23, 18], [27, 12], [34, 5]])
