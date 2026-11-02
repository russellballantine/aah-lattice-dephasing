"""
src/run_phase_3.py
Phase 3 Orchestration: Live Hardware Query and Mitigated Execution Deployment
Author: Russell Ballantine
"""

import sys
import numpy as np
from qiskit.quantum_info import SparsePauliOp
from qiskit_ibm_runtime import QiskitRuntimeService

# Import your validated Phase 1/2/3 workspace modules
try:
    from src.simulation import build_aah_trotter_circuit
    from src.hardware_query import find_defective_7qubit_chain
    from src.mitigated_execution import execute_mitigated_lattice_experiment
except ImportError:
    print("[-] Directory Import Error: Ensure this script runs from your root workspace:")
    print("    /Users/russellballantine/Developer/aah-lattice-dephasing")
    sys.exit(1)

def run_hardware_deployment():
    print("======================================================================")
    print("STARTING PHASE 3: LIVE HARDWARE EXECUTION & ACTIVE ERROR MITIGATION")
    print("======================================================================\n")

    # --- 1. System Parameter Initialization ---
    num_qubits = 7
    lmbda = 1.5          # Quasiperiodic potential strength
    J = 1.0              # Kinetic hopping amplitude
    total_time = 2.0     # Evolution timeframe
    trotter_steps = 30   # Deep execution to observe stable tail dynamics
    
    # --- 2. Initialize Qiskit Runtime Service ---
    print("[*] Connecting to IBM Quantum Runtime Service...")
    try:
        service = QiskitRuntimeService()
    except Exception as e:
        print(f"[-] Authentication Failed: Ensure your API token is configured. Error: {e}")
        return

    # Filter out active, operational real-world systems
    print("[*] Filtering available heavy-hex hardware fleet...")
    backend = service.least_busy(simulator=False, operational=True)
    print(f"    Selected target processor: {backend.name}")

    # --- 3. Topology Scan for Native Central Defect ---
    print("[*] Scanning device properties for a coherence-starved center node...")
    try:
        physical_layout = find_defective_7qubit_chain(backend)
    except Exception as e:
        print(f"[-] Topology Scan Failed: {e}")
        return

    # --- 4. Circuit Assembly (Phase Beta vs. Periodic Baseline) ---
    print(f"\n[*] Generating {trotter_steps}-step Trotter circuits (7-qubit lattice)...")
    
    # Configuration A: Phase Beta (Quantum RAID Array)
    alpha_beta = 0.5850
    circ_beta = build_aah_trotter_circuit(
        num_qubits, lmbda, alpha_beta, J, total_time, trotter_steps
    )
    
    # Configuration B: Periodic Control Baseline (Single Point of Failure)
    alpha_periodic = 0.0
    circ_periodic = build_aah_trotter_circuit(
        num_qubits, lmbda, alpha_periodic, J, total_time, trotter_steps
    )

    # --- 5. Generate One-Hot Site Population Observables ---
    print("[*] Mapping 7-qubit SparsePauliOp tracking observables...")
    observables = []
    for n in range(num_qubits):
        pauli_str = ["I"] * num_qubits
        pauli_str[n] = "Z"
        # Little-endian reversal matching Qiskit's coordinate indexing
        observables.append(SparsePauliOp("".join(reversed(pauli_str))))

    # --- 6. Live Mitigation Deployment (CPMG + TREX) ---
    # We pass duplicate circuit references matching the length of our observables list
    print("\n[*] Packing payload into active mitigation envelopes...")
    
    print("\n[--> Dispatching Phase Beta Experiment]")
    job_beta = execute_mitigated_lattice_experiment(
        backend, [circ_beta] * num_qubits, observables, physical_layout
    )
    
    print("\n[--> Dispatching Periodic Control Baseline]")
    job_periodic = execute_mitigated_lattice_experiment(
        backend, [circ_periodic] * num_qubits, observables, physical_layout
    )

    # --- 7. Summarize Tracking Protocols ---
    print("\n======================================================================")
    print("[+] PHASE 3 PAYLOAD DISPATCH COMPLETED SUCCESSFULLY")
    print("======================================================================")
    print(f"    Target Machine:        {backend.name}")
    print(f"    Physical Layout:       {physical_layout}")
    print(f"    Phase Beta Job ID:     {job_beta.job_id()}")
    print(f"    Periodic Baseline ID:  {job_periodic.job_id()}")
    print("======================================================================")
    print("Track your jobs via the IBM Quantum Platform Console.")
    print("Once complete, parse the results to evaluate the Phase Beta RAID survival tail.")

if __name__ == "__main__":
    run_hardware_deployment()
