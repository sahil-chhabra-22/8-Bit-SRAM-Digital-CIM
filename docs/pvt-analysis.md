# PVT Characterization Results — 8T SRAM DPU Bit-Cell

This page transcribes the worst-case SNM tables from the project's HOLD, READ and WRITE PVT presentations. Values are in volts and represent the reported worst-case marker across the 10, 20, 30, 40 and 50 °C family at each process-corner/supply pair.

## Hold-mode SNM

| Process corner | 1.1 V | 1.2 V | 1.3 V |
|---|---:|---:|---:|
| TT | 0.520 | 0.622 | 0.720 |
| FF | 0.529 | 0.629 | 0.729 |
| SS | 0.531 | 0.631 | 0.731 |
| FS | 0.589 | 0.688 | 0.788 |
| SF | 0.452 | 0.558 | 0.658 |

**Reported range:** 0.452–0.788 V. Lowest: SF at 1.1 V. Highest: FS at 1.3 V.

## Read-mode SNM

| Process corner | 1.1 V | 1.2 V | 1.3 V |
|---|---:|---:|---:|
| TT | 0.528 | 0.633 | 0.733 |
| FF | 0.546* | 0.646 | 0.746 |
| SS | 0.530 | 0.630 | 0.730 |
| FS | 0.608 | 0.709 | 0.810 |
| SF | 0.479 | 0.579 | 0.679 |

**Reported range:** 0.479–0.810 V. Lowest: SF at 1.1 V. Highest: FS at 1.3 V.

*The READ presentation marks FF at 1.1 V as trend-interpolated and pending direct simulation. The presentation states that 70 of 75 read-state simulation points were completed; this value must remain labelled as an estimate until measured.

## Write-mode SNM

| Process corner | 1.1 V | 1.2 V | 1.3 V |
|---|---:|---:|---:|
| TT | 0.529 | 0.629 | 0.729 |
| FF | 0.539 | 0.639 | 0.739 |
| SS | 0.532 | 0.632 | 0.732 |
| FS | 0.601 | 0.701 | 0.801 |
| SF | 0.469 | 0.569 | 0.639 |

**Reported range:** 0.469–0.801 V. Lowest: SF at 1.1 V. Highest: FS at 1.3 V.

## Combined comparison

| Mode | Minimum SNM | Minimum condition | Maximum SNM | Maximum condition |
|---|---:|---|---:|---|
| Hold | 0.452 V | SF, 1.1 V | 0.788 V | FS, 1.3 V |
| Read | 0.479 V | SF, 1.1 V | 0.810 V | FS, 1.3 V |
| Write | 0.469 V | SF, 1.1 V | 0.801 V | FS, 1.3 V |

### Interpretation

- SNM increases with supply voltage in all three reported datasets.
- SF (slow-NMOS / fast-PMOS) is the recurring worst-case corner; FS (fast-NMOS / slow-PMOS) is the recurring best-case corner.
- Do not treat the READ FF / 1.1 V value as a completed simulation result.
- These are values reported in the project's presentations. Re-check the source waveform/table before using them as a formal sign-off claim.

## Test matrix

| Parameter | Values |
|---|---|
| Process corners | TT, FF, SS, SF, FS |
| Supply voltage | 1.1 V, 1.2 V, 1.3 V |
| Temperature | 10 °C, 20 °C, 30 °C, 40 °C, 50 °C |
| Analysis | DC butterfly curve / SNM extraction in Cadence Virtuoso ADE-L and Spectre |
