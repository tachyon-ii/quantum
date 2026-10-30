"""kernel/fit2.py — rung-0 ladder on sparse seating matrices (SPEC v5 §4). Train: D,T,He3,He4,Li6 (D,He4 anchors). Holes: nn,pp,He5,Li5.
Blind: Li7, Be7 (Be9 on the box). LP: L1 residual + reg*|g|, anchors weighted; chosen seating must beat its top competitors;
every hole seating <= threshold. Alternate seat/fit. Grace (Claude Fable 5.1), 20 Oct 2026."""
import sys,os,json,numpy as np,scipy.sparse as sp
from scipy.optimize import linprog
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import data as D, seatmat as SM
HERE=os.path.dirname(os.path.abspath(__file__))
LEVELS={
 'L0 pair2+c3':      lambda k:('np' if k[0]=='np' else 'same',min(k[2],2)),
 'L1 +type':         lambda k:('np' if k[0]=='np' else 'same',min(k[2],2),k[1]),
 'L2 +c>=3':         lambda k:('np' if k[0]=='np' else 'same',min(k[2],3),k[1]),
 'L3 +zmax>=4 flag': lambda k:('np' if k[0]=='np' else 'same',min(k[2],2),k[1],int(k[4]>=4)),
 'L4 +zmax bins 3/4/5':lambda k:('np' if k[0]=='np' else 'same',min(k[2],2),k[1],min(max(k[4],3),5)),
 'L5 +c>=3 +zmax bins':lambda k:('np' if k[0]=='np' else 'same',min(k[2],3),k[1],min(max(k[4],3),5)),
 'L6 +zmax>=4 flag +zmax>=6 flag':lambda k:('np' if k[0]=='np' else 'same',min(k[2],2),k[1],int(k[4]>=4)+int(k[4]>=6)),
 'L7 +zmax in {<=3,4,5,>=6}':lambda k:('np' if k[0]=='np' else 'same',min(k[2],2),k[1],min(max(k[4],3),6)),
}
def projector(proj):
    keys=sorted({proj(k) for k in SM.KEYS},key=str); idx={k:i for i,k in enumerate(keys)}
    Pm=np.zeros((len(SM.KEYS),len(keys)),np.float32)
    for i,k in enumerate(SM.KEYS): Pm[i,idx[proj(k)]]=1
    return keys,Pm
ROUND=False
def design(s,Pm):
    A_=np.asarray(s['M']@Pm); b=-s['coul']+np.where(s['conn']&s['trip'],s['A']*D.Y(2),0.0)
    if ROUND: A_=np.hstack([A_,s['round'][:,None]])
    return A_,b
