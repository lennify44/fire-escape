"""Records a ghost run for every story floor (from the start and from each checkpoint) and every Night Shift run,
and writes them into the /*GHOSTS*/ block of index.html. Run from the repo root after any level or physics change:
  python3 tools/ghosts.py
Ghosts come from tools/solve.js with GHOSTSAFE=1 (keeps clear of hazards, same physics as the game) and are only
kept if they replay to the exit under the game's normal physics."""
import json, pathlib, re, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, 'tools')
from add_rooms import load

_, rooms = load()
env = {'GHOST': '1', 'GHOSTSAFE': '1', 'CPS': '1', 'PATH': '/usr/bin:/bin'}

def record(i):
    out = subprocess.run(['gjs', 'tools/solve.js', str(i + 1), '3', '1500000', '3'], env=env,
                         capture_output=True, text=True, timeout=3600).stdout
    return out

with ThreadPoolExecutor(8) as pool:
    outs = list(pool.map(record, range(len(rooms))))

ghosts, missing = {}, []
for i, out in enumerate(outs):
    label = rooms[i]['head'].split('|')[0].strip()
    for line in out.splitlines():
        if line.startswith('GHOST '):
            _, floor, cp, enc = line.split(' ', 3)
            ghosts.setdefault(floor, {})[cp] = enc
        elif line.startswith('GHOST-DIVERGED') or 'NOT SOLVED' in line:
            missing.append(f'{label}: {line.strip()}')

block = '/*GHOSTS*/\n// Recorded by tools/ghosts.py: per floor label, per start point (-1 = start, 0.. = checkpoint), run-length\n' \
        '// encoded inputs (one letter per input combination, then how many frames it is held).\nconst GHOSTS = ' + \
        json.dumps(ghosts, separators=(',', ':')) + ';\n/*END GHOSTS*/'
p = pathlib.Path('index.html'); s = p.read_text()
if '/*GHOSTS*/' in s:
    s = re.sub(r'/\*GHOSTS\*/.*?/\*END GHOSTS\*/', lambda m: block, s, flags=re.S)
else:
    s = s.replace('/*END ENDLESS*/\n</script>\n', '/*END ENDLESS*/\n</script>\n\n<script>\n' + block + '\n</script>\n', 1)
p.write_text(s)
print(f'{sum(len(v) for v in ghosts.values())} ghost runs for {len(ghosts)} floors, {len(block) // 1024} KB')
for m in missing: print('no ghost:', m)
