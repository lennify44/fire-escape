"""Basement floors B5-B8 (rooms 17-20). Run from the repo root: python3 tools/design/basement_b.py"""
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

# B5 Freight Elevator: catch the lifts; a saw circles the ledge where you wait for the second one
g = G(); frame(g)
f(g, 2, 37, 21, 21, '^'); f(g, 2, 4, 20, 21); g[19][3] = 'S'
f(g, 11, 14, 6, 7); g[5][12] = 'C'; f(g, 11, 14, 8, 8, 'v')
f(g, 33, 37, 20, 21); g[18][37] = g[19][37] = 'E'
f(g, 2, 8, 2, 2, 'v'); f(g, 28, 37, 2, 2, 'v')
f(g, 15, 16, 9, 21); f(g, 15, 16, 8, 8, '^')          # pillar: no walking across the bottom
g[3][31] = 'K'
put(16, 'B5 | Freight Elevator | Every lift runs on the same clock. Miss one and wait for the next trip.', g,
    saws=[{"o": [21, 2.2], "rad": 1.2, "t": 120, "n": 1}, {"a": [10, 11], "b": [27, 11], "t": 240}],
    plats=[{"a": [6, 19], "b": [6, 6], "t": 240}, {"a": [15, 6], "b": [24, 6], "t": 240}, {"a": [30, 6], "b": [30, 17], "t": 240, "ph": 0.5}],
    via=[[7, 17], [12, 5], [16, 5], [22, 5], [31, 5], [31, 16]])

# B6 Laundry: belts, saws and rotten planks
g = G(); frame(g)
f(g, 2, 37, 20, 21); g[19][3] = 'S'
f(g, 6, 15, 20, 20, '}'); g[19][11] = 'o'; f(g, 16, 25, 20, 20, '{'); g[19][20] = 'o'
pit(g, 20, 26, 29); g[19][32] = 'C'
f(g, 2, 31, 7, 12); f(g, 2, 31, 13, 13, 'v'); f(g, 6, 9, 13, 13, ' ')
f(g, 35, 36, 16, 16, '='); f(g, 32, 33, 13, 13, '='); f(g, 35, 36, 10, 10, '=')
f(g, 2, 31, 7, 7)
f(g, 22, 31, 7, 7, '{'); pit(g, 7, 14, 21); f(g, 16, 16, 7, 7, '='); f(g, 19, 19, 7, 7, '=')
f(g, 6, 13, 7, 7, '}')
g[6][29] = 'C'; g[5][2] = g[6][2] = 'E'
g[4][17] = 'K'
put(17, 'B6 | Laundry | Belts feed you into the saws. Jump before the belt decides for you.', g,
    saws=[{"a": [5, 4], "b": [28, 4], "t": 240}])

# B7 Air Handling: three updraft tubes with spiked walls; leave each one through its side door
g = G(); frame(g)
f(g, 2, 37, 2, 21)
f(g, 2, 4, 18, 20, ' '); g[20][3] = 'S'                       # start alcove
f(g, 5, 8, 2, 20, ' '); g[21][6] = g[21][7] = 'F'            # tube 1
f(g, 9, 13, 13, 14, ' ')                                      # door 1 to tube 2
f(g, 14, 17, 2, 20, ' '); g[21][15] = g[21][16] = 'F'        # tube 2
f(g, 18, 22, 5, 6, ' ')                                       # door 2 to tube 3
f(g, 23, 26, 2, 20, ' '); g[21][24] = g[21][25] = 'F'        # tube 3
f(g, 27, 37, 9, 10, ' '); f(g, 31, 37, 7, 10, ' ')           # door 3 to the exit room
f(g, 18, 22, 17, 20, ' ')                                     # side pocket for the hat
for c0, c1, doors in ((5, 8, [(13, 14)]), (14, 17, [(13, 14), (5, 6)]), (23, 26, [(5, 6), (9, 10)])):
    for r in range(3, 20):
        if not any(a <= r <= b for a, b in doors):
            if g[r][c0 - 1] == '#': g[r][c0] = '>'
            if g[r][c1 + 1] == '#': g[r][c1] = '<'
    f(g, c0, c1, 2, 2, 'v')
for r in range(17, 21): g[r][5] = ' '                          # no spikes next to the start alcove
g[12][11] = 'C'; g[4][20] = 'C'
g[9][37] = g[10][37] = 'E'
g[19][20] = 'K'
put(18, 'B7 | Air Handling | Ride the air up and leave through the side door before the spikes on top.', g)

# B8 Cold Storage: springs under breaker ceilings
g = G(); frame(g)
f(g, 2, 37, 20, 21); g[19][3] = 'S'
for c, ch in ((9, 'R'), (17, 'B'), (25, 'R')):
    f(g, c - 2, c + 2, 19, 19, '^'); g[19][c] = 'T'
    f(g, c - 1, c + 1, 12, 12, ch)
f(g, 2, 37, 11, 11); f(g, 8, 10, 11, 11, ' '); f(g, 16, 18, 11, 11, ' '); f(g, 24, 26, 11, 11, ' ')
f(g, 2, 37, 10, 10, ' ')
f(g, 31, 37, 13, 19, ' '); g[19][34] = 'C'; f(g, 35, 36, 16, 16, 'B'); f(g, 32, 33, 13, 13, 'R')
f(g, 30, 30, 11, 11, ' '); f(g, 31, 37, 11, 11, ' ')
f(g, 2, 29, 5, 9); f(g, 2, 29, 2, 4, ' ')
f(g, 30, 37, 2, 10, ' ')
pit(g, 5, 8, 26); 
for c in (11, 16, 21): g[5][c] = 'R' if c != 16 else 'B'
g[4][28] = 'C'; g[3][2] = g[4][2] = 'E'; f(g, 2, 7, 5, 5)
g[14][17] = 'K'
put(19, 'B8 | Cold Storage | Time the spring so the block above you is open.', g)
