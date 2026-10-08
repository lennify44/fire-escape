"""Night Shift, shift 1 (N1-N8): movement basics. Run from the repo root: python3 tools/design/night_a.py"""
import sys; sys.path.insert(0, 'tools/design')
from common import G, f, frame, pit, night

# N1 Punch In: pits and a ledge
g = G(); frame(g)
f(g, 2, 37, 2, 12); f(g, 13, 22, 13, 14); f(g, 13, 22, 15, 15, 'v')
f(g, 2, 37, 20, 21); pit(g, 20, 8, 10); pit(g, 15, 18, 0) if False else pit(g, 20, 15, 18); pit(g, 20, 23, 27)
f(g, 31, 37, 17, 21); g[19][3] = 'S'; g[15][37] = g[16][37] = 'E'
night('N1', 'Punch In', 'Short runs, one screen, no checkpoints. Beat the gold time.', g)

# N2 Stairwell: spiked chimney
g = G(); frame(g); f(g, 2, 37, 2, 21)
f(g, 2, 16, 17, 20, ' '); g[20][4] = 'S'
f(g, 17, 19, 3, 20, ' ')
f(g, 17, 17, 12, 13, '>'); f(g, 19, 19, 8, 9, '<'); f(g, 19, 19, 15, 16, '<'); f(g, 17, 17, 5, 6, '>')
f(g, 20, 37, 3, 5, ' '); g[4][37] = g[5][37] = 'E'
night('N2', 'Stairwell', 'Kick off one wall, then the other.', g)

# N3 Long Jump: dash gaps of 7, 8 and 9
g = G(); frame(g); f(g, 2, 37, 2, 11)
f(g, 2, 37, 20, 21); pit(g, 20, 7, 13); pit(g, 20, 16, 23); pit(g, 20, 26, 34)
g[19][3] = 'S'; g[18][37] = g[19][37] = 'E'
night('N3', 'Long Jump', 'Jump first, dash at the top.', g)

# N4 Hyper Line: a ceiling too low for a normal jump
g = G(); frame(g); f(g, 2, 37, 2, 16); f(g, 2, 37, 17, 17, 'v')
f(g, 2, 37, 20, 21); pit(g, 20, 10, 16); pit(g, 20, 22, 28)
g[19][3] = 'S'; g[18][37] = g[19][37] = 'E'
night('N4', 'Hyper Line', 'Dash down-forward into the floor, then jump: low, fast and long.', g)

# N5 Bounce House: springs up to the roof
g = G(); frame(g)
f(g, 2, 4, 20, 21); f(g, 5, 37, 21, 21, '^'); g[19][3] = 'S'
f(g, 8, 8, 20, 21); g[19][8] = 'T'
f(g, 11, 14, 14, 14); g[13][13] = 'T'; f(g, 11, 14, 15, 15, 'v')
f(g, 16, 20, 9, 9); g[8][19] = 'T'; f(g, 16, 20, 10, 10, 'v')
f(g, 23, 27, 5, 5); f(g, 23, 27, 6, 6, 'v')
f(g, 31, 37, 5, 5); g[3][37] = g[4][37] = 'E'
night('N5', 'Bounce House', 'Springs fire you straight up. Steer on the way.', g)

# N6 Rotten Bridge: planks under a low ceiling
g = G(); frame(g); f(g, 2, 37, 2, 15); f(g, 6, 33, 16, 16, 'v')
f(g, 2, 5, 20, 21); f(g, 6, 33, 21, 21, '^'); g[19][3] = 'S'
for c in (8, 11, 14, 17, 21, 22, 26, 30): g[19][c] = '='
f(g, 34, 37, 20, 21); g[18][37] = g[19][37] = 'E'
night('N6', 'Rotten Bridge', 'Do not stop on the planks.', g)

# N7 Sparks: refills over nothing
g = G(); frame(g, bottom=False)
f(g, 2, 4, 12, 22); g[11][3] = 'S'
for c, r in ((8, 10), (13, 8), (18, 11), (23, 7), (28, 10), (33, 8)): g[r][c] = '*'
f(g, 10, 11, 2, 5); f(g, 10, 11, 6, 6, 'v'); f(g, 20, 21, 2, 4); f(g, 20, 21, 5, 5, 'v')
f(g, 15, 16, 15, 22); f(g, 15, 16, 14, 14, '^'); f(g, 25, 26, 14, 22); f(g, 25, 26, 13, 13, '^')
f(g, 30, 31, 15, 22); f(g, 30, 31, 14, 14, '^')
f(g, 35, 37, 10, 22); g[8][37] = g[9][37] = 'E'
night('N7', 'Sparks', 'Each spark gives the dash back.', g)

# N8 Clock Check: shift 1 in one room
g = G(); frame(g); f(g, 2, 37, 2, 21)
f(g, 2, 5, 17, 20, ' '); g[20][3] = 'S'
f(g, 6, 8, 9, 20, ' '); f(g, 6, 6, 13, 14, '>'); f(g, 8, 8, 16, 17, '<')
f(g, 6, 37, 4, 8, ' ')
pit(g, 9, 12, 24)
for c in (14, 17, 20, 23): g[9][c] = '='
g[8][27] = 'T'
pit(g, 9, 29, 33); g[6][31] = '*'
g[7][37] = g[8][37] = 'E'
night('N8', 'Clock Check', 'Everything from this shift, in one room.', g)
