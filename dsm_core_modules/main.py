from structure import Structure
from solver_1st import Solver1stOrder

# Rahmensystem
s = Structure()
n1 = s.add_node(x=0.0,z=0.0,kind="frame", support={"u": True, "w": True, "phi": False})
n2 = s.add_node(x=0.0,z=-3.0,kind="frame", support={"u": False, "w": False, "phi": False})
n3 = s.add_node(x=5.0,z=-3.0,kind="frame", support={"u": False, "w": False, "phi": False})
n4 = s.add_node(x=5.0,z=0.0,kind="frame", support={"u": True, "w": True, "phi": False})

e1 = s.add_element(node_i=n1,node_j=n2, E=1000, A=1, I=1)
e2 = s.add_element(node_i=n2,node_j=n3, E=1000, A=1, I=1)
e3 = s.add_element(node_i=n3,node_j=n4, E=1000, A=1, I=1)

s.add_node_load(n3, Fx=10.0, Fz=5.0, M=25.0)

solver = Solver1stOrder()
res    = solver.solve(s)

res.print_summary()

# Hier noch Tutorial für Truss Element 
# Element ist automatisch Truss Element, wenn (node_i.kind == "truss" and node_j.kind == "truss")