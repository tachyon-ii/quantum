# --- mesh_glue.py: safer + stronger near-contact model ---

from dataclasses import dataclass
from math import exp

@dataclass(frozen=True)
class MeshGlueParams:
    kappa: float
    mu: float
    eps0: float
    R0: float
    delta_eff: float
    lambda_c: float
    sigma_NN: float = 1.25
    sigma_NP: float = 1.00
    sigma_PP: float = 0.00

def _safe_gap(r, r0, params: MeshGlueParams):
    # physical separation = sheet thickness + extra opening; never < floor
    R0 = params.R0 if (params.R0 and params.R0 > 0) else 1.0
    extra = max(r - r0, 0.0)
    # allow tuning via optional attribute; default = 0.005 * R0 (0.5% of R0)
    gap_floor_ratio = getattr(params, "gap_floor_ratio", 0.005)
    gap_floor = max(1e-3, gap_floor_ratio * R0)
    return max(params.delta_eff + extra, gap_floor)

def u_mesh_per_edge(r, r0, edge_type, params: MeshGlueParams, s1=+1, s2=+1):
    sign_prod = s1 * s2
    if edge_type == 'NN':
        sigma = params.sigma_NN
    elif edge_type == 'NP':
        sigma = params.sigma_NP
    else:
        sigma = params.sigma_PP
    if sigma == 0.0 or sign_prod == 0:
        return 0.0

    R0 = params.R0 if (params.R0 and params.R0 > 0) else 1.0
    mu2_over_eps = (params.mu * params.mu) / (params.eps0 if params.eps0 else 1.0)
    C_edge = 1.0 / (R0 * R0)

    gap = _safe_gap(r, r0, params)
    U = (- sigma * sign_prod * C_edge * mu2_over_eps) * (gap ** -3) * exp(-(r - r0) / max(params.lambda_c, 1e-6))
    return U

def f_mesh_per_edge(r, r0, edge_type, params: MeshGlueParams, s1=+1, s2=+1):
    sign_prod = s1 * s2
    if edge_type == 'NN':
        sigma = params.sigma_NN
    elif edge_type == 'NP':
        sigma = params.sigma_NP
    else:
        sigma = params.sigma_PP
    if sigma == 0.0 or sign_prod == 0:
        return 0.0

    R0 = params.R0 if (params.R0 and params.R0 > 0) else 1.0
    mu2_over_eps = (params.mu * params.mu) / (params.eps0 if params.eps0 else 1.0)
    C_edge = 1.0 / (R0 * R0)

    gap = _safe_gap(r, r0, params)
    U = (- sigma * sign_prod * C_edge * mu2_over_eps) * (gap ** -3) * exp(-(r - r0) / max(params.lambda_c, 1e-6))
    dUdr = U * ( -3.0 / gap - 1.0 / max(params.lambda_c, 1e-6) )
    return -dUdr

