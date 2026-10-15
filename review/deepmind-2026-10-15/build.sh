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
