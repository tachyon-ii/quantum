#!/bin/bash
# Builds docset.md for the DeepMind review from the files in MANIFEST.md. Run from QUANTUM/.
set -e
OUT=review/deepmind-2026-10-15/docset.md
FILES=(
  review/deepmind-2026-10-15/BRIEF.md
  docs/README.md
  "docs/Φ-a-minimal-ontology-of-an-emergent-universe.v2.md"
  "docs/Φ-canon-integrated.md"
  docs/three-term-binding.md
  docs/the-fractal-nucleus.md
  docs/the-turtle-conjecture.md
  docs/fable-freeman-fractal-conjecture.md
  todo/falsifiers-2026-10-15.md
  todo/docs-review-2026-10-10.md
  todo/schrodinger-salvage-2026-10-10.md
  models/turtle/stiffness_ratio.py
  models/turtle/funnel_conform.py
  scripts/paintball.pl
)
{
  echo "# Φ ontology — review docset (GENERATED $(date -u +%Y-%m-%dT%H:%MZ); do not edit — sources listed in MANIFEST.md)"
  echo
  for f in "${FILES[@]}"; do
    echo; echo; echo "<!-- ======================================================================= -->"
    echo "<!-- FILE: $f -->"
    echo "<!-- ======================================================================= -->"; echo
    case "$f" in
      *.py|*.pl) echo '```'; cat "$f"; echo '```' ;;
      *) cat "$f" ;;
    esac
  done
} > "$OUT"
wc -lc "$OUT"
# transport variants: the Gemini app has choked on one large .md — a .txt copy and four parts
cp "$OUT" "${OUT%.md}.txt"
python3 - "$OUT" <<'PY'
import sys,re
p=sys.argv[1]; s=open(p).read()
blocks=re.split(r'(?=\n\n\n<!-- =+ -->\n<!-- FILE: )',s)
n=4; size=len(s)//n; parts=[[]]; cur=0
for b in blocks:
    if cur>size and len(parts)<n: parts.append([]); cur=0
    parts[-1].append(b); cur+=len(b)
for i,pb in enumerate(parts,1):
    body=''.join(pb)
    hdr=f"# Φ ontology review docset — PART {i} of {len(parts)} (same content as docset.md, split for transport; read all parts before Task 1)\n"
    open(p.replace('docset.md',f'docset-part{i}.txt'),'w').write(hdr+body)
    print(f'part{i}: {len(body)} chars')
PY
