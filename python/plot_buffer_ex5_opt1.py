"""Exercise 5 option 1 - non-inverting buffer (two inverter stages): VTC and switching delay.
Usage (from the python/ folder):
    python plot_buffer_ex5_opt1.py ../ltspice/ex5_opt1/buffer_DC.txt ../ltspice/ex5_opt1/buffer_TRAN.raw [out.png]
buffer_DC.txt  : LTspice File > Export data as Text  (columns Vin, V(out1), V(out2))
buffer_TRAN.raw: LTspice raw file of buffer_TRAN.cir (read directly so that V(out1) is available)
Author: Chemitiganti Siva Sai, 25EC01002
"""
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def read_raw(path):
    """Minimal reader for a real, binary LTspice .raw file (time = float64, other variables = float32)."""
    b = open(path, "rb").read()
    k = "Binary:\n".encode("utf-16-le")
    i = b.find(k)
    head = b[:i].decode("utf-16-le")
    nvar = int(head.split("No. Variables:")[1].split()[0])
    npts = int(head.split("No. Points:")[1].split()[0])
    names = [l.split("\t")[2] for l in head.split("Variables:\n")[1].splitlines() if l.strip()]
    rec = np.dtype([("t", "<f8")] + [(f"v{j}", "<f4") for j in range(nvar - 1)])
    a = np.frombuffer(b[i + len(k):], dtype=rec, count=npts)
    out = {names[0]: np.abs(a["t"])}
    for j in range(nvar - 1):
        out[names[j + 1]] = a[f"v{j}"].astype(float)
    return out

def cross(t, y, level, rising):
    """Time of the first crossing of 'level' (linear interpolation)."""
    s = np.sign(y - level)
    idx = np.where((s[:-1] < 0) & (s[1:] >= 0))[0] if rising else np.where((s[:-1] > 0) & (s[1:] <= 0))[0]
    out = []
    for i in idx:
        out.append(t[i] + (level - y[i]) * (t[i + 1] - t[i]) / (y[i + 1] - y[i]))
    return out

dc = pd.read_csv(sys.argv[1], sep="\t")
vin, o1, o2 = dc.iloc[:, 0].to_numpy(), dc.iloc[:, 1].to_numpy(), dc.iloc[:, 2].to_numpy()
vm1 = float(np.interp(2.5, o1[::-1], vin[::-1]))
vm2 = float(np.interp(2.5, o2, vin))
raw = read_raw(sys.argv[2])
t, vi, v1, v2 = raw["time"], raw["V(in)"], raw["V(out1)"], raw["V(out2)"]
out = sys.argv[3] if len(sys.argv) > 3 else "buffer_ex5_opt1.png"

# delays, second cycle (same as the .meas lines)
r_in = cross(t, vi, 2.5, True)[1]
tp_lh = cross(t, v2, 2.5, True)[1] - r_in
st1_hl = cross(t, v1, 2.5, False)[1] - r_in
f_in = cross(t, vi, 2.5, False)[1]
tp_hl = cross(t, v2, 2.5, False)[1] - f_in
st1_lh = cross(t, v1, 2.5, True)[1] - f_in

fig, ax = plt.subplots(1, 2, figsize=(11, 4))
ax[0].plot(vin, o1, color="tab:orange", lw=2, label=f"V(out1), stage 1 (V$_M$ = {vm1:.3f} V)")
ax[0].plot(vin, o2, color="tab:blue", lw=2, label=f"V(out2), buffer output (V$_M$ = {vm2:.3f} V)")
ax[0].axhline(2.5, ls="--", lw=1, color="gray"); ax[0].axvline(vm2, ls=":", lw=1, color="gray")
ax[0].set_xlabel("V$_{IN}$ (V)"); ax[0].set_ylabel("Voltage (V)")
ax[0].set_title("DC sweep: output follows the input"); ax[0].grid(ls=":", alpha=.6); ax[0].legend(fontsize=8, loc="center left")
m = (t > r_in - 10e-9) & (t < r_in + 40e-9)
ax[1].plot((t[m] - r_in) * 1e9, vi[m], color="k", lw=1.5, label="V(in)")
ax[1].plot((t[m] - r_in) * 1e9, v1[m], color="tab:orange", lw=1.5, label="V(out1)")
ax[1].plot((t[m] - r_in) * 1e9, v2[m], color="tab:blue", lw=1.5, label="V(out2)")
ax[1].axhline(2.5, ls="--", lw=1, color="gray")
ax[1].set_xlabel("time after input crossing 2.5 V (ns)"); ax[1].set_ylabel("Voltage (V)")
ax[1].set_title(f"Rising edge: t$_{{pLH}}$ = {tp_lh*1e9:.1f} ns, stage 1 alone {st1_hl*1e9:.1f} ns")
ax[1].grid(ls=":", alpha=.6); ax[1].legend(fontsize=8)
fig.tight_layout(); fig.savefig(out, dpi=300)
print(f"VM1={vm1:.3f} V  VM2={vm2:.3f} V  tpLH={tp_lh*1e9:.2f} ns  tpHL={tp_hl*1e9:.2f} ns  "
      f"stage1 tpHL={st1_hl*1e9:.2f} ns  stage1 tpLH={st1_lh*1e9:.2f} ns  saved {out}")
