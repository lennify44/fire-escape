// Parses every inline <script> in index.html so a typo shows up before a browser does. Run: gjs tools/syntax.js
const GLib = imports.gi.GLib;
const html = new TextDecoder().decode(GLib.file_get_contents('index.html')[1]);
let bad = 0;
[...html.matchAll(/<script>([\s\S]*?)<\/script>/g)].forEach((m, i) => {
  try { new Function(m[1]); print(`script ${i}: ok (${m[1].length} chars)`); } catch (e) { bad++; print(`script ${i}: ${e}`); }
});
if (bad) imports.system.exit(1);
