import csv, math
import numpy as np

CSV = "geom_epsilon.csv"
a_e = 1.159652181e-3   # CODATA-scale electron anomaly

eps, delta = [], []
with open(CSV) as f:
    rd = csv.DictReader(f)
    for row in rd:
        if abs(float(row["beta"]))>1e-12:  # only β≈0 rows
            continue
        e  = float(row["eps"])
        g  = float(row["g_total"])  # = g_geo here
        if e<=0: 
            continue
        d = (2.0 - g)/2.0
        if d<=0:
            continue
        eps.append(e); delta.append(d)

eps = np.array(eps); delta = np.array(delta)

# Log–log fit: log(delta) = log k + p log ε
X = np.vstack([np.ones_like(eps), np.log(eps)]).T
y = np.log(delta)
coef, _, _, _ = np.linalg.lstsq(X, y, rcond=None)
logk, p = coef
k = math.exp(logk)

# Solve epsilon_e from a_e = k * epsilon^p
eps_e = (a_e / k)**(1.0/p)

print(f"Fitted geometry law: delta(ε) = k * ε^p")
print(f"  k = {k:.6g},  p = {p:.6g}")
print(f"Electron anomaly a_e = {a_e:.9e}")
print(f"Implied epsilon_e = (a_e/k)^(1/p) = {eps_e:.6f}")

# Sanity check: predicted g at epsilon_e
g_pred = 2.0*(1.0 - k*(eps_e**p))
print(f"Predicted g_geo(ε_e) = {g_pred:.12f}  (2 - 2*a_e = {2-2*a_e:.12f})")
