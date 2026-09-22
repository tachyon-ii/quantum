# convert_fitsidi_to_uvfits.py  (CASA6, pip build)
# Usage:
#   python convert_fitsidi_to_uvfits.py \
#     --fits-glob "/Users/.../E17B06.[0-3].bin0000.source0000.FITS" \
#     --out uvfits_hi_e17b06 --datacol corrected

import argparse, os, glob, shutil
from casatasks import importfitsidi, exportuvfits

ap = argparse.ArgumentParser()
ap.add_argument("--fits-glob", required=True, help="glob of FITS-IDI files")
ap.add_argument("--out", default="uvfits", help="output directory for UVFITS")
ap.add_argument("--datacol", default="corrected", choices=["corrected","data"],
                help="MS column to export (use 'data' if no CORRECTED column)")
args = ap.parse_args()

os.makedirs(args.out, exist_ok=True)
files = sorted(glob.glob(args.fits_glob))
print(f"[INFO] {len(files)} FITS-IDI files to convert")

for i, f in enumerate(files, 1):
    base = os.path.basename(f).rsplit(".", 1)[0]
    ms   = os.path.join(args.out, base + ".ms")
    uv   = os.path.join(args.out, base + ".uvfits")
    if os.path.exists(uv):
        print(f"[SKIP {i}] {uv} exists"); continue

    print(f"[{i}/{len(files)}] import FITS-IDI -> MS : {f}")
    # CASA6 pip: no 'usescratch' kw
    importfitsidi(fitsidifile=f, vis=ms)

    print(f"[{i}/{len(files)}] export MS -> UVFITS : {uv}")
    exportuvfits(vis=ms, fitsfile=uv, datacolumn=args.datacol)

    # optional: remove MS to save space
    shutil.rmtree(ms, ignore_errors=True)

print("[DONE] conversion complete")

