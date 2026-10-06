// Proves each room in index.html is beatable by searching over held inputs with the game's own engine.
// Run: gjs tools/solve.js [room|all] [framesPerAction=3] [maxNodes=1500000] [weight=3]
const GLib = imports.gi.GLib;
const here = GLib.get_current_dir();
const htmlPath = GLib.getenv('GAME') || here + '/index.html';
const html = new TextDecoder().decode(GLib.file_get_contents(htmlPath)[1]);
if (GLib.getenv('NODASH')) globalThis.NODASH = 1;
const block = n => html.split('/*' + n + '*/')[1].split('/*END ' + n + '*/')[0];
const { Engine: E, LEVELS } = new Function(block('ENGINE') + block('LEVELS') + ';return {Engine, LEVELS};')();

// NERF=0.03 scales run, jump, wall-jump, dash and spring speeds down by 3%; HZ=2 grows hazards by 2px.
// A room that still solves under a small nerf has slack; one that fails a bigger nerf is tight.
const nerf = +(GLib.getenv('NERF') || 0);
for (const k of ['run', 'jump', 'wjV', 'wjH', 'dashV', 'dashEnd', 'spring']) E.K[k] *= 1 - nerf;
E.K.hz = +(GLib.getenv('HZ') || 0);
for (const kv of (GLib.getenv('KSET') || '').split(',').filter(Boolean)) { const [k, v] = kv.split('='); E.K[k] = +v; }
// HUMAN=1 plays like a decent person instead of a perfect one: no coyote frames, jumps at least 5 frames
// before the edge, lands with at least 4 px of foot on the platform, hazards 2 px bigger, wall kicks from 2 px.
const LAND = GLib.getenv('HUMAN') ? 4 : 0;
if (GLib.getenv('HUMAN')) Object.assign(E.K, { coyote: 1, edge: 5, wjReach: 2, hz: E.K.hz + 2 });
for (const kv of (GLib.getenv('KSET2') || '').split(',').filter(Boolean)) { const [k, v] = kv.split('='); E.K[k] = +v; }
// SLOP=2 (on by default with HUMAN=1, SLOP=0 turns it off): no input has to be frame perfect. Every time the bot
// presses or releases jump, starts a dash or changes direction, the same change is also played SLOP frames early
// and SLOP frames late. Such a sloppy copy keeps the planned inputs, except that after SLOP_REACT frames it may
// steer left or right back towards the planned line, the way a person corrects in the air; a jump or dash that went
// off at the wrong moment cannot be taken back. Each copy has to stay alive until it is back on its feet (or
// SLOP_LIFE frames pass), or the move does not count.
// TIGHT=1 searches without SLOP, then replays the route it found and prints each move that would fail it.
const TIGHT = !!GLib.getenv('TIGHT');
let SLOP = TIGHT ? 0 : +(GLib.getenv('SLOP') ?? (GLib.getenv('HUMAN') ? 2 : 0));
const SLOP_REACT = 8, SLOP_LIFE = 60, SLOP_GROUND = 20, SLOP_MAX = 8;
function footing(R, s) {
  const p = s.p, y = p.y + E.K.ph, r = Math.floor(y / 16);
  let n = 0;
  for (let x = p.x; x < p.x + E.K.pw; x++) { const t = E.tile(R, s, Math.floor(x / 16), r); if (t === 1 || t === 2) n++; }
  if (p.pl >= 0) { const b = E.platsAt(R, s.f)[p.pl]; n = Math.max(n, Math.min(p.x + E.K.pw, b.x + b.w) - Math.max(p.x, b.x)); }
  return n;
}
const [which = 'all', kArg = '3', maxArg = '1500000', wArg = '3'] = ARGV;
const KF = +kArg, MAX = +maxArg, W = +wArg;

class Heap {
  constructor() { this.a = []; }
  push(n) { const a = this.a; a.push(n); let i = a.length - 1; while (i) { const j = (i - 1) >> 1; if (a[j].f <= n.f) break; a[i] = a[j]; i = j; } a[i] = n; }
  pop() {
    const a = this.a, top = a[0], last = a.pop();
    if (a.length) { let i = 0; for (;;) { let c = 2 * i + 1; if (c >= a.length) break; if (c + 1 < a.length && a[c + 1].f < a[c].f) c++; if (a[c].f >= last.f) break; a[i] = a[c]; i = c; } a[i] = last; }
    return top;
  }
  get size() { return this.a.length; }
}

