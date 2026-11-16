"""kernel/lanes.py — closed lanes as bodies (the vocabulary DEEPDIVE-conform-foam §3 asked for). ZERO fitted numbers.
Bodies are rigid BCC-lattice motifs (unit R_p; contacts d^2=3 'H' and d^2=4 'S', as seat.py):
   alpha (tetrahedron, C=6), T / 3He (triangle, C=3), D (C=1), 2n (C=1, singlet), single n / p (no lane).
Energy of a composite (MeV):
   BE = Y(2)*n_gated + sum_lanes [u*C^2 - MESH*n_singlet] - Coulomb(all pp pairs, exact positions) + u*ATT
   u = Q_beta = m_n - m_p - m_e ; MESH = 0.854 (np-singlet datum) ; Y(2) from masses ; n_gated = nucleons with an unlike neighbour.
ATT is the attachment count between different bodies. It is NOT derived; every candidate rule is run and reported (R11):
   contacts | np contacts | np - like | triangles spanning bodies | newcomer nucleons touching | none
each with single nucleons either REFUSED by lanes (no attachment, no slingshot) or COUNTED like any body.
All placements (48 orientations x translations in a +-8 box, both species variants of each motif) are enumerated; the
ground state per rule is the maximum. Per-capsid slingshot bookkeeping (Option I) throughout — see DEEPDIVE-C2-lane §8.
Usage: lanes.py NAME ...  (resumable; results/lanes_NAME.json). Grace (Claude Fable 5.2), 17 Nov 2026."""
import numpy as np,itertools,sys,os,json
import data as D
HERE=os.path.dirname(os.path.abspath(__file__))
U=D.MN-D.MP-D.ME; MESH=0.854; Y2=D.Y(2)
MATS=[]
for perm in itertools.permutations(range(3)):
    for signs in itertools.product([1,-1],repeat=3):
        M=np.zeros((3,3),int)
        for r,pc in enumerate(perm): M[r,pc]=signs[r]
        MATS.append(M)
TET=[(0,0,0),(2,0,0),(1,1,1),(1,1,-1)]; TRI=[(0,0,0),(2,0,0),(1,1,1)]
# name -> list of variants (sites, species string); C; n_singlet; is_single
BODIES={'a':([(TET,'pnpn'),(TET,'ppnn')],6,2,False),
        't':([(TRI,'nnp'),(TRI,'pnn'),(TRI,'npn')],3,1,False), 'h':([(TRI,'ppn'),(TRI,'npp'),(TRI,'pnp')],3,1,False),
        'd':([([(0,0,0),(2,0,0)],'pn'),([(0,0,0),(1,1,1)],'pn')],1,0,False),
        '2n':([([(0,0,0),(2,0,0)],'nn'),([(0,0,0),(1,1,1)],'nn')],1,1,False),
        'n':([([(0,0,0)],'n')],0,0,True), 'p':([([(0,0,0)],'p')],0,0,True)}
def adj(S):
    d2=((S[:,None]-S[None])**2).sum(-1); return (d2==3)|(d2==4)
def orient(sites,sp):
    seen={}; S=np.array(sites)
    for M in MATS:
        T=S@M.T; T=T-T[0]                     # anchor first site at origin (translations cover the rest)
        key=tuple(sorted((tuple(x),c) for x,c in zip(T.tolist(),sp)))
        seen[key]=(T,np.array([c=='p' for c in sp]))
    return list(seen.values())
