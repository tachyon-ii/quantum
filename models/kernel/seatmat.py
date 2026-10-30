"""kernel/seatmat.py — compact seating sets: sparse descriptor-count matrices over a fixed global key index (SPEC v5 §4).
Keys: (pair in np/nn/pp, type S/H, c in 0..3, zmin 1..5, zmax 1..5). Grace (Claude Fable 5.1), 20 Oct 2026."""
import itertools,os,pickle,numpy as np,scipy.sparse as sp
import seat, data as D
HERE=os.path.dirname(os.path.abspath(__file__))
KEYS=[(p,t,c,zi,zj) for p in ('np','nn','pp') for t in ('S','H') for c in range(4) for zi in range(1,6) for zj in range(zi,6)]
KIDX={k:i for i,k in enumerate(KEYS)}
def build(A,Z):
    cl=seat.clusters(A); rows=[];cols=[];vals=[];coul=[];conn=[];trip=[];P=[];SPc=[]
    r=0
    for Pc in cl:
        for pr in itertools.combinations(range(A),Z):
            spc=['p' if i in pr else 'n' for i in range(A)]
            f,cu,cn,tr=seat.features(Pc,spc)
            for k,v in f.items(): rows.append(r); cols.append(KIDX[k]); vals.append(v)
            coul.append(cu); conn.append(cn); trip.append(tr); P.append(Pc.astype(np.int8)); SPc.append(''.join(spc)); r+=1
    M=sp.csr_matrix((vals,(rows,cols)),shape=(r,len(KEYS)),dtype=np.float32)
    return dict(M=M,coul=np.array(coul,np.float32),conn=np.array(conn),trip=np.array(trip),P=np.array(P),sp=np.array(SPc),A=A,Z=Z)
def load(name):
    Z,N=D.ZN[name]; A=Z+N; f=os.path.join(HERE,'results',f'seat_{name}.pkl')
    if os.path.exists(f): return pickle.load(open(f,'rb'))
    s=build(A,Z); pickle.dump(s,open(f,'wb')); return s
if __name__=='__main__':
    import sys,time
    for n in sys.argv[1:]:
        t=time.time(); s=load(n); print(n,s['M'].shape,'%.0fs'%(time.time()-t))
