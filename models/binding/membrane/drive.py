"""drive.py — loop paths.advance + parallel job steps inside one sandbox call. Implementer: Grace (Claude Opus 5.5)."""
import sys,os,json,time,subprocess
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,HERE)
import paths
T=float(sys.argv[1]) if len(sys.argv)>1 else 140; t0=time.time()
while True:
    act=paths.advance(); left=T-(time.time()-t0)
    import jobs
    import calib2
    _,cact=calib2.advance()
    extra=[n for n in json.load(open(os.path.join(HERE,'results','queue_fb2.json'))) if not jobs.load(n)['done']]+cact
    json.dump(act+extra[:max(0,4-len(act))],open(os.path.join(HERE,'results','queue_paths.json'),'w'))
    if not act or left<25: break
    subprocess.run([sys.executable,os.path.join(HERE,'runpar.py'),os.path.join(HERE,'results','queue_paths.json'),str(int(left-15))],cwd=HERE)
print('active:',act)
