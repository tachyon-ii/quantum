"""contact/channels.py — (a) erratum check on docs/contact-patch-em.md table; (b) channel table pn/pp/nn x same/counter sense with a
neutral neutron (declared: e- and e+ antipodal on one lane, same sense); (c) potential of mean force W(g) from the retarded fields.
Grace (Claude Fable 5.2), 17 Nov 2026."""
import numpy as np,json,os
from retarded import *
def darwin_noh(g,s2,phi,q1q2,beta=B):   # Darwin WITHOUT the 1/2 (to identify the 31 Oct table)
    T=2*np.pi*R/beta; t=np.arange(NT)*T/NT
    r1,b1,_=traj(1,t,g,s2,phi,beta); r2,b2,_=traj(2,t,g,s2,phi,beta); d=r1-r2; Dn=np.linalg.norm(d,axis=-1)
    return q1q2*E2*np.mean((1-(b1*b2).sum(-1))/Dn)
print("# (a) erratum: 31 Oct table was gear -2.18/-1.66/-1.40/-1.11, belt -0.32/-0.30/-0.29/-0.26")
for g in (0.1,0.2,0.3,0.5):
    print(f"  g={g}: Darwin same-sense {darwin(g,1,0,-1):.3f} counter {darwin(g,-1,0,-1):.3f} | counter phi=pi {darwin(g,-1,np.pi,-1):.3f} same phi=pi {darwin(g,1,np.pi,-1):.3f} | no-half same {darwin_noh(g,1,0,-1):.3f} counter {darwin_noh(g,-1,0,-1):.3f}")
PROT=[(+1,0.0)]; NEUT=[(-1,0.0),(+1,np.pi)]
def chan(L1,L2,g,s2,phis):
    U=np.zeros(len(phis)); F=np.zeros(len(phis))
    for i,p in enumerate(phis):
        for q1,o1 in L1:
            for q2,o2 in L2:
                r=pair(g,s2,p+o2-s2*o1,q1*q2)   # shifting carrier 1 by o1 == shifting carrier 2 by -s2*o1 (time translation)
                U[i]+=r['Usym']; F[i]+=r['fattr']
    return U,F
phis=np.linspace(-np.pi,np.pi,25)[:-1]; out={}
print("\n# (b) channels (U_sym, MeV): min over phase / mean over phase / correlation = min-mean / phase of min")
for g in (0.1,0.3,0.5):
    for nm,L1,L2 in (('pn',PROT,NEUT),('pp',PROT,PROT),('nn',NEUT,NEUT)):
        for s2,sn in ((1,'same-sense  (anti-parallel at contact)'),(-1,'counter-sense (co-moving at contact)')):
            U,F=chan(L1,L2,g,s2,phis); i=U.argmin()
            out[f'{nm}_{s2}_{g}']=dict(U=U.tolist(),F=F.tolist())
            print(f"  g={g} {nm} {sn}: min {U.min():+.3f} mean {U.mean():+.3f} corr {U.min()-U.mean():+.3f} at phi/pi {phis[i]/np.pi:+.2f}")
print("\n# (c) mean attractive force f(g) at phi=0 and W(g) = -int_g^inf f ; pn with neutral neutron and bare e+e-")
gs=np.geomspace(0.03,60,40); res={}
for nm,L2 in (('e+e-',[(-1,0.0)]),('pn',NEUT)):
    for s2 in (1,-1):
        f=np.array([chan(PROT,L2,g,s2,[0.0])[1][0] for g in gs])
        # W(g) = -int_g^inf f dg'  (trapezoid in log g; tail beyond 60 fm dropped)
        Wg=np.array([-np.trapz(f[i:],gs[i:]) for i in range(len(gs))])
        res[(nm,s2)]=(f,Wg); out[f'W_{nm}_{s2}']=dict(g=gs.tolist(),f=f.tolist(),W=Wg.tolist())
        sel=[0,4,8,12,16,20,24,30]
        print(f"  {nm} {'same' if s2==1 else 'counter'}: "+' '.join(f"g={gs[i]:.2f}: f={f[i]:+.3f} W={Wg[i]:+.3f};" for i in sel))
json.dump(out,open('channels_results.json','w'),indent=1)
