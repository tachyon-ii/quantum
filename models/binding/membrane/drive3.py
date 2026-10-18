import sys,os,json,time,subprocess
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,HERE)
import calib2, jobs
T=float(sys.argv[1]) if len(sys.argv)>1 else 140; t0=time.time()
while True:
    st,act=calib2.advance(); left=T-(time.time()-t0)
    extra=[n for n in json.load(open(os.path.join(HERE,'results','queue_fb2.json'))) if not jobs.load(n)['done']]
    q=act+extra
    json.dump(q,open(os.path.join(HERE,'results','queue_v2.json'),'w'))
    if not q or left<30: break
    subprocess.run([sys.executable,os.path.join(HERE,'runpar.py'),os.path.join(HERE,'results','queue_v2.json'),str(int(left-20))],cwd=HERE,stdout=subprocess.DEVNULL)
print('active',len(q))
