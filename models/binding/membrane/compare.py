"""compare.py — the ONLY importer of targets.py (BUILD-SPEC §2). Appends the comparison table. Implementer: Grace (Claude Opus 5.5)."""
import json,os
import targets as T
def table(fb):
    meas={'D':2.224566,'T':T.BE_T,'He3':T.BE_HE3,'He4':28.29566}
    L=["| nucleus | setting | BE model (MeV) | BE measured | miss | R_ch classical (fm) | R_ch measured |","|---|---|---|---|---|---|---|"]
    for tag,rows in fb.items():
        for nuc,r in rows.items():
            m=meas[nuc]; L.append(f"| {nuc} | {tag} | {r['BE']:.3f} | {m:.3f} | {100*(r['BE']/m-1):+.1f} % | {r['Rch']:.3f} | {T.RCH[nuc]:.3f} |")
    return "\n".join(L)
