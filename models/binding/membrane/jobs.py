"""jobs.py — resumable relaxations (the sandbox kills processes at ~180 s). Each job = a System spec + state x saved to
results/state/<name>.npz; work() advances jobs in L-BFGS chunks until a wall-clock budget is spent.
Converged := relative energy change over a chunk < 1e-10 AND max|grad| < GTOL_ABS.  Implementer: Grace (Claude Opus 5.5)."""
import os,json,time,pickle,numpy as np
from scipy.optimize import minimize
HERE=os.path.dirname(os.path.abspath(__file__)); SD=os.path.join(HERE,'results','state'); os.makedirs(SD,exist_ok=True)
GTOL_ABS=1e-3; CHUNK=1500
def path(name): return os.path.join(SD,name+'.pkl')
def submit(name,builder,args,x0=None,overwrite=False):
    """builder: importable 'module:function' returning a System from args (dict)."""
    p=path(name)
    if os.path.exists(p) and not overwrite: return
    pickle.dump(dict(name=name,builder=builder,args=args,x=x0,done=False,nit=0,hist=[]),open(p,'wb'))
def load(name): return pickle.load(open(path(name),'rb'))
def build(job):
    mod,fn=job['builder'].split(':'); m=__import__(mod); return getattr(m,fn)(**job['args'])
def step(name,budget):
    job=load(name)
    if job['done']: return True
    S=build(job); x=S.X0.ravel() if job['x'] is None else job['x']
    t0=time.time(); E0_,_=S.energy(x)
    while time.time()-t0<budget:
        last=[time.time()]
        def cb(intermediate_result):
            if time.time()-last[0]>30:                       # periodic checkpoint
                job['x']=intermediate_result.x; pickle.dump(job,open(path(name),'wb')); last[0]=time.time()
            if time.time()-t0>budget: raise StopIteration
        r=minimize(S.energy,x,jac=True,method='L-BFGS-B',callback=cb,options=dict(maxiter=CHUNK,maxfun=2*CHUNK,gtol=1e-10,ftol=1e-16,maxcor=30))
        timed_out=time.time()-t0>budget
        dE=r.fun-E0_; gmax=np.abs(r.jac).max(); x=r.x; job['nit']+=r.nit
        job['hist'].append((float(r.fun),float(gmax),int(r.nit),str(r.message)[:30]))
        conv=(abs(dE)<=1e-8*max(1,abs(r.fun)) and gmax<GTOL_ABS) or r.nit==0
        E0_=r.fun
        if conv or (r.nit<5 and not timed_out): job['done']=True; break
        if timed_out: break
    job['x']=x; pickle.dump(job,open(path(name),'wb'))
    return job['done']
def work(names,budget=150):
    t0=time.time()
    for n in names:
        left=budget-(time.time()-t0)
        if left<5: break
        if not load(n)['done']: step(n,left)
    return {n:load(n)['done'] for n in names}
