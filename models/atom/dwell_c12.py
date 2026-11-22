"""atom/dwell_c12.py — James's point (22 Nov): low probability at the centre could mean high speed there, not absence.
Test: a classical path straight through the nucleus (zero angular momentum, same energy as carbon's 1s) — what fraction of
its time is inside the nucleus, against the measured-equivalent (quantum) fraction? Inputs as inner_pair_c12.py. Grace, 22 Nov 2026."""
import numpy as np
from scipy.integrate import quad
a0=52917.721; Z=6; Zeff=Z-0.30; a=a0/Zeff; R=np.sqrt(5/3)*2.470
# classical radial Kepler orbit, semi-major axis a/... choose energy E = -Zeff^2 Ry -> r_max = 2a (units: a)
x=R/a
t_in=quad(lambda r:1/np.sqrt(1/r-1/2.0),0,x)[0]          # time 0->R, units sqrt(m a^3/(2 Ze^2))
T=2*quad(lambda r:1/np.sqrt(1/r-1/2.0),0,2.0)[0]         # full period (out and back)
f_cl=2*t_in/T
f_qm=1-np.exp(-2*x)*(1+2*x+2*x*x)                        # 1s probability inside r<R
print(f"R/a = {x:.3e}")
print(f"classical straight-through path: fraction of time inside the nucleus = {f_cl:.2e}   (scales as (R/a)^1.5)")
print(f"quantum 1s (what capture, conversion, hyperfine measure): {f_qm:.2e}   (scales as (R/a)^3)")
print(f"ratio classical/quantum = {f_cl/f_qm:.0f}")
b=R*np.sqrt(f_cl/f_qm)
print(f"if the path's crossing point wanders over a disc of radius b, hits are (R/b)^2 of passes: needs b = {b:.0f} fm = {b/R:.0f} nuclear radii = {b/a:.3f} of the orbit size; one pass in {f_cl/f_qm:.0f} hits")
# speed at the nuclear surface on such a path
v=np.sqrt(2*Zeff*(1/137.036)*197.327/(0.510999*R)) ; print(f"speed at the nuclear surface on that path: {v:.2f} c (non-relativistic formula; i.e. relativistic)")
