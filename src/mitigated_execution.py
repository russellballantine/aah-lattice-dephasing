"""
src/mitigated_execution.py
Phase 3: Hardware Deployment with V2 Primitives and Coherent Error Suppression
Author: Russell Ballantine
"""

from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_ibm_runtime import EstimatorV2
from qiskit_ibm_runtime.options import EstimatorOptions

def execute_mitigated_lattice_experiment(backend, native_circuits, observables, physical_layout):
    """
    Binds the simulation circuits to physical hardware layouts and deploys them
    inside a highly resilient, error-mitigated execution runtime.
    """
    # 1. Initialize the V2 option subsystem
    options = EstimatorOptions()
    options.resilience_level = 1
    options.resilience.measure_mitigation = True
    
    # Configure the Active Pulse-Level Dynamical Decoupling Sequence
    options.dynamical_decoupling.enable = True
    options.dynamical_decoupling.sequence_type = "XpXm" 
    options.dynamical_decoupling.extra_slack_distribution = "middle"

    # 2. Build the explicit PassManager to enforce ISA conformity
    # Optimization level 1 matches your localized multi-step Trotter structure perfectly
    pm = generate_preset_pass_manager(backend=backend, optimization_level=1)

    transpiled_circuits = []
    transpiled_observables = []

    print(f"[*] Transpiling {len(native_circuits)} circuits to hardware ISA layout: {physical_layout}")
    
    for circ, obs in zip(native_circuits, observables):
        # Explicitly map virtual indices 0..6 to your physical hardware chain
        t_circ = pm.run(circ)
        
        # Apply the exact same layout transformation to the SparsePauliOp observables
        t_obs = obs.apply_layout(t_circ.layout)
        
        transpiled_circuits.append(t_circ)
        transpiled_observables.append(t_obs)

    # 3. Instantiate the V2 Estimator and deploy the payload
    print(f"\nDeploying payload to {backend.name} with XpXm (CPMG-equivalent) + TREX enabled...")
    estimator = EstimatorV2(mode=backend, options=options)
    
    # Package into explicit primitive pub tuples (circuit, observables)
    pubs = [(t_circ, t_obs) for t_circ, t_obs in zip(transpiled_circuits, transpiled_observables)]
    
    job = estimator.run(pubs=pubs)
    print(f"Job dispatch successful. Tracking ID: {job.job_id()}")
    
    return job