// Tile distance (through anything that isn't a plain wall) from every tile to the target rectangle
function distField(R, ex) {
  const d = new Float32Array(E.COLS * E.ROWS).fill(1e9), q = [];
  for (let r = Math.floor(ex.y / 16); r < (ex.y + ex.h) / 16; r++) for (let c = Math.floor(ex.x / 16); c < (ex.x + ex.w) / 16; c++) { d[r * E.COLS + c] = 0; q.push(r * E.COLS + c); }
  for (let h = 0; h < q.length; h++) {
    const i = q[h], c = i % E.COLS, r = (i / E.COLS) | 0;
    for (const [dc, dr] of [[1, 0], [-1, 0], [0, 1], [0, -1]]) {
      const c2 = c + dc, r2 = r + dr;
      if (c2 < 0 || c2 >= E.COLS || r2 < 0 || r2 >= E.ROWS) continue;
      const j = r2 * E.COLS + c2;
      if (R.g[j] === 1 || d[j] <= d[i] + 1) continue;
      d[j] = d[i] + 1; q.push(j);
    }
  }
  return d;
}

const BASE = [];
for (const x of [-1, 0, 1]) for (const jump of [false, true]) BASE.push({ x, y: 0, jump, dash: false });
const WAIT = { x: 0, y: 0, jump: false, dash: false, frames: 15 }; // stand still through a beat or a saw pass
const DASHES = [];
for (const y of [-1, 0, 1]) for (const x of [-1, 0, 1]) if (x || y) DASHES.push({ x, y, jump: false, dash: true });

function key(R, s) {
  const p = s.p;
  let k = (p.x >> 1) + ',' + (p.y >> 1) + ',' + Math.round(p.vx / 20) + ',' + Math.round(p.vy / 30) + ',' + p.dash + p.dt + ',' + p.fo + (p.co ? 'c' : '') + (p.jb ? 'b' : '') + (p.pj ? 'j' : '') + (p.cut ? 'u' : '');
  for (const v of s.cr) k += v ? (v <= E.K.crumble ? 'a' : 'g' + ((v - E.K.crumble) / 40 | 0)) : '.';
  for (const v of s.ob) k += v ? 'x' + (v / 50 | 0) : 'o';
  // time matters when things move; breaker rooms use coarser buckets so waiting for a beat stays affordable
  if (R.period > 1) k += '@' + ((s.f % R.period) / (R.toggles ? 15 : 6) | 0);
  return k + (s.got ? 'K' : '') + (p.pl >= 0 ? 'P' + p.pl : '');
}

// Sloppy copies of the run (see SLOP): {s, age, air}. Plays action a on copy c, steering towards x = tx once it
// has had time to react; returns -1 dead, 1 safe again, 0 still pending.
const len = a => a.frames || KF;
function advance(R, c, a, n = len(a), tx = null) {
  for (let k = 0; k < n; k++) {
    const d = tx === null || a.dash || c.age < SLOP_REACT ? 0 : tx - c.s.p.x;
    const res = E.step(R, c.s, Math.abs(d) > 1 ? { ...a, x: Math.sign(d) } : a);
    if (res === E.DEAD) return -1;
    if (res === E.WIN || ++c.age >= SLOP_LIFE) return 1;
    if (!c.s.p.g) c.air = true;
    else if (c.air || c.age >= SLOP_GROUND) return 1;
  }
  return 0;
}
const changed = (prev, a) => prev && (a.x !== prev.x || a.jump !== prev.jump || (a.dash && !prev.dash));
// The copies a child inherits from node after action a, plus new ones if a changes the input; null if one dies.
function sloppy(R, node, a, s) {
  const prev = node.act, out = [], same = key(R, s);
  const keep = c => { if (key(R, c.s) !== same) out.push(c); };
  for (const sh of node.sh) {
    const c = { s: E.cloneState(sh.s), age: sh.age, air: sh.air }, r = advance(R, c, a, len(a), s.p.x);
    if (r < 0) return null;
    if (!r) keep(c);
  }
  if (changed(prev, a)) {
    const late = { s: E.cloneState(node.s), age: 0, air: false };
    let r = advance(R, late, prev, SLOP);
    if (!r) r = advance(R, late, a, len(a) - SLOP, s.p.x);
    if (r < 0) return null;
    if (!r) keep(late);
    if (node.parent && len(prev) >= SLOP) {
      const early = { s: E.cloneState(node.parent.s), age: 0, air: false };
      for (let k = 0; k < len(prev) - SLOP; k++) E.step(R, early.s, prev);
      r = advance(R, early, a, len(a) + SLOP, s.p.x);
      if (r < 0) return null;
      if (!r) keep(early);
    }
  }
  out.sort((x, y) => x.age - y.age);
  return out.slice(0, SLOP_MAX);
}

