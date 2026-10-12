# Methodology

## 1. Setup
- **Tools:** Cadence Virtuoso (schematic), Spectre (DC and transient), ADE-L, Visualization & Analysis XL.
- **Technology:** TSMC 65 nm CMOS (PDK not distributed).
- **Design under test:** the "UNO DPU" schematic, a single FlexDCIM-style DPU bit-cell: 6T SRAM latch (PU1/PU2, PD1/PD2, PG1/PG2)
  plus the digital logic (P1-P3, N2-N5) that gates the stored bit against WS / EN / RWL and drives CBL. 16 instances, 16 nets, 8 I/O pins; logic devices are LVT.
- Cell ratio CR = W_PD / W_PG and pull-up ratio PR = W_PU / W_PG are the main knobs for read stability and write-ability.

## 2. DPU transient verification
Transient analysis, 0 - 100 ns, for Q = 1 and Q = 0.

| Signal | Role |
|---|---|
| WL / BLB | write the operand bit into the cell (Q / QB) |
| WS | weight select, gates the stored bit into the logic slice |
| EN | enables the digital multiply path (precharge / evaluate) |
| RWL | read word-line, times the evaluation window |
| CBL | compute bit-line, accumulated multiply output |

## 3. Butterfly-curve SNM
The feedback loop is broken, one storage node is swept with a DC source and the opposite node recorded, for both inverters (two VTCs).
One VTC is mirrored on the other; **SNM is taken from the largest inscribed square** (marker extraction in Visualization & Analysis XL,
or `scripts/python/snm_butterfly.py` on exported data).

| Mode | WL | Bit-lines | Purpose |
|---|---|---|---|
| Hold | low | n/a | data retention |
| Read | high | precharged | read disturb |
| Write-mode | high | at retention levels | half-selected cell write disturb |

## 4. PVT matrix
| Axis | Values |
|---|---|
| Process corners | TT, FF, SS, SF, FS |
| Temperature | 10, 20, 30, 40, 50 C (swept as a design-variable family) |
| Supply | 1.1 V, 1.2 V (nominal), 1.3 V |

5 corners x 3 supplies x 5 temperatures = **75 simulations per mode**. The worst case over temperature is reported for each corner / supply,
giving **15 values per mode** ([`results.md`](results.md)).

## 5. N-curve
A voltage source forces node Q from 0 to VDD (WL = VDD, BL = BLB = VDD) and the current into Q is recorded. Zero crossings give the stable-low point V0,
the trip point and the stable-high point V1.

| Metric | Definition (`scripts/python/ncurve_metrics.py`) |
|---|---|
| SVNM | V_trip - V0, read voltage margin |
| SINM | max abs(I) between V0 and V_trip, read current margin |
| WTV | V1 - V_trip (V1 = third crossing or VDD), write voltage margin |
| WTI | max abs(I) between V_trip and V1, write current margin |

## 6. Functional model
`scripts/python/mac8_golden.py` models DPU products, binary adder tree and bit-serial shift-and-add, and provides expected values for
digital testbenches.
