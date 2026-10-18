"""analyse.py — BUILD-SPEC §7.1 (energies, radii) and §7.2 (patch geometry). Implementer: Grace (Claude Opus 5.5)."""
import sys,os,json,numpy as np
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import jobs, constants as K
def patch(S,X,i,j,hub=None,thr=0.01):
    idx,f,g,P=S.gaps(X,i,j)
    if len(idx)==0: return None
    s,_=S.s(g); m=s>thr
    if not m.any(): return None
    Av=S.T.S@np.tile(0.5*np.linalg.norm(np.cross(X[i][S.T.F[:,1]]-X[i][S.T.F[:,0]],X[i][S.T.F[:,2]]-X[i][S.T.F[:,0]]),axis=1),3)/3
    v=idx[m]; w=Av[v]*s[m]; xv=X[i][v]; a=Av[v]
    cw=(w[:,None]*xv).sum(0)/w.sum(); cg=(a[:,None]*xv).sum(0)/a.sum()
    ci,cj=X[i].mean(0),X[j].mean(0); ax=(cj-ci)/np.linalg.norm(cj-ci)
    # in-plane second moments (energy-weighted)
    P2=np.eye(3)-np.outer(ax,ax); d=(xv-cw)@P2
    M=(w[:,None,None]*d[:,:,None]*d[:,None,:]).sum(0)/w.sum(); ev=np.sort(np.linalg.eigvalsh(M))[::-1]
    out=dict(area_weighted=float(w.sum()),area_touch=float(a.sum()),n_vertices=int(m.sum()),
             aspect=float(np.sqrt(ev[0]/max(ev[1],1e-30))),E_patch=float(-S.e0*w.sum()))
    if hub is not None:
        h=(hub-(ci+cj)/2)@P2; h/=np.linalg.norm(h)
        out.update(well_minus_geom_hub=float((cw-cg)@h), geom_offset_hub=float((cg-(ci+cj)/2)@h),
                   hub_half_fraction=float(w[((xv-cg)@h)>0].sum()/w.sum()),
                   radial_extent_hub=float(((xv-cg)@h).max()), radial_extent_out=float(-((xv-cg)@h).min()))
        # width profile along the hub axis: front width at hub end vs outer end (for 7.4)
        u=(xv-cg)@h; perp=np.cross(ax,h); wv=(xv-cg)@perp
        lo,hi=u.min(),u.max(); bins=np.linspace(lo,hi,7); prof=[]
        for k in range(6):
            sel=(u>=bins[k])&(u<=bins[k+1])
            prof.append(dict(u=float((bins[k]+bins[k+1])/2),width=float(np.ptp(wv[sel])) if sel.sum()>1 else 0.0,
                             mean_s=float(s[m][sel].mean()) if sel.any() else 0.0))
        out['profile_out_to_hub']=prof
    return out
def nucleus_report(name):
    j=jobs.load(name); S=jobs.build(j); x=j['x']; X=x.reshape(S.C,-1,3); be,p=S.binding(x)
    c=X.mean(1); cm=c.mean(0); hub=cm if S.C>2 else None
    pr=[i for i in range(S.C) if S.sp[i]=='p']
    rch=float(np.sqrt(np.mean([np.sum((c[i]-cm)**2) for i in pr])+K.RP**2))
    pairs={}
    for a in range(S.C):
        for b in range(a+1,S.C):
            pa=patch(S,X,a,b,hub); 
            if pa: pairs[f"{a}{S.sp[a]}-{b}{S.sp[b]}"]=dict(d=float(np.linalg.norm(c[a]-c[b])),**pa)
    return dict(BE=float(be),parts={k:float(v) for k,v in p.items() if isinstance(v,(float,np.floating))},
                contacts=p['contacts'],Rch_classical=rch,pairs=pairs,species=S.sp,e0=S.e0,E0=S.E0,delta=S.delta)
if __name__=='__main__':
    out={n:nucleus_report(n) for n in sys.argv[1:] if jobs.load(n)['done']}
    for n,r in out.items():
        print(f"{n}: BE={r['BE']:.3f} MeV  Rch(classical)={r['Rch_classical']:.3f} fm  mesh={r['parts']['mesh']:.3f} sling={r['parts']['sling']:.3f} coul={r['parts']['coul']:.3f}")
        for k,v in r['pairs'].items():
            extra='' if 'well_minus_geom_hub' not in v else f" well-geom(hub)={v['well_minus_geom_hub']:+.4f} geom-off(hub)={v['geom_offset_hub']:+.4f} hub-half={v['hub_half_fraction']:.3f} ext hub/out={v['radial_extent_hub']:.3f}/{v['radial_extent_out']:.3f}"
            print(f"   {k}: d={v['d']:.3f} E_patch={v['E_patch']:+.3f} n={v['n_vertices']} aspect={v['aspect']:.3f}{extra}")
    json.dump(out,open(os.path.join(jobs.HERE,'results','analyse_'+'_'.join(sorted({n.split('_')[0] for n in out}))+'.json'),'w'),indent=1)
