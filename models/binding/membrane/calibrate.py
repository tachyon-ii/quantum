"""calibrate.py — BUILD-SPEC §4.2-4.3. Implementer: Grace (Claude Opus 5.5).
Exploits exact scaling: with Coulomb excluded, every term is proportional to E0 at fixed r = e0*A0p/E0 (A0p = 4 pi RP^2),
so the D and He-4 contact energies are E0*f_D(r) and E0*f_He(r) + Coulomb.  Step 1: scan f_He/f_D over r at each delta.
Step 2: if the required ratio is bracketed, root-find r and set E0 from D; else report 'no calibration'.
Usage: python3 calibrate.py <delta_index> [subdiv]   (one delta per call; appends to results/calibration.json)
NOTE: superseded for the production scan by jobs.py + calscan.py (resumable); kept for contact_energy() and targets_contact()."""
import sys,json,os,time,numpy as np
import constants as K
from energy import System, E_MESH
from relax import relax
HERE=os.path.dirname(os.path.abspath(__file__)); OUT=os.path.join(HERE,'results','calibration.json')
A0P=4*np.pi*K.RP**2
from builders import geom   # one definition of the starting geometries (DRY)
STARTS=[1.70,1.55,1.40]   # fm, multi-start contact distances (declared); lowest energy kept
def contact_energy(name,r,delta,E0=1.0,subdiv=K.SUBDIV,x0=None,starts=STARTS,**kw):
    best=None
    for a in ([None] if x0 is not None else starts):
        sp,cs=geom(name,a) if a else geom(name); S=System(sp,cs,r*E0/A0P,E0,delta,subdiv=subdiv,**kw)
        x,res=relax(S,x0); be,p=S.binding(x)
        if best is None or p['cont']<best[3]['cont']: best=(S,x,be,p,res)
    return best
def targets_contact():
    """required contact energies (continuous part, Coulomb excluded), MeV — built only from calibration data."""
    D=-(K.BE_D-2*K.Y(2))
    He=-(K.BE_HE4+2*E_MESH()-4*K.Y(4))      # 2 singlet pairs (nn, pp) in He-4
    return D,He
R_GRID=[1,3,10,30,100,300,1000]
if __name__=='__main__':
    di=int(sys.argv[1]); sub=int(sys.argv[2]) if len(sys.argv)>2 else K.SUBDIV
    delta=K.DELTA_GRID[di]; tD,tHe=targets_contact()
    db=json.load(open(OUT)) if os.path.exists(OUT) else {}
    key=f"delta={delta:.4f}_sub{sub}"; rec=db.get(key,{'delta':delta,'subdiv':sub,'scan':[]})
    done={row['r'] for row in rec['scan']}
    t0=time.time()
    for r in R_GRID:
        if r in done: continue
        if time.time()-t0>400: break
        _,_,_,pD,rD=contact_energy('D',r,delta,subdiv=sub)
        _,_,_,pH,rH=contact_energy('He4',r,delta,subdiv=sub)
        fD=pD['cont']; fH=pH['cont']-pH['coul']
        rec['scan'].append(dict(r=r,fD=fD,fHe=fH,ratio=fH/fD,per_contact=fH/fD/6,nitD=int(rD.nit),nitHe=int(rH.nit),
                                msgHe=str(rH.message)[:40],contactsHe=len(pH['contacts'])))
        print(f"{key} r={r:6g} fD={fD:+.4f} fHe={fH:+.4f} ratio={fH/fD:6.3f} per-contact={fH/fD/6:5.3f} ({time.time()-t0:.0f}s)",flush=True)
    rec['required_ratio']=tHe/tD; rec['required_per_contact']=tHe/tD/6
    rs=sorted(rec['scan'],key=lambda z:z['r']); rec['scan']=rs
    rat=[z['ratio'] for z in rs]
    rec['max_ratio_seen']=max(rat) if rat else None
    rec['bracketed']=bool(rat and min(rat)<=tHe/tD<=max(rat))
    db[key]=rec; json.dump(db,open(OUT,'w'),indent=1)
    print(f"required ratio {tHe/tD:.3f} (per contact {tHe/tD/6:.3f}); max seen {rec['max_ratio_seen']}; bracketed={rec['bracketed']}")
