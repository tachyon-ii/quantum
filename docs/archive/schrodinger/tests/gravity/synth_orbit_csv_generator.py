# synth_orbit_csv_generator.py  (patch)
import numpy as np, math
c=2.99792458e8; G=6.67430e-11; Me=5.972e24

T=86400.0; dt=30.0
t = np.arange(0.0, T, dt)

a = 2.656e7             # semi-major axis ~ 26,560 km
e = 0.01                # small eccentricity
n = math.sqrt(G*Me/a**3)   # mean motion ~ 2π/(~12h)

# simple Keplerian first-order approximation
r = a*(1 - e*np.cos(n*t))                   # meters
v = np.sqrt(G*Me*(2.0/r - 1.0/a))          # vis-viva [m/s]

# build s = ΔU/c^2 - v^2/(2c^2), zero-mean both parts
U = -G*Me/r
s = (U - U.mean())/(c*c) - 0.5*((v*v) - (v*v).mean())/(c*c)

kappa = 1.0
noise = 5e-13*np.random.randn(t.size)      # white noise (use AR if you like)
y = kappa*s + noise

np.savetxt("synth_orbit.csv", np.c_[t,y,r,v], delimiter=",", fmt="%.9e")
print("wrote synth_orbit.csv")

