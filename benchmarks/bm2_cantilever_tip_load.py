"""
BM2: Cantilever, transverse point load at the free tip.

Compares the DSM solver against the classical Euler-Bernoulli formulas:
    w_tip = P * L^3 / (3 * E * I)     (tip deflection)
    M_fix = P * L                     (moment at the fixed end)

Run: python3 benchmarks/bm2_cantilever_tip_load.py
"""
from dsm_core import Structure, Solver1stOrder

# Beam properties (consistent kN, cm units) -- IPE 160 steel section
E = 21000.0    # Young's modulus, steel [kN/cm^2]
I = 869.27     # second moment of area, IPE 160 [cm^4]
A = 20.09      # cross-section area, IPE 160 [cm^2]
L = 400.0      # length [cm]  (4 m)
P = 10.0       # point load at the tip [kN]

# Build: fixed support -- free tip, point load at the tip
s = Structure()
n1 = s.add_node(x=0.0, z=0.0, support={"u": True, "w": True, "phi": True})
n2 = s.add_node(x=L,   z=0.0)
s.add_element(node_i=n1, node_j=n2, E=E, A=A, I=I)
s.add_node_load(node=n2, Fz=P)

res = Solver1stOrder().solve(s)
w_dsm = res.displacements(node=n2)["w"]
M_dsm = abs(res.internal_forces(s.elements[0])["M_i"])

# Analytical reference values
w_exact = P * L**3 / (3 * E * I)
M_exact = P * L

print("BM2: cantilever, tip point load")
print(f"  tip deflection    : DSM = {w_dsm:.4f} cm    analytical = {w_exact:.4f} cm")
print(f"  fixed-end moment  : DSM = {M_dsm:.4f} kNcm  analytical = {M_exact:.4f} kNcm")

assert abs(w_dsm - w_exact) / w_exact < 1e-6, "deflection does not match analytical solution"
assert abs(M_dsm - M_exact) / M_exact < 1e-6, "moment does not match analytical solution"
print("  PASS")