r=range(-8,9); TR=np.array([v for v in itertools.product(r,repeat=3) if len({x%2 for x in v})==1])
NF=10  # features: 0 nc 1 nnp 2 tri 3 touch | 4 nc_s 5 nnp_s 6 tri_s 7 touch_s | 8 coul | 9 internal
def add(cfg,B,pb,single):
    """cfg: dict S,p,g(gated),sgl(bool per nucleon: single body),F (features). Returns list of new cfgs (vectorised over translations)."""
    S0,p0=cfg['S'],cfg['p']; A0=adj(S0); Ai=adj(B); X=B[None]+TR[:,None]
    d2=((X[:,:,None,:]-S0[None,None])**2).sum(-1); C=(d2==3)|(d2==4)
    ok=(d2.min((1,2))>0)&C.any((1,2)); X,d2,C=X[ok],d2[ok],C[ok]
    if not len(X): return None
    unlike=pb[:,None]!=p0[None]; nc=C.sum((1,2)); nnp=(C&unlike).sum((1,2)); touch=C.any(2).sum(1)
    Cf=C.astype(float); tri=np.einsum('mij,mik,jk->m',Cf,Cf,A0.astype(float))/2+np.einsum('mij,mlj,il->m',Cf,Cf,Ai.astype(float))/2
    coul=((pb[:,None]&p0[None])[None]*D.AHC/(np.sqrt(d2)*D.RP)).sum((1,2))
    gint=(Ai&(pb[:,None]!=pb[None])).any(1)
    gnew=gint[None]|(C&unlike).any(2); gold=cfg['g'][None]|(C&unlike).any(1)
    # contacts that involve a single-nucleon body (new body single, or old nucleon belonging to a single)
    if single: ncs,nnps,tris,touchs=nc,nnp,tri,touch; nc=nnp=tri=touch=np.zeros(len(X))
    else:
        Cs=C&cfg['sgl'][None,None,:]; ncs=Cs.sum((1,2)); nnps=(Cs&unlike).sum((1,2)); touchs=Cs.any(2).sum(1)*0.0
        Csf=Cs.astype(float); tris=np.einsum('mij,mik,jk->m',Csf,Cf,A0.astype(float))/2  # triangles using a single's contact (approx: counted once)
        nc=nc-ncs; nnp=nnp-nnps; tri=tri-tris
    F=np.tile(cfg['F'],(len(X),1)); 
    for k,v in enumerate((nc,nnp,tri,touch,ncs,nnps,tris,touchs,coul)): F[:,k]+=v
    return dict(X=X,gnew=gnew,gold=gold,F=F)
RULES=[('none',lambda F:0*F[:,0],lambda F:0*F[:,0]),('contacts',lambda F:F[:,0],lambda F:F[:,4]),('np contacts',lambda F:F[:,1],lambda F:F[:,5]),
       ('np - like',lambda F:2*F[:,1]-F[:,0],lambda F:2*F[:,5]-F[:,4]),('triangles',lambda F:F[:,2],lambda F:F[:,6]),('newcomer nucleons touching',lambda F:F[:,3],lambda F:F[:,7])]
def energies(F,ng_lane,ng_single):
    """returns dict rule-> BE array, for singles refused / counted."""
    out={}
    for nm,fl,fs in RULES:
        base=F[:,9]-F[:,8]+Y2*ng_lane
        out[nm+' | singles refused']=base+U*fl(F)
        out[nm+' | singles counted']=base+U*(fl(F)+fs(F))+Y2*ng_single
    return out
def body_internal(name):
    var,C,ns,single=BODIES[name]; return U*C*C-MESH*ns
