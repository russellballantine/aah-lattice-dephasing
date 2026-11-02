Here is the complete, comprehensive Mathematical Methodology section. This formalizes the transition from musical pitch intervals to the Hamiltonian terms executed on ibm_kingston.
Open or create notes/research_note_03.md and append this exact technical text to serve as the core theory section of your future paper.

Mathematical Methodology: Pitch-Space to Hamiltonian Translation


1. Geometric Construction of the Modulation Parameter (\(\alpha \))

The spatial structure of the on-site potential landscape in Phase Beta is fundamentally dictated by the group-theoretic properties of the Spiral of Fifths.
In equal-tempered music theory, a perfect fifth corresponds to a frequency ratio of \(3:2\). Logarithmically mapping this pitch interval into a modulo-1 continuous circle (octave equivalence) defines the generator for the spiral:
\(\alpha _{0}=\log _{2}\left(\frac{3}{2}\right)\approx 0.58496250072...\)
Because \(\alpha_0 \in \mathbb{R} \setminus \mathbb{Q}\), stacking sequential perfect fifths never perfectly closes the circle, generating a dense, non-repeating trajectory. Truncating this irrational generator to four decimal places establishes your empirical experimental constraint:
\(\alpha =0.5850\)
Anhemitonic pentatonic pitch-class sets correspond to a specific localized window of this trajectory. By taking five successive steps along this spiral generator (\(n \in \{0, 1, 2, 3, 4\}\)), we isolate the five fundamental intervals of the pentatonic scale before octave reductions:
\(\mathcal{P}=\{k\cdot \alpha \mathinner{\;\left(\mod \,1\right)}\}\quad \text{for\ }k\in [0,4]\)
This specific projection sets up the spatial frequency of the quasiperiodic lattice potentials.

2. Ingestion into the Tight-Binding Aubry-André-Harper (AAH) Model

The continuous-time quantum walk (CTQW) of your single-excitation wave packet is governed by a modified 1D Aubry-André-Harper Hamiltonian. In the second quantization formalism, restricted to the single-excitation subspace, the Hamiltonian operator is written as:
\(\^{H}=-J\sum _{n=0}^{L-2}\left(\^{c}_{n+1}^{\dag }\^{c}_{n}+\^{c}_{n}^{\dag }\^{c}_{n+1}\right)+2\lambda \sum _{n=0}^{L-1}\cos (2\pi \alpha n+\phi )\^{c}_{n}^{\dag }\^{c}_{n}\)
Where:
• \(L = 7\): The total physical qubit volume of the linear lattice footprint.
• \(\^{c}_{n}^{\dag }\) (\(\^{c}_{n}\)): The standard fermionic creation (annihilation) operators mapping site-localized single excitations.
• \(J = 1.0\): The kinetic hopping amplitude defining nearest-neighbor state transfer.
• \(\lambda = 1.5\): The quasiperiodic potential scaling factor. Because \(\lambda > 1.0\) (\(J=1\)), the system is pushed past the critical self-dual threshold into the spatially localized phase.
• \(\phi = 0.0\): The global phase shift offset.

The Contrast Baselines:

• Periodic Control Baseline (\(\alpha = 0.0\)): Resolves the potential to a static, translationally invariant drone: \(V_n = 2\lambda\). This allows uninhibited wave transport until it encounters a localized hardware bottleneck.
• Phase Beta Experiment (\(\alpha = 0.5850\)): Injects the pentatonic spatial modulation. The on-site potential energies \(V_n = 2\lambda \cos(2\pi (0.5850) n)\) vary across the lattice sites, introducing a self-similar, fractal-like energy barrier configuration.

3. Trotter-Suzuki Product Decomposition for Superconducting QPUs

To deploy this continuous Hamiltonian onto digital quantum hardware (ibm_kingston), the unitary time-evolution operator \(\hat{U}(t) = \exp(-i\hat{H}t)\) must be discretized. We employ a first-order Suzuki-Trotter decomposition over \(M = 30\) discrete time slices (\(\Delta t = t/M = 2.0/30\)):
\(\^{U}(t)=\left[\exp \left(-i\^{H}_{\text{pot}}\Delta t\right)\exp \left(-i\^{H}_{\text{hop}}\Delta t\right)\right]^{M}+\mathcal{O}(\Delta t^{2})\)

Layer A: Diagonal On-Site Potential Gates

The diagonal potential terms commute natively and are mapped onto individual single-qubit phase rotations (\(RZ\)). For each step \(m \in [1, M]\), we apply:
\(\^{U}_{\text{pot}}(\Delta t)=\bigotimes _{n=0}^{L-1}RZ(\theta _{n}),\quad \text{where\ }\theta _{n}=-4\lambda \cos (2\pi \alpha n)\Delta t\)

Layer B: Nearest-Neighbor XY Hopping Blocks

The off-diagonal hopping terms do not commute globally. We partition them into non-conflicting nearest-neighbor pairs, executed via your custom decomposed XY interaction gates:
\(\^{U}_{\text{hop}}(\Delta t)=\prod _{n=0}^{L-2}\exp \left(iJ\Delta t(\^{X}_{n}\^{X}_{n+1}+\^{Y}_{n}\^{Y}_{n+1})\right)\)
This unitary operation explicitly preserves the total excitation number (\(\sum_n \langle \hat{n}_n \rangle = 1\)), keeping the wave packet trapped strictly within your 7-site computational subspace.

4. Hardware Observables Mapping

Because live superconducting QPUs do not support non-destructive statevector tracking, site populations must be extracted via physical Z-basis projective measurements.
For each site \(n\), the physical population probability operator \(\hat{P}_n = \hat{c}_n^\dagger \hat{c}_n\) maps directly to a 7-qubit SparsePauliOp expectation value string:
\(\^{P}_{n}=\frac{\^{I}-\^{Z}_{n}}{2}\bigotimes _{k\ne n}\^{I}_{k}\)
The hardware returns the expectation value \(\langle \hat{Z}_n \rangle\), which your extraction pipeline converts to the final site populations:
\(P(\text{Site\ }n)=\frac{1-\langle \^{Z}_{n}\rangle _{M}}{2}\)
This mathematical translation directly explains how the pentatonic geometric frequency \(\alpha \) altered the on-site potential landscape to successfully protect your quantum wave packet from the high-dephasing center node (\(Q48\)).