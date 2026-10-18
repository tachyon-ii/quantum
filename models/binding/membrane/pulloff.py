"""pulloff.py — BUILD-SPEC v2 §4: the pull-off (peak-strength) peel profile of a patch. Implementer: Grace (Claude Fable 5.1), 18 Oct 2026.
F(s) = b(s) * G(s): front width (chord of the contact outline at coordinate s along the lift axis) times local line energy
(adhesion + cooperative density at the front, e(s) = e0*s + E1*coop, per unit area == Kendall line energy).
Reports F_max, s*, and the stable-branch ('tinkle') energy fraction = patch energy on the far side of s* from where the front starts.
Two fronts: 'tangential' (front runs from the outer point toward the hub) and 'axisymmetric' (b = 2 pi rho about the energy centroid)."""
import sys,os,json,numpy as np
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import jobs
from mesh import face_geom
def patch_field(S,X,i,j):
    """vertices of i in the well of j with their areas, local densities e_v (MeV/fm^2) and positions."""
    idx,f,g,P=S.gaps(X,i,j); s,_=S.s(g); m=s>0.01
    if not m.any(): return None
    a,b,c,n,nn=face_geom(X[i],S.T.F); Av=S.T.S@np.tile(0.5*nn,3)/3
    # cooperative density at these vertices: E1 * sum_{k != j} s_j s_k  (the part of the coop energy that this front releases)
    coop=np.zeros(len(idx))
    for k in range(S.C):
        if k in (i,j): continue
        idk,fk,gk,Pk=S.gaps(X,i,k)
        if len(idk)==0: continue
        sk,_=S.s(gk); mp={v:q for v,q in zip(idk,sk)}
        coop+=np.array([mp.get(v,0.0) for v in idx])*s
    e=S.e0*s+S.E1*coop
    return dict(v=idx[m],A=Av[idx][m],e=e[m],x=X[i][idx][m],s=s[m])
def profile(S,X,i,j,hub,nb=12):
    pf=patch_field(S,X,i,j)
    if pf is None: return None
    ci,cj=X[i].mean(0),X[j].mean(0); ax=(cj-ci)/np.linalg.norm(cj-ci); P2=np.eye(3)-np.outer(ax,ax)
    w=pf['A']*pf['e']; cE=(w[:,None]*pf['x']).sum(0)/w.sum(); Etot=w.sum()
    out={'E_patch':float(Etot),'n':int(len(pf['v']))}
    # --- tangential front: coordinate u along the hub direction (outer point = min u) ---
    if hub is not None:
        h=(hub-(ci+cj)/2)@P2; h/=np.linalg.norm(h); perp=np.cross(ax,h)
        u=(pf['x']-cE)@h; t=(pf['x']-cE)@perp
        edges=np.linspace(u.min(),u.max(),nb+1); rows=[]
        for k in range(nb):
            sel=(u>=edges[k])&(u<=edges[k+1]+1e-12)
            if sel.sum()<2: continue
            b=np.ptp(t[sel]); G=(pf['A'][sel]*pf['e'][sel]).sum()/pf['A'][sel].sum()
            rows.append(dict(u=float((edges[k]+edges[k+1])/2),b=float(b),G=float(G),F=float(b*G),E_bin=float((pf['A'][sel]*pf['e'][sel]).sum())))
        if rows:
            F=np.array([r['F'] for r in rows]); k=int(F.argmax()); ustar=rows[k]['u']
            tinkle=sum(r['E_bin'] for r in rows[:k])/Etot    # energy the front has already paid before the peak, starting at the outer point
            out['tangential']=dict(rows=rows,F_max=float(F[k]),u_star=float(ustar),u_range=[float(u.min()),float(u.max())],tinkle_fraction=float(tinkle))
    # --- axisymmetric front about the energy centroid ---
    d=(pf['x']-cE)@P2; rho=np.linalg.norm(d,axis=1); edges=np.linspace(0,rho.max(),nb+1); rows=[]
    for k in range(nb):
        sel=(rho>=edges[k])&(rho<=edges[k+1]+1e-12)
        if sel.sum()<1: continue
        rm=(edges[k]+edges[k+1])/2; G=(pf['A'][sel]*pf['e'][sel]).sum()/pf['A'][sel].sum()
        rows.append(dict(rho=float(rm),b=float(2*np.pi*rm),G=float(G),F=float(2*np.pi*rm*G),E_bin=float((pf['A'][sel]*pf['e'][sel]).sum())))
    F=np.array([r['F'] for r in rows]); k=int(F.argmax())
    out['axisymmetric']=dict(rows=rows,F_max=float(F[k]),rho_star=float(rows[k]['rho']),rho_max=float(rho.max()),
                             tinkle_fraction=float(sum(r['E_bin'] for r in rows[k+1:])/Etot))
    return out
def run(name):
    j=jobs.load(name); S=jobs.build(j); X=j['x'].reshape(S.C,-1,3); hub=X.mean(1).mean(0) if S.C>2 else None
    res={}
    for a in range(S.C):
        for b in range(a+1,S.C):
            pr=profile(S,X,a,b,hub)
            if pr: res[f'{a}{S.sp[a]}-{b}{S.sp[b]}']=pr
    return res
if __name__=='__main__':
    for n in sys.argv[1:]:
        res=run(n); print(n)
        for k,v in res.items():
            ax=v['axisymmetric']; line=f"  {k}: E_patch={v['E_patch']:.3f} | axisym: F_max={ax['F_max']:.3f} MeV/fm at rho*/rho_max={ax['rho_star']/ax['rho_max']:.2f}, tinkle={ax['tinkle_fraction']:.2f}"
            if 'tangential' in v:
                t=v['tangential']; ur=t['u_range']; line+=f" | tangential: F_max={t['F_max']:.3f} at u*={(t['u_star']-ur[0])/(ur[1]-ur[0]):.2f} of point->hub, tinkle={t['tinkle_fraction']:.2f}"
            print(line)
        json.dump(res,open(os.path.join(jobs.HERE,'results',f'pulloff_{n}.json'),'w'),indent=1)
