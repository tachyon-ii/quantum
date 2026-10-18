# models/binding/membrane/targets.py
# Implementer: Argon (Gemini, DeepMind) — 18 Oct 2026
# GUARDRAIL (§2, §8): May be imported ONLY by compare.py, which runs last.

BE_T    = 8.481795   # MeV, AME2020
BE_HE3  = 7.718043   # MeV, AME2020
RCH_HE4 = 1.678      # fm
RCH_D   = 2.128      # fm
RCH_T   = 1.759      # fm
RCH_HE3 = 1.966      # fm

# 16 Oct required per-bond energies after slingshot and Coulomb (MeV)
EBOND_REQ = {
    'D':   0.788624,
    'T':   2.070717,
    'He3': 1.972080,
    'He4': 4.305000,
}

# Unfolded quantum-average rms centroid distances (fm) — for comparison ONLY (§5)
D_RMS_QUANTUM = {
    'D':   3.910,
    'T':   2.676,
    'He3': 3.078,
    'He4': 2.371,
}