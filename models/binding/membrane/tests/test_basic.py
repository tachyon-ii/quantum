"""tests — BUILD-SPEC §9 subset that is meaningful without a calibration. Implementer: Grace (Claude Opus 5.5)."""
import sys,os,numpy as np; sys.path.insert(0,os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import constants as K
from energy import System
from relax import relax
from mesh import face_geom
def t1_isolated(kb=0.3):
    S=System(['p'],[[0,0,0]],3/(4*np.pi*K.RP**2),1.0,K.DELTA_GRID[1],kbend_fac=kb); x,_=relax(S)
    X=x.reshape(-1,3); r=np.linalg.norm(X-X.mean(0),axis=1); a,b,c,n,nn=face_geom(X,S.T.F)
    return dict(sphericity=float(r.std()/r.mean()),V_over_V0=float((a*np.cross(b,c)).sum()/6/S.V0m[0]),area_strain=float((0.5*nn).sum()/S.A0m[0]-1))
def t7_rotation(S_builder):
    pass
if __name__=='__main__':
    from test_grad import run as g
    print('grad check max rel err',g()); print('isolated capsid',t1_isolated())
