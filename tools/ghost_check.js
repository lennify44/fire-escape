// Replays every ghost stored in index.html through the engine exactly as the game does and checks it reaches the exit.
// Run: gjs tools/ghost_check.js
const GLib = imports.gi.GLib;
const html = new TextDecoder().decode(GLib.file_get_contents('index.html')[1]);
const block = n => html.split('/*' + n + '*/')[1].split('/*END ' + n + '*/')[0];
const { Engine: E, LEVELS, GHOSTS } = new Function(block('ENGINE') + block('LEVELS') + block('GHOSTS') + ';return {Engine, LEVELS, GHOSTS};')();
const CH = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJ';
let ok = 0, bad = [];
for (const def of LEVELS) {
  const R = E.buildRoom(def), runs = GHOSTS[def.floor] || {};
  for (const cp of ['-1', ...R.checks.map((_, i) => String(i))]) {
    if (!runs[cp]) { bad.push(`${def.floor} from ${cp}: missing`); continue; }
    const s = E.initState(R, +cp); let r = 0, frames = 0;
    for (const m of runs[cp].matchAll(/([a-zA-J])(\d+)/g)) {
      const c = CH.indexOf(m[1]), inp = { x: Math.floor(c / 12) - 1, y: Math.floor(c % 12 / 4) - 1, jump: !!(c & 2), dash: !!(c & 1) };
      for (let k = 0; k < +m[2] && !r; k++) { r = E.step(R, s, inp); frames++; }
    }
    if (r === E.WIN) ok++; else bad.push(`${def.floor} from ${cp}: ${r === E.DEAD ? 'dies' : 'stops short'} after ${frames} frames`);
  }
}
print(`${ok} ghost runs reach the exit`);
bad.forEach(b => print('  ' + b));
if (bad.length) imports.system.exit(1);
