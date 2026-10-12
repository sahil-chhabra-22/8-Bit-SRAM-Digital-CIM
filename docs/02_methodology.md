# Methodology (Cadence Virtuoso, TSMC 65 nm)

## 1. Setup
- Tool: Cadence Virtuoso + Spectre (ADE Assembler / ADE XL for corners).
- Library: TSMC 65 nm PDK (not distributed). Use the PDK's standard-Vt devices for the 6T latch; LVT for read
  path / digital logic as in FlexDCIM.
- Sizing: record W/L of PU, PD, PG (and N1/N2) in the table below.

| Device | Role | Type (SVT/LVT) | W (nm) | L (nm) |
|---|---|---|---|---|
| PU1/PU2 | pull-up | | | |
| PD1/PD2 | pull-down | | | |
| PG1/PG2 | pass-gate | | | |
| N1/N2 | LVT read path | | | |

Cell ratio CR = W_PD/W_PG; pull-up ratio PR = W_PU/W_PG.

## 2. Butterfly-curve SNM
Break the feedback loop and sweep one storage node, recording the other, for each inverter (the two VTCs).
Plot VTC1 and mirrored VTC2; **SNM = side of the largest square inscribed in the smaller lobe**.

| Mode | WL | BL / BLB | Notes |
|---|---|---|---|
| Hold | 0 | don't care (VDD) | retention |
| Read | VDD | VDD / VDD | worst-case read disturb |
| Write | VDD | 0 / VDD (writing '0' on the Q side) | one lobe collapses; write-SNM = remaining lobe |

DC sweep: `Vin` on Q (0 -> VDD, step 5-10 mV), output = QB; repeat on the QB side. Export `v, qb_of_q, q_of_qb`.

## 3. N-curve
Insert a voltage source `Vin` on node Q, sweep 0 -> VDD (BL = BLB = VDD, WL = VDD) and record the current `Iin`
flowing into Q. The curve crosses zero at the stable-low point, the trip point and the stable-high point.

| Metric | Definition (convention in `ncurve_metrics.py`) |
|---|---|
| SVNM | V_trip - V_stable0 (1st to 2nd zero crossing) - read voltage margin |
| SINM | max abs(I) between stable0 and trip - read current margin |
| WTV | V_stable1 - V_trip (stable1 = 3rd crossing, or VDD if absent) - write voltage margin |
| WTI | max abs(I) between trip and stable1 - write current margin |

If your report uses a different convention, edit the definitions in the script and update this table.

## 4. PVT sweep
| Axis | Values (edit to match your runs) |
|---|---|
| Process | TT, FF, SS, FS, SF |
| Voltage | e.g. nominal -10 %, nominal, nominal +10 % |
| Temperature | e.g. -40, 27, 125 C |

In ADE XL: *Corners* tab -> add model-section corners, set `temperature` and `VDD` variables, run all, export
results to CSV as `corner,temp_c,vdd,metric,value` (see `data/pvt_template.csv`).

## 5. Optional: Monte Carlo
Mismatch Monte Carlo (e.g. 500-1000 samples) at TT/27 C for read SNM and write margin; report mean, sigma and
mean/sigma.

## 6. Functional verification
`scripts/python/mac8_golden.py` models DPU -> adder tree -> shift-and-add. Use its vectors as expected values
when testing the digital schematic.
