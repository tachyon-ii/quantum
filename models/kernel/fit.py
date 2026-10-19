"""kernel/fit.py — rung-0 table fit (SPEC v5 §4): LP with anchors as equalities, holes as inequalities, L1 residual on training;
complexity ladder by descriptor projection. Alternation: seat (argmax over seatings at current g) -> fit -> re-seat.
Grace (Claude Fable 5.1), 19 Oct 2026."""
import sys,os,json,pickle,itertools,numpy as np
from scipy.optimize import linprog
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import data as D, seat as S
HERE=os.path.dirname(os.path.abspath(__file__))
LEVELS={  # name -> projection of full key (pair,type,c,zmin,zmax) to table key
 'L0 pair2+c3':      lambda k:( 'np' if k[0]=='np' else 'same', min(k[2],2)),
 'L1 +type':         lambda k:( 'np' if k[0]=='np' else 'same', min(k[2],2), k[1]),
 'L2 +nn/pp':        lambda k:( k[0], min(k[2],2), k[1]),
 'L3 +c>=3':         lambda k:( k[0], min(k[2],3), k[1]),
 'L4 +zmax>=4 flag': lambda k:( k[0], min(k[2],3), k[1], int(k[4]>=4)),
}
def load_seatings(names):
    cache=os.path.join(HERE,'results','seatings.pkl'); st=pickle.load(open(cache,'rb')) if os.path.exists(cache) else {}
    for n in names:
        if n in st: continue
        Z,N=D.ZN[n]; st[n]=S.seatings(Z+N,Z); pickle.dump(st,open(cache,'wb'))
    return st
def design(seats,proj,keys):
    """rows: one per seating -> (coef vector over table keys, constant term = -coul + sling)"""
    idx={k:i for i,k in enumerate(keys)}; A_=np.zeros((len(seats),len(keys))); b=np.zeros(len(seats))
    for r,s in enumerate(seats):
        for k,cnt in s['feats'].items(): A_[r,idx[proj(k)]]+=cnt
        A=len(s['sp']); b[r]=-s['coul']+(A*D.Y(2) if (s['connected'] and s['triplet']) else 0.0)
    return A_,b
def fit_level(level,train,holes,st,iters=12,tol_hole=0.0,verbose=True,reg=0.02,gmax=12.0):
    proj=LEVELS[level]
    keys=sorted({proj(k) for n in train+holes for s in st[n] for k in s['feats']},key=str)
    n=len(keys); des={m:design(st[m],proj,keys) for m in train+holes}
    g=np.full(n,1.0)
    hist=[]
    for it in range(iters):
        # seat: best seating per training nucleus at current g
        best={m:int(np.argmax(des[m][0]@g+des[m][1])) for m in train}
        # LP variables: g (n), slack+ and slack- per training nucleus (2*len(train)); minimise sum of slacks (anchors exact)
        nt=len(train); nv=n+2*nt+n          # g, slacks, |g| auxiliaries (L1 regularisation = MDL proxy)
        c=np.zeros(nv); c[n:n+2*nt]=1.0; c[n+2*nt:]=reg
        for t_i,m in enumerate(train):
            if m in D.ANCHORS or m in D.OPEN_ANCHORS: c[n+2*t_i]=c[n+2*t_i+1]=1e4   # anchors: effectively exact
        A_eq=np.zeros((nt,nv)); b_eq=np.zeros(nt)
        for t_i,m in enumerate(train):
            r=best[m]; A_eq[t_i,:n]=des[m][0][r]; A_eq[t_i,n+2*t_i]=1; A_eq[t_i,n+2*t_i+1]=-1; b_eq[t_i]=D.target(m)-des[m][1][r]
        # inequalities: (a) chosen seating is the ground state: for other seatings r' of m: E(r') <= E(r)  (top competitors only)
        A_ub=[]; b_ub=[]
        for m in train:
            Am,bm=des[m]; r=best[m]; E=Am@g+bm; comp=np.argsort(-E)[:200]
            for rp in comp:
                if rp==r: continue
                row=np.zeros(nv); row[:n]=Am[rp]-Am[r]; A_ub.append(row); b_ub.append(bm[r]-bm[rp])
        # (b) holes: every seating of a hole nucleus has BE <= threshold BE + tol
        for h in holes:
            Z,N,e,thr=D.HOLES[h]; Ah,bh=des[h]
            if h in ('nn','pp'): thrBE=0.0
            elif h=='He5' or h=='Li5': thrBE=D.target('He4')
            else: continue
            for rp in range(len(Ah)):
                row=np.zeros(nv); row[:n]=Ah[rp]; A_ub.append(row); b_ub.append(thrBE+tol_hole-bh[rp])
        # |g| >= g and |g| >= -g
        for i in range(n):
            row=np.zeros(nv); row[i]=1; row[n+2*nt+i]=-1; A_ub.append(row); b_ub.append(0.0)
            row=np.zeros(nv); row[i]=-1; row[n+2*nt+i]=-1; A_ub.append(row); b_ub.append(0.0)
        bounds=[(-gmax,gmax)]*n+[(0,None)]*(2*nt)+[(0,None)]*n
        res=linprog(c,A_ub=np.array(A_ub),b_ub=np.array(b_ub),A_eq=A_eq,b_eq=b_eq,bounds=bounds,method='highs')
        if not res.success:
            hist.append(dict(it=it,status=res.message)); 
            if verbose: print(level,'LP infeasible:',res.message); 
            return dict(level=level,keys=keys,g=None,hist=hist,feasible=False)
        gn=res.x[:n]; resid={m:float((des[m][0][best[m]]@gn+des[m][1][best[m]])-D.target(m)) for m in train}
        hist.append(dict(it=it,g=gn.tolist(),resid=resid,best={m:int(b) for m,b in best.items()}))
        if np.allclose(gn,g,atol=1e-6): g=gn; break
        g=gn
    return dict(level=level,keys=keys,g=g,hist=hist,feasible=True,resid=resid,best=best)
