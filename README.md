# Fire Escape

Ein schwerer 2D-Plattformer im Browser. Der Turm wird heute Nacht abgerissen und du stehst noch im 12. Stock.
Zwölf Etagen nach unten, und weil die Straßentür verkettet ist, danach zwölf Kellergeschosse bis zum Fluss.
Jede Etage hat genau ein grünes Notausgangsschild und einen versteckten goldenen Bauhelm.
Stacheln, Sägen und der Abgrund schicken dich zurück zur letzten Checkpoint-Fahne.

Alles steckt in einer einzigen Datei: `index.html` im Browser öffnen und losspielen. Keine Installation, kein Build.

## Steuerung

| Tastatur | Gamepad | Touch | Aktion |
|---|---|---|---|
| ← → / A D | Stick, Steuerkreuz | linke Bildschirmhälfte | laufen |
| Leertaste / Z | A, Y | rechte Bildschirmhälfte | springen (kurz tippen = kleiner Hüpfer, halten = hoch) |
| X / Shift | B, X, RB, RT | Dash-Knopf | Dash in 8 Richtungen (ab Etage 10) |
| R | Select | – | zurück zur letzten Checkpoint-Fahne |
| Esc / P | Start | II | Pause: Etage neu starten, überspringen, Ton |
| M | – | – | Ton an/aus |

- **Wandsprung:** an einer Wand noch einmal springen.
- **Super:** während eines Dashes am Boden springen – der Sprung behält das Dash-Tempo.
  Schräg nach unten in den Boden dashen und dann springen ergibt einen flacheren, schnelleren **Hyper**.
- **Goldene Bauhelme:** einer pro Etage, meist abseits des Wegs. Er zählt, wenn du damit den Ausgang erreichst.
- **Etagen-Auswahl** auf dem Titelbildschirm: jede erreichte Etage einzeln üben, mit Bestzeit und Helm.
- Fortschritt, Helme und Bestzeiten speichert der Browser (localStorage).
- **Versteckter Entwickler-Modus:** fünfmal schnell auf den Titel „Fire Escape“ tippen (oder auf dem Titelbildschirm
  `dev` tippen). Dann sind alle Etagen offen, im Pausenmenü gibt es „Skip floor“ auch beim Üben und
  „Next checkpoint“, und **N** überspringt eine Etage. Nochmal fünfmal tippen schaltet ihn aus.

## Etagen

| Etage | Name | Neu |
|---|---|---|
| 12 | Roof Access | Springen, Stachel-Decken |
| 11 | Elevator Shaft | Wandsprünge |
| 10 | Open Plan | Dash, Super |
| 9 | Rotten Floor | morsche Bretter, die nachgeben |
| 8 | Machine Shop | Sägen auf Schienen |
| 7 | Break Room | gelbe Funken füllen den Dash in der Luft auf |
| 6 | Gym | Sprungfedern |
| 5 | Scaffolding | Gerüstbretter, durch die man von unten springt; kreisende Sägen |
| 4 | Ventilation | enge Schächte |
| 3 | Collapse | nichts unter den Füßen |
| 2 | Atrium | alles zusammen |
| 1 | Lobby | das Finale des Turms |
| B1 | Loading Dock | Förderbänder |
| B2 | Parking Level | fahrende Lastenaufzüge |
| B3 | Boiler Room | Ventilatoren mit Aufwind |
| B4 | Breaker Room | Schaltblöcke (pink und blau wechseln im Takt) |
| B5 | Freight Elevator | Aufzüge im Takt, kreisende Säge |
| B6 | Laundry | Bänder, Sägen, morsche Bretter |
| B7 | Air Handling | Luftschächte mit Stacheln, rechtzeitig seitlich raus |
| B8 | Cold Storage | Sprungfedern unter Schaltblock-Decken |
| B9 | Server Room | Bänder ziehen zurück, während man auf den Takt wartet |
| B10 | Sewer Access | Aufzüge über dem Nichts, Aufwind Richtung Stacheln |
| B11 | Pump Station | alles auf einer Etage |
| B12 | Outfall | Finale, drei Ebenen bis zum Fluss |

## Level bearbeiten

Die Etagen stehen als ASCII-Karten (40 × 23 Kacheln) in `tools/levels.txt`; die Legende steht oben in der Datei.
Die Kellergeschosse werden aus `tools/design/basement_*.py` erzeugt (Hilfsfunktionen statt Handarbeit).
Nach einer Änderung:

```sh
python3 tools/build_levels.py   # schreibt die Level in index.html
tools/check.sh                  # prüft jede Etage mit dem Bot
```

Die Werkzeuge laufen mit `gjs` (bei Fedora/GNOME dabei), Node wird nicht gebraucht.

- `tools/solve.js` – ein Bot sucht mit genau der Physik des Spiels einen Weg zum Ausgang. `MAP=1` zeichnet den
  gefundenen Weg in die Karte, `CPS=1` prüft zusätzlich ab jeder Checkpoint-Fahne.
- `HUMAN=1` lässt den Bot wie ein ordentlicher Mensch spielen statt perfekt: keine Gnadenframes an Kanten, jeder
  Sprung mindestens 5 Frames vor der Kante, Landung mit mindestens 4 px Fuß auf der Plattform, Gefahren 2 px größer.
  `tools/check.sh` verlangt, dass jede Etage so schaffbar ist – vom Start und von jedem Checkpoint.
- `HAT=1` zählt nur Durchläufe, die unterwegs den goldenen Helm einsammeln.
- `via:` in `levels.txt` gibt dem Bot Wegpunkte in der gedachten Reihenfolge; das Spiel ignoriert sie.
- `tools/window.js` misst für Sprünge ohne Dash, wie viele Frames Spielraum beim Absprung bleiben.
