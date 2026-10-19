"""kernel/data.py — the solution set (SPEC v5 §2). The ONLY reader of AME. Anchors flagged; holes as inequalities.
Grace (Claude Fable 5.1), 19 Oct 2026."""
import os,numpy as np
HERE=os.path.dirname(os.path.abspath(__file__)); AME=os.path.join(HERE,'..','..','data','ame2020-mass-table.txt')
HC=197.3269804; AHC=1.439964547; ME=0.510998950; MP=938.2720882; MN=939.5654205; RP=0.8409; RN=1.023*RP
CPRIME=np.sqrt(1-(ME/(MN-MP))**2)
def Y(n): return ME*((MN-MP)/ME-1/np.sqrt(1-(CPRIME/n)**2)) if n>1 else 0.0
def load_ame():
    rows={}
    for line in open(AME,encoding='latin-1'):
        if len(line)<80 or not line[1:4].strip().lstrip('-').isdigit(): continue
        try: N=int(line[4:9]); Z=int(line[9:14]); A=int(line[14:19]); be=line[54:68]
        except: continue
        if '#' in be: continue
        rows[(Z,N)]=float(be)*A/1000.0
    return rows
BE=load_ame()
def be(Z,N): return BE[(Z,N)]
# --- anchors (R13): hard equalities, one per rung ---
ANCHORS={'He4':(2,2),'O16':(8,8),'Fe52':(26,26)}
OPEN_ANCHORS={'D':(1,1),'Be8':(4,4)}
# --- holes (R14): unbound systems, as (Z,N, energy above the lowest threshold, threshold description) ---
HOLES={'nn':(0,2,0.066,'n+n'), 'pp':(2,0,0.0,'p+p (unbound; no resonance energy assigned)'),
       'He5':(2,3,0.89,'He4+n'), 'Li5':(3,2,1.97,'He4+p'), 'Be8':(4,4,0.092,'He4+He4'), 'Li4':(3,1,3.1,'He3+p'),
       'He7':(2,5,0.44,'He6+n'), 'B9':(5,4,0.19,'Be8+p')}
# --- training / blind splits (fixed, §4) ---
RUNG0_TRAIN=['D','T','He3','He4']; RUNG0_HOLES=['nn','pp','He5','Li5']
RUNG0_BLIND=['Li6','Li7','Be7','Be9','B10','B11','C12']
ZN={'D':(1,1),'T':(1,2),'He3':(2,1),'He4':(2,2),'Li6':(3,3),'Li7':(3,4),'Be7':(4,3),'Be8':(4,4),'Be9':(4,5),'B10':(5,5),'B11':(5,6),'C12':(6,6),
    'He5':(2,3),'Li5':(3,2),'nn':(0,2),'pp':(2,0),'Li4':(3,1),'He7':(2,5),'B9':(5,4)}
def target(name):
    Z,N=ZN[name]; return BE.get((Z,N))
if __name__=='__main__':
    print('Y(2)=%.6f'%Y(2))
    for n in RUNG0_TRAIN+RUNG0_BLIND: print(n,ZN[n],target(n))
    for h,(Z,N,e,thr) in HOLES.items(): print('hole',h,Z,N,'unbound by',e,'vs',thr, 'AME BE:',BE.get((Z,N)))
