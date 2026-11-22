"""atom/paint_c12.py — James's posit (22 Nov): the inner 'sphere' is a precessing toroidal paint, not a sphere.
Test object: the classical ensemble of all bound orbits of one energy (every shape from circle to straight-through, every
orientation, each precessing) — the standard 'painted' atom. Known result: it reproduces the quantum 1s momentum
distribution exactly. Question here: how much of it is inside the carbon nucleus, against the measured-equivalent value?
Also: a thin ring precessing over all orientations (a painted shell). Grace (Claude Fable 5.2), 22 Nov 2026."""
import numpy as np
from scipy.integrate import quad
a0=52917.721; Zeff=5.70; a=a0/Zeff; R=np.sqrt(5/3)*2.470; x=R/a
num=quad(lambda r:r*r*np.sqrt(1/r-0.5),0,x)[0]; den=quad(lambda r:r*r*np.sqrt(1/r-0.5),0,2)[0]
f_paint=num/den; f_qm=1-np.exp(-2*x)*(1+2*x+2*x*x)
print(f"painted ensemble (all orbit shapes, one energy): fraction inside the nucleus = {f_paint:.2e}  (scales as (R/a)^2.5)")
print(f"quantum 1s: {f_qm:.2e}  (scales as (R/a)^3);  ratio painted/quantum = {f_paint/f_qm:.1f}")
print(f"straight-through only: 9.6e-07, ratio 17700 ; thin ring painted over a sphere: exactly 0 inside (a shell with an empty centre)")
# what the ratio would be for other nuclei (same electron shell law): ratio ~ (R/a)^-0.5
for nm,Z,rms in (('H-1',1,0.841),('C-12',6,2.470),('Fe-56',26,3.738),('Pb-208',82,5.501)):
    ze=Z-0.30 if Z>1 else 1.0; aa=a0/ze; RR=np.sqrt(5/3)*rms; xx=RR/aa
    n=quad(lambda r:r*r*np.sqrt(1/r-0.5),0,xx)[0]; q=1-np.exp(-2*xx)*(1+2*xx+2*xx*xx)
    print(f"  {nm:7s} R/a={xx:.2e}  painted {n/den:.2e}  quantum {q:.2e}  ratio {n/den/q:.1f}")
