"""runpar.py <queue.json> [budget] — advance up to 4 unfinished jobs, one subprocess per core, each hard-limited by `timeout`.
Implementer: Grace (Claude Opus 5.5)."""
import sys,json,os,subprocess
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,HERE)
import jobs
if __name__=='__main__':
    names=json.load(open(sys.argv[1])); b=float(sys.argv[2]) if len(sys.argv)>2 else 100
    todo=[n for n in names if not jobs.load(n)['done']][:4]
    env=dict(os.environ,OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1',MKL_NUM_THREADS='1')
    ps=[subprocess.Popen(['timeout',str(int(b+20)),sys.executable,'-c',f"import sys;sys.path.insert(0,{HERE!r});import jobs;print({n!r},jobs.step({n!r},{b}))"],
                         cwd=HERE,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True) for n in todo]
    for p in ps: print(p.communicate()[0].strip()[-200:])
    print(sum(jobs.load(n)['done'] for n in names),'/',len(names),'done')
