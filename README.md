# AAH Phase Beta: Quantum Lattice Dephasing Simulation

An investigation into the resilience of **Incommensurate Musical Lattices (Phase Beta / Spiral of Fifths)** against environmental dephasing and thermal noise using open quantum system simulations on superconducting hardware blueprints.

## Project Lineage & Context

This repository represents the next phase of research following the initial proof of concept developed in [pentatonic-quantum-walks](https://github.com). 

While the previous project successfully demonstrated the theoretical foundations of continuous-time quantum walks across non-periodic, untempered lattices in idealized environments, **this project serves as a direct follow-on to test whether those theories hold up in a real physical environment.** By deploying these circuits onto live IBM Quantum superconducting quantum computers, we aim to measure exactly how well the structural theory protects against true environmental decoherence.

---

## Core Research Objective

This project evaluates whether the low spectral fractal dimension ($D_f = 0.5744$) of the **Aubry-André-Harper (AAH) Phase Beta** configuration provides a mechanism of hardware-level "geometric locking." The goal is to determine if this topological structure can actively suppress environmental decoherence ($T_1$ energy relaxation and $T_2$ dephasing errors) when mapped to an open quantum system.

---

## Quantum Mapping & Architecture

### Unary (One-Hot) Encoding Scheme
To implement a Continuous-Time Quantum Walk (CTQW) layout efficiently on physical processors, this framework avoids standard compact binary registers in favor of a unary mapping:
* **Qubit Assignment:** Each individual physical lattice site maps directly to a single physical qubit (e.g., a 5-site lattice maps to a 5-qubit array).
* **State Initialization:** A single excitation is injected at the center site. For a 5-qubit array, the initial walker state is prepared as $|00100\rangle$, positioning the excitation on qubit 2 (0-indexed).
* **Conservation Rule:** The total number of qubit excitations is strictly conserved at 1 ($\sum \langle Z_i \rangle$) throughout the entire execution duration.

---

## Methodology & Hamiltonian Translation

### Trotterization Setup
Because the kinetic hopping term ($J$) and the quasiperiodic potential term ($\lambda$) do not commute, the global time-evolution operator $U(t) = e^{-iHt}$ is discretized into finite time slices ($\Delta t = t/n$) via a first-order Trotter-Suzuki product formula:

$$U(\Delta t) \approx e^{-i H_{\text{hop}} \Delta t} \times e^{-i H_{\text{pot}} \Delta t}$$

1. **On-Site Potential Implementation:** The diagonal landscape is driven by single-qubit $R_z(\theta_n)$ gates on each qubit $n$, parameterized by:
   $$\theta_n = -2 \lambda \cos(2\pi\alpha n) \Delta t$$
   * For **Phase Beta (Spiral of Fifths)**, the irrational modulation frequency is locked to $\alpha \approx 0.5850$.
   * For the **Periodic Control**, the modulation is disabled by setting $\alpha = 0.0$.
2. **Nearest-Neighbor Hopping Layer:** Off-diagonal kinetic coupling requires state exchanges between adjacent nodes. This is executed using an excitation-preserving $XY$-interaction layout (built via CNOT chains and rotation blocks), smoothly sliding the single excitation between neighbors $n$ and $n+1$.

---

## Experimental Workflow

* **Step 1: Noise-Free Controls:** Circuits are verified using Qiskit's `AerSimulator` (Statevector mode) to construct the mathematically ideal physical reference states.
* **Step 2: Real Hardware Execution:** Identical transpiled circuits are targeted for deployment on active IBM Quantum heavy-hex processors (e.g., `ibm_brisbane`).
* **Step 3: Fidelity Tracking:** Quantum State Fidelity is evaluated across expanding gate depths. If the Spiral of Fifths model inherently provides geometric locking, its hardware fidelity profile will degrade significantly slower over time than the periodic baseline control.

## Engineering Constraints

* **Circuit Depth Mitigation:** Physical two-qubit gates are highly error-prone. The lattice footprint is intentionally kept compact (5 to 7 qubits) with compressed Trotter steps ($n = 2$ or $3$) to prevent early channel decoherence.
* **Hardware Topology Matching:** To completely bypass the automatic insertion of costly, noisy `SWAP` gates, the Qiskit transpiler is explicitly forced to pin the logical layout to a physically connected linear string of hardware qubits on the chip.

---

## Local Setup & Environment

Ensure you have Python 3.10+ and a virtual environment activated:

```bash
# Clone the repository
git clone https://github.com/russellballantine/aah-lattice-dephasing
cd aah-lattice-dephasing

# Install localized dependencies
pip install -r requirements.txt
```
