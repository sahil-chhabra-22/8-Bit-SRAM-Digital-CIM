# Background

Reference designs: FlexDCIM (Sharma et al., 2025) and the SRAM-CIM survey by Jhang et al. (2021).

## Why compute-in-memory
Von Neumann machines move weights and activations between memory and PEs; this dominates latency and energy
for AI edge workloads. CIM merges the two (Jhang et al., 2021, Fig. 1-2).

## NMAC vs IMAC
- **NMAC (near-memory-array computing)**: array stores data as usual; adjacent digital/analog logic computes in the same cycle.
- **IMAC (in-memory-array computing)**: cells themselves multiply (weight x input); bit-line accumulates; an ADC digitises.

## SRAM-CIM design challenges (Jhang et al., Sec. II-C)
Read disturb, signal margin, process variation, cell area and computing latency. These motivate the stability
analyses in this repository: **read disturb -> read SNM / SVNM**, **process variation -> PVT + Monte-Carlo**.

## FlexDCIM design highlights
1. Fully digital MAC with no accuracy loss (no ADC, no analog non-idealities).
2. Weight precision reconfigurable 1-8 b (`WS<7:0>` from `WSEL<2:0>`), input precision via bit-serial.
3. SA-less SRAM read: all CBLs go through the adder tree and an OR gate (Fig. 12).
4. Power-gated, clock-enabled full adder.

### Bit-cell (Sec. III-A)
- 8T SRAM part: 6T latch + LVT N1, N2 that discharge BLX when RWL (input) and Q (weight) are both '1'.
- Digital logic: LVT P1-P3, N3-N5; output inverter P3-N4-N5 drives CBL. N4 holds CBL until the next evaluation.
- Precharge of BLX/BLI with EN = '0'; evaluation when EN and WS go high.

### Area (Sec. III-B)
Eight 8T parts share one logic block: 6/8 = 0.75 T per bit overhead -> **8.75 T** per bit-cell (8x1 DPU).

### Macro (Sec. IV)
512 x 128 array, 16 adder trees, 16 accumulators; 64 x 16 parallel 1b x 8b multiplications, 14-bit outputs.

## Unsigned 8-bit MAC arithmetic
For N = 64 parallel inputs: one cycle gives sum of 64 products of 1b x 8b -> max 64 x 255 = 16320 < 2^14 (14-bit).
Over 8 bit-serial cycles with shift-and-add: max 64 x 255 x 255 = 4,161,600 < 2^22 (22-bit accumulator).
