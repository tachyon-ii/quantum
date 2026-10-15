# the-turtle-conjecture.md §3b — k (He-4 skin tension) against c^4/(G R_H). Grace, 2026-10-15. Run: python3 -I stiffness_ratio.py
import math
c=2.99792458e8; G=6.6743e-11; hbar=1.054571817e-34; MeV=1.602176634e-13; fm=1e-15
mp=1.67262192e-27; H0=67.4e3/3.0857e22
P=1.912  # MeV per square unit (He-4 calibration, three-term-binding §7a)
Rp=0.841 # fm charge radius
# three ways to set the truncated-octahedron edge a (library: D_SS=2.828a, D_HH=2.449a)
edges={'a from D_SS=2R_p':2*Rp/(2*math.sqrt(2)), 'a from D_HH=2R_p':2*Rp/math.sqrt(6),
       'a from saturation 0.16/fm3':(1/0.16/(8*math.sqrt(2)))**(1/3)}
print("k = P/a^2 as a surface tension")
ks={}
for n,a in edges.items():
    k=P/a**2; ks[n]=k
    print(f"  {n:28s} a={a:.3f} fm  k={k:.2f} MeV/fm^2 = {k*MeV/fm**2:.2e} N/m")
# textbook: SEMF surface term a_s A^{2/3}, area 4 pi r0^2 A^{2/3}
for a_s,r0 in [(17.8,1.2),(18.3,1.25)]:
    print(f"  SEMF a_s={a_s} r0={r0}: {a_s/(4*math.pi*r0**2):.2f} MeV/fm^2")
RH=c/H0; MU=c**3/(2*G*H0)
print(f"\nR_H={RH:.3e} m  M_U={MU:.3e} kg")
FP=c**4/G
print(f"Planck force c^4/G = {FP:.3e} N")
gU=FP/RH; gL=3*FP/(8*math.pi*RH)
print(f"c^4/(G R_H)        = {gU:.3e} N/m = {gU*fm**2/MeV:.2f} MeV/fm^2")
print(f"3c^4/(8piG R_H) [Laplace: rho c^2 = gamma/R]= {gL:.3e} N/m = {gL*fm**2/MeV:.2f} MeV/fm^2")
print("\nratios k_nuc / gamma_U:")
for n,k in ks.items():
    print(f"  {n:28s} {k*MeV/fm**2/gU:6.2f} (vs c^4/GR_H)  {k*MeV/fm**2/gL:6.2f} (vs Laplace)")
# What L makes c^4/(G k) : 
for n,k in ks.items():
    L=FP/(k*MeV/fm**2); print(f"  L=c^4/(G k): {L:.2e} m = {L/RH:.2f} R_H  [{n}]")
# Dirac check
print(f"\nG m_p^2/hbar c = {G*mp**2/(hbar*c):.3e}   R_H/lambdabar_p = {RH/(hbar/(mp*c)):.3e}")
print(f"k lambdabar_p^2/(m_p c^2) = {ks['a from saturation 0.16/fm3']*MeV*(hbar/(mp*c))**2/fm**2/(mp*c**2):.2e}")
# original ratio: k vs Planck tension
print(f"k / (E_P/l_P^2) = {ks['a from saturation 0.16/fm3']*MeV/fm**2 / (FP/math.sqrt(hbar*G/c**3)):.1e}")
