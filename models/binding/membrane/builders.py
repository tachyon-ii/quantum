"""builders.py — System constructors for jobs (picklable specs). Implementer: Grace (Claude Opus 5.5)."""
import numpy as np, constants as K
from energy import System
A0P=4*np.pi*K.RP**2
def geom(name,a=None):
    a=a or 2*K.RP*1.01
    if name=='D': return ['p','n'],[[0,0,0],[a,0,0]]
    if name=='He4':
        T=np.array([[1,1,1],[1,-1,-1],[-1,1,-1],[-1,-1,1]])*a/(2*np.sqrt(2)); return ['p','p','n','n'],T.tolist()
    if name in ('T','He3'):
        sp=['p','n','n'] if name=='T' else ['p','p','n']
        return sp,[[0,0,0],[a,0,0],[a/2,a*np.sqrt(3)/2,0]]
def nucleus(name,r,E0,delta,a=None,subdiv=K.SUBDIV,fade=K.FADE,kbend_fac=K.K_BEND_FAC,karea_fac=K.K_AREA_FAC,
            fext=None,tether=None,fixed=None,shift=None,E1=0.0,singlet_np=False):
    sp,cs=geom(name,a); S=System(sp,cs,r*E0/A0P,E0,delta,subdiv=subdiv,fade=fade,kbend_fac=kbend_fac,karea_fac=karea_fac,E1=E1,singlet_np=singlet_np)
    if fext: S.Fext={int(k):np.array(v) for k,v in fext.items()}
    if tether: S.tether={int(k):np.array(v) for k,v in tether.items()}
    if fixed: S.fixed[list(fixed)]=True
    return S
