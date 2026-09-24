"""
BM7: Theory-of-2nd-Order moment amplification for a beam-column.

A pinned-pinned column under a transverse point load plus axial
compression N amplifies its bending moment compared to a 1st-order analysis.
This compares the DSM solver's amplification against the classical approximate formula:

    M_2nd / M_1st = 1 / (1 - N / Pcr)

Note: that formula is itself an engineering approximation, 
and dsm_core's Solver2ndOrder is an iterative fixed-point method. 
So this check uses a 10% tolerance.

Run: python3 benchmarks/bm7_beam_column_amplification.py
"""
import numpy as np
from dsm_core import Structure, Solver1stOrder, Solver2ndOrder

# Column/beam properties (consistent kN, cm units) -- IPE 160 steel section
E = 21000.0    # Young's modulus, steel [kN/cm^2]
I = 869.27     # second moment of area, IPE 160 [cm^4]
A = 20.09      # cross-section area, IPE 160 [cm^2]
L = 400.0      # length [cm]  (4 m)
P = 10.0       # transverse point load at midspan [kN]

n_elem = 20
N_ratio = 0.3   # axial compression as a fraction of the Euler critical load

s = Structure()
nodes = [s.add_node(x=i * L / n_elem, z=0.0) for i in range(n_elem + 1)]
nodes[0].support  = {"u": True,  "w": True, "phi": False}
nodes[-1].support = {"u": False, "w": True, "phi": False}
for i in range(n_elem):
    s.add_element(nodes[i], nodes[i + 1], E=E, A=A, I=I)

Pcr = np.pi**2 * E * I / L**2
N = N_ratio * Pcr

mid = nodes[n_elem // 2]
s.add_node_load(mid, Fz=P)
s.add_node_load(nodes[-1], Fx=-N)

res_1st = Solver1stOrder().solve(s)
res_2nd = Solver2ndOrder(tol=1e-8, max_iter=100).solve(s)

M_1st = max(abs(res_1st.internal_forces(e)["M_i"]) for e in s.elements)
M_2nd = max(abs(res_2nd.internal_forces(e)["M_i"]) for e in s.elements)

amplification_dsm        = M_2nd / M_1st
amplification_analytical = 1.0 / (1.0 - N_ratio)

print("BM7: beam-column, 2nd-order moment amplification (approximate check)")
print(f"  axial load N = {N_ratio:.0%} of Pcr = {N:.2f} kN")
print(f"  1st-order max moment : {M_1st:.2f} kNcm")
print(f"  2nd-order max moment : {M_2nd:.2f} kNcm")
print(f"  amplification factor : DSM = {amplification_dsm:.4f} (-)   "
      f"1/(1-N/Pcr) = {amplification_analytical:.4f} (-)")

rel_err = abs(amplification_dsm - amplification_analytical) / amplification_analytical
assert rel_err < 0.1, "amplification factor is off by more than the expected engineering tolerance"
print("  PASS")
