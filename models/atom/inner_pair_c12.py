"""atom/inner_pair_c12.py — what the inner electron pair (1s^2) does to the carbon-12 nucleus it passes through.
Hydrogen-like 1s with Slater screening (Z_eff = Z - 0.30). Sources: CODATA constants; C-12 rms charge radius 2.470 fm
(Angeli & Marinova 2013, from memory — to be checked); nuclear incompressibility ~230 MeV (from memory).
Everything here is standard atomic physics arithmetic; nothing is fitted. Grace (Claude Fable 5.2), 22 Nov 2026."""
import numpy as np
a0=52917.721; alpha=1/137.035999; hc=197.3269804; e2=1.439964547; Ry2=27.211386  # fm, -, MeV fm, MeV fm, eV (Hartree)
Z=6; A=12; Zeff=Z-0.30; rms=2.470; R=np.sqrt(5/3)*rms
rho0=Zeff**3/(np.pi*a0**3)                      # one electron's density at the centre, fm^-3
inside=2*rho0*4/3*np.pi*R**3                    # electrons of the pair inside the nucleus at any instant
v=Zeff*alpha                                    # speed / c
t_cross=2*R/v                                   # fm/c
fmc=3.33564e-24                                 # seconds per fm/c
rate=inside/(t_cross*fmc)                       # crossings per second
T_orb=2*np.pi*(a0/Zeff)/v*fmc                   # classical 1s period, s
T_nuc=1e-22
V0=-2*Zeff*Ry2                                  # eV, potential energy of a unit + charge at the centre due to the pair
E_nuc=Z*V0                                      # eV
dE=(2*np.pi/3)*Z*e2*(2*rho0)*rms**2*1e6         # eV, finite-size (field) shift from the pair
dE_dr2=dE/rms**2                                # eV per fm^2 of <r^2>
# nuclear stiffness against a change of <r^2>: breathing mode. E = (1/2) K_A (dR/R)^2 * A/9 ... use K ~ 230 MeV per nucleon: E = A*K/18*(d<r2>/<r2>)^2/... 
K=230.0; stiff=A*K/18.0                         # MeV for unit fractional change of radius squared-ish (order of magnitude)
force_e=dE_dr2*rms**2*1e-6                      # MeV per unit fractional change of <r^2>
sig_pair=alpha**2/3*2*Zeff; sig_tot=260.7e-6
print(f"1s radius a0/Zeff = {a0/Zeff:.0f} fm ; nuclear radius (uniform-sphere equivalent) = {R:.2f} fm ; ratio {a0/Zeff/R:.0f}")
print(f"density at the centre, the pair: {2*rho0:.2e} per fm^3 ; fraction of the pair inside the nucleus: {inside:.2e}")
print(f"electron speed {v:.4f} c ; time to cross the nucleus {t_cross*fmc:.1e} s = {t_cross*fmc/T_nuc:.1f} nuclear turns (turn = 1e-22 s)")
print(f"crossings per second (pair): {rate:.2e} -> one every {1/rate:.1e} s = {1/rate/T_nuc:.1e} nuclear turns")
print(f"1s orbital period {T_orb:.1e} s = {T_orb/T_nuc:.1e} nuclear turns")
print(f"potential at the nucleus from the pair: {V0:.1f} V -> energy of the 6 charges {E_nuc/1e3:.2f} keV ; uniform across the nucleus to {((R/(a0/Zeff))**2):.1e}")
print(f"field at the centre from a round shell: 0 (Gauss)")
print(f"finite-size energy of the pair: {dE:.2e} eV ; per fm^2 of <r^2>: {dE_dr2:.2e} eV -> squeeze, as a fraction of nuclear stiffness ~ {force_e/stiff:.1e}")
print(f"magnetic shielding of the nucleus by the pair: {sig_pair*1e6:.0f} ppm of the applied field ; whole carbon atom {sig_tot*1e6:.0f} ppm ; pair's share {100*sig_pair/sig_tot:.0f} %")
print(f"total binding of all six electrons ~1030 eV = {1030/92.16e6:.1e} of the nuclear binding")
