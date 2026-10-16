# Grace 16 Oct — re-run of Argon's Coulomb rebuild §1-§3 (Y(n), P_I/P_II, patches, k) and the Be-8 placement search.
import math, numpy as np, itertools
hc=197.3269804; a_hc=1.439964547; me=0.510998950; dm=1.2933323
Rp=0.8409; Upp=a_hc/(2*Rp)
g=dm/me; cp=math.sqrt(1-1/g**2); print("gamma",g,"c'",cp)
def Y(n): return me*(g-1/math.sqrt(1-(cp/n)**2))
for n in [2,3,4,6,7,1000]: print(" Y(%d)=%.6f"%(n,Y(n)))
BE={'D':2.224566,'T':8.481795,'He3':7.718043,'He4':28.29566,'Be8':56.4995,'Li7':39.2446,'Be7':37.6004,'C12':92.1617,'O16':127.6193}
A4=2+4*2.598076
# Option I
P1=(BE['He4']+Upp-4*Y(4))/A4; P2=(BE['He4']+Upp-6*Y(4))/A4
print("Upp=%.6f  P_I=%.6f  P_II=%.6f"%(Upp,P1,P2))
print(" D face (I):",BE['D']-2*Y(2)," /P =",(BE['D']-2*Y(2))/P1, " pi/8=",math.pi/8)
print(" T face/contact:",(BE['T']-3*Y(3))/3/P1," He3:",(BE['He3']+Upp-3*Y(3))/3/P1)
for a_name,a in [('D_SS',2*Rp/(2*math.sqrt(2))),('D_HH',2*Rp/math.sqrt(6)),('sat0.1542',(1/0.1542/(8*math.sqrt(2)))**(1/3))]:
    print(" k(%s)=%.3f MeV/fm^2"%(a_name,P1/a**2))
# Be-8: two he4_cross tetrahedra in integer BCC coords (unit = Rp): verts (0,0,0),(2,0,0),(1,1,1),(1,-1,1)
t=np.array([[0,0,0],[2,0,0],[1,1,1],[1,-1,1]],float)
# centroid (1,0,0.5); translate second alpha to share a square face? S-S contact distance 2 along x: shift by (2,0,0)? that overlaps vertex (2,0,0). Try shift by (0,0,2)... search translations on BCC lattice giving min inter distance = sqrt3 (H-H) or 2 (S-S) with no overlap
best=[]
for dx in range(-4,5):
  for dy in range(-4,5):
    for dz in range(-4,5):
      t2=t+np.array([dx,dy,dz]); d=[np.linalg.norm(p-q) for p in t for q in t2]
      m=min(d); 
      if abs(m-2)<1e-9 or abs(m-math.sqrt(3))<1e-9:
          best.append((m,(dx,dy,dz),sorted(d)[:4]))
print(" Be8 candidate placements (min inter distance, shift):",[(round(b[0],3),b[1]) for b in best[:8]])
# For each placement, protons: choose 2 of 4 in each alpha to minimize inter pp Coulomb
import itertools
res=[]
for m,sh,_ in best:
    t2=t+np.array(sh)
    bestE=None
    for pa in itertools.combinations(range(4),2):
        for pb in itertools.combinations(range(4),2):
            E=sum(a_hc/(np.linalg.norm(t[i]-t2[j])*Rp) for i in pa for j in pb)
            if bestE is None or E<bestE: bestE=E
    res.append((round(m,3),sh,round(bestE,4)))
res=sorted(set(res),key=lambda r:r[2]); print(" Be8 min inter-alpha pp Coulomb by placement:",res[:6])
print(" Argon: 4 pairs at 2.6592 fm -> ",4*a_hc/2.6592)
