"""berry/tangent_phase.py — geometric (Berry/Rytov–Vladimirskii) phase of a wave carried round a closed path:
Omega = signed solid angle enclosed by the tangent indicatrix T(t) on the unit sphere; phase for spin s is s*Omega.
Checks: planar circle (turning number 1 -> Omega=2pi), planar figure-eight (turning number 0 -> 0), and the tetrahedral
'baseball-seam' lemniscate r(t)=(a cos t + b cos 3t, a sin t - b sin 3t, c sin 2t) whose four extrema in z sit at the
tetrahedral directions; its mirror image. Also Bishop-frame holonomy as an independent check of Omega mod 2pi.
Grace (Claude Fable 5.1), 31 Oct 2026."""
import numpy as np
def tangent(r):
    dr=np.gradient(r,axis=0,edge_order=2); return dr/np.linalg.norm(dr,axis=1)[:,None]
def solid_angle_fan(T):
    """signed solid angle enclosed by closed spherical curve T (N x 3, closed) via fan of spherical triangles from a pole p.
    Pole chosen as the mean direction (robust when the curve stays in one hemisphere); result unique mod 4pi, reported in (-2pi,2pi]."""
    p=T.mean(0); p/=np.linalg.norm(p); tot=0.0
    for i in range(len(T)):
        a,b,c=p,T[i],T[(i+1)%len(T)]
        num=np.dot(a,np.cross(b,c)); den=1+np.dot(a,b)+np.dot(b,c)+np.dot(c,a)
        tot+=2*np.arctan2(num,den)
    return tot
def bishop_holonomy(T):
    """parallel-transport a normal vector along T; return rotation angle of the transported frame after one loop (mod 2pi)."""
    N=np.cross(T[0],[0.3,0.5,0.81]); N-=np.dot(N,T[0])*T[0]; N/=np.linalg.norm(N); N0=N.copy()
    for i in range(1,len(T)+1):
        t=T[i%len(T)]; N=N-np.dot(N,t)*t; N/=np.linalg.norm(N)
    B0=np.cross(T[0],N0); return np.degrees(np.arctan2(np.dot(N,B0),np.dot(N,N0)))
t=np.linspace(0,2*np.pi,20001)[:-1]
curves={
 'planar circle':np.c_[np.cos(t),np.sin(t),0*t],
 'planar figure-eight (Bernoulli)':np.c_[np.cos(t)/(1+np.sin(t)**2),np.sin(t)*np.cos(t)/(1+np.sin(t)**2),0*t],
 'tetra seam a=1 b=0.3 c=0.7':np.c_[np.cos(t)+0.3*np.cos(3*t),np.sin(t)-0.3*np.sin(3*t),0.7*np.sin(2*t)],
 'tetra seam MIRROR (z->-z)':np.c_[np.cos(t)+0.3*np.cos(3*t),np.sin(t)-0.3*np.sin(3*t),-0.7*np.sin(2*t)],
 'tetra seam a=1 b=0.3 c=1.0':np.c_[np.cos(t)+0.3*np.cos(3*t),np.sin(t)-0.3*np.sin(3*t),1.0*np.sin(2*t)],
 'tetra seam a=1 b=0.3 c=0.4':np.c_[np.cos(t)+0.3*np.cos(3*t),np.sin(t)-0.3*np.sin(3*t),0.4*np.sin(2*t)],
 'tetra seam a=1 b=0.0 c=0.7 (circle+z wobble)':np.c_[np.cos(t),np.sin(t),0.7*np.sin(2*t)],
 'helix 1 turn, pitch 0.5 (closed by return? no: open) ':None,
}
print(f"{'curve':48s} {'Omega/pi':>9s} {'spin-1 phase/pi':>16s} {'spin-1/2 phase/pi':>18s} {'Bishop holonomy (deg)':>22s}")
for name,r in curves.items():
    if r is None: continue
    T=tangent(r); Om=solid_angle_fan(T); hol=bishop_holonomy(T)
    print(f"{name:48s} {Om/np.pi:9.4f} {Om/np.pi:16.4f} {Om/2/np.pi:18.4f} {hol:22.2f}")
# lobe geometry check for the seam: directions of the four z-extrema
r=curves['tetra seam a=1 b=0.3 c=0.7']; z=r[:,2]; idx=[np.argmax(z[:5000]),np.argmin(z[5000:10000])+5000,np.argmax(z[10000:15000])+10000,np.argmin(z[15000:])+15000]
L=r[idx]/np.linalg.norm(r[idx],axis=1)[:,None]
ang=[np.degrees(np.arccos(np.clip(L[i]@L[j],-1,1))) for i in range(4) for j in range(i+1,4)]
print("\nseam lobe directions pairwise angles (deg):",np.round(ang,1),"  (tetrahedral = 109.47)")
