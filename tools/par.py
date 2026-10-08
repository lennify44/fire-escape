"""Sets the gold time (par) of every Night Shift run from the human-mode bot's time, plus 25%, rounded up to half a second.
Run from the repo root: python3 tools/par.py  (then python3 tools/build_levels.py)"""
import math, re, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, 'tools')
from add_rooms import load, put

head, rooms = load()
night = [(i, r) for i, r in enumerate(rooms) if r['head'].strip().startswith('N')]

def solve(i):
    out = subprocess.run(['gjs', 'tools/solve.js', str(i + 1), '3', '1000000', '3'], env={'HUMAN': '1', 'PATH': '/usr/bin:/bin'},
                         capture_output=True, text=True, timeout=1800).stdout
    m = re.search(r'solved in ([\d.]+) s', out)
    return float(m.group(1)) if m else None

with ThreadPoolExecutor(8) as pool:
    times = list(pool.map(solve, [i for i, _ in night]))

for (i, r), t in zip(night, times):
    parts = [p.strip() for p in r['head'].split('|')]
    label = parts[0]
    if t is None:
        print(f'{label}: human-mode bot did not finish, par left as is')
        continue
    par = math.ceil(t * 1.25 * 2) / 2  # 25% slack over a perfectly executed human-mode route
    parts = [p for p in parts if not p.startswith('par=')] + [f'par={par}']
    put(i, ' | '.join(parts), r['rows'], r['saws'], r['plats'], r['via'])
    print(f'{label}: bot {t:.2f} s -> gold {par:.1f} s')
