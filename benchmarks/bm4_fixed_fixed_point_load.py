"""
BM4: Fixed-fixed beam, point load at midspan.

Compares the DSM solver against the classical Euler-Bernoulli formulas:
    w_max = P * L^3 / (192 * E * I)   (deflection at midspan)
    M     = P * L / 8                  (moment, both at the fixed ends
                                         and at midspan -- equal by symmetry)

Run: python3 benchmarks/bm4_fixed_fixed_point_load.py
"""
from dsm_core import Structure, Solver1stOrder

# Beam properties (consistent kN, cm units) -- IPE 160 steel section
E = 21000.0    # Young's modulus, steel [kN/cm^2]
I = 869.27     # second moment of area, IPE 160 [cm^4]
A = 20.09      # cross-section area, IPE 160 [cm^2]
L = 400.0      # span [cm]  (4 m)
P = 10.0       # point load at midspan [kN]

# Build: fixed -- (midspan node) -- fixed, point load at midspan
s = Structure()
n1 = s.add_node(x=0.0, z=0.0, support={"u": True, "w": True, "phi": True})
n2 = s.add_node(x=L/2, z=0.0)
n3 = s.add_node(x=L,   z=0.0, support={"u": True, "w": True, "phi": True})
s.add_element(node_i=n1, node_j=n2, E=E, A=A, I=I)
s.add_element(node_i=n2, node_j=n3, E=E, A=A, I=I)
s.add_node_load(node=n2, Fz=P)

res = Solver1stOrder().solve(s)
w_dsm     = res.displacements(node=n2)["w"]
M_end_dsm = abs(res.internal_forces(s.elements[0])["M_i"])
M_mid_dsm = abs(res.internal_forces(s.elements[0])["M_j"])

# Analytical reference values
w_exact = P * L**3 / (192 * E * I)
M_exact = P * L / 8

print("BM4: fixed-fixed beam, midspan point load")
print(f"  midspan deflection : DSM = {w_dsm:.4f} cm    analytical = {w_exact:.4f} cm")
print(f"  fixed-end moment   : DSM = {M_end_dsm:.4f} kNcm  analytical = {M_exact:.4f} kNcm")
print(f"  midspan moment     : DSM = {M_mid_dsm:.4f} kNcm  analytical = {M_exact:.4f} kNcm")

assert abs(w_dsm - w_exact) / w_exact < 1e-6, "deflection does not match analytical solution"
assert abs(M_end_dsm - M_exact) / M_exact < 1e-6, "fixed-end moment does not match analytical solution"
assert abs(M_mid_dsm - M_exact) / M_exact < 1e-6, "midspan moment does not match analytical solution"
print("  PASS")
