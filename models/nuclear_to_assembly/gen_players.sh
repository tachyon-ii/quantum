#!/bin/sh
# gen_players.sh — build, score and draw every A<=4 assembly the library knows.
# Output: players/<name>.json, players/<name>.png, players/<name>.score.json, players/bond-table.md
# Why: the bond data (contacts, S-S/H-H, edges, loops) feeds docs/three-term-binding.md §5;
# regenerate rather than hand-edit (docs/agents/000, "never hand-edit a generated file").
set -e
cd "$(dirname "$0")"
export PYTHONPATH=. MPLBACKEND=Agg
T=players/bond-table.md
printf '| assembly | A | Z | N | contacts | NP | PP | NN | S-S | H-H | orth links | shear | curvature | closed loop | bad phase |\n' > $T
printf '|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|\n' >> $T
for n in d2 h3_linear h3_orth h3_tri he3_linear he3_orth he3_tri he4_cross he4_ring; do
  python3 -m nuclear_to_assembly.cli.toasm build $n -o players/$n.json >/dev/null
  python3 -m nuclear_to_assembly.cli.toasm score players/$n.json 2>/dev/null | sed -n '/^{/,$p' > players/$n.score.json
  python3 -m nuclear_to_assembly.cli.toasm viz players/$n.json --out players/$n.png --title "$n" >/dev/null
  python3 - "$n" >> $T <<'PY'
import json,sys
n=sys.argv[1]; r=json.load(open(f"players/{n}.score.json")); c=r["comprehensive"]; ch=r["channels"]; b=r["brickwork"]
contacts=c["bonds_SS"]+c["bonds_HH"]+c["bonds_SH"]
print(f"| {n} | {c['A']} | {c['Z']} | {c['N']} | {contacts} | {ch['NP']} | {ch['PP']} | {ch['NN']} | {c['bonds_SS']} | {c['bonds_HH']} | {b['orthogonal_links']} | {b['shear_penalty']} | {b['curvature_penalty']} | {c['has_closed_loop']} | {r['phase']['bad_phase_bonds']} |")
PY
done
cat $T
