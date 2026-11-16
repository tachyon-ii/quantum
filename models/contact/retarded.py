"""contact/retarded.py — two carriers on tangent lanes with the FULL Lienard-Wiechert interaction (no v<<c expansion).
Source for every input: R_p, c' from models/kernel/data.py; e^2 = AHC. Declared quantities:
  U_ret  = q1 q2 <(1 - b1.b2)/(D kappa)>  (minus the time-averaged retarded interaction Lagrangian), 1<-2 and 2<-1 averaged
  U_sym  = (U_ret + U_adv)/2              (Fokker / Wheeler-Feynman time-symmetric)
  U_dar  = Darwin (validation against docs/contact-patch-em.md)
  f(g)   = mean attractive force along the line of centres from the full retarded E,B (velocity + acceleration fields)
  W(g)   = -int_g^inf f dg'               (potential of mean force at fixed lab-phase lock)
Phase phi: carrier 2's lag behind simultaneous arrival at the contact. Correlation energy = U(phi) - <U>_phi.
Grace (Claude Fable 5.2), 17 Nov 2026."""
import numpy as np,sys,os,json
sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','kernel'))
import data as D
R=D.RP; B=float(D.CPRIME); W0=B/R; E2=D.AHC; NT=4096
def traj(k,t,g,s2,phi,beta=B):
    w=beta/R
    if k==1: th=w*t; cx=-(R+g/2); s=1
    else: th=np.pi+s2*(w*t)+phi; cx=(R+g/2); s=s2
    r=np.stack([cx+R*np.cos(th),R*np.sin(th)],-1); b=s*beta*np.stack([-np.sin(th),np.cos(th)],-1)
    a=-beta*w*np.stack([np.cos(th),np.sin(th)],-1)
    return r,b,a
def emit_time(obs,src,t,g,s2,phi,beta,sign):
    """sign=+1 retarded (t_e<t), -1 advanced."""
    ro,_,_=traj(obs,t,g,s2,phi,beta); te=t-sign*np.linalg.norm(ro-traj(src,t,g,s2,phi,beta)[0],axis=-1)
    for _ in range(60):
        rs,bs,_=traj(src,te,g,s2,phi,beta); d=ro-rs; Dn=np.linalg.norm(d,axis=-1); n=d/Dn[:,None]
        f=t-te-sign*Dn; fp=-1+sign*(n*bs).sum(-1); te=te-f/fp
    return te
def one(obs,src,g,s2,phi,q1q2,beta=B,sign=1):
    T=2*np.pi*R/beta; t=np.arange(NT)*T/NT
    te=emit_time(obs,src,t,g,s2,phi,beta,sign)
    ro,bo,_=traj(obs,t,g,s2,phi,beta); rs,bs,as_=traj(src,te,g,s2,phi,beta)
    d=ro-rs; Dn=np.linalg.norm(d,axis=-1); n=d/Dn[:,None]; kap=1-sign*(n*bs).sum(-1)
    U=q1q2*E2*np.mean((1-(bo*bs).sum(-1))/(Dn*kap))
    if sign!=1: return U,None
    gam2=1/(1-beta**2); nb=n-bs
    Ev=nb/(gam2*kap**3*Dn**2)[:,None]
    cr=nb[:,0]*as_[:,1]-nb[:,1]*as_[:,0]                     # (n-b) x a  (z)
    Ea=np.stack([n[:,1]*cr,-n[:,0]*cr],-1)/(kap**3*Dn)[:,None]  # n x ((n-b) x a)
    E=Ev+Ea; Bz=n[:,0]*E[:,1]-n[:,1]*E[:,0]
    F=q1q2*E2*(E+np.stack([bo[:,1]*Bz,-bo[:,0]*Bz],-1))
    return U,F.mean(0)
def pair(g,s2,phi,q1q2,beta=B):
    U12,F1=one(1,2,g,s2,phi,q1q2,beta); U21,F2=one(2,1,g,s2,phi,q1q2,beta)
    A12,_=one(1,2,g,s2,phi,q1q2,beta,-1); A21,_=one(2,1,g,s2,phi,q1q2,beta,-1)
    Uret=(U12+U21)/2; Uadv=(A12+A21)/2
    return dict(Uret=Uret,Usym=(Uret+Uadv)/2,fattr=(F1[0]-F2[0])/2,F1x=F1[0],F2x=F2[0],Fy=(F1[1]+F2[1])/2)
