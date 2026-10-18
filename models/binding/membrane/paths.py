"""paths.py — BUILD-SPEC §6 quasi-static load paths on T (resumable driver). Implementer: Grace (Claude Opus 5.5).
P1 = capsid 0 (proton), P2 = 1, P3 = 2 (neutrons). Load F on P1's centroid; P2, P3 centroids tethered (TETHER_K) at their
relaxed positions — DECLARED deviation: with only the system centroid pinned, rigid rotation is a zero mode that turns any
tangential load radial; the tethers stand for the inertia of P2, P3 (impulsive limit). The P2 counter-roll (SPEC §6.4) is
therefore suppressed in the centroid motion but not in the skins.
Coarse steps F_STEP_COARSE until snap, then bisection to F_STEP_FINE.  Snap := P1 loses contact (g<0.5 delta) with P2 or P3,
or P1's centroid moves > 0.5 fm from its last stable position in one step.
Usage: python3 paths.py init <base_job> | python3 paths.py advance | python3 paths.py report"""
import sys,os,json,numpy as np
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import jobs, constants as K
PD=os.path.join(jobs.HERE,'results','paths'); os.makedirs(PD,exist_ok=True)
def frames(X):
    c=X.mean(1); hub=c.mean(0); r=(c[0]-hub)/np.linalg.norm(c[0]-hub)
    n=np.cross(c[1]-c[0],c[2]-c[0]); n/=np.linalg.norm(n)
    t=(c[2]-c[0]); t=t-(t@r)*r; t/=np.linalg.norm(t)
    return dict(radial=r,tangential=t,outofplane=n),c
def init(base):
    j=jobs.load(base); S=jobs.build(j); X=j['x'].reshape(S.C,-1,3); dirs,c=frames(X)
    for path,u in dirs.items():
        st=dict(base=base,path=path,u=u.tolist(),c0=c.tolist(),x_stable=j['x'].tolist(),F_stable=0.0,F_try=K.F_STEP_COARSE,
                phase='coarse',hi=None,steps=[],done=False)
        json.dump(st,open(os.path.join(PD,path+'.json'),'w'))
def jobname(st,F): return f"path_{st['base']}_{st['path']}_F{F:.4f}"   # base in the name: v1 and v2 paths must not share job files
def submit(st):
    j=jobs.load(st['base']); a=dict(j['args']); F=st['F_try']
    a['fext']={0:(F*np.array(st['u'])).tolist()}; a['tether']={1:st['c0'][1],2:st['c0'][2]}
    jobs.submit(jobname(st,F),'builders:nucleus',a,x0=np.array(st['x_stable']))
def measure(S,x,st):
    from analyse import patch
    X=x.reshape(S.C,-1,3); c=X.mean(1); hub=np.array(st['c0']).mean(0)
    con=S.contacts(x); p12=(0,1) in con; p13=(0,2) in con
    m={}
    for (a,b) in ((0,1),(0,2),(1,2)):
        pa=patch(S,X,a,b,hub)
        m[f'{a}{b}']=None if pa is None else dict(E=pa['E_patch'],wg=pa.get('well_minus_geom_hub'),go=pa.get('geom_offset_hub'),
                                               hub_half=pa.get('hub_half_fraction'),n=pa['n_vertices'],aspect=pa['aspect'])
    c0=np.array(st['c0']); n=np.cross(c0[1]-c0[0],c0[2]-c0[0]); n/=np.linalg.norm(n)
    v0=c0[0]-c0[2]; v1=c[0]-c[2]; v1p=v1-(v1@n)*n
    theta=np.degrees(np.arctan2(np.cross(v0,v1p)@n,v0@v1p))
    # P1 spin (Kabsch) relative to the base state
    Xb=np.array(jobs.load(st['base'])['x']).reshape(S.C,-1,3)[0]; A=Xb-Xb.mean(0); B=X[0]-c[0]
    U,_,Vt=np.linalg.svd(A.T@B); dd=np.sign(np.linalg.det(U@Vt)); R=(U@np.diag([1,1,dd])@Vt).T
    ang=np.degrees(np.arccos(np.clip((np.trace(R)-1)/2,-1,1)))
    axis=np.array([R[2,1]-R[1,2],R[0,2]-R[2,0],R[1,0]-R[0,1]]); axis=axis/np.linalg.norm(axis) if np.linalg.norm(axis)>1e-12 else axis
    return dict(contact12=p12,contact13=p13,theta_roll_deg=float(theta),spin_deg=float(ang),spin_axis_dot_n=float(axis@n),
                dP1=float(np.linalg.norm(c[0]-c0[0])),patches=m)
