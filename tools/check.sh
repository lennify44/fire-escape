#!/bin/bash
# Fairness check per floor: the bot must clear it playing like a decent human (HUMAN=1: no edge grace,
# jumps at least 5 frames before an edge, lands with 4 px of foot, hazards 2 px bigger), from the start
# and from every checkpoint, and must also manage it with the gold hard hat (HAT=1).
# Usage: tools/check.sh 1,3,5   (defaults to every floor). Runs in parallel.
cd "$(dirname "$0")/.."
rooms=${1:-$(seq -s, 1 $(grep -c '^= ' tools/levels.txt))}
budget=${BUDGET:-800000}
one() {
  HUMAN=1 CPS=1 timeout 1500 gjs tools/solve.js $1 3 $budget 3 | sed 's/, [0-9]* nodes.*//;s/ after [0-9]* nodes ([0-9]* ms)//'
  HUMAN=1 HAT=1 timeout 1500 gjs tools/solve.js $1 3 $budget 3 | sed 's/, [0-9]* nodes.*//;s/ after [0-9]* nodes ([0-9]* ms)//'
}
export -f one; export budget
echo "$rooms" | tr ',' '\n' | xargs -P 8 -I{} bash -c 'one {}' | sort -n
