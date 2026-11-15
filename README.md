# 25EC01002_PCB_Design

EC2L104 – Introduction to EDA Tools (IIT Bhubaneswar), Module 10 laboratory work  
**Chemitiganti Siva Sai – 25EC01002**

A discrete CMOS inverter (2N7000 NMOS + BS250 PMOS, 5 V, LED output indicator) taken from
LTspice simulation to a two-layer KiCad 10 PCB with fabrication files.

## Repository layout
| Folder | Content |
|---|---|
| `ltspice/` | LTspice schematics (.asc), manufacturer model libraries (2N7000 onsemi, BS250 Philips), logs, exported VTC data (5 V and 9 V), 65 nm VTC export, `ex5_opt1/` (buffer schematics `Buffer_DC.asc` and `Buffer_TRAN.asc`, netlists, logs, exports, raw) and `ex5_opt2/` runs |
| `python/` | `plot_vtc_discrete.py` (L4 - VTC with VM marked, 300 dpi PNG), `plot_overlay_65nm.py` (L5 - normalised overlay), `plot_vtc_compare_ex5.py` (option 2 VTC overlay), `plot_buffer_ex5_opt1.py` (option 1 buffer VTC and delay) |
| `kicad/25EC01002_INV/` | Exercise 1-4 KiCad project (`.kicad_pro/.kicad_sch/.kicad_pcb`), BOM CSV, ERC/DRC reports, `gerbers/` (Gerbers + drill files) |
| `kicad/ex5_opt1/`, `ex5_opt2/`, `ex5_opt3/`, `ex5_opt4/` | Exercise 5 projects, one per option, each with its own Gerbers |
| `docs/` | Lab report (PDF), its LaTeX source in `docs/latex/`, and screenshots |

## Key results (Exercises 0-4)
- Switching threshold VM = 2.349 V (VDD = 5 V, manufacturer SPICE models); VOH = 4.94 V, VOL ~ 0 V; VM = 4.07 V at VDD = 9 V
- LED current 4.25 mA with R1 = 1 kohm (simulated, 2N7000 onsemi + BS250 Philips models)
- Board: 50 x 40 mm, 2-layer, 4 x M3 holes, ground pour on B.Cu
- ERC: 0 errors / 0 warnings; DRC: 0 violations, 0 unconnected, 0 parity errors

## Exercise 5 (extra explorations)
Each option was done on its own copy of the Exercise 4 project.

| Option | Where | Result |
|---|---|---|
| 1 - second inverter stage (non-inverting buffer) | `kicad/ex5_opt1/`, `ltspice/ex5_opt1/`, `python/plot_buffer_ex5_opt1.py` | VM 2.415 V (both stages), tpLH 16.4 ns / tpHL 16.8 ns, LED lit when VIN high; board still 50 x 40 mm, R1/D1 moved 7.5 mm, copper 214.5 -> 253.9 mm, DRC 0/0/0 |
| 2 - LED lights when output is low | `kicad/ex5_opt2/`, `ltspice/ex5_opt2/`, `python/plot_vtc_compare_ex5.py` | VM 2.35 V -> 2.48 V, LED current 4.29 mA now through the NMOS, +17.5 mm copper, DRC 0/0/0 |
| 3 - minimum clearance 0.4 mm | `kicad/ex5_opt3/` | Q1/Q2 changed to `TO-92_Inline_Wide` (pad gap 0.22 -> 1.04 mm), board unchanged, DRC 0/0/0 |
| 4 - trimpot replaced by 2-pin header J3, board shrunk | `kicad/ex5_opt4/` | Board 50 x 40 -> 34 x 29 mm, copper 214.5 -> 82.4 mm, DRC 0/0/0 |

## Run the plots
```
cd python
python plot_vtc_discrete.py "../ltspice/circuit VDD =5V.txt"   # -> CMOS_Inverter_VTC.png
python plot_overlay_65nm.py                                    # -> VTC_overlay_normalised.png
python plot_buffer_ex5_opt1.py ../ltspice/ex5_opt1/buffer_DC.txt ../ltspice/ex5_opt1/buffer_TRAN.raw   # -> buffer_ex5_opt1.png
```
Requires Python 3 with numpy, pandas, matplotlib.
