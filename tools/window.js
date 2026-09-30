// Measures how forgiving single no-dash jumps are, the way a person does them.
// Run: gjs tools/window.js ROOM "row,from0,from1,to0,to1,dir" ...
//   row: tile row you stand on; from0-from1 / to0-to1: tile columns of the take-off and landing
//   platforms; dir: -1 left, 1 right.
// For every take-off frame and jump-hold length it simulates: start already running at the back of
// the take-off platform, hold the direction, press jump, release after `hold` frames.
// "window" = the most take-off frames that work for every hold within ±2 frames of some hold length.
// Rough reading: 1-2 frames is frame perfect, 3-4 is very hard, 6+ is fair for a hard game.
const GLib = imports.gi.GLib;
const html = new TextDecoder().decode(GLib.file_get_contents(GLib.getenv('GAME') || 'index.html')[1]);
const block = n => html.split('/*' + n + '*/')[1].split('/*END ' + n + '*/')[0];
const { Engine: E, LEVELS } = new Function(block('ENGINE') + block('LEVELS') + ';return {Engine, LEVELS};')();

const [roomArg, ...segs] = ARGV;
const R = E.buildRoom(LEVELS[+roomArg - 1]), TS = E.TS, K = E.K;

function trial(seg, jumpAt, hold) {
  const [row, f0, f1, t0, t1, dir] = seg;
  const s = E.initState(R), p = s.p;
  p.y = row * TS - K.ph; p.x = dir > 0 ? f0 * TS : (f1 + 1) * TS - K.pw;
  p.vx = dir * K.run; p.face = dir; p.pj = false; p.g = true;
  let air = false;
  for (let f = 0; f < 150; f++) {
    const jump = f >= jumpAt && f < jumpAt + hold;
    const res = E.step(R, s, { x: dir, y: 0, jump, dash: false });
    if (res === E.DEAD) return false;
    if (!p.g) air = true;
    else if (air) {
      const c0 = Math.floor(p.x / TS), c1 = Math.floor((p.x + K.pw - 1) / TS);
      return p.y + K.ph === row * TS && c1 >= t0 && c0 <= t1;
    }
    if (res === E.WIN) return true;
  }
  return false;
}

for (const str of segs) {
  const seg = str.split(',').map(Number);
  const ok = [];
  for (let h = 1; h <= 40; h++) { ok[h] = new Set(); for (let a = 0; a < 90; a++) if (trial(seg, a, h)) ok[h].add(a); }
  let best = 0, bestH = 0;
  for (let h0 = 3; h0 <= 38; h0++) {
    let n = 0;
    for (const a of ok[h0]) { let all = true; for (let h = h0 - 2; h <= h0 + 2; h++) if (!ok[h].has(a)) all = false; if (all) n++; }
    if (n > best) { best = n; bestH = h0; }
  }
  const any = ok.reduce((m, set) => Math.max(m, set ? set.size : 0), 0);
  print(`${str}: window ${best} frames (hold ~${bestH}), best single hold ${any} frames`);
}
