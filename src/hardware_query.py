"""
src/hardware_query.py
Phase 3: Hardware Topology and Fault-Tolerant Calibration Profiling
Author: Russell Ballantine
"""

import numpy as np
from qiskit_ibm_runtime import QiskitRuntimeService

def find_defective_7qubit_chain(backend):
    """
    Scans the backend coupling map for a linear chain of 7 qubits where
    the center qubit (index 3) is a local coherence defect (low T2).
    Skips any paths containing qubits with missing calibration properties.
    """
    configuration = backend.configuration()
    properties = backend.properties()
    coupling_map = configuration.coupling_map
    
    # Build an adjacency list representation of the heavy-hex map
    adj = {}
    for u, v in coupling_map:
        if u not in adj: adj[u] = []
        if v not in adj: adj[v] = []
        adj[u].append(v)
        adj[v].append(u)
        
    # Helper to pull T2 time safely for a physical qubit
    def get_t2_safe(q):
        try:
            # First try the newer direct wrapper or fallback to standard dictionary property
            return properties.t2(q)
        except Exception:
            try:
                # Secondary property lookup fallback
                val_tuple = properties.qubit_property(q, 'T2')
                return val_tuple[0] if isinstance(val_tuple, tuple) else val_tuple
            except Exception:
                # If neither works, flag it as missing/dead
                return None

    found_chains = []
    
    # Simple recursive DFS to isolate unique paths of length 7
    def dfs(node, path):
        if len(path) == 7:
            found_chains.append(list(path))
            return
        for neighbor in adj.get(node, []):
            if neighbor not in path:
                path.append(neighbor)
                dfs(neighbor, path)
                path.pop()

    for start_node in adj.keys():
        dfs(start_node, [start_node])
        
    best_candidate_chain = None
    max_defect_ratio = 0.0  # Ratio of average outer T2 to center T2
    valid_paths_count = 0
    
    print(f"Scanned backend '{backend.name}'. Found {len(found_chains)} total 7-qubit topological lines.")
    
    for chain in found_chains:
        # Pull T2 profile safely, discarding any chains with missing properties
        t2_profile = [get_t2_safe(q) for q in chain]
        if None in t2_profile:
            continue  # Silently drop lines passing through uncalibrated/dead qubits
            
        valid_paths_count += 1
        
        # Isolate the center node vs its surrounding neighbors
        center_t2 = t2_profile[3]
        outer_t2s = t2_profile[:3] + t2_profile[4:]
        avg_outer_t2 = np.mean(outer_t2s)
        
        # Look for a maximized ratio where outer qubits are pristine but the center drops
        defect_ratio = avg_outer_t2 / center_t2
        
        if defect_ratio > max_defect_ratio:
            max_defect_ratio = defect_ratio
            best_candidate_chain = (chain, t2_profile)

    print(f"    Filtered out paths with dead telemetry tags. {valid_paths_count} paths fully verified.")

    if best_candidate_chain:
        chain, t2s = best_candidate_chain
        print("\n[+] Optimal Defect-Centred Layout Isolated:")
        print(f"    Physical Qubit Layout: {chain}")
        print(f"    Center Node (Q{chain[3]}) T2: {t2s[3]*1e6:.2f} µs")
        print(f"    Average Neighbor T2: {np.mean(t2s[:3]+t2s[4:])*1e6:.2f} µs")
        print(f"    Defect Factor: {max_defect_ratio:.2f}x worse coherence at center.")
        return chain
    else:
        raise ValueError("No suitable 7-qubit linear chains with complete T2 attributes found.")

if __name__ == "__main__":
    service = QiskitRuntimeService()
    target_backend = service.least_busy(simulator=False, operational=True)
    target_chain = find_defective_7qubit_chain(target_backend)
