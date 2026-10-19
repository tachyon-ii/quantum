"""drive2.py — loop calib4.advance + parallel job steps within one sandbox call. Implementer: Grace (Claude Fable 5.1)."""
import sys,os,json,time,subprocess
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,HERE)
import calib4
T=float(sys.argv[1]) if len(sys.argv)>1 else 140; t0=time.time()
while True:
    st,act=calib4.advance(); left=T-(time.time()-t0)
    if not act or left<30: break
    subprocess.run([sys.executable,os.path.join(HERE,'runpar.py'),os.path.join(HERE,'results','queue_v4.json'),str(int(left-20))],cwd=HERE,stdout=subprocess.DEVNULL)
print('active',len(act))
