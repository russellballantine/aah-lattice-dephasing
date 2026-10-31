# Research Note 02: Open Quantum System Noisy Simulation & Error Budget Characterization
**Author:** Russell Ballantine  
**Date:** October 31, 2026  
**Project Lineage:** Direct follow-on to Phase 1 Noise-Free Baseline Validation (`aah-lattice-dephasing`)

---

## 1. Executive Summary & Core Physical Framework
In this phase, we transitioned the continuous-time quantum walk from the idealized, statevector sandbox of Phase 1 into an open quantum system density matrix simulator ($\rho(t)$). Utilizing an isolated 7-qubit digital twin profile parameterized by the physical properties of a 127-qubit heavy-hex architecture, we evaluated the dephasing resilience of the Aubry-André-Harper (AAH) model in the intermediate phase-beta regime ($\lambda = 1.5$, $J = 1.0$) against a translationally invariant periodic control baseline ($\lambda = 0.0$).

The core physical finding is a **passive reduction in the global state's effective decay rate, governed strictly by the spatial profile of the system's eigenstates**. By deliberately introducing a severe local dephasing channel ($T_2 = 5\ \mu\text{s}$) at the center node (Qubit 3), we demonstrated that the spatial properties of the phase-beta configuration alter the system's susceptibility to localized dissipation. This behavior is not an active routing mechanism; rather, it is a static consequence of the multifractal eigenbasis, which limits the global state's spatial overlap with the defect site and preserves a higher residual fidelity floor at long times.

---

## 2. Localization vs. Delocalization in the Open Chain
The comparative survival of the global state under a localized noise source is entirely determined by the projection of the initial state onto the eigenbasis and the subsequent spatial overlap of those eigenstates with the dissipation channel:

* **Periodic Control Baseline ($\lambda = 0.0$):** The system possesses full translational symmetry, yielding standard, spatially uniform Bloch waves. When the initial single-excitation wave packet is localized at the center node (Qubit 3), it projects evenly across all momentum states. Because these Bloch states have uniform amplitude across all sites, every mode interacts strongly and continuously with the dephasing channel at Qubit 3. The center node acts as an efficient entropy sink, rapidly scrambling the phases of all constituent modes and causing a rapid collapse of the global state fidelity.
* **Phase Beta Regime ($\lambda = 1.5$, $\alpha = 0.5850$):** This regime sits at the critical threshold between the fully extended and fully localized limits of the AAH model. The eigenstates are neither plane waves nor exponentially localized Anderson states; instead, they display a multifractal structure characterized by discrete spatial striping. Because the incommensurate potential shifts the onsite energies, the spatial probability density $|\psi_n(x)|^2$ of the dominant eigenstates at the position of Qubit 3 is significantly constrained. The wave function remains largely distributed across the remaining healthy nodes (Qubits 0, 1, 4, 5, 6). The global state decays slower simply because its interaction rate with the localized defect is lower.

---

## 3. Quantitative Error Budget & Statistical Bounds
To determine if this passive survival advantage is observable on live hardware, the absolute signal gap must be characterized against the composite physical noise floor of the target architecture.

### 3.1 The Long-Time Fidelity Tail (Trotter Step 20 Profile)
* **Phase Beta (Striped State):** $F \approx 0.045$ (4.5% absolute overlap)
* **Periodic Control (Trapped State):** $F \approx 0.020$ (2.0% absolute overlap)
* **Absolute Saved Signal ($\Delta F$):** $\mathbf{0.025}$ (A 2.5% absolute fidelity gap)
* **Relative State Vector Advantage:** $\frac{0.045 - 0.020}{0.020} = \mathbf{+125\%}$

### 3.2 Hardware Noise Envelope Characterization
When transitioning from the digital twin simulation to a physical processor, the 2.5% absolute signal gap must be resolved against three distinct physical noise sources:

