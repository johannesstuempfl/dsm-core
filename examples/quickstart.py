"""
Quickstart example: a simple 3-member portal frame under a combined
point load and moment, solved with Theory of 1st Order.

Run from the repository root:
    python3 examples/quickstart.py
(requires the package to be installed, e.g. `pip install -e .`)
"""
from dsm_core import Structure, Solver1stOrder

# Portal frame: two columns and a beam
s = Structure()

n1 = s.add_node(x=0.0, z=0.0, kind="frame", support={"u": True,  "w": True,  "phi": False})
n2 = s.add_node(x=0.0, z=-3.0, kind="frame", support={"u": False, "w": False, "phi": False})
n3 = s.add_node(x=5.0, z=-3.0, kind="frame", support={"u": False, "w": False, "phi": False})
n4 = s.add_node(x=5.0, z=0.0, kind="frame", support={"u": True,  "w": True,  "phi": False})

s.add_element(node_i=n1, node_j=n2, E=1000, A=1, I=1)
s.add_element(node_i=n2, node_j=n3, E=1000, A=1, I=1)
s.add_element(node_i=n3, node_j=n4, E=1000, A=1, I=1)

s.add_node_load(n3, Fx=10.0, Fz=5.0, M=25.0)

solver = Solver1stOrder()
res = solver.solve(s)

res.print_summary()
