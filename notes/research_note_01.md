# Research Note 01: Phase 1 Simulation Baseline Analytics
**Date:** October 2026  
**Author:** Russell Ballantine  
**Project:** AAH Phase Beta Lattice Dephasing Simulation

---

## 1. Executive Summary & Verification Context
Initial noise-free verification runs have been successfully executed via the Qiskit `AerSimulator` (Statevector mode). The script confirmed complete subspace isolation inside the targeted unary (one-hot) manifold. Out of $2^5 = 32$ possible global states, the CNOT-decomposed hopping gates successfully confined the quantum walker to the 5 valid single-excitation states.

The purpose of this note is to document the exact probability distributions of the ideal states and outline the mathematical framework for the upcoming simulated noise channels.

---

## 2. Quantitative Baseline Metrics

The two configurations distribute quantum information across the 5-site physical lattice in fundamentally distinct ways over identical evolution timeframes ($t = 2.0$, $\text{steps} = 3$):

### Configuration A: Periodic Control ($\alpha = 0.0$)
* **State Population Vector:**
  * $|00001\rangle$: 0.0082
  * $|00010\rangle$: 0.0749
  * $|00100\rangle$: **0.6591** (Initialization Site)
  * $|01000\rangle$: 0.1893
  * $|10000\rangle$: 0.0686

* **Decoherence Vulnerability Assessment:** The wavefunction is heavily localized at the center node ($|00100\rangle$). This represents high vulnerability to single-point hardware defects. Because the excitation remains concentrated on a single physical qubit, localized $T_1$ energy relaxation or sharp $T_2$ phase drifts on that specific node will catastrophically degrade global state fidelity.

### Configuration B: Phase Beta / Spiral of Fifths ($\alpha \approx 0.5850$)
* **State Population Vector:**
  * $|00001\rangle$: **0.2163** (Boundary Site)
  * $|00010\rangle$: 0.0131
  * $|00100\rangle$: 0.3763 (Initialization Site)
  * $|01000\rangle$: 0.1188
  * $|10000\rangle$: **0.2755** (Boundary Site)

* **Resilience Mechanics Theory:** The incommensurate phase landscape forces the wavefunction to tunnel and fragment cleanly across the topology, populating the outer boundary nodes. This spatial delocalization desensitizes the global system to single-qubit failure modes. Spreading the population across the entire linear array allows local, independent $T_2$ environmental phase fluctuations to self-average via complex destructive interference.

---

## 3. Next Milestone: Simulated Open Quantum Systems

To rigorously validate this "geometric locking" resilience before real hardware deployment, Phase 2 will implement local **Noisy Simulations**:

1. **Hardware Noise Profiling:** Import real-world calibration metrics ($T_1$ relaxation, $T_2$ dephasing, and coherent gate error rates) from modern 127-qubit heavy-hex processors (such as `ibm_fez` or `ibm_marrakesh`).
2. **Open System Modeling:** Build custom Qiskit thermal relaxation channels using Lindblad-type Kraus operators.
3. **Fidelity Decay Tracking:** Measure and plot Quantum State Fidelity degradation as a function of expanded Trotter gate depth to confirm if Phase Beta suppresses decoherence compared to the periodic baseline.