def run(decomp):
    """decomp: list of body names, largest first. Returns best BE per rule + features of the best."""
    best={}
    def consider(F,ngl,ngs,tag):
        for k,E in energies(F,ngl,ngs).items():
            i=int(np.argmax(E))
            if k not in best or E[i]>best[k][0]: best[k]=(float(E[i]),F[i].tolist(),tag)
    first=decomp[0]; cfgs=[]
    for sites,sp in BODIES[first][0]:
        S=np.array(sites); p=np.array([c=='p' for c in sp]); A=adj(S)
        g=(A&(p[:,None]!=p[None])).any(1); pr=np.where(p)[0]
        coul=sum(D.AHC/(np.sqrt(((S[i]-S[j])**2).sum())*D.RP) for i,j in itertools.combinations(pr,2))
        F=np.zeros(NF); F[8]=coul; F[9]=body_internal(first)
        cfgs.append(dict(S=S,p=p,g=g,sgl=np.full(len(S),BODIES[first][3]),F=F))
    for bi,name in enumerate(decomp[1:]):
        last=(bi==len(decomp)-2); new=[]; seen=set(); single=BODIES[name][3]
        for cfg in cfgs:
            for sites,sp in BODIES[name][0]:
                for B,pb in orient(sites,sp):
                    Ai=adj(B); pr=np.where(pb)[0]
                    ci=sum(D.AHC/(np.sqrt(((B[i]-B[j])**2).sum())*D.RP) for i,j in itertools.combinations(pr,2))
                    r=add(cfg,B,pb,single)
                    if r is None: continue
                    r['F'][:,8]+=ci; r['F'][:,9]+=body_internal(name)
                    sgl=np.r_[cfg['sgl'],np.full(len(B),single)]
                    if last:
                        gall=np.c_[r['gold'],r['gnew']]; consider(r['F'],(gall&~sgl[None]).sum(1),(gall&sgl[None]).sum(1),'+'.join(decomp))
                    else:
                        for m in range(len(r['X'])):
                            S=np.r_[cfg['S'],r['X'][m]]; p=np.r_[cfg['p'],pb]
                            # dedupe up to lattice symmetry (labelled by species and single flag)
                            key=None
                            for M in MATS:
                                T=S@M.T; T=T-T.min(0); k=tuple(sorted((tuple(x),bool(c),bool(s)) for x,c,s in zip(T.tolist(),p,sgl)))
                                if key is None or k<key: key=k
                            if key in seen: continue
                            seen.add(key); new.append(dict(S=S,p=p,g=np.r_[r['gold'][m],r['gnew'][m]],sgl=sgl,F=r['F'][m]))
        if not last: cfgs=new; print(f"   {'+'.join(decomp)}: {len(cfgs)} distinct {bi+2}-body configurations",flush=True)
    if len(decomp)==1:
        c=cfgs; F=np.array([x['F'] for x in c]); ngl=np.array([(x['g']&~x['sgl']).sum() for x in c]); ngs=np.array([(x['g']&x['sgl']).sum() for x in c]); consider(F,ngl,ngs,decomp[0])
    return best
NUC={'D':((1,1),[['d']]),'T':((1,2),[['t']]),'He3':((2,1),[['h']]),'He4':((2,2),[['a']]),
     'He5':((2,3),[['a','n']]),'Li5':((3,2),[['a','p']]),'He6':((2,4),[['a','2n'],['a','n','n']]),'Li6':((3,3),[['a','d'],['t','h']]),
     'Li7':((3,4),[['a','t']]),'Be7':((4,3),[['a','h']]),'Be8':((4,4),[['a','a']]),'Li8':((3,5),[['a','t','n']]),'B8':((5,3),[['a','h','p']]),
     'Be9':((4,5),[['a','a','n']]),'B9':((5,4),[['a','a','p']]),'Be10':((4,6),[['a','a','2n']]),'B10':((5,5),[['a','a','d']]),
     'B11':((5,6),[['a','a','t']]),'C11':((6,5),[['a','a','h']]),'C12':((6,6),[['a','a','a']])}
if __name__=='__main__':
    for nm in sys.argv[1:]:
        f=os.path.join(HERE,'results',f'lanes_{nm}.json')
        if os.path.exists(f): continue
        (Z,N),decs=NUC[nm]; best={}
        for dec in decs:
            b=run(dec)
            for k,v in b.items():
                if k not in best or v[0]>best[k][0]: best[k]=v
        json.dump(dict(Z=Z,N=N,meas=D.BE.get((Z,N)),best=best),open(f+'.tmp','w'),indent=1); os.replace(f+'.tmp',f)
        print(nm,'meas',D.BE.get((Z,N)),{k:round(v[0],2) for k,v in best.items() if 'refused' in k},flush=True)