function solve(idx, cp = -1) {
  const def = LEVELS[idx], R = E.buildRoom(def), dist = distField(R, R.exit);
  // HAT=1: only a clear that picked up the gold hard hat on the way counts
  const wantHat = GLib.getenv('HAT') && R.hat, hatDist = wantHat && distField(R, R.hat);
  const hatToExit = wantHat && dist[Math.floor((R.hat.y + 5) / 16) * E.COLS + Math.floor((R.hat.x + 5) / 16)];
  if (GLib.getenv('HAT') && !R.hat) { print(`${idx + 1}. ${def.name}: no hat on this floor`); return true; }
  // Waypoints (via) steer the search along the intended route: h = distance to the next one + the rest of the chain.
  const via = (wantHat ? def.hatvia : def.via) || [];  // a hat run follows hatvia, if the floor has one
  const viaDist = via.map(([c, r]) => distField(R, { x: c * 16, y: r * 16, w: 16, h: 16 }));
  const rest = via.map((_, i) => { let sum = 0; for (let j = i; j < via.length; j++) { const [c, r] = via[j + 1] || []; sum += j + 1 < via.length ? viaDist[j + 1][via[j][1] * E.COLS + via[j][0]] : dist[via[j][1] * E.COLS + via[j][0]]; } return sum; });
  const h = (s, wp = via.length) => {
    const c = Math.floor((s.p.x + 5) / 16), r = Math.floor((s.p.y + 7) / 16);
    if (r >= E.ROWS || r < 0) return 1e6;
    if (wp < via.length) return viaDist[wp][r * E.COLS + c] + rest[wp];
    return wantHat && !s.got ? hatDist[r * E.COLS + c] + hatToExit : dist[r * E.COLS + c];
  };
  // a waypoint on the hat itself only counts once the hat is picked up
  const hatWp = wantHat ? via.findIndex(([c, r]) => c === Math.floor(R.hat.x / 16) && r === Math.floor(R.hat.y / 16)) : -1;
  const nextWp = (s, wp) => {
    while (wp < via.length) {
      if (wp === hatWp && !s.got) break;
      const c = Math.floor((s.p.x + 5) / 16), r = Math.floor((s.p.y + 7) / 16);
      if (r < 0 || r >= E.ROWS || viaDist[wp][r * E.COLS + c] > 1) break;
      wp++;
    }
    return wp;
  };
  const root = { s: E.initState(R, cp), g: 0, parent: null, act: null, wp: 0, sh: [] };
  let wp0 = 0;
  if (cp >= 0 && via.length) {
    const ck = R.checks[cp], i0 = Math.floor((ck.sy + 7) / 16) * E.COLS + Math.floor((ck.sx + 5) / 16);
    via.forEach((_, i) => { if (viaDist[i][i0] < viaDist[wp0][i0]) wp0 = i; });
  }
  root.wp = nextWp(root.s, wp0);
  root.f = h(root.s, root.wp) * W;
  const open = new Heap(), seen = new Set([key(R, root.s) + '#' + root.wp]);
  open.push(root);
  let n = 0, goal = null, best = 1e9, bestNode = root;
  const t0 = Date.now();
  while (open.size && n < MAX) {
    const node = open.pop();
    // sloppy copies are only checked for positions the search actually explores (cheaper than for every child)
    if (!node.sh) { node.sh = sloppy(R, node.parent, node.act, node.s); if (!node.sh) { seen.delete(node.kk); continue; } }
    n++;
    let acts = !globalThis.NODASH && node.s.p.dash && !node.s.p.dt ? BASE.concat(DASHES) : BASE;
    if (R.period > 1 && node.s.p.g) acts = acts.concat([WAIT]);
    for (const a of acts) {
      const s = E.cloneState(node.s);
      let res = 0;
      for (let k = 0; k < (a.frames || KF) && !res; k++) res = E.step(R, s, a);
      if (res === E.DEAD) continue;
      if (LAND && (s.ev & E.EV.LAND) && footing(R, s) < LAND) continue;
      const child = { s, g: node.g + 1, parent: node, act: a, wp: nextWp(s, node.wp), sh: SLOP ? null : [] };
      if (res === E.WIN) {
        if (wantHat && !s.got) continue;
        // the last move has to be forgiving too: its sloppy copies must reach the door as well, or at least survive
        const sh = SLOP ? sloppy(R, node, a, s) : [];
        if (!sh || !sh.every(c => { for (let k = 0; k < SLOP_LIFE; k++) { const r = E.step(R, c.s, a); if (r) return r === E.WIN; } return true; })) continue;
        goal = child; break;
      }
      const shaky = SLOP && (node.sh.length || changed(node.act, a));
      const kk = child.kk = key(R, s) + '#' + child.wp + (shaky ? '~' : '');
      if (seen.has(kk)) continue;
      seen.add(kk);
      const hv = h(s, child.wp);
      if (hv >= 1e6) continue;
      if (hv < best) { best = hv; bestNode = child; }
      child.f = child.g + hv * W;
      open.push(child);
    }
    if (goal) break;
  }
  const ms = Date.now() - t0;
  const label = `${idx + 1}. ${def.name}${cp >= 0 ? ' from checkpoint ' + (cp + 1) : ''}${wantHat ? ' with hat' : ''}`;
  if (!goal) {
    const bp = bestNode.s.p;
    print(`${label}: NOT SOLVED after ${n} nodes (${ms} ms), got furthest at column ${Math.floor((bp.x + 5) / 16)}, row ${Math.floor((bp.y + 7) / 16)}`);
    if (GLib.getenv('MAP')) {
      const trail = new Set();
      for (let x = bestNode; x; x = x.parent) trail.add(Math.floor((x.s.p.y + 7) / 16) * E.COLS + Math.floor((x.s.p.x + 5) / 16));
      print(def.map.map((l, r) => [...l.padEnd(E.COLS)].map((ch, c) => trail.has(r * E.COLS + c) && ch === ' ' ? '·' : ch).join('')).join('\n'));
    }
    return false;
  }

  const acts = [];
  for (let x = goal; x.parent; x = x.parent) acts.unshift(x.act);
  // replay to verify and trace the route
  const s = E.initState(R, cp), trail = new Set();
  let res = 0, frames = 0;
  for (const a of acts) for (let k = 0; k < (a.frames || KF) && !res; k++) {
    res = E.step(R, s, a); frames++;
    trail.add(Math.floor((s.p.y + 7) / 16) * E.COLS + Math.floor((s.p.x + 5) / 16));
  }
  const dashes = acts.filter((a, i) => a.dash && !(acts[i - 1] || {}).dash).length;
  print(`${label}: solved in ${(frames / 60).toFixed(2)} s, ${dashes} dashes, ${n} nodes (${ms} ms)${res === E.WIN ? '' : '  !! REPLAY FAILED'}`);
  if (TIGHT) {
    SLOP = +(GLib.getenv('SLOP') || 2);
    let cur = { s: E.initState(R, cp), act: null, parent: null, sh: [] }, f = 0;
    for (const a of acts) {
      const s = E.cloneState(cur.s);
      for (let k = 0; k < len(a); k++) E.step(R, s, a);
      const sh = sloppy(R, cur, a, s), p = cur.s.p;
      const was = cur.act || {}, what = a.dash ? 'dash' : a.jump && !was.jump ? 'jump' : !a.jump && was.jump ? 'release jump' : 'steer';
      const dir = [a.x < 0 ? 'left' : a.x > 0 ? 'right' : '', a.dash && a.y < 0 ? 'up' : a.dash && a.y > 0 ? 'down' : ''].filter(Boolean).join(' ');
      if (!sh) print(`  tight at ${(f / 60).toFixed(2)} s, column ${Math.floor((p.x + 5) / 16)}, row ${Math.floor((p.y + 7) / 16)}: ${what}${dir ? ' ' + dir : ''}`);
      cur = { s, act: a, parent: cur, sh: sh || [] }; f += len(a);
    }
    SLOP = 0;
  }
  if (GLib.getenv('MAP')) {
    const rows = def.map.map((l, r) => [...l.padEnd(E.COLS)].map((ch, c) => trail.has(r * E.COLS + c) && ch === ' ' ? '·' : ch).join(''));
    print(rows.join('\n'));
  }
  return res === E.WIN;
}

const list = which === 'all' ? LEVELS.map((_, i) => i) : which.split(',').map(x => +x - 1);
let ok = true;
for (const i of list) {
  // CP=2 proves the floor from its second checkpoint only
  if (GLib.getenv('CP')) { ok = solve(i, +GLib.getenv('CP') - 1) && ok; continue; }
  ok = solve(i) && ok;
  // CPS=1 also proves the floor from every checkpoint
  if (GLib.getenv('CPS')) E.buildRoom(LEVELS[i]).checks.forEach((_, c) => { ok = solve(i, c) && ok; });
}
if (!ok) imports.system.exit(1);
