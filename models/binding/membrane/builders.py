"""builders.py — System constructors for jobs (picklable specs). Implementer: Grace (Claude Opus 5.5)."""
import numpy as np, constants as K
from energy import System
A0P=4*np.pi*K.RP**2
def geom(name,a=None):
    a=a or 2*K.RP*1.01
    if name=='D': return ['p','n'],[[0,0,0],[a,0,0]]
    if name=='He4':
        T=np.array([[1,1,1],[1,-1,-1],[-1,1,-1],[-1,-1,1]])*a/(2*np.sqrt(2)); return ['p','p','n','n'],T.tolist()
    if name in ('He5_face','He5_face2','He5_edge','He5_vertex','Li5_face','Li5_face2','Li5_edge','Li5_vertex','Li6_stack','Li6_faces'):
        # v4 A1 seatings on the alpha. Alpha: regular tetrahedron edge a; extra nucleon(s) at touching distance t=1.70 fm.
        T=np.array([[1,1,1],[1,-1,-1],[-1,1,-1],[-1,-1,1]],float)*a/(2*np.sqrt(2)); t=K.RP+K.RN
        sp=['p','p','n','n']; pts=T.tolist()
        def face(idx):
            c=T[list(idx)].mean(0); n=c/np.linalg.norm(c); rc=np.linalg.norm(T[idx[0]]-c); return c+n*np.sqrt(max(t*t-rc*rc,0.01))
        def edge(i,j):
            m=(T[i]+T[j])/2; d=m/np.linalg.norm(m); return m+d*np.sqrt(t*t-(a/2)**2)
        def vertex(i):
            return T[i]*(1+t/np.linalg.norm(T[i]))
        extra={'face':face((0,1,2)),'face2':face((0,2,3)),'edge':edge(0,2),'vertex':vertex(0)}   # face=(p,p,n), face2=(p,n,n)
        if name.startswith('He5'): sp.append('n'); pts.append(extra[name.split('_')[1]].tolist())
        elif name.startswith('Li5'): sp.append('p'); pts.append(extra[name.split('_')[1]].tolist())
        elif name=='Li6_stack':
            # third dumbbell (pn) stacked orthogonal to the nn dumbbell (T[2],T[3]) above it: along the pp direction, at height h above the nn plane
            nn_mid=(T[2]+T[3])/2; axis=nn_mid/np.linalg.norm(nn_mid); ppdir=(T[0]-T[1])/np.linalg.norm(T[0]-T[1])
            h=np.sqrt(max(t*t-(a/2)**2-(a/2)**2,0.04))   # each new nucleon touches both nn nucleons
            c=nn_mid+axis*h; sp+=['p','n']; pts+=[(c+ppdir*a/2).tolist(),(c-ppdir*a/2).tolist()]
        elif name=='Li6_faces':
            sp+=['p','n']; pts+=[face((0,1,2)).tolist(),face((0,1,3)).tolist()]
        return sp,pts
    if name in ('T','He3'):
        sp=['p','n','n'] if name=='T' else ['p','p','n']
        return sp,[[0,0,0],[a,0,0],[a/2,a*np.sqrt(3)/2,0]]
def nucleus(name,r,E0,delta,a=None,subdiv=K.SUBDIV,fade=K.FADE,kbend_fac=K.K_BEND_FAC,karea_fac=K.K_AREA_FAC,
            fext=None,tether=None,fixed=None,shift=None,E1=0.0,singlet_np=False,lam=0.0,lane_mode='triplet',lane_form='linear'):
    sp,cs=geom(name,a); S=System(sp,cs,r*E0/A0P,E0,delta,subdiv=subdiv,fade=fade,kbend_fac=kbend_fac,karea_fac=karea_fac,E1=E1,singlet_np=singlet_np,lam=lam,lane_mode=lane_mode,lane_form=lane_form)
    if fext: S.Fext={int(k):np.array(v) for k,v in fext.items()}
    if tether: S.tether={int(k):np.array(v) for k,v in tether.items()}
    if fixed: S.fixed[list(fixed)]=True
    return S
