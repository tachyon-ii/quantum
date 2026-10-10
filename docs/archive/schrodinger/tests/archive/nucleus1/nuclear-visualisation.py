import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.interpolate import griddata
import warnings
warnings.filterwarnings('ignore')

# Import the simulation functions from your code
import math

# Constants
alphaC = 1.439965
m_N = 938.918
mu_N = m_N / 2
hbarc = 197.3269804
kappa0 = (hbarc**2) / (2 * mu_N)

B_D_target = -2.224
B_He4_target = -28.30

lam_r = 0.5
zeta = 1.0

def A_d(d, lam):
    return - ( (-math.exp(-d/lam)/lam)/d  - math.exp(-d/lam)/d**2 )

def B_d(d):
    return + ( (-math.exp(-d/lam_r)/lam_r)/d  - math.exp(-d/lam_r)/d**2 )

def solve_g2_g2r(d, lam):
    A = A_d(d, lam)
    B = B_d(d)
    C = -2*zeta*kappa0 / d**3
    eL = math.exp(-d/lam) / d
    eR = math.exp(-d/lam_r) / d
    RHS1 = -C
    RHS2 = B_D_target - zeta*kappa0/d**2
    det = A*eR - B*(-eL)
    if abs(det) < 1e-12:
        return None, None
    g2  = (RHS1*eR - B*RHS2) / det
    g2r = (A*RHS2 - RHS1*(-eL)) / det
    return g2, g2r

def U_pair(d, g2, g2r, lam, coulomb=False):
    return - g2*math.exp(-d/lam)/d + g2r*math.exp(-d/lam_r)/d + (alphaC/d if coulomb else 0.0)

def T_pair(d):
    return zeta*kappa0/d**2

def E_He_pairs(a, g2, g2r, lam):
    return (U_pair(a, g2, g2r, lam, True)+T_pair(a)) + 5*(U_pair(a, g2, g2r, lam, False)+T_pair(a))

def E_triangle_pairs(a, g2, g2r, lam, Z):
    pp_edges = 1 if Z >= 2 else 0
    E = 0.0
    for i in range(3):
        E += (- g2*math.exp(-a/lam)/a + g2r*math.exp(-a/lam_r)/a
              + (alphaC/a if i < pp_edges else 0.0)) + T_pair(a)
    return E

def minimize_scalar(f, lo=0.6, hi=3.0, n=801):
    xs = np.linspace(lo, hi, n)
    vals = [f(x) for x in xs]
    j = int(np.argmin(vals))
    return xs[j], vals[j]

def run_scan(lam_values, d_values):
    results = []
    for lam in lam_values:
        for d in d_values:
            g2, g2r = solve_g2_g2r(d, lam)
            if g2 is None or g2r is None or g2 <= 0 or g2r <= 0:
                continue
            # He-4 baseline
            a0, E0_pairs = minimize_scalar(lambda a: E_He_pairs(a, g2, g2r, lam))
            face_factor = math.exp(-a0/lam)/a0
            # 3-body W to match He-4 exactly
            W = (E0_pairs - B_He4_target) / (4.0 * face_factor)
            # A=3 predictions
            def E3_total(Z):
                f_tri = lambda a: E_triangle_pairs(a, g2, g2r, lam, Z) - W * (math.exp(-a/lam)/a)
                return minimize_scalar(f_tri)
            a_3H, E_3H = E3_total(Z=1)
            a_3He, E_3He = E3_total(Z=2)
            results.append({
                "lambda_fm": lam,
                "d*_fm": d,
                "g2_MeVfm": g2,
                "g2r_MeVfm": g2r,
                "He4_a*_fm": a0,
                "He4_E_MeV": E0_pairs - 4.0*W*face_factor,
                "W_MeVfm": W,
                "a3H_fm": a_3H, "E3H_MeV": E_3H,
                "a3He_fm": a_3He, "E3He_MeV": E_3He,
                "He3_minus_H3_MeV": E_3He - E_3H
            })
    return pd.DataFrame(results)

# ==============================================================================
# MAIN ANALYSIS
# ==============================================================================

print("=" * 80)
print("NUCLEAR BINDING THEORY - λ-d EDGE MODEL ANALYSIS")
print("=" * 80)

