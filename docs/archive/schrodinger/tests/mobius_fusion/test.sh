#!/bin/sh

python3 mobius_fusion.py --grid 220 220 --plane A-E \
  --Amin 0 --Amax 1 --Emin 0 --Emax 1 \
  --A-thresh 0.4 --hysteresis 0.05 --opp-helicity \
  --E0c 0.9 --wEc 0.35 --bmaxc 0.25 --smaxc 0.30 \
  --cell-trials 1000 \
  --basin basin_AE_capsid.png --chaos chaos_AE_capsid.png \
  --prob-capsid P_caps_AE.png --grid-csv grid_AE_caps.csv
