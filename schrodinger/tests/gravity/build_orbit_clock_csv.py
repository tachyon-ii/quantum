# build_orbit_clock_csv.py
# Join t,y (clock residuals) with t, x,y,z (SP3) into t,y,r,v CSV
import numpy as np, pandas as pd, argparse

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--clk_csv", required=True, help="CSV: t(s), y(s/s)")
    ap.add_argument("--sp3_csv", required=True, help="CSV: t(s), x(m), y(m), z(m)")
    ap.add_argument("--out", default="orbit_fit.csv")
    args=ap.parse_args()

    clk = pd.read_csv(args.clk_csv, header=None, names=["t","y"])
    orb = pd.read_csv(args.sp3_csv, header=None, names=["t","x","y","z"])
    df = pd.merge_asof(clk.sort_values("t"), orb.sort_values("t"), on="t", direction="nearest", tolerance=0.6)
    # compute r and v (finite difference)
    r = np.linalg.norm(df[["x","y","z"]].values, axis=1)
    v = np.zeros_like(r)
    x = df[["x","y","z"]].values
    dt = np.gradient(df["t"].values)
    vx = np.gradient(x[:,0], dt); vy = np.gradient(x[:,1], dt); vz = np.gradient(x[:,2], dt)
    v[:] = np.sqrt(vx*vx + vy*vy + vz*vz)
    out = np.c_[df["t"].values, df["y"].values, r, v]
    np.savetxt(args.out, out, delimiter=",", fmt="%.9e")
    print("wrote", args.out)
if __name__=="__main__": main()

