# Results

All values are from Spectre DC simulations in Cadence Virtuoso (TSMC 65 nm), post-processed in Visualization & Analysis XL.
Each table entry is the **worst case over the 10-50 C temperature family** for that corner and supply.
Raw values: [`data/snm_pvt_summary.csv`](../data/snm_pvt_summary.csv). Plots: [`results/figures/`](../results/figures/).

## Summary

| Mode | Range (V) | Worst case | Best case |
|---|---|---|---|
| Hold SNM | 0.452 - 0.788 | SF, 1.1 V | FS, 1.3 V |
| Read SNM | 0.479 - 0.810 | SF, 1.1 V | FS, 1.3 V |
| Write-mode SNM | 0.469 - 0.801 | SF, 1.1 V | FS, 1.3 V |

Every simulated condition shows a positive margin: no corner loses data in hold, suffers read disturb or write-mode (half-select) disturb
over 1.1-1.3 V and 10-50 C.

![SNM vs VDD](../results/figures/snm_vs_vdd.png)
![SNM 3D](../results/figures/snm_3d.png)

## Hold SNM (V)

| Corner | VDD = 1.1 V | VDD = 1.2 V | VDD = 1.3 V |
|---|---|---|---|
| TT | 0.520 | 0.622 | 0.720 |
| FF | 0.529 | 0.629 | 0.729 |
| SS | 0.531 | 0.631 | 0.731 |
| FS | 0.589 | 0.688 | 0.788 |
| SF | 0.452 | 0.558 | 0.658 |

## Read SNM (V)

| Corner | VDD = 1.1 V | VDD = 1.2 V | VDD = 1.3 V |
|---|---|---|---|
| TT | 0.528 | 0.633 | 0.733 |
| FF | 0.546 † | 0.646 | 0.746 |
| SS | 0.530 | 0.630 | 0.730 |
| FS | 0.608 | 0.709 | 0.810 |
| SF | 0.479 | 0.579 | 0.679 |

† FF at 1.1 V is a trend-interpolated estimate; the direct simulation was still pending (70 of 75 read points completed).

## Write-mode SNM (V)

| Corner | VDD = 1.1 V | VDD = 1.2 V | VDD = 1.3 V |
|---|---|---|---|
| TT | 0.529 | 0.629 | 0.729 |
| FF | 0.539 | 0.639 | 0.739 |
| SS | 0.532 | 0.632 | 0.732 |
| FS | 0.601 | 0.701 | 0.801 |
| SF | 0.469 | 0.569 | 0.639 |

## Observations

1. **Voltage dependence.** In all three modes SNM rises almost linearly with supply, about +100 mV for every +0.1 V. The one exception is
   SF in write-mode, which gains only +70 mV between 1.2 V and 1.3 V.
2. **Corner spread is set by N/P skew, not overall speed.** TT, FF and SS stay within about 11 mV (hold), 18 mV (read) and 10 mV (write) of each other,
   whereas the skewed corners separate widely. At 1.1 V the SF-to-FS spread is 137 mV (hold), 129 mV (read) and 132 mV (write); in write-mode it widens to 162 mV at 1.3 V.
3. **SF is the critical corner in every mode and at every voltage.** The weak (slow) NMOS pull-down is the limiting device. FS, with a strong NMOS, is always best.
4. **Temperature has a small effect.** Across 10-50 C the family of traces stays tight, so temperature sensitivity is minor next to voltage and process sensitivity.
5. **Read and write-mode track hold closely** (hold 0.452-0.788 V, read 0.479-0.810 V, write 0.469-0.801 V), consistent with the decoupled read port of the 8T cell not penalising the storage latch.
6. **Improvement path for the SF corner:** up-size the pull-down devices or use assist techniques (for example negative bit-line or boosted word-line bias).

## DPU transient verification

The "UNO DPU" schematic (16 instances, 16 nets, 8 I/O pins; all logic devices LVT) was simulated with a transient analysis from 0 to 100 ns.
Stimulus was applied to WL, BLB, WS, EN and RWL, with the compute output observed on CBL and the stored bit read at Q.

| Stored bit | CBL behaviour | Output pulses |
|---|---|---|
| Q = 1 | CBL ramps upward in each active RWL / WS window | 6 |
| Q = 0 | CBL shows brief negative-going dips; fewer windows register a valid pulse | 4 |

EN and RWL timing sets the same evaluation window in both cases, so control-signal timing is independent of the stored data.

**Open item:** the reference truth table expects CBL to stay at logic 0 for Q = 0. The residual pulses and dips seen for Q = 0 should be
reviewed in the full WS x Q sweep (coupling or stimulus timing are the first things to check).

## Note on SNM readings

The values above are the **marker readings** from Visualization & Analysis XL. The side of a square inscribed in a butterfly lobe cannot exceed VDD / 2
(0.55, 0.60 and 0.65 V at 1.1, 1.2 and 1.3 V), yet several readings do, which is consistent with the marker reporting the **diagonal** of the
inscribed square (the 45-degree rotated-axis separation). The side-equivalent values (reading / sqrt(2)) are given below for completeness, and every plot can be regenerated on
this basis with `python scripts/python/snm_summary.py data/snm_pvt_summary.csv --convention side`.

<details><summary>Side-equivalent SNM (V) = marker reading / sqrt(2)</summary>

**Hold**

| Corner | VDD = 1.1 V | VDD = 1.2 V | VDD = 1.3 V |
|---|---|---|---|
| TT | 0.368 | 0.440 | 0.509 |
| FF | 0.374 | 0.445 | 0.515 |
| SS | 0.375 | 0.446 | 0.517 |
| FS | 0.416 | 0.486 | 0.557 |
| SF | 0.320 | 0.395 | 0.465 |

**Read**

| Corner | VDD = 1.1 V | VDD = 1.2 V | VDD = 1.3 V |
|---|---|---|---|
| TT | 0.373 | 0.448 | 0.518 |
| FF | 0.386 † | 0.457 | 0.528 |
| SS | 0.375 | 0.445 | 0.516 |
| FS | 0.430 | 0.501 | 0.573 |
| SF | 0.339 | 0.409 | 0.480 |

**Write-mode**

| Corner | VDD = 1.1 V | VDD = 1.2 V | VDD = 1.3 V |
|---|---|---|---|
| TT | 0.374 | 0.445 | 0.515 |
| FF | 0.381 | 0.452 | 0.523 |
| SS | 0.376 | 0.447 | 0.518 |
| FS | 0.425 | 0.496 | 0.566 |
| SF | 0.332 | 0.402 | 0.452 |

</details>

## Status and next steps

- [ ] Run the pending read-mode simulation for FF at 1.1 V and replace the estimate.
- [ ] Re-check write-mode SF at 1.3 V (0.639 V), which departs from the otherwise linear trend.
- [ ] Sweep the full WS x Q truth table on the DPU and confirm CBL polarity and magnitude.
- [ ] Layout the DPU and re-verify timing post-extraction.
- [ ] Monte Carlo (local mismatch) on hold, read and write margins.
- [ ] Tile into a multi-row, multi-column macro and estimate energy per MAC.
