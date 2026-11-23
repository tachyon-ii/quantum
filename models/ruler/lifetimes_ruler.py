"""ruler/lifetimes_ruler.py — T5 of the Euler-ruler tests. James's posit (18 Nov): a half-life counts how many things must
coincide, so lifetime in turns = (1/eps)^n for whole n. Then log(lifetime / one turn) should be whole multiples of one unit.
Test: common measure on log10(T_half / 1e-22 s) for 34 half-lives (values as fact-checked on 19 Nov from secondary tables;
typed from that list — NOT from the primary evaluation). Control: the same number of values drawn uniformly over the same
range. Also the same test within one decay kind (beta-minus only). Grace (Claude Fable 5.2), 23 Nov 2026."""
import numpy as np
rng=np.random.default_rng(7)
y=3.156e7; d=86400.0; h=3600.0; m=60.0
T={'Fe-59':44.5*d,'Fe-60':2.6e6*y,'Fe-61':5.98*m,'Fe-62':68.0,'C-14':5700*y,'C-15':2.45,'Si-31':2.62*h,'Si-32':153*y,'Si-33':6.1,
   'Ca-45':163*d,'Ca-47':4.54*d,'Ca-49':8.7*m,'O-19':26.9,'O-20':13.5,'O-21':3.4,'O-22':2.25,'He-6':0.807,'He-8':0.119,
   'Pb-209':3.25*h,'Pb-210':22.2*y,'Pb-211':36.1*m,'Pb-212':10.6*h,'Pb-213':10.2*m,'Pb-214':27*m,'H-3':12.32*y,'neutron':610.0}
OTHER={'Fe-55':2.74*y,'Ca-41':9.9e4*y,'Ni-56':6.08*d,'Co-56':77.2*d,'Be-7':53.2*d,'Be-8':8e-17,'U-238':4.47e9*y,'Fe-57 (14.4 keV state)':98e-9}
def stat(x):
    x=np.asarray(x); us=np.linspace(0.6,6.0,2701); r=x[None,:]/us[:,None]; s=np.abs(r-np.round(r)).mean(1); i=s.argmin(); return s[i],us[i]
def test(x,n=5000):
    s0,u0=stat(x); lo,hi=min(x),max(x); c=sum(stat(rng.uniform(lo,hi,len(x)))[0]<=s0 for _ in range(n)); return s0,u0,(c+1)/(n+1)
print("| set | values | range of log10(lifetime in turns) | best unit (decades) | mean distance from whole (chance 0.25) | p |"); print("|---|---|---|---|---|---|")
for nm,dd in (('beta-minus decays only',T),('all 34, every decay kind',{**T,**OTHER})):
    x=np.log10(np.array(list(dd.values()))/1e-22); s0,u0,p=test(x); print(f"| {nm} | {len(x)} | {x.min():.1f} – {x.max():.1f} | {u0:.2f} | {s0:.3f} | {p:.3f} |")
