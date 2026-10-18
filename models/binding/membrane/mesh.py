"""mesh.py — icosphere, sparse scatter, geometry. Implementer: Grace (Claude Opus 5.5)."""
import numpy as np, scipy.sparse as sp
def icosphere(n):
    t=(1+5**.5)/2
    V=[(-1,t,0),(1,t,0),(-1,-t,0),(1,-t,0),(0,-1,t),(0,1,t),(0,-1,-t),(0,1,-t),(t,0,-1),(t,0,1),(-t,0,-1),(-t,0,1)]
    F=[(0,11,5),(0,5,1),(0,1,7),(0,7,10),(0,10,11),(1,5,9),(5,11,4),(11,10,2),(10,7,6),(7,1,8),
       (3,9,4),(3,4,2),(3,2,6),(3,6,8),(3,8,9),(4,9,5),(2,4,11),(6,2,10),(8,6,7),(9,8,1)]
    V=[np.array(v,float)/np.linalg.norm(v) for v in V]
    for _ in range(n):
        cache={}; NF=[]
        def mid(a,b):
            k=(min(a,b),max(a,b))
            if k not in cache:
                m=V[a]+V[b]; V.append(m/np.linalg.norm(m)); cache[k]=len(V)-1
            return cache[k]
        for a,b,c in F:
            ab,bc,ca=mid(a,b),mid(b,c),mid(c,a)
            NF+= [(a,ab,ca),(b,bc,ab),(c,ca,bc),(ab,bc,ca)]
        F=NF
    V=np.array(V); F=np.array(F)
    # orient outward
    a,b,c=V[F[:,0]],V[F[:,1]],V[F[:,2]]
    flip=(np.cross(b-a,c-a)*(a+b+c)).sum(1)<0
    F[flip]=F[flip][:,[0,2,1]]
    return V,F
class Topo:
    def __init__(self,n):
        self.V,self.F=icosphere(n); self.nv=len(self.V); self.nf=len(self.F)
        rows=self.F.T.ravel(); cols=np.arange(3*self.nf)
        self.S=sp.csr_matrix((np.ones(3*self.nf),(rows,cols)),shape=(self.nv,3*self.nf))  # (corner-major: corner k of face f at k*nf+f)
    def scatter(self,ga,gb,gc):
        return self.S@np.concatenate([ga,gb,gc],0)
def face_geom(X,F):
    a,b,c=X[F[:,0]],X[F[:,1]],X[F[:,2]]
    n=np.cross(b-a,c-a); nn=np.linalg.norm(n,axis=1)
    return a,b,c,n,nn
def tri_grad(a,b,c,q):
    """gradient of q.((b-a)x(c-a)) w.r.t. a,b,c (q held fixed)."""
    u=b-a; v=c-a
    gb=np.cross(v,q); gc=np.cross(q,u); return -gb-gc,gb,gc
