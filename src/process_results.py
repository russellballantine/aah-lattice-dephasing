"""
src/process_results.py
Phase 3: Asynchronous Result Extraction and Physical Array Formatting
Author: Russell Ballantine
"""

import numpy as np
from qiskit_ibm_runtime import QiskitRuntimeService

def download_and_process_lattice_results(job_id_beta, job_id_periodic):
    service = QiskitRuntimeService()
    
    print(f"[*] Fetching completed returns from the cloud...")
    job_beta = service.job(job_id_beta)
    job_periodic = service.job(job_id_periodic)
    
    # This call blocks execution locally until the remote results are pulled down
    res_beta = job_beta.result()
    res_periodic = job_periodic.result()
    
    # 1. Parse Phase Beta (Quantum RAID) expectation values
    # Population on site n = (1 - <Z_n>) / 2
    pop_beta = []
    for pub_result in res_beta:
        # Cast the 0-dimensional scalar array directly to a float
        z_expectation = float(pub_result.data.evs) 
        pop_beta.append((1.0 - z_expectation) / 2.0)
        
    # 2. Parse Periodic Baseline expectation values
    pop_periodic = []
    for pub_result in res_periodic:
        z_expectation = float(pub_result.data.evs)
        pop_periodic.append((1.0 - z_expectation) / 2.0)
        
    print("\n=======================================================")
    print("   PHASE 3 EXPERIMENTAL RETURNS EXTRACTED SUCCESSFULLY")
    print("=======================================================")
    print(f"Phase Beta (Striped) Site Populations:\n{np.array(pop_beta)}")
    print(f"Periodic Control (Trapped) Site Populations:\n{np.array(pop_periodic)}")
    
    # Save arrays cleanly as text backups for your visualization pipeline
    np.savetxt("notes/phase3_beta_pop.txt", pop_beta)
    np.savetxt("notes/phase3_periodic_pop.txt", pop_periodic)
    print("\n[+] Raw telemetry data saved to notes/ directory.")

if __name__ == "__main__":
    BETA_ID = "dbkaqponceqs73alhcfg"
    PERIODIC_ID = "dbkaqq1ffo6c73bb5hlg"
    
    download_and_process_lattice_results(BETA_ID, PERIODIC_ID)
