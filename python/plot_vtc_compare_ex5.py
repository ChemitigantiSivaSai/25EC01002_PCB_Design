"""Exercise 5 (option 2) - overlay the Exercise 4 and Exercise 5 VTCs.
Usage: python plot_vtc_compare_ex5.py "ex4_export.txt" "ex5_export.txt" [out.png]
Both files: LTspice  File > Export data as Text  (tab separated, first column Vin, second V(out)).
Author: Chemitiganti Siva Sai, 25EC01002
"""
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

f4, f5 = sys.argv[1], sys.argv[2]
out = sys.argv[3] if len(sys.argv) > 3 else "VTC_ex4_vs_ex5.png"
VDD = 5.0
d4, d5 = pd.read_csv(f4, sep="\t"), pd.read_csv(f5, sep="\t")
v4, y4 = d4.iloc[:, 0].to_numpy(), d4.iloc[:, 1].to_numpy()
v5, y5 = d5.iloc[:, 0].to_numpy(), d5.iloc[:, 1].to_numpy()
vm4 = float(np.interp(VDD / 2, y4[::-1], v4[::-1]))
vm5 = float(np.interp(VDD / 2, y5[::-1], v5[::-1]))

fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(v4, y4, lw=2, color="tab:blue", label=f"Exercise 4 (LED to GND), V$_M$ = {vm4:.2f} V")
ax.plot(v5, y5, lw=2, color="tab:green", label=f"Option 2 (LED from +5 V), V$_M$ = {vm5:.2f} V")
ax.axhline(VDD / 2, ls="--", lw=1, color="gray")
ax.set_xlabel("Input voltage, V$_{IN}$ (V)"); ax.set_ylabel("Output voltage, V$_{OUT}$ (V)")
ax.set_title("VTC before and after moving the LED"); ax.grid(ls=":", alpha=.6); ax.legend()
fig.tight_layout(); fig.savefig(out, dpi=300)
print(f"V_M: {vm4:.3f} V -> {vm5:.3f} V; saved {out}")
