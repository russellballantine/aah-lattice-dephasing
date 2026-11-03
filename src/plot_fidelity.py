"""
src/plot_fidelity.py
Author: Russell Ballantine
Description: Generates publication-ready comparative multi-panel line plots
             contrasting AAH and Symmetric wave scaling behaviors.
"""

import os
import pandas as pd
import matplotlib.pyplot as plt

def generate_publication_plot():
    csv_path = "notes/scaling_trendlines.csv"
    output_image = "notes/fidelity_decay_comparison.png"
    
    if not os.path.exists(csv_path):
        print(f"Error: Could not locate data at '{csv_path}'. Please run 'src/noisy_simulation.py' first.")
        return

    # Load numerical data
    df = pd.read_csv(csv_path)
    
    # Configure academic plot styling parameters
    plt.rcParams.update({
        "font.family": "serif",
        "font.size": 11,
        "axes.labelsize": 12,
        "axes.titlesize": 12,
        "xtick.labelsize": 10,
        "ytick.labelsize": 10,
        "legend.fontsize": 10,
        "grid.alpha": 0.3
    })
    
    # Initialize 1x2 side-by-side subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.5), sharex=True)
    
    # --- PANEL A: CENTER NODE POPULATION TRANSITION ---
    ax1.plot(df["System_Size"], df["AAH_Center"], color="#1f77b4", marker="o", linewidth=2, label="AAH (Quasi-Periodic)")
    ax1.plot(df["System_Size"], df["SYM_Center"], color="#d62728", marker="s", linestyle="--", linewidth=2, label="SYM (Periodic Control)")
    
    ax1.set_title("Panel A: Center Node Stagnation ($P_{\\text{center}}$)")
    ax1.set_ylabel("Probability Density Fraction")
    ax1.set_xlabel("System Size ($n$ Qubits)")
    ax1.set_ylim(-0.05, 1.05)
    ax1.set_xticks([11, 15, 21])
    ax1.grid(True, linestyle=":")
    ax1.legend(loc="lower left")
    
    # --- PANEL B: NEIGHBOR CLUSTER SUM RESERVATION ---
    ax2.plot(df["System_Size"], df["AAH_Neighbor_Sum"], color="#2ca02c", marker="o", linewidth=2, label="AAH Spectator Ring")
    ax2.plot(df["System_Size"], df["SYM_Neighbor_Sum"], color="#9467bd", marker="s", linestyle="--", linewidth=2, label="SYM Spectator Ring")
    
    ax2.set_title("Panel B: Bystander Cluster Sum ($P_{\\text{neighbors}}$)")
    ax2.set_xlabel("System Size ($n$ Qubits)")
    ax2.set_ylim(-0.05, 1.05)
    ax2.grid(True, linestyle=":")
    ax2.legend(loc="upper left")
    
    plt.tight_layout()
    
    # Save directly to notes directory matching workspace specifications
    plt.savefig(output_image, dpi=300, bbox_inches="tight")
    plt.close()
    print(f">> Publication asset successfully rendered and saved to '{output_image}'.")

if __name__ == "__main__":
    generate_publication_plot()
