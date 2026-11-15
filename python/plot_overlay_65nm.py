"""L5 - Normalised VTC overlay: discrete inverter vs 65 nm inverter (EC2L104).
Run from this folder:  python plot_overlay_65nm.py
"""
import pandas as pd
import matplotlib.pyplot as plt

d = pd.read_csv("../ltspice/circuit VDD =5V.txt", sep="\t")       # VIN, V(out)  (VDD = 5 V)
p = pd.read_csv("../ltspice/65nm_CMOS_inverter.txt", sep="\t")     # Vin, V(vout) (VDD = 1.1 V)
vdd_d, vdd_p = 5.0, float(p.iloc[0, 1])

fig, ax = plt.subplots(figsize=(7, 5.5))
ax.plot(d.iloc[:, 0] / vdd_d, d.iloc[:, 1] / vdd_d, lw=2, label="Discrete (2N7000 + BS250), VDD = 5 V")
ax.plot(p.iloc[:, 0] / vdd_p, p.iloc[:, 1] / vdd_p, lw=2, color="tab:red", label=f"65 nm inverter, VDD = {vdd_p:.1f} V")
ax.plot([0, 1], [1, 0], "k:", lw=0.8)
ax.set_xlabel("VIN / VDD"); ax.set_ylabel("VOUT / VDD"); ax.set_title("Normalised VTC comparison")
ax.grid(True, linestyle=":"); ax.legend(fontsize=8)
fig.tight_layout(); fig.savefig("VTC_overlay_normalised.png", dpi=300)
print("saved VTC_overlay_normalised.png")
