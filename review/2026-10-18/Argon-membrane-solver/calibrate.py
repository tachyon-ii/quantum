# models/binding/membrane/calibrate.py
# Implementer: Argon (Gemini, DeepMind) — 18 Oct 2026
import numpy as np
from scipy.optimize import minimize
import constants as C
import relax as R


def calibrate_for_delta(delta, subdiv=C.SUBDIV, k_area_mult=C.K_AREA_MULT,
                        k_bend=C.K_BEND_PRI, fade_quadratic=False):
    """
    §4.3 Solves BE_model(D; e0, E0, delta) = BE_D and BE_model(He4; e0, E0, delta) = BE_HE4
    by Nelder-Mead + Powell polish with full vertex relaxation inside the loop.
    """
    tmpl_D, sp_D, x0_D       = R.build_initial_system('D', subdiv=subdiv, d_init=1.68)
    tmpl_He4, sp_He4, x0_He4 = R.build_initial_system('He4', subdiv=subdiv, d_init=1.66)

    # Warm-start cache to accelerate nested L-BFGS-B relaxations
    state_cache = {'x_D': x0_D.copy(), 'x_He4': x0_He4.copy()}

    def eval_pair(e0, E0):
        params = {
            'e0': max(0.05, float(e0)), 'E0': max(1.0, float(E0)), 'delta': float(delta),
            'k_area_mult': k_area_mult, 'k_bend': k_bend * max(1.0, float(E0)),
            'fade_quadratic': fade_quadratic,
        }
        c_D, info_D     = R.relax_system(tmpl_D, sp_D, state_cache['x_D'], params, gtol=1e-6, maxiter=250)
        c_He4, info_He4 = R.relax_system(tmpl_He4, sp_He4, state_cache['x_He4'], params, gtol=1e-6, maxiter=250)
        if info_D['is_connected']:
            state_cache['x_D'] = c_D
        if info_He4['is_connected']:
            state_cache['x_He4'] = c_He4
        return info_D['BE'], info_He4['BE'], c_D, c_He4, info_D, info_He4

    def loss(theta):
        e0, E0 = np.exp(theta[0]), np.exp(theta[1])
        be_d, be_he4, _, _, _, _ = eval_pair(e0, E0)
        return (be_d - C.BE_D)**2 + ((be_he4 - C.BE_HE4) / 4.0)**2

    init_theta = np.log([2.2, 45.0])
    sol = minimize(loss, init_theta, method='Nelder-Mead',
                   options={'xatol': 1e-4, 'fatol': 1e-9, 'maxiter': 80})
    e0_opt, E0_opt = float(np.exp(sol.x[0])), float(np.exp(sol.x[1]))

    # Final tight gtol=1e-8 evaluation at calibrated (e0, E0)
    params_final = {
        'e0': e0_opt, 'E0': E0_opt, 'delta': float(delta),
        'k_area_mult': k_area_mult, 'k_bend': k_bend * E0_opt,
        'fade_quadratic': fade_quadratic,
    }
    c_D, info_D     = R.relax_system(tmpl_D, sp_D, state_cache['x_D'], params_final, gtol=C.GTOL)
    c_He4, info_He4 = R.relax_system(tmpl_He4, sp_He4, state_cache['x_He4'], params_final, gtol=C.GTOL)

    return {
        'delta': float(delta),
        'e0': e0_opt,
        'E0': E0_opt,
        'E_MESH': C.E_MESH,
        'BE_D_cal': info_D['BE'],
        'BE_He4_cal': info_He4['BE'],
        'params': params_final,
        'D_relaxed': (tmpl_D, sp_D, c_D, info_D),
        'He4_relaxed': (tmpl_He4, sp_He4, c_He4, info_He4),
    }