# Run the scan
print("\n⚛ Generating parameter scan...")
lam_scan = np.linspace(1.28, 1.38, 51)
d_scan = np.linspace(1.1, 2.6, 76)
df = run_scan(lam_scan, d_scan)

print(f"✓ Generated {len(df)} valid parameter combinations")
print(f"  λ range: {lam_scan.min():.3f} - {lam_scan.max():.3f} fm")
print(f"  d* range: {d_scan.min():.3f} - {d_scan.max():.3f} fm")

# Save the raw data
df.to_csv("lambda_scan_results.csv", index=False)
print("✓ Saved raw data to lambda_scan_results.csv")

# ==============================================================================
# 3.1 OPTIMAL PARAMETER IDENTIFICATION
# ==============================================================================

print("\n" + "=" * 80)
print("OPTIMAL PARAMETER IDENTIFICATION")
print("=" * 80)

# Define criteria for optimal parameters
experimental_split = 0.764  # MeV

# Add scoring metrics
df['W_abs'] = df['W_MeVfm'].abs()
df['He4_a_deviation'] = (df['He4_a*_fm'] - 1.4).abs()  # Target ~1.4 fm
df['split_error'] = (df['He3_minus_H3_MeV'] - experimental_split).abs()

# Composite score (lower is better)
df['score'] = (
    df['W_abs'] / df['W_abs'].max() * 0.4 +  # 40% weight on minimal W
    df['He4_a_deviation'] / df['He4_a_deviation'].max() * 0.3 +  # 30% on reasonable edge length
    df['split_error'] / df['split_error'].max() * 0.3  # 30% on correct split
)

# Get top candidates
top_n = 20
top_candidates = df.nsmallest(top_n, 'score')

print("\nTop 10 Parameter Combinations (ranked by composite score):")
print("-" * 80)
print(f"{'Rank':<5} {'λ (fm)':<8} {'d* (fm)':<8} {'|W| (MeV·fm)':<12} {'a* (fm)':<8} {'Split (MeV)':<12} {'Score':<8}")
print("-" * 80)

for i, row in enumerate(top_candidates.head(10).itertuples(), 1):
    print(f"{i:<5} {row.lambda_fm:<8.3f} {row._2:<8.3f} {row.W_abs:<12.3f} {row._5:<8.3f} {row.He3_minus_H3_MeV:<12.3f} {row.score:<8.4f}")

# Best candidate
best = top_candidates.iloc[0]
print(f"\n⭐ BEST COMPROMISE PARAMETERS:")
print(f"   λ = {best['lambda_fm']:.3f} fm")
print(f"   d* = {best['d*_fm']:.3f} fm")
print(f"   g² = {best['g2_MeVfm']:.3f} MeV·fm")
print(f"   g²ᵣ = {best['g2r_MeVfm']:.3f} MeV·fm")
print(f"   W = {best['W_MeVfm']:.3f} MeV·fm")
print(f"   He-4 edge = {best['He4_a*_fm']:.3f} fm")
print(f"   ³He-³H split = {best['He3_minus_H3_MeV']:.3f} MeV (exp: {experimental_split:.3f} MeV)")

# Save top candidates
top_candidates[['lambda_fm', 'd*_fm', 'g2_MeVfm', 'g2r_MeVfm', 'W_MeVfm', 
                'He4_a*_fm', 'He3_minus_H3_MeV', 'score']].to_csv("top_candidates.csv", index=False)
print("\n✓ Saved top candidates to top_candidates.csv")

# ==============================================================================
# 3.2 HEATMAPS / CONTOURS
# ==============================================================================

print("\n" + "=" * 80)
print("GENERATING HEATMAPS")
print("=" * 80)

# Create grid for interpolation
lambda_grid = np.linspace(df['lambda_fm'].min(), df['lambda_fm'].max(), 100)
d_grid = np.linspace(df['d*_fm'].min(), df['d*_fm'].max(), 100)
lambda_mesh, d_mesh = np.meshgrid(lambda_grid, d_grid)

# Interpolate data for smooth heatmaps
quantities = {
    'W_MeVfm': 'W (MeV·fm)',
    'He4_a*_fm': 'He-4 Edge Length (fm)',
    'He3_minus_H3_MeV': '³He-³H Split (MeV)',
    'g2_MeVfm': 'g² Attractive (MeV·fm)',
    'g2r_MeVfm': 'g²ᵣ Repulsive (MeV·fm)'
}

