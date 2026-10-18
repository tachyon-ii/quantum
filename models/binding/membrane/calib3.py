"""calib3.py — v3 lane/graph cooperativity: same state machine as calib2 with E1 -> lam. Rows x variants (lane_mode, lane_form). Implementer: Grace (Claude Fable 5.1), 18 Oct 2026.
Per row (r, delta, kb): stage 'D' -> E0 = (BE_D - 2Y(2)) / (-f_D)  (D has no coop term; exact scaling in E0)
                        stage 'He4' -> secant/bisection on E1 so that BE(He4) = BE_HE4 (tol 0.05 MeV; E1 >= 0)
                        stage 'blind' -> T, He3 at (E0, E1); stage 'done'.
State in results/calib2.json. Usage: python3 calib2.py advance  (submits/collects jobs; run runpar on results/queue_v2.json between calls)"""
import sys,os,json,numpy as np
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,HERE)
import jobs, constants as K
from energy import E_MESH
SF=os.path.join(HERE,'results','calib3.json')
TOL=0.05; LAM_MAX=12.0
VARIANTS=[('triplet','linear'),('all','linear'),('triplet','sat')]
def rows():
    base=[dict(r=1,di=1,kb=0.2),dict(r=1,di=2,kb=0.2),dict(r=1,di=2,kb=0.3),dict(r=3,di=2,kb=0.3)]
    return [dict(b,mode=m,form=f) for (m,f) in VARIANTS for b in base]
def key(row): return f"r{row['r']}_d{row['di']}_kb{row['kb']}_{row['mode']}_{row['form']}"
def load():
    if os.path.exists(SF): return json.load(open(SF))
    return {key(rw):dict(row=rw,stage='D',E0=None,E1=None,he4=[],blind={},flags=[]) for rw in rows()}
def save(st):
    tmp=SF+'.tmp'; json.dump(st,open(tmp,'w'),indent=1); os.replace(tmp,SF)
def jn(k,tag): return f"v3_{k}_{tag}"
def sub(k,tag,nuc,E0,lam,row):
    jobs.submit(jn(k,tag),'builders:nucleus',dict(name=nuc,r=row['r'],E0=E0,delta=K.DELTA_GRID[row['di']],kbend_fac=row['kb'],lam=lam,lane_mode=row['mode'],lane_form=row['form']))
def be_of(name):
    j=jobs.load(name); S=jobs.build(j); be,p=S.binding(j['x']); X=j['x'].reshape(S.C,-1,3); c=X.mean(1)
    dmin=min(np.linalg.norm(c[a]-c[b]) for a in range(S.C) for b in range(a+1,S.C)); rmax=max(np.linalg.norm(X[i]-c[i],axis=1).max() for i in range(S.C))
    return be,p,dmin,rmax
def _clone_if_possible(k,tag,st):
    """D1 and He4_lam_0 are lam-independent: reuse another variant's finished job for the same (r,di,kb)."""
    import shutil
    row=st[k]['row']
    for k2,rec2 in st.items():
        r2=rec2['row']
        if (r2['r'],r2['di'],r2['kb'])==(row['r'],row['di'],row['kb']) and k2!=k:
            p2=jobs.path(jn(k2,tag))
            if os.path.exists(p2) and jobs.load(jn(k2,tag))['done']:
                shutil.copy(p2,jobs.path(jn(k,tag))); return True
    return False
