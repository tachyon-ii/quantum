"""kernel/lanes_report.py — the whole rule scan from results/lanes_*.json (R4': report written by code). Grace, 17 Nov 2026."""
import json,os,numpy as np,data as D
from lanes import NUC,RULES
HERE=os.path.dirname(os.path.abspath(__file__)); R={n:json.load(open(os.path.join(HERE,'results',f'lanes_{n}.json'))) for n in NUC if os.path.exists(os.path.join(HERE,'results',f'lanes_{n}.json'))}
THR={'He5':('He4',None),'Li5':('He4',None),'Be8':('He4','He4'),'B9':('Be8',None),'He6':('He4',None),'Li6':('He4','D'),'Li7':('He4','T'),'Be7':('He4','He3'),'Be9':('Be8',None),'Li8':('Li7',None),'B8':('Be7',None),'Be10':('Be9',None),'B10':('Li6','He4'),'B11':('Li7','He4'),'C11':('Be7','He4'),'C12':('Be8','He4')}
HOLES={'He5':-0.89,'Li5':-1.97,'Be8':-0.092,'B9':-0.19}
bound=[n for n in R if n not in HOLES and n not in ('D','T','He3','He4')]
L=[]
for sg in ('singles refused','singles counted'):
    L.append(f"\n### {sg}: predicted BE (MeV) and miss; lowest-threshold separation energy S in brackets for the holes\n")
    L.append("| nucleus | measured | "+" | ".join(r[0] for r in RULES)+" |"); L.append("|---|---|"+"---|"*len(RULES))
    score={r[0]:[] for r in RULES}; holes_ok={r[0]:0 for r in RULES}; bound_ok={r[0]:0 for r in RULES}
    for n,v in R.items():
        row=f"| {n}{' (hole)' if n in HOLES else ''} | {v['meas']:.2f} |"
        for r in RULES:
            k=f"{r[0]} | {sg}"; E=v['best'][k][0]; cell=f" {E:.2f} ({100*(E/v['meas']-1):+.1f} %)"
            if n in THR:
                a,b=THR[n]; thr=R[a]['best'][k][0]+(R[b]['best'][k][0] if b else 0); S=E-thr
                cell+=f" [S={S:+.2f}]"
                if n in HOLES: holes_ok[r[0]]+= S<=1e-9
                else: bound_ok[r[0]]+= S>1e-9
            if n in bound: score[r[0]].append(100*(E/v['meas']-1))
            row+=cell+" |"
        L.append(row)
    L.append("| **rms miss, bound A ≥ 6** | |"+"|".join(f" **{np.sqrt(np.mean(np.square(score[r[0]]))):.1f} %** (mean {np.mean(score[r[0]]):+.1f})" for r in RULES)+" |")
    L.append(f"| **holes kept unbound (of {len(HOLES)})** | |"+"|".join(f" {holes_ok[r[0]]}" for r in RULES)+" |")
    L.append(f"| **bound nuclei bound vs lowest threshold (of {len([n for n in bound if n in THR])})** | |"+"|".join(f" {bound_ok[r[0]]}" for r in RULES)+" |")
L.append("\n### What the data require of the attachment: (BE_measured − BE_model['none', singles refused]) / u — the count each rule has to produce\n")
L.append("| nucleus | decomposition | required ATT (units of Q_β) | best-config counts: contacts / np / triangles / touching (under the 'contacts' rule) |"); L.append("|---|---|---|---|")
from lanes import U
for n in R:
    if n in ('D','T','He3','He4'): continue
    v=R[n]; b0=v['best']['none | singles refused']; bc=v['best']['contacts | singles counted']; F=bc[1]
    L.append(f"| {n} | {b0[2]} | {(v['meas']-b0[0])/U:+.2f} | {F[0]+F[4]:.0f} / {F[1]+F[5]:.0f} / {F[2]+F[6]:.0f} / {F[3]+F[7]:.0f} |")
open(os.path.join(HERE,'results','LANES-rule-scan.md'),'w').write("\n".join(L)+"\n"); print("\n".join(L))
