"""calscan.py — reads finished calibration jobs, prints f_D, f_He, ratio vs required (BUILD-SPEC §4.3).
Implementer: Grace (Claude Opus 5.5)."""
import sys,json,os,re,numpy as np; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import jobs, constants as K
from energy import E_MESH
def required():
    tD=-(K.BE_D-2*K.Y(2)); tHe=-(K.BE_HE4+2*E_MESH()-4*K.Y(4)); return tD,tHe
def row(name):
    j=jobs.load(name)
    if not j['done']: return None
    S=jobs.build(j); be,p=S.binding(j['x'])
    return dict(cont=p['cont'],coul=p['coul'],contacts=len(p['contacts']),parts=p)
if __name__=='__main__':
    tD,tHe=required(); out={}
    names=json.load(open(sys.argv[1]))
    keys=sorted({re.sub(r'cal_(D|He4)_','',n) for n in names})
    for k in keys:
        a=row('cal_D_'+k); b=row('cal_He4_'+k)
        if not a or not b: continue
        fD=a['cont']; fH=b['cont']-b['coul']
        out[k]=dict(fD=fD,fHe=fH,ratio=fH/fD,per_contact=fH/fD/6,contactsHe=b['contacts'])
        print(f"{k:20s} fD={fD:+8.4f} fHe={fH:+8.4f} ratio={fH/fD:6.3f} per-contact={fH/fD/6:5.3f} contacts(He4)={b['contacts']}")
    print(f"required: ratio {tHe/tD:.3f}  per-contact {tHe/tD/6:.3f}  (D {tD:.4f} MeV, He-4 {tHe:.4f} MeV, Coulomb excluded)")
    json.dump(dict(rows=out,required_ratio=tHe/tD),open(os.path.join(jobs.HERE,'results','calscan.json'),'w'),indent=1)
