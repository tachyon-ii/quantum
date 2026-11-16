"""berry/bmt.py — the geometric phase for a MASSIVE spin-1/2 carrier (owed item of BERRY-ring-chirality.md §5).
Thomas-BMT on a prescribed closed path at constant speed. For a force perpendicular to v the spin's angular velocity is
   Omega_s = lam * (beta x beta_dot)/beta^2      (the velocity direction's own angular velocity, times lam)
   magnetic bending (B perp v):  lam_M = 1 + a*gamma
   electric bending (E perp v):  lam_E = 1 - 1/gamma + a*gamma*beta^2
   no torque (pure Thomas; non-EM constraint or g=0 in the rest frame):  lam_T = -(gamma-1)
[derived from T-BMT, Jackson 11.170; checked below by direct integration of the full T-BMT equation on the circle.]
Spinor holonomy U in SU(2) accumulated as a quaternion; 'return' = Re(U) = cos(Theta/2): -1 antiperiodic (spinor), +1 periodic.
Sources: gamma = (m_n-m_p)/m_e (kernel/data.py); a_e = 0.00115965218 (CODATA). Grace (Claude Fable 5.2), 17 Nov 2026."""
import numpy as np,sys,os
sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','kernel'))
import data as D
AE=0.00115965218; GAM=(D.MN-D.MP)/D.ME; BET=np.sqrt(1-1/GAM**2)
def qmul(p,q):
    return np.array([p[0]*q[0]-p[1:]@q[1:],*(p[0]*q[1:]+q[0]*p[1:]+np.cross(p[1:],q[1:]))])
def holonomy(r,lam):
    dr=np.roll(r,-1,0)-r; T=dr/np.linalg.norm(dr,axis=1)[:,None]; U=np.array([1.,0,0,0])
    for i in range(len(T)):
        a,b=T[i],T[(i+1)%len(T)]; ax=np.cross(a,b); s=np.linalg.norm(ax)
        if s<1e-15: continue
        th=lam*np.arctan2(s,a@b); U=qmul(np.r_[np.cos(th/2),np.sin(th/2)*ax/s],U)
    return U
def ring(A,k,hand=1,n=40001):
    t=np.linspace(0,2*np.pi,n)[:-1]; rho=1+A*np.cos(k*t)
    return np.c_[rho*np.cos(t),rho*np.sin(t),hand*A*np.sin(k*t)]
def tbmt_circle(gam,a,mode,n=200000):
    """direct integration of the full T-BMT equation on a circle (unit e/m, R=1); returns lab spin rotation per turn / 2pi."""
    b=np.sqrt(1-1/gam**2); w=b; dt=2*np.pi/w/n; S=np.array([1.,0,0]); ang=0.0
    for i in range(n):
        th=w*(i+0.5)*dt; bv=b*np.array([-np.sin(th),np.cos(th),0]); acc=-b*w*np.array([np.cos(th),np.sin(th),0])
        if mode=='M': Bf=gam*np.cross(acc,bv)/b**2; Ef=np.zeros(3)
        else: Ef=gam*acc; Bf=np.zeros(3)
        Om=-((a+1/gam)*Bf-(a*gam/(gam+1))*(bv@Bf)*bv-(a+1/(gam+1))*np.cross(bv,Ef))
        ang+=Om[2]*dt
    return ang/(2*np.pi)