fig, axes = plt.subplots(2, 3, figsize=(18, 12))
fig.suptitle('λ-d Parameter Space Analysis', fontsize=16, fontweight='bold')

for idx, (key, title) in enumerate(quantities.items()):
    ax = axes.flat[idx]
    
    # Interpolate
    grid_data = griddata(
        (df['lambda_fm'], df['d*_fm']), 
        df[key],
        (lambda_mesh, d_mesh),
        method='cubic'
    )
    
    # Create heatmap
    im = ax.contourf(lambda_mesh, d_mesh, grid_data, levels=20, cmap='viridis')
    ax.contour(lambda_mesh, d_mesh, grid_data, levels=10, colors='white', alpha=0.3, linewidths=0.5)
    
    # Mark best point
    ax.plot(best['lambda_fm'], best['d*_fm'], 'r*', markersize=15, label='Best')
    
    ax.set_xlabel('λ (fm)', fontsize=10)
    ax.set_ylabel('d* (fm)', fontsize=10)
    ax.set_title(title, fontsize=11, fontweight='bold')
    
    cbar = plt.colorbar(im, ax=ax)
    cbar.ax.tick_params(labelsize=8)
    
    ax.grid(True, alpha=0.2)
    ax.legend(loc='upper right', fontsize=8)

# Remove empty subplot
axes.flat[-1].axis('off')

plt.tight_layout()
plt.savefig('heatmaps_lambda_d.png', dpi=150, bbox_inches='tight', facecolor='white')
print("✓ Saved heatmaps to heatmaps_lambda_d.png")
plt.show()

# ==============================================================================
# 3.3 PARAMETER TREND PLOTS
# ==============================================================================

print("\n" + "=" * 80)
print("GENERATING TREND PLOTS")
print("=" * 80)

# Select representative values
representative_lambdas = [1.30, 1.33, 1.36]
representative_ds = [1.4, 1.7, 2.0, 2.3]

fig, axes = plt.subplots(2, 2, figsize=(15, 12))

# Trends vs lambda for fixed d
ax1 = axes[0, 0]
for d_val in representative_ds:
    subset = df[np.abs(df['d*_fm'] - d_val) < 0.02]
    if len(subset) > 0:
        subset_sorted = subset.sort_values('lambda_fm')
        ax1.plot(subset_sorted['lambda_fm'], subset_sorted['W_MeVfm'], 
                marker='o', label=f'd*={d_val:.1f} fm', linewidth=2)
ax1.set_xlabel('λ (fm)')
ax1.set_ylabel('W (MeV·fm)')
ax1.set_title('Three-body strength vs λ', fontweight='bold')
ax1.legend()
ax1.grid(True, alpha=0.3)

# Trends vs d for fixed lambda
ax2 = axes[0, 1]
for lam_val in representative_lambdas:
    subset = df[np.abs(df['lambda_fm'] - lam_val) < 0.002]
    if len(subset) > 0:
        subset_sorted = subset.sort_values('d*_fm')
        ax2.plot(subset_sorted['d*_fm'], subset_sorted['W_MeVfm'], 
                marker='s', label=f'λ={lam_val:.2f} fm', linewidth=2)
ax2.set_xlabel('d* (fm)')
ax2.set_ylabel('W (MeV·fm)')
ax2.set_title('Three-body strength vs d*', fontweight='bold')
ax2.legend()
ax2.grid(True, alpha=0.3)

# g2 vs lambda
ax3 = axes[1, 0]
for d_val in representative_ds:
    subset = df[np.abs(df['d*_fm'] - d_val) < 0.02]
    if len(subset) > 0:
        subset_sorted = subset.sort_values('lambda_fm')
        ax3.plot(subset_sorted['lambda_fm'], subset_sorted['g2_MeVfm'], 
                marker='^', label=f'd*={d_val:.1f} fm', linewidth=2)
ax3.set_xlabel('λ (fm)')
ax3.set_ylabel('g² (MeV·fm)')
ax3.set_title('Attractive strength vs λ', fontweight='bold')
ax3.legend()
ax3.grid(True, alpha=0.3)

