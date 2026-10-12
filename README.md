# SRAM-Based Digital Compute-in-Memory (FlexDCIM)

**Cadence Virtuoso · Spectre · SRAM Bit-Cell Analysis · PVT Characterization**

A VLSI design and simulation project focused on a FlexDCIM-style SRAM Digital Processing Unit (DPU), including schematic-level transient verification and SRAM stability analysis using static noise margin (SNM).

> **Scope note:** This repository documents the circuit implementation and analyses described in the project materials. The full 64 Kb FlexDCIM macro and its published performance figures belong to the referenced research paper; they are not claims of a full-chip implementation in this repository.

## Project at a glance

- **EDA flow:** Cadence Virtuoso, ADE-L / Visualization & Analysis XL, Spectre
- **Technology context:** TSMC 65 nm CMOS
- **Circuit focus:** SRAM storage cell combined with a digital compute logic slice
- **Verification:** Transient response for stored states Q = 0 and Q = 1
- **Stability:** Hold-, read-, and write-mode butterfly-curve SNM
- **Variation study:** TT, FF, SS, SF and FS process corners; 1.1 V, 1.2 V and 1.3 V supplies; 10–50 °C temperature sweep

## Why SRAM compute-in-memory?

In a conventional processor-memory system, moving data between memory and compute logic consumes time and energy. Compute-in-memory (CIM) places selected operations closer to stored data, reducing repeated data movement. Digital SRAM-CIM uses digital logic for computation and is designed to integrate with conventional CMOS logic flows.

This project examines a DPU-style cell from the FlexDCIM architecture and studies both compute-path behaviour and SRAM storage stability.

## Circuit architecture

The reference DPU combines an SRAM storage section with a digital logic section. The storage nodes retain the bit (Q / QB), while control signals select and time the compute path. The compute output is observed on CBL.

| Signal | Role in the presented testbench |
|---|---|
| WL / BLB | Write/control the stored operand state |
| WS | Weight-select control |
| EN | Enables the digital compute path |
| RWL | Read/evaluation timing |
| Q / QB | Complementary SRAM storage nodes |
| CBL | Compute bit-line output |

The project presentation includes the architecture, Cadence schematic and simulation waveforms. Technical figures should be actual circuit/simulation artefacts; conceptual illustrations should be labelled as illustrations.

## Methodology

### 1. Schematic implementation
The DPU-style SRAM cell and digital logic slice were captured in Cadence Virtuoso, following the reference architecture and device connections described in the project presentation.

### 2. Transient verification
Spectre transient analysis was run over a 0–100 ns interval. Input/control stimuli were applied to the word-line, weight-select, enable and read-word-line signals. The stored state and compute output were inspected for Q = 0 and Q = 1.

### 3. SRAM stability analysis
Butterfly curves were used to estimate static noise margin (SNM). The largest square that fits between the mirrored voltage-transfer curves provides the SNM measure.

- **Hold SNM:** word-line held low; evaluates data-retention stability.
- **Read SNM:** read condition with word-line asserted and bit-lines precharged; evaluates read-disturb robustness.
- **Write-mode SNM:** evaluates stability under the write/half-select condition used in the simulation setup.

### 4. PVT characterization
The presented sweeps cover five process corners (TT, FF, SS, SF, FS), three supply values (1.1 V, 1.2 V, 1.3 V) and five temperatures (10–50 °C). Each mode is assessed using the worst-case SNM reported for each corner/supply combination.

## Reported results

The project presentation reports these SNM ranges across the evaluated corners and supply values:

| Analysis | Reported SNM range | Lowest reported condition | Highest reported condition |
|---|---:|---|---|
| Hold | 0.452–0.788 V | SF, 1.1 V | FS, 1.3 V |
| Read | 0.479–0.810 V* | SF, 1.1 V | FS, 1.3 V |
| Write mode | 0.469–0.801 V | SF, 1.1 V | FS, 1.3 V |

*The source presentation identifies the FF-corner result at 1.1 V as an estimate pending direct simulation. Treat it as provisional rather than a fully simulated measurement.

The transient presentation reports six CBL output pulses for the shown Q = 1 case and four for the shown Q = 0 case. These are observations from the presented waveforms, not a substitute for a complete truth-table sweep.

For corner-by-corner tables, waveform interpretation and open items, see [results notes](docs/results.md) and [methodology](docs/methodology.md).

## Tools and why they are used

| Tool | Purpose in this project |
|---|---|
| **Cadence Virtuoso** | Schematic capture and circuit-level design |
| **Spectre** | Transient and DC simulation |
| **ADE-L / Visualization & Analysis XL** | Simulation setup, waveform inspection and curve analysis |
| **Python (supporting scripts only)** | Optional post-processing, tabulation and plotting of exported numerical results; not the circuit-design or simulation engine |
| **Git / GitHub** | Versioning and documentation |

Python is a supporting analysis/automation tool where scripts are provided. The core engineering work is circuit design and simulation in the EDA flow.

## Repository structure

~~~text
.
├── assets/              # Repository artwork
├── data/                # Numerical input/result data
├── docs/                # Background, methodology and results
├── results/figures/     # Plots derived from documented data
├── schematics/          # Circuit schematic material
├── scripts/             # Supporting analysis and automation
├── testbenches/         # Testbench templates
└── tests/               # Automated checks for supporting scripts
~~~

## Scope and next steps

- Complete and document the full WS × Q truth-table sweep.
- Clearly separate measured simulation output from estimated or interpolated values.
- Add high-resolution screenshots of the actual Cadence schematic and transient/SNM plots from the project presentation.
- If layout and extracted-view verification are completed, include the corresponding layout, DRC/LVS and post-layout evidence; otherwise list them as future work.

## References

1. V. Sharma, X. Zhang, N. S. Dhakad and T. T.-H. Kim, “FlexDCIM: A 400 MHz 249.1 TOPS/W 64 Kb Flexible Digital Compute-in-Memory SRAM Macro for CNN Acceleration,” *IEEE Transactions on Circuits and Systems I*, vol. 72, no. 10, 2025.
2. C.-J. Jhang et al., “Challenges and Trends of SRAM-Based Computing-In-Memory for AI Edge Devices,” *IEEE Transactions on Circuits and Systems I*, vol. 68, no. 5, 2021.

The referenced papers describe research architectures and published macro-level results. Those figures should not be presented as measurements from this project unless independently reproduced.

## Author

**Sahil Chhabra**  
B.Tech — VLSI Design & Technology
