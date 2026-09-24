"""
BM6: Linear (eigenvalue) buckling of a pinned-pinned column (Euler II case).

Compares the DSM solver against the Euler critical load:
    Pcr = pi^2 * E * I / L^2

The buckling mode shape is sinusoidal, so this converges 
toward the exact value as the column is discretized into
more elements.

Run: python3 benchmarks/bm6_euler_buckling.py
"""
import numpy as np
from dsm_core import Structure, BucklingAnalysis

# Column properties (consistent kN, cm units) -- IPE 160 steel section
E = 21000.0    # Young's modulus, steel [kN/cm^2]
I = 869.27     # second moment of area, IPE 160 [cm^4]
A = 20.09      # cross-section area, IPE 160 [cm^2]
L = 400.0      # column length [cm]  (4 m)

n_elem = 10
s = Structure()
nodes = [s.add_node(x=i * L / n_elem, z=0.0) for i in range(n_elem + 1)]
nodes[0].support  = {"u": True,  "w": True, "phi": False}   # pinned
nodes[-1].support = {"u": False, "w": True, "phi": False}   # pinned (free to move axially)
for i in range(n_elem):
    s.add_element(nodes[i], nodes[i + 1], E=E, A=A, I=I)

# Small axial probe load for initialization of the stiffness matrix
s.add_node_load(nodes[-1], Fx=-1.0)

result = BucklingAnalysis(n_modes=1).solve(s)
Pcr_dsm = result["lambda"][0]

# Analytical reference value
Pcr_exact = np.pi**2 * E * I / L**2

print(f"BM6: Euler buckling, pinned-pinned column ({n_elem} elements)")
print(f"  critical load : DSM = {Pcr_dsm:.4f} kN   analytical = {Pcr_exact:.4f} kN")

assert abs(Pcr_dsm - Pcr_exact) / Pcr_exact < 1e-4, "critical load does not match analytical solution"
print("  PASS")
