"""L4 - Plot the LTspice-exported VTC of the discrete CMOS inverter (EC2L104).
Usage:  python plot_vtc_discrete.py "circuit VDD =5V.txt" [output.png]
Export in LTspice: plot window active -> File > Export data as Text.
Author: Chemitiganti Siva Sai, 25EC01002
"""
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

path = sys.argv[1] if len(sys.argv) > 1 else "circuit VDD =5V.txt"
out = sys.argv[2] if len(sys.argv) > 2 else "CMOS_Inverter_VTC.png"
df = pd.read_csv(path, sep="\t")            # columns: VIN, V(out)
vin, vout = df.iloc[:, 0].to_numpy(), df.iloc[:, 1].to_numpy()
VDD = 5.0

# switching threshold: VIN where VOUT = VDD/2 (linear interpolation; vout is falling)
vm = float(np.interp(VDD / 2, vout[::-1], vin[::-1]))

fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(vin, vout, lw=2, color="tab:blue", label="Discrete CMOS inverter (2N7000 + BS250)")
ax.axhline(VDD / 2, ls="--", lw=1, color="gray", label="V$_{DD}$/2 = 2.5 V")
ax.axvline(vm, ls="--", lw=1, color="red")
ax.plot([vm], [VDD / 2], "ro")
ax.annotate(f"V$_M$ = {vm:.3f} V", (vm, VDD / 2), (vm + 0.6, VDD / 2 + 1.0),
            arrowprops=dict(arrowstyle="->", color="red"), color="red")
ax.set_xlabel("Input voltage, V$_{IN}$ (V)")
ax.set_ylabel("Output voltage, V$_{OUT}$ (V)")
ax.set_title("Voltage transfer characteristic - discrete CMOS inverter, V$_{DD}$ = 5 V")
ax.grid(True, which="both", linestyle=":")
ax.legend(loc="lower left")
fig.tight_layout()
fig.savefig(out, dpi=300)
print(f"Vm = {vm:.4f} V  -> saved {out} (300 dpi)")
