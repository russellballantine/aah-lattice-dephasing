import numpy as np
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime.fake_provider import FakeFez
from qiskit_aer.noise import NoiseModel, thermal_relaxation_error
from qiskit.quantum_info import state_fidelity

def extract_fez_calibrations(qubits_of_interest):
    """Helper to inspect the baseline properties of our active qubits."""
    backend = FakeFez()
    print("--- FakeFez Digital Twin Hardware Calibration Snapshot ---", flush=True)
    for q in qubits_of_interest:
        props = backend.qubit_properties(q)
        print(f"Qubit {q}: T1 = {getattr(props, 't1', 'N/A')}s, T2 = {getattr(props, 't2', 'N/A')}s", flush=True)
    print("----------------------------------------------------------\n", flush=True)

def build_aah_trotter_circuit(num_qubits, lmbda, J, alpha, beta, total_time, trotter_steps):
    """Constructs the AAH quantum walk circuit using a 7-qubit single-excitation subspace."""
    qc = QuantumCircuit(num_qubits)
    
    # Position injection at the center of the 7-qubit chain (Qubit 3)
    center_qubit = num_qubits // 2
    qc.x(center_qubit) 
    
    dt = total_time / trotter_steps
    
    for step in range(trotter_steps):
        # 1. On-site potential energies
        for j in range(num_qubits):
            v_j = lmbda * np.cos(2 * np.pi * alpha * j + beta)
            qc.rz(2 * v_j * dt, j)
            
        # 2. XY Hopping terms across the open chain
        for j in range(num_qubits - 1):
            qc.h(j)
            qc.h(j+1)
            qc.cx(j, j+1)
            qc.rz(J * dt, j+1)
            qc.cx(j, j+1)
            qc.h(j)
            qc.h(j+1)
            
            qc.s(j)
            qc.s(j+1)
            qc.h(j)
            qc.h(j+1)
            qc.cx(j, j+1)
            qc.rz(J * dt, j+1)
            qc.cx(j, j+1)
            qc.h(j)
            qc.h(j+1)
            qc.sdg(j)
            qc.sdg(j+1)
            
    return qc

def run_noisy_analysis():
    num_qubits = 7
    lmbda = 1.5
    J = 1.0
    total_time = 2.0  
    max_steps = 30  # Keep it deep to see the long-term separation profile
    
    configs = {
        "Periodic Control": {"alpha": 0.0, "beta": 0.0},
        "Phase Beta": {"alpha": 0.5850, "beta": 0.0}
    }
    
    fake_backend = FakeFez()
    active_qubits = list(range(num_qubits))
    
    # Print the native hardware properties before override
    extract_fez_calibrations(active_qubits)
    
    filtered_noise_model = NoiseModel()
    single_qubit_gate_time = 35e-9  
    two_qubit_gate_time = 300e-9    
    
    # Build noise model with your intentional localized "Disk 3" drive failure
    for q in active_qubits:
        props = fake_backend.qubit_properties(q)
        t1 = props.t1
        
        # INJECT LOCALIZED SABOTAGE: Force the center qubit (Qubit 3) to have a lethal dephasing sink
        if q == 3:
            t2 = 5e-6  # 5 microseconds Coherence defect
            print(f"--> [RAID ALERT] Injecting severe localized defect on Center Qubit 3: T2 = {t2}s", flush=True)
        else:
            t2 = props.t2 # Keep the clean native hardware T2 for the surrounding disks
        
        thermal_err_1q = thermal_relaxation_error(t1, t2, single_qubit_gate_time)
        thermal_err_2q = thermal_relaxation_error(t1, t2, two_qubit_gate_time)
        
        if t2 <= 2 * t1:
            filtered_noise_model.add_quantum_error(thermal_err_1q, ['rz', 'x', 'sx', 'h'], [q])
            if q < num_qubits - 1:
                filtered_noise_model.add_quantum_error(thermal_err_2q.tensor(thermal_err_2q), ['cx'], [q, q+1])

    noisy_simulator = AerSimulator(method="density_matrix", noise_model=filtered_noise_model)
    ideal_simulator = AerSimulator(method="statevector")
    
    fidelity_results = {name: [] for name in configs}
    steps_range = list(range(1, max_steps + 1))
    
    for name, params in configs.items():
        print(f"Simulating dynamics for: {name}...", flush=True)
        for steps in steps_range:
            circuit = build_aah_trotter_circuit(
                num_qubits, lmbda, J, params["alpha"], params["beta"], total_time, steps
            )
            
            circuit_ideal = circuit.copy()
            circuit_ideal.save_statevector()
            
            transpiled_ideal = transpile(circuit_ideal, ideal_simulator)
            transpiled_noisy = transpile(circuit, basis_gates=['rz', 'x', 'sx', 'cx'], optimization_level=1)
            transpiled_noisy.save_density_matrix(label='final_rho')
            
            ideal_state = ideal_simulator.run(transpiled_ideal).result().get_statevector()
            noisy_result = noisy_simulator.run(transpiled_noisy).result()
            noisy_density_mat = noisy_result.data()['final_rho']
            
            fid = state_fidelity(ideal_state, noisy_density_mat)
            fidelity_results[name].append(fid)

    print("Generating and saving RAID striping comparison plot...", flush=True)
    plt.figure(figsize=(8, 5))
    plt.plot(steps_range, fidelity_results["Periodic Control"], 'o--', label="Periodic Control (Single Point Failure)", color='red')
    plt.plot(steps_range, fidelity_results["Phase Beta"], 'o-', label="Phase Beta (Quantum Data Striping)", color='blue')
    plt.title("Quantum Error Mitigation: Mitigating a Localized Coherence Defect")
    plt.xlabel("Trotter Steps")
    plt.ylabel("State Fidelity")
    plt.grid(True, linestyle=":")
    plt.legend()
    plt.savefig("notes/fidelity_decay_comparison.png")
    print("Execution complete! Plot saved to notes/fidelity_decay_comparison.png", flush=True)

if __name__ == "__main__":
    run_noisy_analysis()