def advance():
    st=load(); active=[]
    for k,rec in st.items():
        row=rec['row']
        if rec['stage']=='D':
            n=jn(k,'D1')
            if not os.path.exists(jobs.path(n)) and not _clone_if_possible(k,'D1',st): sub(k,'D1','D',1.0,0.0,row); active.append(n); continue
            if not jobs.load(n)['done']: active.append(n); continue
            be,p,dmin,rmax=be_of(n); fD=p['cont']
            rec['fD']=fD; rec['dmin_D']=dmin; rec['rmax_D']=rmax
            if fD>=0: rec['stage']='dead'; rec['flags'].append('D unbound at E0=1'); continue
            rec['E0']=(K.BE_D-2*K.Y(K.SLING_N))/(-fD); rec['e0']=row['r']*rec['E0']/(4*np.pi*K.RP**2)
            if dmin<1.3 or rmax>1.2: rec['flags'].append(f'D engulfed (dmin {dmin:.2f}, rmax {rmax:.2f})')
            rec['stage']='He4'; rec['he4']=[]
        if rec['stage']=='He4':
            # sequence of E1 trials; each entry: [E1, BE or None]
            e0=rec['e0']
            if not rec['he4']: rec['he4']=[[0.0,None]]
            cur=rec['he4'][-1]
            n=jn(k,f"He4_lam_{cur[0]:.5f}")
            if cur[1] is None:
                if not os.path.exists(jobs.path(n)) and cur[0]==0.0 and _clone_if_possible(k,'He4_lam_0.00000',st): pass
                elif not os.path.exists(jobs.path(n)):
                    x0=None
                    if len(rec['he4'])>1:
                        prev=jn(k,f"He4_lam_{rec['he4'][-2][0]:.5f}"); x0=jobs.load(prev)['x']
                    sub(k,n[len(f'v3_{k}_'):],'He4',rec['E0'],cur[0],row)
                    if x0 is not None:
                        j=jobs.load(n); j['x']=x0; import pickle; pickle.dump(j,open(jobs.path(n),'wb'))
                    active.append(n); continue
                if not jobs.load(n)['done']: active.append(n); continue
                be,p,dmin,rmax=be_of(n); cur[1]=be; cur.append(dict(dmin=dmin,rmax=rmax,coop=p['coop'],adh=p['adh'],contacts=len(p['contacts']),all_triplet=p['all_triplet'],lane_factors=p['lane_factors']))
            if cur[2]['dmin']<1.3 or cur[2]['rmax']>1.2: rec['flags'].append(f"He4 engulfed at lam={cur[0]:.3f} (dmin {cur[2]['dmin']:.2f}, rmax {cur[2]['rmax']:.2f})"); rec['stage']='dead'; continue
            # decide next E1
            pts=[(a,b) for a,b,*_ in rec['he4']]
            tgt=K.BE_HE4
            if abs(pts[-1][1]-tgt)<TOL:
                rec['E1']=pts[-1][0]; rec['stage']='blind'   # rec['E1'] holds lam here
            else:
                lo=[(a,b) for a,b in pts if b<tgt]; hi=[(a,b) for a,b in pts if b>tgt]
                if lo and hi:
                    (a1,b1)=max(lo,key=lambda t:t[1]); (a2,b2)=min(hi,key=lambda t:t[1])
                    nxt=a1+(tgt-b1)*(a2-a1)/(b2-b1)
                    nxt=min(max(nxt,a1+0.1*(a2-a1)),a2-0.1*(a2-a1))
                elif not hi:
                    if len(pts)==1: nxt=1.0
                    else:
                        (a1,b1),(a2,b2)=pts[-2],pts[-1]
                        nxt=a2+(tgt-b2)*(a2-a1)/(b2-b1) if b2>b1 else 2*a2
                        nxt=min(max(nxt,1.5*a2),3*a2) if a2>0 else 1.0
                    if nxt>LAM_MAX: rec['stage']='dead'; rec['flags'].append(f'He4 unreachable: lam > {LAM_MAX}'); continue
                else:
                    rec['stage']='dead'; rec['flags'].append('He4 overbound at E1=0'); continue
                rec['he4'].append([float(nxt),None])
                n=jn(k,f"He4_lam_{nxt:.5f}"); sub(k,n[len(f'v3_{k}_'):],'He4',rec['E0'],float(nxt),row)
                prev=jn(k,f"He4_lam_{pts[-1][0]:.5f}"); j=jobs.load(n); j['x']=jobs.load(prev)['x']; import pickle; pickle.dump(j,open(jobs.path(n),'wb'))
                active.append(n); continue
        if rec['stage']=='blind':
            todo=[]
            for nuc in ('T','He3'):
                n=jn(k,nuc)
                if not os.path.exists(jobs.path(n)): sub(k,nuc,nuc,rec['E0'],rec['E1'],row)
                if not jobs.load(n)['done']: todo.append(n)
                elif nuc not in rec['blind']:
                    be,p,dmin,rmax=be_of(n); rec['blind'][nuc]=dict(BE=be,dmin=dmin,rmax=rmax,coop=p['coop'],adh=p['adh'],coul=p['coul'],mesh=p['mesh'],sling=p['sling'],contacts=len(p['contacts']),lane_factors=p['lane_factors'])
            if todo: active+=todo; continue
            rec['stage']='done'
    save(st); json.dump(active,open(os.path.join(HERE,'results','queue_v3.json'),'w'))
    return st,active
if __name__=='__main__':
    st,act=advance()
    for k,rec in st.items(): print(k,rec['stage'],'E0=%.3f'%rec['E0'] if rec['E0'] else '','E1=%.3f'%rec['E1'] if rec['E1'] is not None else '',rec['flags'],{n:round(v['BE'],3) for n,v in rec['blind'].items()})
    print(len(act),'active')
