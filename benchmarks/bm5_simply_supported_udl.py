"""
BM5: Simply supported beam, uniformly distributed load.

Compares the DSM solver against the classical Euler-Bernoulli formulas:
    w_max = 5 * q * L^4 / (384 * E * I)   (deflection at midspan)
    M_max = q * L^2 / 8                    (bending moment at midspan)

Run: python3 benchmarks/bm5_simply_supported_udl.py
"""
from dsm_core import Structure, Solver1stOrder

# Beam properties (consistent kN, cm units) -- IPE 160 steel section
E = 21000.0    # Young's modulus, steel [kN/cm^2]
I = 869.27     # second moment of area, IPE 160 [cm^4]
A = 20.09      # cross-section area, IPE 160 [cm^2]
L = 400.0      # span [cm]  (4 m)
q = 0.1        # uniformly distributed load [kN/cm]  (= 10 kN/m)

# Build: pin -- (midspan node) -- roller, uniform load over both spans
s = Structure()
n1 = s.add_node(x=0.0, z=0.0, support={"u": True,  "w": True, "phi": False})
n2 = s.add_node(x=L/2, z=0.0)
n3 = s.add_node(x=L,   z=0.0, support={"u": False, "w": True, "phi": False})
e1 = s.add_element(node_i=n1, node_j=n2, E=E, A=A, I=I)
e2 = s.add_element(node_i=n2, node_j=n3, E=E, A=A, I=I)
s.add_dist_load(e1, qz=q, local=False)
s.add_dist_load(e2, qz=q, local=False)

res = Solver1stOrder().solve(s)
w_dsm = res.displacements(node=n2)["w"]
M_dsm = abs(res.internal_forces(e1)["M_j"])

# Analytical reference values
w_exact = 5 * q * L**4 / (384 * E * I)
M_exact = q * L**2 / 8

print("BM5: simply supported beam, uniformly distributed load")
print(f"  midspan deflection : DSM = {w_dsm:.4f} cm    analytical = {w_exact:.4f} cm")
print(f"  midspan moment      : DSM = {M_dsm:.4f} kNcm  analytical = {M_exact:.4f} kNcm")

assert abs(w_dsm - w_exact) / w_exact < 1e-4, "deflection does not match analytical solution"
assert abs(M_dsm - M_exact) / M_exact < 1e-4, "moment does not match analytical solution"
print("  PASS")
