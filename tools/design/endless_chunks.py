"""Deep Basement (endless mode) pieces. Run from the repo root: python3 tools/design/endless_chunks.py
Writes the /*ENDLESS*/ block of index.html. Each piece is 8 columns wide and covers rows 10-21 (12 strings).
Rule for every piece: columns 0 and 7 are open in rows 10-19 and solid floor in rows 20-21, so pieces join on flat
ground and the player can always stop between two pieces. Saws/lifts use the piece's own columns and the room's rows."""
import json, pathlib, re, sys

P = []
def piece(tier, name, rows, saws=None, plats=None):
    rows = [r.replace('.', ' ') for r in rows]
    assert len(rows) == 12, (name, len(rows))
    for r in rows: assert len(r) == 8, (name, r)
    for i, r in enumerate(rows):
        for c in (0, 7):
            want = '#' if i >= 10 else ' '
            assert r[c] == want, (name, i, c, r)
    P.append({'t': tier, 'n': name, 'm': rows, **({'saws': saws} if saws else {}), **({'plats': plats} if plats else {})})

E = '........'
FL = '########'
# tier 1: one simple thing
piece(1, 'pit3',    [E] * 10 + ['##...###', '##^^^###'])
piece(1, 'step',    [E] * 8 + ['...##...', '...##...', FL, FL])
piece(1, 'saw',     [E] * 9 + ['....o...', FL, FL])
piece(1, 'spikes',  [E] * 9 + ['..^^^^..', FL, FL])
piece(1, 'planks',  [E] * 10 + ['#..==..#', '#^^^^^^#'])
piece(1, 'springwall', [E] * 4 + ['....##..'] * 5 + ['..T.##..', FL, FL])
piece(1, 'ledge',   [E] * 8 + ['....###.', '....###.', '#...####', '#^^^####'])
# tier 2: one hard thing
piece(2, 'pit6',    [E] * 10 + ['#......#', '#^^^^^^#'])
piece(2, 'lowpit',  ['.######.'] * 6 + ['.vvvvvv.', E, E, E, '##....##', '##^^^^##'])
piece(2, 'wall',    [E] * 4 + ['...^^...'] + ['...##...'] * 5 + [FL, FL])
piece(2, 'sawrail', [E] * 10 + ['##....##', '##^^^^##'], saws=[{"a": [3.5, 14], "b": [3.5, 18], "t": 60}])
piece(2, 'beltpit', [E] * 10 + ['#{{{...#', '####^^^#'])
piece(2, 'fan',     [E] * 2 + ['..####..'] * 2 + [E] * 6 + ['#......#', '#^^FF^^#'])
piece(2, 'beat',    ['.######.'] * 6 + ['.vvvvvv.', E, '.....BB.', '..RR....', '#......#', '#^^^^^^#'])
piece(2, 'sparkwall', ['.....^^.'] + ['.....##.'] * 3 + ['...*.##.'] + ['.....##.'] * 5 + ['######.#'.replace('.#', '##'), FL])
# tier 3: combinations
piece(3, 'hyper',   ['.######.'] * 7 + ['.vvvvvv.', E, E, '##....##', '##^^^^##'])
piece(3, 'lift',    ['.######.'] * 6 + ['.vvvvvv.', E, E, E, '#......#', '#^^^^^^#'], plats=[{"a": [1, 19], "b": [4, 19], "t": 240}])
piece(3, 'sawpair', [E] * 7 + ['..o.....', E, '.....o..', FL, FL])
piece(3, 'crumbleclimb', [E] * 6 + ['....==..', E, '..==....', E, '#......#', '#^^^^^^#'])
piece(3, 'sparkpit', ['.######.'] * 6 + ['.vvvvvv.', E, '...*....', E, '#......#', '#^^^^^^#'])
piece(3, 'gatebelt', [E] * 7 + ['...B....', '...B....', '...B..o.', '#}}}}}}#', FL])

block = '/*ENDLESS*/\n' + '''// Deep Basement: endless rooms put together from 8-column pieces. Room n always comes out the same.
const Endless = (() => {
  const PIECES = ''' + json.dumps(P, separators=(',', ':')) + ''';
  const NAMES = ['Drain', 'Cistern', 'Boiler Annex', 'Cable Vault', 'Old Tunnel', 'Pump Pit', 'Sump', 'Coal Cellar', 'Valve Room', 'Crawlspace', 'Overflow', 'Storm Drain', 'Root Cellar', 'Bedrock'];
  const rng = a => () => { a |= 0; a = a + 0x6d2b79f5 | 0; let t = Math.imul(a ^ a >>> 15, 1 | a); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; };
  // which tiers room n may use, and how often: deeper rooms lean on the harder pieces
  function tiers(n) {
    if (n <= 3) return [1, 1, 1];
    if (n <= 8) return [1, 1, 2];
    if (n <= 15) return [1, 2, 2, 3];
    if (n <= 25) return [2, 2, 3, 3];
    return [2, 3, 3, 3];
  }
  function assemble(list, n, name, hint) {
    const map = [], saws = [], plats = [];
    for (let r = 0; r < 23; r++) {
      if (r < 2 || r === 22) { map.push('#'.repeat(40)); continue; }
      let row = '##';
      if (r < 10) row += ' '.repeat(36);
      else {
        row += r === 19 ? ' S ' : r >= 20 ? '###' : '   ';
        for (const p of list) row += p.m[r - 10];
        row += r === 18 || r === 19 ? 'E' : r >= 20 ? '#' : ' ';
      }
      map.push(row + '##');
    }
    list.forEach((p, k) => {
      const dx = 5 + 8 * k, shift = q => [q[0] + dx, q[1]];
      for (const s of p.saws || []) saws.push({ ...s, a: shift(s.a), b: shift(s.b) });
      for (const m of p.plats || []) plats.push({ ...m, a: shift(m.a), b: shift(m.b) });
    });
    return { floor: 'B' + (12 + n), name, hint, map, saws, plats, endless: true };
  }
  function room(n) {
    const r = rng(n * 7919 + 101), pool = tiers(n), list = [];
    while (list.length < 4) {
      const t = pool[Math.floor(r() * pool.length)], options = PIECES.filter(p => p.t === t && !list.includes(p));
      list.push(options[Math.floor(r() * options.length)]);
    }
    return assemble(list, n, NAMES[(n - 1) % NAMES.length], n === 1 ? 'The stairs keep going down. How deep can you get?' : '');
  }
  // one piece between flat floor, for checking pieces on their own
  function pieceRoom(i) {
    const flat = { m: Array(10).fill('        ').concat(['########', '########']) };
    return assemble([flat, PIECES[i], flat, flat], 0, PIECES[i].n, '');
  }
  return { room, pieceRoom, PIECES };
})();
/*END ENDLESS*/'''
p = pathlib.Path('index.html'); s = p.read_text()
if '/*ENDLESS*/' in s:
    s = re.sub(r'/\*ENDLESS\*/.*?/\*END ENDLESS\*/', lambda m: block, s, flags=re.S)
else:
    s = s.replace('/*END LEVELS*/\n</script>\n', '/*END LEVELS*/\n</script>\n\n<script>\n' + block + '\n</script>\n', 1)
p.write_text(s)
print(len(P), 'pieces written', {t: sum(1 for x in P if x['t'] == t) for t in (1, 2, 3)})
