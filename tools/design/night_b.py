"""Night Shift, shift 2 (N9-N16): machinery. Run from the repo root: python3 tools/design/night_b.py"""
import sys; sys.path.insert(0, 'tools/design')
from common import G, f, frame, pit, night

# N9 Treadmill: a belt pushing you back into saws, then one throwing you at a pit
g = G(); frame(g); f(g, 2, 37, 2, 13); f(g, 6, 30, 14, 14, 'v')
f(g, 2, 37, 20, 21); g[19][3] = 'S'
f(g, 6, 17, 20, 20, '{'); g[19][10] = 'o'; g[19][15] = 'o'
pit(g, 20, 18, 21); f(g, 22, 30, 20, 20, '}'); pit(g, 20, 31, 34)
g[18][37] = g[19][37] = 'E'
night('N9', 'Treadmill', 'The belt is not on your side.', g)

# N10 Updraft: four fan columns over a long pit
g = G(); frame(g)
f(g, 2, 5, 20, 21); g[19][3] = 'S'; f(g, 6, 33, 21, 21, '^')
for c, cap in ((9, 8), (15, 12), (21, 6), (27, 10)):
    g[21][c] = 'F'; f(g, c - 1, c + 1, cap - 1, cap)
f(g, 12, 12, 2, 9); g[10][12] = 'v'; f(g, 18, 18, 2, 7); g[8][18] = 'v'; f(g, 24, 24, 2, 4); g[5][24] = 'v'
f(g, 31, 37, 14, 21); g[12][37] = g[13][37] = 'E'
night('N10', 'Updraft', 'Hover under the cap, then dash to the next column.', g,
      via=[[9, 10], [15, 13], [21, 8], [27, 12], [34, 13]])

# N11 Lift Hop: three sideways lifts, each a level higher; jump up while they wait at the end of their run
g = G(); frame(g, bottom=False); f(g, 2, 37, 2, 2, 'v')
f(g, 2, 4, 14, 22); g[13][3] = 'S'
f(g, 33, 37, 8, 22); g[6][37] = g[7][37] = 'E'
night('N11', 'Lift Hop', 'Lifts stop for a moment at each end. Jump up to the next one then. | nodash', g,
      plats=[{"a": [5, 13], "b": [11, 13], "t": 240}, {"a": [14, 10], "b": [20, 10], "t": 240, "ph": 0.5},
             {"a": [23, 7], "b": [29, 7], "t": 240}],
      via=[[9, 12, 1], [17, 9, 1], [26, 6, 1], [34, 7]])

# N12 On the Beat: breaker stepping stones
g = G(); frame(g); f(g, 2, 37, 2, 11); f(g, 5, 33, 12, 12, 'v')
f(g, 2, 4, 20, 21); f(g, 5, 33, 21, 21, '^'); f(g, 34, 37, 20, 21); g[19][3] = 'S'
for i, (c, r) in enumerate(((7, 19), (11, 18), (15, 17), (19, 16), (23, 17), (27, 18), (31, 19))):
    f(g, c, c + 1, r, r, 'R' if i % 2 == 0 else 'B')
g[18][37] = g[19][37] = 'E'
night('N12', 'On the Beat', 'Pink, blue, pink. Move on the click.', g,
      via=[[8, 18], [12, 17], [16, 16], [20, 15], [24, 16], [28, 17], [32, 18], [36, 19]])

# N13 Grinder: saws on rails
g = G(); frame(g); f(g, 2, 37, 2, 13)
f(g, 2, 37, 20, 21); g[19][3] = 'S'; pit(g, 20, 28, 33)
g[18][37] = g[19][37] = 'E'
night('N13', 'Grinder', 'Watch one cycle. Then go.', g,
      saws=[{"a": [9, 14], "b": [9, 19], "t": 60}, {"a": [14, 14], "b": [14, 19], "t": 60, "ph": 0.33},
            {"a": [19, 14], "b": [19, 19], "t": 60, "ph": 0.66}, {"a": [24, 14], "b": [24, 19], "t": 60},
            {"a": [27, 16], "b": [34, 16], "t": 120}],
      via=[[12, 19], [17, 19], [22, 19], [26, 19], [36, 19]])

# N14 Tailwind: belt into an updraft, then a belt against you
g = G(); frame(g); f(g, 18, 37, 2, 5); f(g, 18, 31, 6, 6, 'v')
f(g, 2, 18, 20, 21); g[19][3] = 'S'; f(g, 5, 12, 20, 20, '}')
pit(g, 20, 13, 18); g[21][15] = g[21][16] = 'F'; f(g, 14, 17, 8, 9)
f(g, 19, 37, 21, 21, '^')
f(g, 20, 27, 13, 14); f(g, 20, 27, 13, 13, '{'); f(g, 20, 27, 15, 15, 'v')
f(g, 32, 37, 13, 21); g[11][37] = g[12][37] = 'E'
night('N14', 'Tailwind', 'Let the belt throw you into the air.', g,
      via=[[11, 19], [15, 12], [22, 12], [34, 12]])

# N15 Night Lift: saws that only hurt if you jump off the lift
g = G(); frame(g); f(g, 2, 37, 2, 21)
f(g, 2, 9, 18, 20, ' '); g[20][3] = 'S'
f(g, 10, 14, 3, 20, ' ')
g[15][10] = 'o'; g[11][14] = 'o'; g[7][10] = 'o'
f(g, 15, 37, 3, 5, ' '); pit(g, 6, 20, 23); pit(g, 6, 28, 31); f(g, 15, 37, 7, 7, '#')
g[4][37] = g[5][37] = 'E'
night('N15', 'Night Lift', 'Stand still and ride. The saws pass you by.', g,
      plats=[{"a": [11, 20], "b": [11, 3], "t": 240}],
      via=[[6, 20], [12, 12], [12, 4], [25, 5], [36, 5]])

# N16 Off Beat: springs through breaker plugs
g = G(); frame(g)
f(g, 2, 37, 20, 21); g[19][3] = 'S'
f(g, 2, 37, 12, 14); f(g, 7, 9, 12, 14, 'B'); f(g, 10, 37, 19, 19, '^'); g[19][8] = 'T'; f(g, 5, 6, 19, 19, '^')
f(g, 2, 37, 4, 6); f(g, 24, 26, 4, 6, 'R'); g[11][25] = 'T'; pit(g, 12, 14, 18)
f(g, 2, 37, 2, 3, ' '); g[2][37] = g[3][37] = 'E'
night('N16', 'Off Beat', 'Spring when the plug above you is open, then dash up.', g,
      via=[[8, 16], [8, 10], [25, 10], [25, 3], [36, 3]])