def advance():
    active=[]
    for f in sorted(x for x in os.listdir(PD) if x.endswith('.json')):
        st=json.load(open(os.path.join(PD,f)))
        if st['done']: continue
        n=jobname(st,st['F_try'])
        if not os.path.exists(jobs.path(n)): submit(st); active.append(n); continue
        jb=jobs.load(n)
        if not jb['done']:
            if jb['nit']>3000 and jb['x'] is not None:      # runaway check: a load with no resistance never converges
                Sx=jobs.build(jb); C=Sx.C
                mv=np.linalg.norm(np.array(jb['x']).reshape(C,-1,3)[0].mean(0)-np.array(st['x_stable']).reshape(C,-1,3)[0].mean(0))
                if mv>0.5 or jb['nit']>20000:
                    jb['done']=True; jb['runaway']=True; import pickle; pickle.dump(jb,open(jobs.path(n),'wb'))
            if not jb['done']: active.append(n); continue
        S=jobs.build(jb); m=measure(S,jb['x'],st); m['F']=st['F_try']
        moved=np.linalg.norm(np.array(jb['x']).reshape(S.C,-1,3)[0].mean(0)-np.array(st['x_stable']).reshape(S.C,-1,3)[0].mean(0))
        snap=(not m['contact12']) or (not m['contact13']) or moved>0.5 or bool(jb.get('runaway'))
        m['creep']=bool(jb.get('runaway') and moved<=0.5)
        m['snap']=bool(snap); st['steps'].append(m)
        if not snap:
            st['x_stable']=jb['x'].tolist(); st['F_stable']=st['F_try']
            st['F_try']=st['F_try']+K.F_STEP_COARSE if st['hi'] is None else 0.5*(st['F_stable']+st['hi'])
        else:
            st['hi']=st['F_try']; st['phase']='bisect'; st['F_try']=0.5*(st['F_stable']+st['hi'])
        if st['hi'] is not None and st['hi']-st['F_stable']<=K.F_STEP_FINE+1e-9: st['done']=True
        if st['F_try']>20: st['done']=True
        tmp=os.path.join(PD,f+'.tmp'); json.dump(st,open(tmp,'w')); os.replace(tmp,os.path.join(PD,f))
        if not st['done']: submit(st); active.append(jobname(st,st['F_try']))
    json.dump(active,open(os.path.join(jobs.HERE,'results','queue_paths.json'),'w'))
    return active
if __name__=='__main__':
    if sys.argv[1]=='init': init(sys.argv[2])
    elif sys.argv[1]=='advance': print(advance())
    elif sys.argv[1]=='report':
        for f in sorted(x for x in os.listdir(PD) if x.endswith('.json')):
            st=json.load(open(os.path.join(PD,f)))
            print(st['path'],'done' if st['done'] else 'running','F_stable',st['F_stable'],'hi',st['hi'])
            for m in st['steps']:
                p13=m['patches']['02']; p12=m['patches']['01']; p23=m['patches']['12']
                print(f"  F={m['F']:.3f} snap={m['snap']} c12={m['contact12']} c13={m['contact13']} roll={m['theta_roll_deg']:+.2f} spin={m['spin_deg']:.2f} dP1={m['dP1']:.3f}"
                      f" | P1P2 E={p12['E'] if p12 else 0:+.3f} wg={(p12 or {}).get('wg') or 0:+.4f} | P1P3 E={p13['E'] if p13 else 0:+.3f} wg={(p13 or {}).get('wg') or 0:+.4f} hub-half={(p13 or {}).get('hub_half') or 0:.3f}"
                      f" | P2P3 E={p23['E'] if p23 else 0:+.3f} wg={(p23 or {}).get('wg') or 0:+.4f}")