if __name__=='__main__':
    print(f"gamma={GAM:.5f} beta={BET:.5f} a_e={AE}")
    print("\n# 1. check of the lam formulas against direct T-BMT integration (circle): rotation of S per turn / 2pi")
    for gam in (1.05,2.0,GAM,10.0):
        for a in (0.0,AE):
            print(f"  gamma={gam:7.4f} a={a:.5f}: magnetic {tbmt_circle(gam,a,'M'):+.6f} (formula {1+a*gam:+.6f}) | electric {tbmt_circle(gam,a,'E'):+.6f} (formula {1-1/gam+a*gam*(1-1/gam**2):+.6f}) | Thomas-only formula {-(gam-1):+.6f}")
    print("\n# 2. planar circle at c': spinor return Re(U) (-1 = antiperiodic)")
    C=ring(0,1)
    for nm,lam in (('photon / Rytov (lam=1)',1.0),('magnetic, g=2 exactly',1.0),('magnetic, g=2(1+a_e)',1+AE*GAM),('electric, g=2',1-1/GAM),('electric, g=2(1+a_e)',1-1/GAM+AE*GAM*BET**2),('Thomas only',-(GAM-1))):
        U=holonomy(C,lam); print(f"  {nm:28s} lam={lam:+.6f}  rotation/2pi={lam:+.6f}  spinor phase/pi={lam%2:.6f}  Re(U)={U[0]:+.6f}")
    print("  speeds at which electric / Thomas-only bending would be exactly antiperiodic: electric needs 1-1/gamma odd -> never (<1); Thomas needs gamma-1 odd -> gamma=2 (beta=0.8660), 4, ...")
    print("\n# 3. twisted rings (k,1) amplitude A: rotation angle Theta/2pi of the holonomy, lam=1 and lam=1+a_e*gamma")
    lamM=1+AE*GAM
    for k in (1,2,3):
        for A in (0.0,0.02,0.05,0.1,0.15,0.2,0.3):
            r=ring(A,k); U1=holonomy(r,1.0); U2=holonomy(r,lamM); U3=holonomy(ring(A,k,-1),lamM)
            th=lambda U:2*np.arccos(np.clip(U[0],-1,1))/(2*np.pi)
            print(f"  k={k} A={A:4.2f}: lam=1 Theta/2pi={th(U1):.6f} Re(U)={U1[0]:+.7f} | lam_M: Theta/2pi={th(U2):.6f} Re(U)={U2[0]:+.7f} (mirror {U3[0]:+.7f}) axis.z={U2[3]/max(np.linalg.norm(U2[1:]),1e-12):+.3f}")
    print(f"\n  detuning on the planar ring from the anomaly: a_e*gamma = {AE*GAM:.6f} turns = {2*np.pi*AE*GAM:.5f} rad; alpha*gamma/(2pi) = {GAM/137.035999/(2*np.pi):.6f}")
    # 4. Koide / Brannen
    me,mm,mt=0.51099895,105.6583755,1776.93; s=np.sqrt([me,mm,mt]); Q=(me+mm+mt)/s.sum()**2
    mu=s.sum()/3; c=(s/mu-1)/np.sqrt(2); 
    # solve delta: c_k = cos(delta + 2 pi k/3) for the three masses (tau k=0)
    dl=np.arccos(np.clip(c[2],-1,1)); 
    print(f"\n# 4. Koide Q={Q:.7f} (2/3={2/3:.7f}); Brannen: mu^2={mu**2:.4f} MeV, delta={dl:.6f} rad (2/9={2/9:.6f}); residuals cos: {[round(float(np.cos(dl+2*np.pi*k/3)-c[2-k if k else 2]),6) for k in (0,)]}")
    for k,nm in ((0,'tau'),(1,'e'),(2,'mu')):
        print(f"   {nm}: mu^2 (1+sqrt2 cos(delta+2pi k/3))^2 = {mu**2*(1+np.sqrt(2)*np.cos(dl+2*np.pi*k/3))**2:.5f}")
    # tau mass predicted from e, mu with Q=2/3
    from scipy.optimize import brentq
    f=lambda x:(me+mm+x)/(np.sqrt(me)+np.sqrt(mm)+np.sqrt(x))**2-2/3
    print(f"   m_tau from (e, mu, Q=2/3): {brentq(f,1000,3000):.3f} MeV (measured 1776.93 +- 0.09)")
    print(f"   AC/DC: <(sqrt m - mean)^2>/mean^2 = {np.var(s)/mu**2:.6f}  (Q=2/3 <=> exactly 1: equal power in the constant and the oscillating part)")