def predict(fitres,names,st):
    proj=LEVELS[fitres['level']]; keys=fitres['keys']; g=np.array(fitres['g']); out={}
    for m in names:
        Am,bm=design(st[m],proj,keys); E=Am@g+bm; r=int(np.argmax(E))
        s=st[m][r]; out[m]=dict(BE=float(E[r]),target=D.target(m),feats={str(k):v for k,v in s['feats'].items()},P=s['P'].tolist(),sp=s['sp'],n_seatings=len(E),range=[float(E.min()),float(E.max())])
    return out
if __name__=='__main__':
    train=D.RUNG0_TRAIN; holes=['nn','pp','He5','Li5']
    st=load_seatings(train+holes+['Li6'])
    print({m:len(st[m]) for m in st})
    results={}
    for level in LEVELS:
        fr=fit_level(level,train,holes,st)
        if not fr['feasible']: results[level]=fr; continue
        pred=predict(fr,['Li6'],st); hole_max={h:float(max(design(st[h],LEVELS[level],fr['keys'])[0]@fr['g']+design(st[h],LEVELS[level],fr['keys'])[1])) for h in holes}
        results[level]=dict(fr,pred=pred,hole_max=hole_max)
        print(f"\n{level}: {len(fr['keys'])} entries; train resid {dict((m,round(v,3)) for m,v in fr['resid'].items())}")
        print('  table:',{str(k):round(v,3) for k,v in zip(fr['keys'],fr['g'])})
        print('  holes max BE:',{h:round(v,3) for h,v in hole_max.items()},' (He4 =',round(D.target('He4'),3),')')
        print('  BLIND Li6: %.3f vs %.3f (%+.1f%%)  seating feats %s'%(pred['Li6']['BE'],pred['Li6']['target'],100*(pred['Li6']['BE']/pred['Li6']['target']-1),pred['Li6']['feats']))
    json.dump({k:{kk:(vv if kk!='keys' else [str(x) for x in vv]) for kk,vv in v.items() if kk not in ('best',)} for k,v in results.items()},open(os.path.join(HERE,'results','rung0_ladder.json'),'w'),indent=1,default=lambda o:o.tolist() if hasattr(o,'tolist') else str(o))
