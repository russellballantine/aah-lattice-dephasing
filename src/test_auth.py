"""
src/test_auth.py
Quick connection and authorization ping for IBM Quantum API channels.
"""

from qiskit_ibm_runtime import QiskitRuntimeService

def ping_ibm_quantum():
    print("[*] Probing local environment for stored IBM Quantum credentials...")
    
    try:
        # Initializing without arguments forces a check on your local json configuration profile
        service = QiskitRuntimeService()
        print("[+] Active Session Verification Achieved.")
        print(f"    Available Allocation Channel: {service.channel}")
        
        # Pull instances/instances configurations to prove network connection is green
        instances = service.instances()
        print(f"    Authenticated Access Profiles: {instances}")
        print("\n=======================================================")
        print("[+] CONNECTION STATUS: VERIFIED AND ACTIVE")
        print("=======================================================")
        
    except Exception as base_error:
        print("\n[-] CONNECTION STATUS: FAILURE")
        print("    No valid local credentials were found cached or your API token is invalid.")
        print("    Error Details:", str(base_error))
        print("-------------------------------------------------------")
        print("[*] Remedy: Please provide your 44-character IBM Quantum API Token below to save it locally.")

if __name__ == "__main__":
    ping_ibm_quantum()
