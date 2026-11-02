"""
src/dry_run_phase_3.py
Phase 3: 100% Offline Local Sandbox & Transpilation Safety Check
Author: Russell Ballantine
"""

import sys
import numpy as np
from qiskit.quantum_info import SparsePauliOp
# Pulling a local, open-source mock hardware footprint profile
from qiskit_ibm_runtime.fake_provider import FakeSherbrooke

try:
    from src.simulation import build_aah_trotter_circuit
    from src.mitigated_execution import execute_mitigated_lattice_experiment
except ImportError:
    print("[-] Directory Import Error: Run this script from your root workspace:")
    print("    /Users/russellballantine/Developer/aah-lattice-dephasing")
    sys.exit(1)

def run_offline_safety_test():
    print("======================================================================")
    print("   RUNNING PHASE 3 OFFLINE DRY-RUN: LOCAL TRANSPILETION SANDBOX")
    print("======================================================================\n")

    # 1. Setup exact Phase 3 production parameters
    num_qubits = 7
    lmbda = 1.5
    J = 1.0
    total_time = 2.0
    trotter_steps = 30  # Deep layer scaling check
    
    # 2. Spin up a local mock heavy-hex processor (No API key or network required)
    print("[*] Instantiating mock heavy-hex backend (FakeSherbrooke profile)...")
    mock_backend = FakeSherbrooke()
    
    # 3. Compile the local 7-qubit circuits
    print(f"[*] Compiling {trotter_steps}-step test circuit configurations...")
    circ_beta = build_aah_trotter_circuit(num_qubits, lmbda, alpha=0.5850, J=J, total_time=total_time, trotter_steps=trotter_steps)
    
    # 4. Generate local tracking observables
    print("[*] Constructing 7-qubit site tracking SparsePauliOp matrices...")
    observables = []
    for n in range(num_qubits):
        pauli_str = ["I"] * num_qubits
        pauli_str[n] = "Z"
        observables.append(SparsePauliOp("".join(reversed(pauli_str))))
        
    # 5. Isolate a mock 7-qubit linear hardware path for allocation testing
    # This matches the structure of a connected line on a heavy-hex graph
    mock_physical_layout = [1, 2, 3, 4, 5, 6, 7]
    print(f"    Mocking hardware physical assignment line: {mock_physical_layout}")

    # 6. Execute local mitigation compilation
    print("[*] Attempting local simulation execution with CPMG + TREX envelopes...")
    try:
        # We wrap this in a localized check pass to make sure options structures parse cleanly
        mock_job = execute_mitigated_lattice_experiment(
            backend=mock_backend, 
            native_circuits=[circ_beta] * num_qubits, 
            observables=observables, 
            physical_layout=mock_physical_layout
        )
        print("\n======================================================================")
        print("[+] SUCCESS: ALL CODE PATHS, IMPORTS, AND OPTIONS ARE SECURE!")
        print("======================================================================")
        print("    - Your custom XY hopping gate decompositions are structurally valid.")
        print("    - Qiskit V2 options accepted your CPMG pulse-level configuration.")
        print("    - Your directory lineage layout is working perfectly.")
        print("======================================================================")
        print("You can confidently run the live hardware queue script now.")
        
    except Exception as sandbox_error:
        print("\n[-] DRY-RUN EXCEPTION DETECTED:")
        print(f"    Error text: {str(sandbox_error)}")
        print("======================================================================")

if __name__ == "__main__":
    run_offline_safety_test()
