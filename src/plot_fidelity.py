import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Ensure notes directory exists
os.makedirs('notes', exist_ok=True)

# Set publication style defaults
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams.update({
    'font.size': 11,
    'axes.labelsize': 12,
    'axes.titlesize': 12,
    'xtick.labelsize': 11,
    'ytick.labelsize': 11,
})

def plot_spatial_hardware_distribution():
    """Dynamically loads real QPU telemetries and generates the spatial distribution plot."""
    print("Generating Figure 1: 7-node spatial hardware comparison plot...")
    try:
        phase_beta_striped = np.loadtxt("notes/phase3_beta_pop.txt")
        periodic_control = np.loadtxt("notes/phase3_periodic_pop.txt")
    except Exception as e:
        print(f"Error loading hardware files: {e}")
        return

    nodes = np.arange(7) 
    fig, ax = plt.subplots(figsize=(8, 5))
    width = 0.35
    
    ax.bar(nodes - width/2, periodic_control, width, label='Periodic Control Baseline', color='#7f8c8d', edgecolor='black')
    ax.bar(nodes + width/2, phase_beta_striped, width, label='Phase Beta Striped', color='#2c3e50', edgecolor='black')
    ax.axvspan(2.5, 3.5, color='#e74c3c', alpha=0.15, label='Defect Node Workspace (Qubit 48)')
    
    defect_idx = 3
    gap = phase_beta_striped[defect_idx] - periodic_control[defect_idx]
    ax.annotate(f'+{gap*100:.2f}% Gap', 
                xy=(defect_idx + width/2, phase_beta_striped[defect_idx]), 
                xytext=(defect_idx + 0.8, phase_beta_striped[defect_idx] + 0.03),
                fontweight='bold', color='#e74c3c',
                arrowprops=dict(arrowstyle="->", color="#e74c3c", connectionstyle="arc3,rad=-0.2"))

    ax.set_xlabel('Physical QPU String Index (Center = Node 3 / Qubit 48)', fontweight='bold', labelpad=10)
    ax.set_ylabel('Site Population Probability', fontweight='bold')
    ax.set_title('Physical 7-Qubit Spatial Distribution Benchmark (ibm_kingston)', pad=15, fontweight='bold')
    ax.set_xticks(nodes)
    ax.set_xticklabels([f'Node {i}' for i in range(7)])
    ax.set_ylim(0, max(np.max(periodic_control), np.max(phase_beta_striped)) + 0.08)
    ax.legend(loc='upper right', frameon=True)
    plt.tight_layout()
    plt.savefig('notes/hardware_7qubit_comparison.png', dpi=300)
    plt.close()
    print("Saved: notes/hardware_7qubit_comparison.png")

def plot_numerical_scaling():
    """Dynamically loads scaling CSV data and plots true physical IPR scaling trendlines."""
    print("Generating Figure 2: IPR scaling trendline plot...")
    try:
        df = pd.read_csv("notes/scaling_trendlines.csv")
    except Exception as e:
        print(f"Error loading scaling CSV: {e}")
        return

    fig, ax = plt.subplots(figsize=(8, 5))
    
    # Plot IPR trajectories
    ax.plot(df['System_Size'], df['AAH_IPR'], marker='s', linewidth=2.5, color='#2c3e50', 
            label='AAH Pentatonic (Dynamic Delocalization/Routing)')
    ax.plot(df['System_Size'], df['SYM_IPR'], marker='o', linewidth=2.0, linestyle='--', color='#7f8c8d', 
            label='SYM Flat Control (Stagnant/Localized Core)')
    ax.plot(df['System_Size'], df['Ideal_Delocalized_Limit'], linestyle=':', color='#e74c3c', alpha=0.6,
            label='Theoretical Maximum Delocalization (1/N)')
    
    ax.set_xlabel('Lattice Dimension (Total Available Qubits)', fontweight='bold', labelpad=10)
    ax.set_ylabel('Inverse Participation Ratio (IPR)', fontweight='bold')
    ax.set_title('Topological Anti-Localization Trends under Defect Dephasing', pad=15, fontweight='bold')
    ax.set_xticks(df['System_Size'])
    ax.set_ylim(0.0, 0.6)
    ax.legend(loc='upper right', frameon=True)
    plt.tight_layout()
    plt.savefig('notes/numerical_scaling_trends.png', dpi=300)
    plt.close()
    print("Saved: notes/numerical_scaling_trends.png")


if __name__ == '__main__':
    plot_spatial_hardware_distribution()
    print("-" * 50)
    plot_numerical_scaling()
    print("\nAll plotting channels are completely isolated, decoupled, and clean!")
