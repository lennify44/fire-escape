"""Legacy floors L1-L4 (rooms 25-28). Run from the repo root: python3 tools/design/legacy_a.py"""
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
def room(text):
    return [r.ljust(40) for r in text.strip('\n').split('\n')]

# L1 Foundry Gate: belts against you, a spiked shaft, and a low spiked ceiling on the way back
put(24, 'L1 | Foundry Gate | The old works. Mind the ceiling: a full jump is too much up here.', room('''
########################################
########################################
##vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv    ##
##                                    ##
##E                     K             ##
##E                         C         ##
#####}}}}}      {{{{{{      ######    ##
#####^^^^^^^^^^^#########^^^^######   ##
#################################>   <##
#################################>   <##
#################################    <##
#################################    <##
#################################--  <##
#################################>    ##
##    vvvvvvvvvvvvvvvvvvvvvvvv###>    ##
##                           v###>    ##
##                            ###     ##
##                            ###     ##
##                                    ##
## S                               C  ##
######{{{{{     ##     }}}}}   #########
###########^^^^^##^^^^^#####^^^#########
########################################
'''), via=[[17, 18], [35, 18], [34, 11], [36, 4], [29, 4], [10, 4], [3, 5]])

# L2 Coal Chute: rotten planks under a spiked ceiling, then a long drop past saws and a low tunnel home
g = G(); frame(g)
f(g, 2, 37, 2, 21)
f(g, 2, 30, 2, 5, ' '); f(g, 7, 23, 2, 2, 'v'); g[5][3] = 'S'
pit(g, 6, 5, 22)
for c in (8, 12, 16, 20): g[6][c] = '='
f(g, 25, 30, 6, 17, ' ')                                       # the chute
f(g, 25, 25, 8, 9, '>'); f(g, 30, 30, 11, 12, '<'); f(g, 25, 25, 14, 15, '>')
f(g, 2, 37, 18, 20, ' '); f(g, 2, 24, 17, 17, ' '); f(g, 31, 37, 17, 17, ' ')
f(g, 2, 24, 17, 17, 'v'); f(g, 31, 35, 17, 17, 'v')            # low tunnel
for c0, c1 in ((5, 7), (10, 12), (15, 17), (20, 22)): f(g, c0, c1, 21, 21, '^')
g[20][27] = 'C'
f(g, 31, 35, 21, 21, '^'); g[20][37] = 'K'
g[19][2] = g[20][2] = 'E'
put(25, 'L2 | Coal Chute | Down the chute. Steer while you fall; the saws do not wait.', g,
    saws=[{"a": [26, 10], "b": [29, 10], "t": 90}, {"a": [29, 15], "b": [26, 15], "t": 90, "ph": 0.5},
          {"a": [8, 19], "b": [16, 19], "t": 150}],
    via=[[22, 5], [27, 9], [27, 16], [27, 20], [13, 20], [3, 20]])

# L3 Pressure Line: updrafts into a spiked ceiling; get off the air at the right height, between saws
g = G(); frame(g)
f(g, 2, 37, 20, 21); g[19][3] = 'S'
f(g, 6, 37, 2, 2, 'v')
pit(g, 20, 5, 7); g[21][6] = 'F'                               # fan 1
f(g, 8, 11, 7, 19)                                             # pillar A
pit(g, 20, 12, 14); g[21][13] = 'F'                            # fan 2, a saw rides it up and down
f(g, 15, 18, 6, 19); g[5][16] = 'C'                            # pillar B
pit(g, 20, 19, 21); g[21][20] = 'F'                            # fan 3
f(g, 22, 24, 10, 19)                                           # pillar C
pit(g, 20, 25, 32); g[21][28] = 'F'                            # fan 4 over a wide pit
f(g, 33, 37, 8, 21); g[6][37] = g[7][37] = 'E'
g[11][33] = g[12][33] = g[13][33] = '<'
g[4][27] = 'K'
put(26, 'L3 | Pressure Line | Ride each updraft only as far as you need. The ceiling is waiting.', g,
    saws=[{"a": [13, 9], "b": [13, 17], "t": 100}, {"a": [19, 5], "b": [21, 5], "t": 60},
          {"o": [28, 11], "rad": 2, "t": 120, "n": 2}, {"a": [25, 6], "b": [31, 6], "t": 160}],
    via=[[6, 12], [10, 6], [13, 9], [16, 5], [20, 7], [23, 9], [28, 14], [35, 7]])

# L4 Turbine Hall: lifts carry you through orbiting saws over a spiked floor
g = G(); frame(g)
f(g, 2, 37, 21, 21, '^')
f(g, 2, 4, 14, 21); g[13][3] = 'S'
f(g, 21, 23, 10, 11); g[9][22] = 'C'; f(g, 21, 23, 12, 12, 'v')
f(g, 34, 37, 9, 21); g[7][37] = g[8][37] = 'E'
f(g, 2, 37, 2, 2, 'v')
g[6][13] = 'K'
put(27, 'L4 | Turbine Hall | The lifts go through the turbines. Pick the gap, not the lift.', g,
    saws=[{"o": [11, 13], "rad": 2.2, "t": 150, "n": 2}, {"a": [16, 4], "b": [16, 12], "t": 120},
          {"o": [28, 9], "rad": 2.5, "t": 180, "n": 3, "ccw": 1}],
    plats=[{"a": [5, 14], "b": [13, 14], "t": 300}, {"a": [18, 17], "b": [18, 8], "t": 240, "ph": 0.25},
           {"a": [24, 13], "b": [31, 13], "t": 240}],
    via=[[7, 13], [14, 13], [18, 10], [22, 9], [26, 12], [33, 10], [36, 8]])