def darwin(g,s2,phi,q1q2,beta=B):
    T=2*np.pi*R/beta; t=np.arange(NT)*T/NT
    r1,b1,_=traj(1,t,g,s2,phi,beta); r2,b2,_=traj(2,t,g,s2,phi,beta); d=r1-r2; Dn=np.linalg.norm(d,axis=-1); n=d/Dn[:,None]
    return q1q2*E2*np.mean((1-((b1*b2).sum(-1)+(b1*n).sum(-1)*(b2*n).sum(-1))/2)/Dn)
if __name__=='__main__':
    out={}
    print(f"R={R} beta={B:.4f} gamma={1/np.sqrt(1-B*B):.4f}  Larmor P = {2/3*E2*B**4/(1-B*B)**2/R**2:.1f} MeV per fm/c  (KE = {D.ME*(1/np.sqrt(1-B*B)-1):.3f} MeV)")
    # validation: static limit and Darwin table
    print("validation beta->0.01: Uret gear g=0.3 =",round(pair(0.3,1,0,-1,0.01)['Uret'],4),' static <1/D> =',round(darwin(0.3,1,0,-1,0.01),4))
    print("\n# e+ / e- (np), phi=0 :  gap | Darwin gear, belt | U_ret gear, belt | U_sym gear, belt | sym ratio")
    for g in (0.1,0.2,0.3,0.5,1.0):
        dg,db=darwin(g,1,0,-1),darwin(g,-1,0,-1); pg,pb=pair(g,1,0,-1),pair(g,-1,0,-1)
        out[f'phi0_g{g}']=dict(darwin=(dg,db),gear=pg,belt=pb)
        print(f"  {g:4.1f} | {dg:7.3f} {db:7.3f} | {pg['Uret']:7.3f} {pb['Uret']:7.3f} | {pg['Usym']:7.3f} {pb['Usym']:7.3f} | {pg['Usym']/pb['Usym']:5.2f}")
    # phase scan at g=0.3: correlation energy
    print("\n# phase scan, g=0.3: phi/pi | U_sym gear | U_sym belt   (correlation energy = U(phi) - mean over phi)")
    phis=np.linspace(-np.pi,np.pi,49)[:-1]; sc={}
    for g in (0.1,0.3,0.5):
        Ug=np.array([pair(g,1,p,-1)['Usym'] for p in phis]); Ub=np.array([pair(g,-1,p,-1)['Usym'] for p in phis])
        sc[g]=(Ug,Ub)
        ig,ib=Ug.argmin(),Ub.argmin()
        print(f"  g={g}: gear mean {Ug.mean():7.3f} min {Ug.min():7.3f} at phi/pi={phis[ig]/np.pi:+.3f}  corr(phi=0) {Ug[24]-Ug.mean():+.3f}  corr(best) {Ug.min()-Ug.mean():+.3f}")
        print(f"         belt mean {Ub.mean():7.3f} min {Ub.min():7.3f} at phi/pi={phis[ib]/np.pi:+.3f}  corr(phi=0) {Ub[24]-Ub.mean():+.3f}  corr(best) {Ub.min()-Ub.mean():+.3f}")
        # neutral neutron: e- at phi and e+ antipodal on the same lane, same sense: U(phi)-U(phi+pi)
        Ng=Ug-np.roll(Ug,24); Nb=Ub-np.roll(Ub,24)
        print(f"         neutral-neutron (e- at phi, e+ at phi+pi): gear min {Ng.min():+.3f} at {phis[Ng.argmin()]/np.pi:+.3f}; belt min {Nb.min():+.3f} at {phis[Nb.argmin()]/np.pi:+.3f}; ratio {Ng.min()/Nb.min():.2f}")
        out[f'scan_g{g}']=dict(phi=phis.tolist(),gear=Ug.tolist(),belt=Ub.tolist())
    json.dump(out,open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'retarded_results.json'),'w'),indent=1,default=float)