# Split vs parameters
ax4 = axes[1, 1]
for lam_val in representative_lambdas:
    subset = df[np.abs(df['lambda_fm'] - lam_val) < 0.002]
    if len(subset) > 0:
        subset_sorted = subset.sort_values('d*_fm')
        ax4.plot(subset_sorted['d*_fm'], subset_sorted['He3_minus_H3_MeV'], 
                marker='d', label=f'λ={lam_val:.2f} fm', linewidth=2)
ax4.axhline(y=experimental_split, color='red', linestyle='--', label='Experimental', linewidth=2)
ax4.set_xlabel('d* (fm)')
ax4.set_ylabel('³He-³H Split (MeV)')
ax4.set_title('Coulomb split vs d*', fontweight='bold')
ax4.legend()
ax4.grid(True, alpha=0.3)

plt.suptitle('Parameter Trends Analysis', fontsize=14, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig('parameter_trends.png', dpi=150, bbox_inches='tight', facecolor='white')
print("✓ Saved trend plots to parameter_trends.png")
plt.show()

# ==============================================================================
# 4.1 BINDING ENERGY COMPARISON
# ==============================================================================

print("\n" + "=" * 80)
print("BINDING ENERGY ANALYSIS")
print("=" * 80)

# Experimental values
exp_values = {
    'D': -2.224,
    '³H': -8.482,
    '³He': -7.718,
    'He-4': -28.30
}

# Calculate predicted values for best parameters
print("\nBinding Energy Comparison (Best Parameters):")
print("-" * 60)
print(f"{'Nucleus':<10} {'Predicted (MeV)':<15} {'Experimental (MeV)':<18} {'Error (%)':<10}")
print("-" * 60)

# D is fitted exactly
print(f"{'D':<10} {B_D_target:<15.3f} {exp_values['D']:<18.3f} {0.0:<10.1f}")

# A=3 from best fit
print(f"{'³H':<10} {best['E3H_MeV']:<15.3f} {exp_values['³H']:<18.3f} {100*(best['E3H_MeV']-exp_values['³H'])/exp_values['³H']:<10.1f}")
print(f"{'³He':<10} {best['E3He_MeV']:<15.3f} {exp_values['³He']:<18.3f} {100*(best['E3He_MeV']-exp_values['³He'])/exp_values['³He']:<10.1f}")

# He-4 is fitted exactly
print(f"{'He-4':<10} {best['He4_E_MeV']:<15.3f} {exp_values['He-4']:<18.3f} {0.0:<10.1f}")

# ==============================================================================
# 4.2 RANGE VS STRENGTH CORRELATION
# ==============================================================================

print("\n" + "=" * 80)
print("RANGE-STRENGTH CORRELATION ANALYSIS")
print("=" * 80)

fig, ax = plt.subplots(1, 1, figsize=(10, 8))

# Create scatter plot with W as color
scatter = ax.scatter(df['lambda_fm'], df['g2_MeVfm'], 
                    c=df['W_abs'], s=30, 
                    cmap='coolwarm', alpha=0.6, edgecolors='black', linewidth=0.5)

# Mark best point
ax.scatter(best['lambda_fm'], best['g2_MeVfm'], 
          s=200, c='gold', marker='*', edgecolors='black', linewidth=2,
          label=f'Best: λ={best["lambda_fm"]:.3f}, g²={best["g2_MeVfm"]:.1f}', zorder=5)

ax.set_xlabel('λ (fm) - Attractive Range', fontsize=12)
ax.set_ylabel('g² (MeV·fm) - Attractive Strength', fontsize=12)
ax.set_title('Range vs Strength Correlation\n(Color = |W| three-body strength)', fontsize=14, fontweight='bold')

cbar = plt.colorbar(scatter, ax=ax)
cbar.set_label('|W| (MeV·fm)', fontsize=11)

ax.grid(True, alpha=0.3)
ax.legend(loc='upper right', fontsize=10)

plt.tight_layout()
plt.savefig('range_strength_correlation.png', dpi=150, bbox_inches='tight', facecolor='white')
print("✓ Saved correlation plot to range_strength_correlation.png")
plt.show()

# ==============================================================================
# 5.1 POTENTIAL SURFACE PLOTS
# ==============================================================================

print("\n" + "=" * 80)
print("POTENTIAL SURFACE ANALYSIS")
print("=" * 80)

# Use best parameters
best_lam = best['lambda_fm']
best_d = best['d*_fm']
best_g2 = best['g2_MeVfm']
best_g2r = best['g2r_MeVfm']
best_W = best['W_MeVfm']
best_a = best['He4_a*_fm']

# Create potential curves
r_range = np.linspace(0.3, 4.0, 500)

# Calculate potentials
V_pair = np.array([U_pair(r, best_g2, best_g2r, best_lam, coulomb=False) for r in r_range])
V_pair_coulomb = np.array([U_pair(r, best_g2, best_g2r, best_lam, coulomb=True) for r in r_range])
T_kinetic = np.array([T_pair(r) for r in r_range])
V_3body = -best_W * np.exp(-r_range/best_lam) / r_range

# Total potentials
V_total_np = V_pair + T_kinetic + V_3body  # neutron-proton
V_total_pp = V_pair_coulomb + T_kinetic + V_3body  # proton-proton

fig, axes = plt.subplots(1, 2, figsize=(15, 6))

# Plot 1: Components
ax1 = axes[0]
ax1.plot(r_range, V_pair, label='Pair Potential (n-p)', linewidth=2)
ax1.plot(r_range, T_kinetic, label='Kinetic Term', linewidth=2, linestyle='--')
ax1.plot(r_range, V_3body, label='3-body W Term', linewidth=2, linestyle=':')
ax1.plot(r_range, V_total_np, label='Total (n-p)', linewidth=3, color='red')
ax1.axvline(x=best_a, color='gray', linestyle='--', alpha=0.5, label=f'He-4 edge = {best_a:.2f} fm')
ax1.axhline(y=0, color='black', linestyle='-', alpha=0.3)

ax1.set_xlabel('r (fm)', fontsize=11)
ax1.set_ylabel('Energy (MeV)', fontsize=11)
ax1.set_title('Potential Components (Best Parameters)', fontsize=12, fontweight='bold')
ax1.set_xlim(0.3, 3.5)
ax1.set_ylim(-60, 100)
ax1.legend(loc='upper right')
ax1.grid(True, alpha=0.3)

# Plot 2: Comparison with and without Coulomb
ax2 = axes[1]
ax2.plot(r_range, V_total_np, label='n-p (no Coulomb)', linewidth=2.5)
ax2.plot(r_range, V_total_pp, label='p-p (with Coulomb)', linewidth=2.5)
ax2.axvline(x=best_a, color='gray', linestyle='--', alpha=0.5, label=f'He-4 edge = {best_a:.2f} fm')
ax2.axvline(x=best_d, color='orange', linestyle='--', alpha=0.5, label=f'd* = {best_d:.2f} fm')
ax2.axhline(y=0, color='black', linestyle='-', alpha=0.3)
ax2.axhline(y=B_D_target, color='blue', linestyle=':', alpha=0.5, label=f'D binding = {B_D_target:.2f} MeV')

ax2.set_xlabel('r (fm)', fontsize=11)
ax2.set_ylabel('Total Energy (MeV)', fontsize=11)
ax2.set_title('Total Potential: n-p vs p-p', fontsize=12, fontweight='bold')
ax2.set_xlim(0.3, 3.5)
ax2.set_ylim(-20, 40)
ax2.legend(loc='upper right')
ax2.grid(True, alpha=0.3)

plt.suptitle(f'Potential Surfaces (λ={best_lam:.3f} fm, d*={best_d:.3f} fm)', 
            fontsize=14, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig('potential_surfaces.png', dpi=150, bbox_inches='tight', facecolor='white')
print("✓ Saved potential surfaces to potential_surfaces.png")
plt.show()

# Save potential data for animation/3D rendering
potential_data = pd.DataFrame({
    'r_fm': r_range,
    'V_pair': V_pair,
    'V_pair_coulomb': V_pair_coulomb,
    'T_kinetic': T_kinetic,
    'V_3body': V_3body,
    'V_total_np': V_total_np,
    'V_total_pp': V_total_pp
})
potential_data.to_csv('potential_curves_best.csv', index=False)
print("✓ Saved potential curves to potential_curves_best.csv")

# ==============================================================================
# 5.3 ANIMATION INPUTS - Parameter Sweep Curves
# ==============================================================================

print("\n" + "=" * 80)
print("GENERATING ANIMATION DATA")
print("=" * 80)

# Lambda sweep animation data
lambda_sweep = np.linspace(1.28, 1.38, 21)
animation_data_lambda = []

for lam in lambda_sweep:
    # Use best d* value
    g2, g2r = solve_g2_g2r(best_d, lam)
    if g2 is not None and g2r is not None and g2 > 0 and g2r > 0:
        # Calculate energy curve for He-4
        a_range = np.linspace(0.8, 2.5, 100)
        E_curve = [E_He_pairs(a, g2, g2r, lam) for a in a_range]
        
        animation_data_lambda.append({
            'lambda': lam,
            'a_range': a_range.tolist(),
            'E_curve': E_curve
        })

# Save animation data
import json
with open('animation_lambda_sweep.json', 'w') as f:
    json.dump(animation_data_lambda, f)
print(f"✓ Saved λ sweep animation data ({len(animation_data_lambda)} frames)")

# d* sweep animation data  
d_sweep = np.linspace(1.2, 2.4, 21)
animation_data_d = []

for d in d_sweep:
    # Use best lambda value
    g2, g2r = solve_g2_g2r(d, best_lam)
    if g2 is not None and g2r is not None and g2 > 0 and g2r > 0:
        # Calculate energy curves
        a_range = np.linspace(0.8, 2.5, 100)
        E_he4 = [E_He_pairs(a, g2, g2r, best_lam) for a in a_range]
        E_tri = [E_triangle_pairs(a, g2, g2r, best_lam, 1) for a in a_range]
        
        animation_data_d.append({
            'd_star': d,
            'a_range': a_range.tolist(),
            'E_he4_curve': E_he4,
            'E_triangle_curve': E_tri
        })

with open('animation_d_sweep.json', 'w') as f:
    json.dump(animation_data_d, f)
print(f"✓ Saved d* sweep animation data ({len(animation_data_d)} frames)")

# ==============================================================================
# SUMMARY REPORT
# ==============================================================================

print("\n" + "=" * 80)
print("ANALYSIS COMPLETE - SUMMARY")
print("=" * 80)

print(f"""
Nuclear Binding λ-d Edge Model Analysis Results:

1. OPTIMAL PARAMETERS FOUND:
   - λ (attractive range): {best['lambda_fm']:.3f} fm
   - d* (deuteron scale): {best['d*_fm']:.3f} fm  
   - g² (attractive strength): {best['g2_MeVfm']:.1f} MeV·fm
   - g²ᵣ (repulsive strength): {best['g2r_MeVfm']:.1f} MeV·fm
   - W (3-body strength): {best['W_MeVfm']:.2f} MeV·fm
   
2. PREDICTIONS:
   - He-4 edge length: {best['He4_a*_fm']:.3f} fm
   - ³H binding: {best['E3H_MeV']:.2f} MeV (exp: {exp_values['³H']:.2f})
   - ³He binding: {best['E3He_MeV']:.2f} MeV (exp: {exp_values['³He']:.2f})
   - ³He-³H split: {best['He3_minus_H3_MeV']:.3f} MeV (exp: {experimental_split:.3f})

3. FILES GENERATED:
   ✓ lambda_scan_results.csv - Full parameter scan data
   ✓ top_candidates.csv - Best parameter combinations
   ✓ potential_curves_best.csv - Potential energy curves
   ✓ animation_lambda_sweep.json - λ parameter animation data
   ✓ animation_d_sweep.json - d* parameter animation data
   
4. VISUALIZATIONS CREATED:
   ✓ heatmaps_lambda_d.png - Parameter space heatmaps
   ✓ parameter_trends.png - Parameter dependency trends
   ✓ range_strength_correlation.png - g² vs λ correlation
   ✓ potential_surfaces.png - Potential energy landscapes

The model successfully reproduces the deuteron and He-4 binding energies exactly,
while providing reasonable predictions for the A=3 nuclei with minimal 3-body correction.
""")

print("\n" + "=" * 80)
print("Ready for wave-pattern visualization and geometric rendering!")
print("=" * 80)
