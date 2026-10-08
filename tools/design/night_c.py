"""Night Shift, shift 3 (N17-N24): lights out. Run from the repo root: python3 tools/design/night_c.py"""
import sys; sys.path.insert(0, 'tools/design')
from common import G, f, frame, pit, night

# N17 Needle: hop into short spike lanes and dash through
g = G(); frame(g); f(g, 2, 37, 2, 14)
f(g, 2, 37, 20, 21); g[19][3] = 'S'
for c in (8, 15, 22):
    f(g, c, c + 1, 15, 17); f(g, c, c + 1, 18, 18, 'v'); f(g, c, c + 1, 19, 19, '^')
pit(g, 20, 27, 32); g[17][29] = '*'
g[18][37] = g[19][37] = 'E'
night('N17', 'Needle', 'Tap jump, then dash flat through the gap.', g)

# N18 Chimney Sweep: a chimney with a rotten wall
g = G(); frame(g); f(g, 2, 37, 2, 21)
f(g, 2, 16, 18, 20, ' '); g[20][3] = 'S'
f(g, 17, 19, 4, 20, ' '); f(g, 17, 17, 5, 17, '='); f(g, 16, 16, 5, 17, ' ')
f(g, 19, 19, 8, 9, '<'); f(g, 19, 19, 14, 15, '<')
f(g, 20, 37, 3, 4, ' '); g[3][37] = g[4][37] = 'E'
night('N18', 'Chimney Sweep', 'The left wall rots under your hands. Keep climbing.', g)

# N19 Spark Gap: sparks and breaker stones over nothing
g = G(); frame(g, bottom=False); f(g, 2, 37, 2, 2, 'v')
f(g, 2, 4, 12, 22); g[11][3] = 'S'
g[10][9] = '*'; f(g, 13, 14, 11, 11, 'R'); g[8][19] = '*'; f(g, 23, 24, 10, 10, 'B'); g[7][29] = '*'
f(g, 33, 37, 9, 22); g[7][37] = g[8][37] = 'E'
f(g, 16, 17, 14, 22); f(g, 16, 17, 13, 13, '^'); f(g, 26, 27, 13, 22); f(g, 26, 27, 12, 12, '^')
night('N19', 'Spark Gap', 'Sparks and breaker stones. The stones only hold on their beat.', g,
      via=[[9, 10], [13, 10, 1], [19, 8], [23, 9, 1], [29, 7], [34, 8]])

# N20 Conveyor Hell: belts, saws and a breaker gate
g = G(); frame(g); f(g, 2, 37, 2, 13); f(g, 7, 33, 14, 14, 'v')
f(g, 2, 37, 20, 21); g[19][3] = 'S'
f(g, 6, 13, 20, 20, '{'); g[19][10] = 'o'
f(g, 14, 14, 17, 19, 'B')
f(g, 15, 22, 20, 20, '}'); pit(g, 20, 23, 26); f(g, 27, 33, 20, 20, '{'); g[19][30] = 'o'
g[18][37] = g[19][37] = 'E'
night('N20', 'Conveyor Hell', 'Every belt wants something different from you.', g,
      via=[[12, 19], [16, 19], [27, 19], [36, 19]])

# N21 Updraft Maze: climb two fan tubes with spiked walls
g = G(); frame(g); f(g, 2, 37, 2, 21)
f(g, 2, 7, 18, 20, ' '); g[20][3] = 'S'
f(g, 8, 11, 6, 20, ' '); g[21][9] = g[21][10] = 'F'; f(g, 8, 11, 5, 5); 
for r in range(7, 18): g[r][8] = '>'
f(g, 12, 20, 6, 8, ' ')
f(g, 21, 24, 3, 20, ' '); g[21][22] = g[21][23] = 'F'; f(g, 21, 24, 2, 2, 'v')
for r in range(9, 21): g[r][21] = '>'
for r in range(3, 20):
    if not 11 <= r <= 13: g[r][24] = '<'
f(g, 25, 37, 11, 13, ' '); g[12][37] = g[13][37] = 'E'
night('N21', 'Updraft Maze', 'Ride the air and leave each tube through its side door.', g,
      via=[[9, 18], [10, 7], [16, 7], [22, 12], [36, 13]])

# N22 Freight: sideways lifts over nothing, with sparks between
g = G(); frame(g, bottom=False); f(g, 2, 37, 2, 2, 'v')
f(g, 2, 4, 16, 22); g[15][3] = 'S'
g[12][15] = '*'; g[9][27] = '*'
f(g, 34, 37, 7, 22); g[5][37] = g[6][37] = 'E'
night('N22', 'Freight', 'Ride, jump, dash, catch the next lift.', g,
      plats=[{"a": [6, 15], "b": [11, 15], "t": 240}, {"a": [18, 12], "b": [23, 12], "t": 240, "ph": 0.5},
             {"a": [29, 8], "b": [31, 8], "t": 240}],
      via=[[9, 14, 1], [15, 12], [20, 11, 1], [27, 9], [30, 7, 1], [35, 6]])

# N23 Overtime: spring, breaker, belt, saw, plank
g = G(); frame(g)
f(g, 2, 37, 20, 21); g[19][3] = 'S'
g[19][7] = 'T'; f(g, 5, 9, 12, 12); f(g, 7, 7, 12, 12, 'R'); f(g, 2, 37, 8, 8, 'v'); f(g, 2, 37, 2, 7)
f(g, 10, 37, 19, 19, '^')
f(g, 10, 17, 11, 12); f(g, 10, 17, 11, 11, '}'); g[10][14] = 'o'
f(g, 20, 21, 11, 11, '='); f(g, 24, 25, 11, 11, '=')
f(g, 28, 37, 11, 12); g[10][31] = 'o'; f(g, 33, 33, 8, 10, 'B')
g[9][37] = g[10][37] = 'E'; f(g, 34, 37, 8, 8, ' ')
night('N23', 'Overtime', 'One of everything. No checkpoints.', g,
      via=[[7, 10], [12, 10], [21, 10], [29, 10], [37, 10]])

# N24 Clock Out: the last run, top to bottom and back
g = G(); frame(g)
f(g, 2, 37, 7, 9); f(g, 2, 37, 15, 17)
g[6][3] = 'S'
pit(g, 7, 8, 13); f(g, 10, 10, 7, 7, '='); pit(g, 7, 17, 22); g[4][19] = '*'
f(g, 26, 26, 4, 6, 'R'); f(g, 31, 33, 7, 9, ' '); f(g, 31, 33, 8, 8, ' ')
f(g, 33, 33, 10, 14, ' ')
f(g, 34, 37, 10, 14, ' '); f(g, 31, 37, 15, 17, ' ')
f(g, 2, 30, 10, 14, ' '); pit(g, 15, 6, 28); g[16][17] = 'F'; f(g, 16, 18, 11, 11)
f(g, 2, 37, 18, 21, ' '); f(g, 2, 37, 21, 21)
f(g, 2, 3, 15, 17, ' ')
f(g, 8, 11, 21, 21, '}'); pit(g, 21, 14, 19); f(g, 24, 30, 21, 21, '{'); g[20][27] = 'o'
g[19][37] = g[20][37] = 'E'
night('N24', 'Clock Out', 'The last run of the night. Down, back, down again.', g,
      via=[[11, 6], [20, 6], [29, 6], [35, 13], [20, 12], [3, 13], [3, 19], [20, 19], [36, 20]])
