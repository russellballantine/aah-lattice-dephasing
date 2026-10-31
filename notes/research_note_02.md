# Research Note 02: Open Quantum System Noisy Simulation & Error Budget Characterization
**Author:** Russell Ballantine  
**Date:** October 31, 2026  
**Project Lineage:** Direct follow-on to Phase 1 Noise-Free Baseline Validation (`aah-lattice-dephasing`)

---

## 1. Executive Summary & Core Breakthroughs
In this phase, we successfully transitioned our continuous-time quantum walk simulation from an idealized statevector sandbox into a realistic open quantum system environment. Utilizing a customized, isolated 7-qubit digital twin profile based on the hardware parameters of the `FakeFez` 127-qubit heavy-hex processor, we evaluated the dephasing resilience of the Aubry-André-Harper (AAH) Phase Beta configuration against a standard periodic control baseline.

The primary architectural breakthrough was the empirical demonstration of a **"Quantum RAID" data striping mechanism** inherent to the quasiperiodic AAH geometry. By intentionally injecting a severe localized dephasing defect ($T_2 = 5\ \mu\text{s}$) on the center qubit (Qubit 3), we monitored how spatial delocalization shields global state vectors from point-source environmental decay over long Trotter horizons.

---

## 2. The Computer Science Analogy: Quantum Data Striping (RAID)
To understand why the AAH Phase Beta geometry outlasts the flat baseline, the results can be mapped directly to classical hard-disk array redundancy frameworks (RAID-4/RAID-5):

* **The Hardware Disks (Physical Qubits):** Each physical qubit in our 7-qubit open boundary chain functions as an independent hard-disk storage drive holding a fractional piece of the global state space.
* **Periodic Control ($\alpha = 0.0$) — Single Point Failure:** Storing the quantum walk packet purely on the center node is identical to saving a mission-critical file on a single hard drive (Disk 3) with zero redundancy. When Disk 3 encounters a severe localized defect, the file is instantly corrupted. The stationary quantum state has a catastrophic single point of failure.
* **Phase Beta ($\alpha = 0.5850$) — Quantum Data Striping:** The incommensurate modulation acts as an automatic hardware-level striping algorithm. It splits and distributes the wave function across all healthy drives simultaneously (Disks 0, 1, 4, 5, 6). While Disk 3 still inflicts local damage, the remaining drives retain the distributed structural pieces of the global state, enabling a resilient, flatter decay tail that routes around the hardware failure in real time.

---

## 3. Quantitative Error Budget & Statistical Bounds

While the geometric routing mechanism functions perfectly in a deterministic simulation, a rigorous statistical analysis is required to determine if this survival advantage stands out against real-world processor noise floors.

### 3.1 The Long-Time Fidelity Tail (Trotter Step 20 Profile)
* **Phase Beta (Striped State):** $F \approx 0.045$ (4.5% absolute overlap)
* **Periodic Control (Trapped State):** $F \approx 0.020$ (2.0% absolute overlap)
* **Absolute Saved Signal ($\Delta F$):** $\mathbf{0.025}$ (A tiny 2.5% absolute gap)
* **Relative State Vector Advantage:** $\frac{0.045 - 0.020}{0.020} = \mathbf{+125\%}$

### 3.2 Hardware Noise Envelope Characterization
When transitioning from our digital twin loop to a live physical processor like `ibm_brisbane`, our 2.5% signal must fight through three separate physical noise ceilings:

1. **Statistical Projection Error (Shot Noise):** For a high-shot measurement strategy ($N = 8,192$ shots), the standard statistical projection uncertainty is:
   $$\sigma = \frac{1}{\sqrt{\text{Shots}}} = \frac{1}{\sqrt{8192}} \approx \mathbf{1.1\%}$$
   Our absolute signal gap ($2.5\%$) sits at roughly **$2.27\sigma$** relative to shot noise. It represents a mathematically clear trend line, but possesses a very slim clearance window.
2. **State Preparation and Measurement (SPAM) Errors:** Physical readout lines on superconducting architectures introduce an assignment error of 1% to 2% per line. Across our active 7-qubit array, this adds a systematic measurement uncertainty envelope of roughly **$\pm 1.5\%$**.
3. **Daily Calibration Drift:** The baseline execution noise of our deep Trotter circuits (requiring up to 144 two-qubit CNOT gates by step 30) fluctuates over time due to ambient cryogenic shifts, introducing a calibration error margin of roughly **$\pm 2.0\%$**.

### 3.3 The Physical Verdict
Summing our physical hardware variables ($1.1\% \text{ shot} + 1.5\% \text{ SPAM} + 2.0\% \text{ drift}$), the real-world device error budget expands to a total envelope of **$\pm 3\% \text{ to } 4\%$**. 

Because our raw absolute signal gap is **$2.5\%$**, **the geometric advantage would be completely swallowed alive by background noise on a live chip unless active error mitigation layers are implemented.** The global state decays so rapidly under the unmitigated CNOT gate noise floor that the structural advantage becomes difficult to extract. Phase 3 must introduce active layers like Zero-Noise Extrapolation (ZNE) or Dynamical Decoupling (DD) to artificially suppress this background gate floor.

---

## 4. Rationale for Enhanced 'RAID' Performance on Live Physical Machines
Crucially, our digital twin utilizes a simplified, Markovian white-noise model. There are three physical mechanisms present on real superconducting processors that could cause the geometric "RAID" striping effect to be **significantly more effective on a live machine** than our simulation predicts:

### 4.1 Coherent Crosstalk Scrambling
Our simulation assumes noise is strictly localized and independent per line. Real transmon processors suffer from parasitic microwave leakage (crosstalk) across adjacent qubits. In a stationary, localized circuit, these parasitic phases accumulate constructively over time, compounding into large phase errors on the target qubit. Phase Beta's rapid spatial motion continuously fragments and shuffles the wave packet, scrambling local parasitic phases before they can form systematic multi-qubit coherent errors.

### 4.2 Spatial Filtering of Non-Markovian $1/f$ Material Noise
Superconducting circuits are heavily degraded by slow, lingering $1/f$ noise caused by microscopic substrate impurities and flux fluctuations. A stationary quantum state is completely at the mercy of its local environment drifting off-resonance over long durations. Phase Beta's continuous spatial quantum walks sweep the wave function through localized material defects faster than the slow environment can establish a phase lock. This works as a spatial analogue to dynamical decoupling, allowing the information to outrun local slow-drifting defects.

### 4.3 Statistical Self-Averaging Across the Lattice
Striping the wave function across a 7-qubit open boundary chain forces the global state to sample a broad spatial ensemble of noise distributions simultaneously. Instead of suffering the catastrophic failure of a single bad drive, the distributed state averages out local variations. This self-averaging properties slow down global decay rates into a stable, predictable tail that is inherently more robust than the localized control.

---

## 5. Next Steps for Phase 3
To prepare for physical deployment onto live IBM Quantum backends, our immediate next milestones are:
1. **Live Backend Topology Queries:** Write an automated execution routine via `qiskit-ibm-runtime` to scan active processors and find a linear chain of 7 qubits where the central qubit possesses a distinct daily coherence defect ($T_2$ drop).
2. **Dynamical Decoupling Integration:** Build a pulse-level sequencer to embed refocusing pulse trains ($X-\tau-X$) into the circuit's idling periods, manually crushing the global gate-error floor to let our geometric advantage stand out cleanly outside the hardware noise budget.
