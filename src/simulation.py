import numpy as np
from qiskit import QuantumCircuit, QuantumRegister
from qiskit_aer import AerSimulator

def apply_xy_hopping_gate(qc, q_ctrl, q_targ, angle):
    """
    Decomposes the excitation-preserving XY / XX+YY interaction into native 
    basis gates (CNOT, RY, RZ) that the simulator and hardware can read directly.
    """
    # Map out the exact matrix translation for the single excitation swap
    # This structure natively preserves the total excitation number
    qc.rz(np.pi / 2, q_targ)
    qc.cx(q_targ, q_ctrl)
    qc.rz(-np.pi / 2, q_ctrl)
    qc.ry(angle / 2, q_targ)
    qc.cx(q_ctrl, q_targ)
    qc.ry(-angle / 2, q_targ)
    qc.cx(q_targ, q_ctrl)
    qc.rz(-np.pi / 2, q_ctrl)

def build_aah_trotter_circuit(num_qubits, lmbda, alpha, J, total_time, trotter_steps):
    """
    Constructs a Trotterized circuit for a continuous-time quantum walk (CTQW)
    on an Aubry-André-Harper (AAH) lattice using unary encoding.
    """
    qr = QuantumRegister(num_qubits, 'lattice')
    qc = QuantumCircuit(qr)
    
    # --- 1. State Initialization (Unary / One-Hot) ---
    # Inject a single excitation at the center site
    center_site = num_qubits // 2
    qc.x(qr[center_site])
    qc.barrier(label="init")
    
    # Calculate time slice duration
    delta_t = total_time / trotter_steps
    
    # --- 2. Hamiltonian Translation via Trotterization ---
    for step in range(trotter_steps):
        # Layer A: On-Site Potential Implementation (Diagonal Elements)
        for n in range(num_qubits):
            # theta_n = -2 * lambda * cos(2 * pi * alpha * n) * delta_t
            theta_n = -2 * lmbda * np.cos(2 * np.pi * alpha * n) * delta_t
            qc.rz(theta_n, qr[n])
        qc.barrier(label=f"pot_step_{step}")
        
        # Layer B: Nearest-Neighbor Hopping Implementation (Off-Diagonal Elements)
        for n in range(num_qubits - 1):
            # Effective interaction angle for the time slice
            angle = 2 * J * delta_t
            apply_xy_hopping_gate(qc, qr[n], qr[n+1], angle)
        qc.barrier(label=f"hop_step_{step}")
        
    return qc

def run_noise_free_simulation():
    # --- Core Configuration ---
    num_qubits = 7       # Updated to match the Phase 2/3 validated model sizing
    lmbda = 1.5          
    J = 1.0              
    total_time = 2.0     
    trotter_steps = 30   # Scaled up from 3 to observe deep localization tails
    
    print("--- Running AAH Phase Beta Reference Controls ---")
    # 1. Phase Beta (Spiral of Fifths Irrational Modulation)
    alpha_beta = 0.5850
    qc_beta = build_aah_trotter_circuit(num_qubits, lmbda, alpha_beta, J, total_time, trotter_steps)
    
    # 2. Periodic Control Baseline
    alpha_periodic = 0.0
    qc_periodic = build_aah_trotter_circuit(num_qubits, lmbda, alpha_periodic, J, total_time, trotter_steps)
    
    # --- Execute via AerSimulator (Statevector Mode) ---
    qc_beta.save_statevector()
    qc_periodic.save_statevector()
    
    simulator = AerSimulator(method="statevector")
    
    result_beta = simulator.run(qc_beta).result()
    result_periodic = simulator.run(qc_periodic).result()
    
    statevector_beta = result_beta.get_statevector()
    statevector_periodic = result_periodic.get_statevector()
    
        # --- Display Subspace Population Properties ---
    print("\n[Phase Beta Statevector Amplitudes]:")
    # FIX: Loop over .data to avoid the array deprecation warning
    for idx, amp in enumerate(statevector_beta.data):
        if np.abs(amp) > 1e-4:
            print(f"  |{idx:0{num_qubits}b}⟩: {amp:.4f} (Prob: {np.abs(amp)**2:.4f})")
            
    print("\n[Periodic Control Statevector Amplitudes]:")
    # FIX: Loop over .data here as well
    for idx, amp in enumerate(statevector_periodic.data):
        if np.abs(amp) > 1e-4:
            print(f"  |{idx:0{num_qubits}b}⟩: {amp:.4f} (Prob: {np.abs(amp)**2:.4f})")


if __name__ == "__main__":
    run_noise_free_simulation()