def fit(level,train,holes,sets,iters=15,reg=0.02,gmax=12.0,ncomp=300,tol_hole=0.0):
    keys,Pm=projector(LEVELS[level])
    if ROUND: keys=keys+[('ROUND',)]
    n=len(keys); des={m:design(sets[m],Pm) for m in train+holes}
    used=np.zeros(n,bool)
    for m in train+holes: used|=(np.abs(des[m][0]).sum(0)>0)
    g=np.full(n,1.0); hist=[]
    if ROUND: g[n-1]=-1.0          # start with a roundness cost so the first seating choice is already round-ish
    for it in range(iters):
        best={m:int(np.argmax(des[m][0]@g+des[m][1])) for m in train}
        nt=len(train); nv=n+2*nt+n
        c=np.zeros(nv); c[n:n+2*nt]=1.0; c[n+2*nt:]=reg
        for i,m in enumerate(train):
            if m in D.ANCHORS or m in D.OPEN_ANCHORS: c[n+2*i]=c[n+2*i+1]=1e4
        A_eq=np.zeros((nt,nv)); b_eq=np.zeros(nt)
        for i,m in enumerate(train):
            r=best[m]; A_eq[i,:n]=des[m][0][r]; A_eq[i,n+2*i]=1; A_eq[i,n+2*i+1]=-1; b_eq[i]=D.target(m)-des[m][1][r]
        rows=[];rhs=[]
        for m in train:
            Am,bm=des[m]; r=best[m]; E=Am@g+bm; comp=np.argsort(-E)[:ncomp]
            for rp in comp:
                if rp==r: continue
                row=np.zeros(nv); row[:n]=Am[rp]-Am[r]; rows.append(row); rhs.append(bm[r]-bm[rp])
        for h in holes:
            Ah,bh=des[h]; thr={'nn':0.0,'pp':0.0,'He5':D.target('He4'),'Li5':D.target('He4')}[h]
            E=Ah@g+bh; cand=np.argsort(-E)[:2000]           # top candidates only (others far below)
            for rp in cand:
                row=np.zeros(nv); row[:n]=Ah[rp]; rows.append(row); rhs.append(thr+tol_hole-bh[rp])
        for i in range(n):
            r1=np.zeros(nv); r1[i]=1; r1[n+2*nt+i]=-1; rows.append(r1); rhs.append(0.0)
            r2=np.zeros(nv); r2[i]=-1; r2[n+2*nt+i]=-1; rows.append(r2); rhs.append(0.0)
        bounds=[(-gmax,gmax) if used[i] else (0,0) for i in range(n)]+[(0,None)]*(2*nt)+[(0,None)]*n
        if ROUND: bounds[n-1]=(-gmax,0.0)   # roundness is a cost or nothing
        res=linprog(c,A_ub=np.array(rows),b_ub=np.array(rhs),A_eq=A_eq,b_eq=b_eq,bounds=bounds,method='highs')
        if not res.success:
            if ROUND and it<iters-1: g[n-1]*=2.0; continue      # stronger initial roundness cost, re-seat
            return dict(level=level,feasible=False,msg=res.message,keys=[str(k) for k in keys])
        gn=res.x[:n]
        # verify hole constraints on ALL seatings at gn (not just candidates); if violated, loop
        viol=0
        for h in holes:
            Ah,bh=des[h]; thr={'nn':0.0,'pp':0.0,'He5':D.target('He4'),'Li5':D.target('He4')}[h]
            viol=max(viol,float((Ah@gn+bh).max()-thr))
        conv=np.allclose(gn,g,atol=1e-6); g=gn
        hist.append(dict(it=it,viol=viol))
        if conv and viol<=1e-6: break
    resid={m:float((des[m][0][best[m]]@g+des[m][1][best[m]])-D.target(m)) for m in train}
    hm={h:float((des[h][0]@g+des[h][1]).max()) for h in holes}
    return dict(level=level,feasible=True,keys=[str(k) for k in keys],g=g.tolist(),resid=resid,hole_max=hm,hist=hist,Pm=Pm)
def predict(fr,names,sets):
    out={}
    for m in names:
        Am,bm=design(sets[m],fr['Pm']); E=Am@np.array(fr['g'])+bm; r=int(np.argmax(E))
        out[m]=dict(BE=float(E[r]),target=D.target(m),P=sets[m]['P'][r].tolist(),sp=str(sets[m]['sp'][r]),n=int(len(E)),range=[float(E.min()),float(E.max())])
    return out
if __name__=='__main__':
    import builtins
    args=[a for a in sys.argv[1:] if a!='--round']; ROUND=('--round' in sys.argv); globals()['ROUND']=ROUND
    train=['D','T','He3','He4','Li6']; holes=['nn','pp','He5','Li5']; blind=args
    sets={m:SM.load(m) for m in train+holes+blind}
    out={}
    for level in LEVELS:
        fr=fit(level,train,holes,sets)
        if not fr['feasible']: print(level,'INFEASIBLE',fr['msg']); out[level]=dict(feasible=False); continue
        pred=predict(fr,blind,sets) if blind else {}
        print(f"{level}: {len(fr['keys'])} entries | resid {dict((m,round(v,2)) for m,v in fr['resid'].items())} | holes {dict((h,round(v,2)) for h,v in fr['hole_max'].items())} (He4 28.30)"+
              (' | BLIND '+' '.join(f"{m} {p['BE']:.2f}/{p['target']:.2f} ({100*(p['BE']/p['target']-1):+.0f}%)" for m,p in pred.items()) if pred else ''))
        out[level]={k:v for k,v in fr.items() if k!='Pm'}; out[level]['pred']=pred
    json.dump(out,open(os.path.join(HERE,'results','rung0_ladder2'+('_round' if ROUND else '')+'.json'),'w'),indent=1)
