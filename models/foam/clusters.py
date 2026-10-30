"""foam/clusters.py — standard N-bubble clusters (equal pressures: flat films, equal outer radii R, centres at mutual distance R so films meet at 120 deg).
Monte Carlo areas/volumes. Test: does the area SAVED by sharing (vs N separate bubbles of the same volume) go as C^2 (1:9:36) or as the film count (1:3:6)?
Grace (Claude Fable 5.1), 30 Oct 2026."""
import numpy as np,itertools
rng=np.random.default_rng(0); R=1.0
def centres(N):
    if N==2: return np.array([[0,0,0],[R,0,0]],float)
    if N==3: return np.array([[0,0,0],[R,0,0],[R/2,R*np.sqrt(3)/2,0]],float)
    if N==4: return np.array([[1,1,1],[1,-1,-1],[-1,1,-1],[-1,-1,1]],float)*R/(2*np.sqrt(2))
    if N==5:
        T=np.array([[0,0,0],[R,0,0],[R/2,R*np.sqrt(3)/2,0]],float); c=T.mean(0); h=np.sqrt(R*R-np.linalg.norm(T[0]-c)**2)
        return np.vstack([T,c+[0,0,h],c-[0,0,h]])
    if N==6:  # octahedron edge R
        return np.array([[R/np.sqrt(2),0,0],[-R/np.sqrt(2),0,0],[0,R/np.sqrt(2),0],[0,-R/np.sqrt(2),0],[0,0,R/np.sqrt(2)],[0,0,-R/np.sqrt(2)]])
def cluster(N,ns=400000):
    C=centres(N); A_out=0.0; V=0.0; A_film=0.0; films=0
    for i in range(N):
        # outer cap: points on sphere i kept if in Voronoi cell i
        v=rng.normal(size=(ns,3)); v/=np.linalg.norm(v,axis=1)[:,None]; X=C[i]+R*v
        d=np.linalg.norm(X[:,None,:]-C[None,:,:],axis=2); keep=(d.argmin(1)==i); A_out+=4*np.pi*R*R*keep.mean()
        # volume of cell i: points in sphere i kept if in Voronoi cell i
        u=rng.random(ns)**(1/3); w=rng.normal(size=(ns,3)); w/=np.linalg.norm(w,axis=1)[:,None]; Y=C[i]+R*u[:,None]*w
        d=np.linalg.norm(Y[:,None,:]-C[None,:,:],axis=2); V+=4/3*np.pi*R**3*(d.argmin(1)==i).mean()
    for i,j in itertools.combinations(range(N),2):
        dij=np.linalg.norm(C[i]-C[j])
        if dij>2*R-1e-9: continue
        m=(C[i]+C[j])/2; n=(C[j]-C[i])/dij; a=np.cross(n,[0.3,0.7,0.1]); a/=np.linalg.norm(a); b=np.cross(n,a)
        rd=np.sqrt(R*R-(dij/2)**2); r=rd*np.sqrt(rng.random(ns)); th=2*np.pi*rng.random(ns)
        X=m+r[:,None]*(np.cos(th)[:,None]*a+np.sin(th)[:,None]*b)
        d=np.linalg.norm(X[:,None,:]-C[None,:,:],axis=2); dm=np.sort(d,axis=1)
        keep=(np.abs(d[:,i]-d[:,j])<1e-9)&(d[:,i]<=dm[:,0]+1e-9)   # equidistant to i,j and no closer centre
        A_film+=np.pi*rd*rd*keep.mean(); films+=1
    return A_out,A_film,V,films
print(" N  films  cluster area  separate area  saved   saved/saved(2)   C=films  C^2")
base=None
for N in (2,3,4,5,6):
    Ao,Af,V,f=cluster(N); Atot=Ao+Af; r0=(3*V/N/(4*np.pi))**(1/3); Asep=N*4*np.pi*r0**2; saved=Asep-Atot
    if base is None: base=saved
    print(f"{N:2d}  {f:3d}    {Atot:7.3f}       {Asep:7.3f}     {saved:6.3f}   {saved/base:7.2f}        {f:3d}   {f*f:4d}")
