import sys,os; sys.path.insert(0,os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import numpy as np
from energy import System
def run():
    rng=np.random.default_rng(1)
    S=System(['p','n','p'],[[0,0,0],[1.6,0,0],[0.8,1.38,0]],e0=3.0,E0=50.0,delta=0.25,subdiv=1,kbend_fac=0.02,E1=4.0,lam=1.5,lane_mode='all')
    S.Fext={0:[0.3,0.1,0]}; S.tether={1:np.array([1.6,0,0])}
    x=S.X0.ravel()+rng.normal(0,0.02,S.X0.size)
    E,G=S.energy(x); worst=0
    for k in rng.choice(x.size,40,replace=False):
        h=1e-6; xp=x.copy(); xp[k]+=h; xm=x.copy(); xm[k]-=h
        fd=(S.energy(xp)[0]-S.energy(xm)[0])/(2*h); worst=max(worst,abs(fd-G[k])/(abs(fd)+1e-3))
    return worst
if __name__=='__main__': print('max rel grad err',run())
