"""atom/torus_wave.py — first step of 'Schroedinger from the geometry' (James, 22 Nov): the spread.
Object: ONE closed winding (torus) for the inner electron, fixed by whole-number-plus-a-half conditions on its two
circuits (Einstein 1917; Keller 1958; Langer 1937):   radial circuit: (0 + 1/2) h ;  angular circuit: (0 + 1/2) hbar.
 (i)  where does the PATH go?  -> classical turning points; the path never enters the hole.
 (ii) carry a phase round the winding and demand it be continuous across the edge of the hole (standard connection rule):
      what presence does that give INSIDE the hole, at the nucleus?  Compare with the exact Schroedinger value.
Units: orbit scale a = a0/Z_eff = 1, hbar = m = 1, E = -1/2. No fitted number. Grace (Claude Fable 5.2), 22 Nov 2026."""
import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq
E=-0.5
def run(Lang):
    k2=lambda r:2*(E+1/r)-Lang**2/r**2
    r1=brentq(k2,1e-9,1.0); r2=brentq(k2,1.0,5.0)
    Jr=quad(lambda r:np.sqrt(max(k2(r),0)),r1,r2)[0]/np.pi          # radial action / h  (should be 1/2)
    half=quad(lambda r:1/np.sqrt(max(k2(r),1e-300)),r1,r2,limit=400)[0]  # = half period
    C2=2/half                                                        # normalisation: int u^2 dr = (C^2/2) * half = 1
    kap=lambda r:np.sqrt(-k2(r))
    def u_in(r): return np.sqrt(C2)/(2*np.sqrt(kap(r)))*np.exp(-quad(kap,r,r1,limit=400)[0])
    R0=[u_in(r)/r for r in (1e-3,3e-4,1e-4)]
    return r1,r2,Jr,R0
print("Langer torus (angular circuit = 1/2):")
r1,r2,Jr,R0=run(0.5)
print(f"  turning points {r1:.4f} and {r2:.4f} of the orbit scale; radial action = {Jr:.4f} h (condition: 0.5)")
print(f"  phase-continuous wave at the centre: R(0) = {R0[-1]:.4f} (values at r=1e-3,3e-4,1e-4: {[round(x,4) for x in R0]}); exact Schroedinger: 2.0000")
ratio=(R0[-1]/2)**2
print(f"  presence at the nucleus, this construction / exact = {ratio:.3f}")
a0=52917.721
print("\n  nucleus   hole radius (fm)   hole / nuclear radius   presence inside nucleus: path alone | with continuous phase | exact")
for nm,Z,rms in (('H-1',1,0.841),('C-12',6,2.470),('Fe-56',26,3.738),('Pb-208',82,5.501)):
    ze=Z-0.30 if Z>1 else 1.0; a=a0/ze; R=np.sqrt(5/3)*rms; x=R/a
    ex=1-np.exp(-2*x)*(1+2*x+2*x*x)
    print(f"  {nm:7s}  {r1*a:9.0f}          {r1*a/R:9.0f}            0            | {ex*ratio:.2e}            | {ex:.2e}")
print("\nFor comparison (angular circuit = 0, the straight-through path): no hole; presence 17,700 x exact in carbon (dwell_c12.py).")
print("Full painted ensemble (all shapes): 15 x exact in carbon, 60 x in hydrogen (paint_c12.py).")