1. **Statistical Projection Error (Shot Noise):** For a high-shot measurement strategy ($N = 8,192$ shots), the standard statistical projection uncertainty is:
   $$\sigma = \frac{1}{\sqrt{\text{Shots}}} = \frac{1}{\sqrt{8192}} \approx \mathbf{1.1\%}$$
   The absolute signal gap (2.5%) sits at exactly **$2.27\sigma$** relative to shot noise. This confirms a mathematically clear trend line but provides an insufficient operational margin.
2. **State Preparation and Measurement (SPAM) Errors:** Physical readout lines introduce assignment errors. Across the active 7-qubit array, this adds a systematic measurement uncertainty envelope of roughly **$\pm 1.5\%$**.
3. **Daily Calibration Drift & Gate Depolarization:** The baseline execution noise of our deep Trotter circuits (requiring up to 144 two-qubit CNOT gates by step 30) fluctuates over time due to ambient cryogenic shifts and gate infidelity, introducing a calibration error margin of roughly **$\pm 2.0\%$**.

### 3.3 The Physical Verdict
Compounding these variables ($1.1\%$ shot $+ 1.5\%$ SPAM $+ 2.0\%$ drift), the total physical hardware error budget expands to an envelope of **$\pm 3\% \text{ to } 4\%$**. 

Because the raw absolute signal gap is **$2.5\%$**, **the quasiperiodic survival advantage will be completely obscured by background noise on an unmitigated live processor.** The global state will decay under the weight of coherent gate noise before the structural difference can be resolved. Phase 3 must introduce active mitigation layers (e.g., Dynamical Decoupling and Zero-Noise Extrapolation) to artificially suppress the background gate floor and push the signal clear of the noise envelope.

---

## 4. Physical Mechanisms Influencing Live Hardware Scaling
Crucially, our digital twin relies on a simplified, Markovian white-noise model. On a physical superconducting processor, there are three non-Markovian and coherent mechanisms that will alter the phase-beta survival gap relative to the simulation predictions:

### 4.1 Coherent Crosstalk Suppression via Energy Mismatch
Physical transmon processors suffer from parasitic microwave leakage (crosstalk) across adjacent qubits. In a translationally invariant, periodic circuit, these parasitic phases accumulate constructively over time, compounding into severe systematic multi-qubit coherent errors. The spatial variation of the incommensurate AAH potential shifts adjacent qubits off-resonance from one another. This acts as a passive hardware-level filter, disrupting the phase-matching conditions required for parasitic microwave leakage and preventing coherent crosstalk from building up systematically.

### 4.2 Non-Markovian $1/f$ Environmental Interaction
Superconducting circuits are heavily degraded by slow, low-frequency $1/f$ noise caused by microscopic substrate impurities and flux fluctuations. A translationally invariant quantum walk is highly sensitive to these slow parameter drifts. In the phase-beta regime, the discrete spatial striping of the eigenstates forces the wave function to sample a broad, static distribution of onsite energies. This structural mismatch can disrupt the slow accumulation of relative phase errors from localized, slow-drifting environmental defects.

### 4.3 Statistical Self-Averaging Across the Lattice
Distributing the wave function across a 7-qubit open boundary chain forces the global state to sample a broad spatial ensemble of noise distributions simultaneously. Instead of suffering the catastrophic failure of a single bad node, the distributed state averages out local variations. This self-averaging property slows down global decay rates into a stable, predictable tail that is inherently more robust than the localized control.

---

## 5. Next Steps for Phase 3
To prepare for physical deployment onto live backends, our immediate next milestones are:
1. **Live Backend Topology Queries (`src/hardware_query.py`):** Automate a hardware scanning routine using `qiskit-ibm-runtime` to isolate a linear string of 7 connected hardware qubits where the center qubit naturally exhibits a severe daily coherence or charge-noise defect.
2. **Active Gate-Floor Suppression (`src/mitigated_execution.py`):** Build a pulse-level Dynamical Decoupling (DD) sequencer to embed refocusing pulse trains ($X-\tau-X$) into circuit idling intervals to crush the global CNOT noise floor, widening the signal window clear of the hardware noise budget.
