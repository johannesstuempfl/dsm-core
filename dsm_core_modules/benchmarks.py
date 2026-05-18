from structure import Structure
from solver_1st import Solver1stOrder
from solver_2nd import Solver2ndOrder
from plotter import Plotter
from buckling_analysis import BucklingAnalysis

# ------------------------------------------------------------------ #
#  Test 1 - Träger auf zwei Stützen                                  #
# ------------------------------------------------------------------ #

# s = Structure()

# n1 = s.add_node(x=0.0,z=0.0,kind="frame", support={"u": True, "w": True, "phi": False})
# n2 = s.add_node(x=5.0,z=0.0,kind="frame", support={"u": False, "w": True, "phi": False})

# e1 = s.add_element(node_i=n1,node_j=n2, E=1000, A=1, I=1)

# s.add_node_load(n2, M=100)

# solver = Solver1stOrder()
# res = solver.solve(s)

# res.print_summary()

# ------------------------------------------------------------------ #
#  Test 2 - Träger mit rechtsseitiger Einspannung                    #
# ------------------------------------------------------------------ #

# s = Structure()

# n1 = s.add_node(x=0.0,z=0.0,kind="frame", support={"u": True, "w": True, "phi": False})
# n2 = s.add_node(x=5.0,z=0.0,kind="frame", support={"u": True, "w": True, "phi": True})

# e1 = s.add_element(node_i=n1,node_j=n2, E=1000, A=1, I=1)

# s.add_node_load(n1, M=-100)

# solver = Solver1stOrder()
# res = solver.solve(s)

# res.print_summary()


# ------------------------------------------------------------------ #
#  Test 3  Träger mit Last in Feldmitte                              #
# ------------------------------------------------------------------ #

# s = Structure()

# n1 = s.add_node(x=0.0,z=0.0,kind="frame", support={"u": True, "w": True, "phi": False})
# n2 = s.add_node(x=5.0,z=0.0,kind="frame", support={"u": False, "w": False, "phi": False})
# n3 = s.add_node(x=10.0,z=0.0,kind="frame", support={"u": False, "w": True, "phi": False})

# e1 = s.add_element(node_i=n1,node_j=n2, E=1000, A=1, I=1)
# e2 = s.add_element(node_i=n2,node_j=n3, E=1000, A=1, I=1)

# s.add_node_load(n2, M=10)

# solver = Solver1stOrder()
# res = solver.solve(s)

# res.print_summary()

# ------------------------------------------------------------------ #
#  Test 4  Träger mit Last in Feldmitte und beidseitiger Einspannung          #
# ------------------------------------------------------------------ #

# s = Structure()

# n1 = s.add_node(x=0.0,z=0.0,kind="frame", support={"u": True, "w": True, "phi": True})
# n2 = s.add_node(x=5.0,z=0.0,kind="frame", support={"u": False, "w": False, "phi": False})
# n3 = s.add_node(x=10.0,z=0.0,kind="frame", support={"u": True, "w": True, "phi": True})

# e1 = s.add_element(node_i=n1,node_j=n2, E=1000, A=1, I=1)
# e2 = s.add_element(node_i=n2,node_j=n3, E=1000, A=1, I=1)

# s.add_node_load(n2, Fz=10)

# solver = Solver1stOrder()
# res = solver.solve(s)

# res.print_summary()

# ------------------------------------------------------------------ #
#  Test 5  Biegesteifes Dreieck                                      #
# ------------------------------------------------------------------ #

# s = Structure()

# n1 = s.add_node(x=0.0,z=0.0,kind="frame", support={"u": True, "w": True, "phi": False})
# n2 = s.add_node(x=5.0,z=-5.0,kind="frame", support={"u": False, "w": False, "phi": False})
# n3 = s.add_node(x=10.0,z=0.0,kind="frame", support={"u": True, "w": True, "phi": False})

# e1 = s.add_element(node_i=n1,node_j=n2, E=1000, A=1, I=1)
# e2 = s.add_element(node_i=n2,node_j=n3, E=1000, A=1, I=1)

# s.add_node_load(n2, Fz=20, Fx=10)

# solver = Solver1stOrder()
# res = solver.solve(s)

# res.print_summary()

# ------------------------------------------------------------------ #
#  Test 6  Rahmentragwerk.                                           #
# ------------------------------------------------------------------ #

# s = Structure()

# n1 = s.add_node(x=0.0,z=0.0,kind="frame", support={"u": True, "w": True, "phi": False})
# n2 = s.add_node(x=0.0,z=-3.0,kind="frame", support={"u": False, "w": False, "phi": False})
# n3 = s.add_node(x=3.0,z=-3.0,kind="frame", support={"u": False, "w": False, "phi": False})
# n4 = s.add_node(x=6.0,z=-3.0,kind="frame", support={"u": False, "w": False, "phi": False})
# n5 = s.add_node(x=6.0,z=0.0,kind="frame", support={"u": True, "w": True, "phi": False})

# e1 = s.add_element(node_i=n1,node_j=n2, E=1000, A=1, I=1)
# e2 = s.add_element(node_i=n2,node_j=n3, E=1000, A=1, I=1)
# e3 = s.add_element(node_i=n3,node_j=n4, E=1000, A=1, I=1)
# e4 = s.add_element(node_i=n4,node_j=n5, E=1000, A=1, I=1)


# s.add_node_load(n2, Fx=10)
# s.add_node_load(n3, Fz=20)

# solver = Solver1stOrder()
# res = solver.solve(s)

# res.print_summary()

# ------------------------------------------------------------------ #
#  Test 7  Kragarm Th.I.O. und Th.II.O.                              #
# ------------------------------------------------------------------ #

# s = Structure()

# n1 = s.add_node(x=0.0,z=0.0,kind="frame", support={"u": True, "w": True, "phi": True})
# n2 = s.add_node(x=0.5,z=0.0,kind="frame", support={"u": False, "w": False, "phi": False})
# n3 = s.add_node(x=1.0,z=0.0,kind="frame", support={"u": False, "w": False, "phi": False})
# n4 = s.add_node(x=1.5,z=0.0,kind="frame", support={"u": False, "w": False, "phi": False})
# n5 = s.add_node(x=2.0,z=0.0,kind="frame", support={"u": False, "w": False, "phi": False})
# n6 = s.add_node(x=2.5,z=0.0,kind="frame", support={"u": False, "w": False, "phi": False})
# n7 = s.add_node(x=3.0,z=0.0,kind="frame", support={"u": False, "w": False, "phi": False})
# n8 = s.add_node(x=3.5,z=0.0,kind="frame", support={"u": False, "w": False, "phi": False})
# n9 = s.add_node(x=4.0,z=0.0,kind="frame", support={"u": False, "w": False, "phi": False})
# n10 = s.add_node(x=4.5,z=0.0,kind="frame", support={"u": False, "w": False, "phi": False})
# n11 = s.add_node(x=5.0,z=0.0,kind="frame", support={"u": False, "w": False, "phi": False})

# e1 = s.add_element(node_i=n1,node_j=n2, E=10000, A=1000, I=1)
# e2 = s.add_element(node_i=n2,node_j=n3, E=10000, A=1000, I=1)
# e3 = s.add_element(node_i=n3,node_j=n4, E=10000, A=1000, I=1)
# e4 = s.add_element(node_i=n4,node_j=n5, E=10000, A=1000, I=1)
# e5 = s.add_element(node_i=n5,node_j=n6, E=10000, A=1000, I=1)
# e6 = s.add_element(node_i=n6,node_j=n7, E=10000, A=1000, I=1)
# e7 = s.add_element(node_i=n7,node_j=n8, E=10000, A=1000, I=1)
# e8 = s.add_element(node_i=n8,node_j=n9, E=10000, A=1000, I=1)
# e9 = s.add_element(node_i=n9,node_j=n10, E=10000, A=1000, I=1)
# e9 = s.add_element(node_i=n10,node_j=n11, E=10000, A=1000, I=1)

# s.add_node_load(n11, Fx=-500, Fz=0)

# solver1 = Solver1stOrder()
# solver2 = Solver2ndOrder(tol=1e-6, max_iter=50)

# res1 = solver1.solve(s)
# res2 = solver2.solve(s)
# #res2.print_summary()

# # Stabilitätsanalyse
# buckling = BucklingAnalysis(n_modes=3)
# result   = buckling.solve(s)

# # Ausgabe
# buckling.print_summary(result, s)


# # Th. 1. Ordnung
# plotter1 = Plotter(res1, scale_deform=100.0, scale_forces=0.005)
# plotter1.plot_all(title="Kragarm – Theorie 1. Ordnung")

# # Th. 2. Ordnung
# plotter2 = Plotter(res2, scale_deform=100.0, scale_forces=0.005)
# plotter2.plot_all(title="Kragarm – Theorie 2. Ordnung")



# ------------------------------------------------------------------ #
#  Test 8  Träger auf zwei Stützen mit Last in Feldmitte und Druck   #
# ------------------------------------------------------------------ #

# s = Structure()

# n1 = s.add_node(x=0.0,z=0.0,kind="frame", support={"u": True, "w": True, "phi": False})
# n2 = s.add_node(x=0.5,z=0.0,kind="frame", support={"u": False, "w": False, "phi": False})
# n3 = s.add_node(x=1.0,z=0.0,kind="frame", support={"u": False, "w": False, "phi": False})
# n4 = s.add_node(x=1.5,z=0.0,kind="frame", support={"u": False, "w": False, "phi": False})
# n5 = s.add_node(x=2.0,z=0.0,kind="frame", support={"u": False, "w": False, "phi": False})
# n6 = s.add_node(x=2.5,z=0.0,kind="frame", support={"u": False, "w": False, "phi": False})
# n7 = s.add_node(x=3.0,z=0.0,kind="frame", support={"u": False, "w": False, "phi": False})
# n8 = s.add_node(x=3.5,z=0.0,kind="frame", support={"u": False, "w": False, "phi": False})
# n9 = s.add_node(x=4.0,z=0.0,kind="frame", support={"u": False, "w": False, "phi": False})
# n10 = s.add_node(x=4.5,z=0.0,kind="frame", support={"u": False, "w": False, "phi": False})
# n11 = s.add_node(x=5.0,z=0.0,kind="frame", support={"u": False, "w": True, "phi": False})

# e1 = s.add_element(node_i=n1,node_j=n2, E=10000, A=1000, I=1)
# e2 = s.add_element(node_i=n2,node_j=n3, E=10000, A=1000, I=1)
# e3 = s.add_element(node_i=n3,node_j=n4, E=10000, A=1000, I=1)
# e4 = s.add_element(node_i=n4,node_j=n5, E=10000, A=1000, I=1)
# e5 = s.add_element(node_i=n5,node_j=n6, E=10000, A=1000, I=1)
# e6 = s.add_element(node_i=n6,node_j=n7, E=10000, A=1000, I=1)
# e7 = s.add_element(node_i=n7,node_j=n8, E=10000, A=1000, I=1)
# e8 = s.add_element(node_i=n8,node_j=n9, E=10000, A=1000, I=1)
# e9 = s.add_element(node_i=n9,node_j=n10, E=10000, A=1000, I=1)
# e10 = s.add_element(node_i=n10,node_j=n11, E=10000, A=1000, I=1)

# s.add_node_load(node=n6, Fz=100)
# s.add_node_load(node=n11, Fx=-500)

# solver1 = Solver1stOrder()
# solver2 = Solver2ndOrder(tol=1e-6, max_iter=50)

# res1 = solver1.solve(s)
# res2 = solver2.solve(s)

# res1.print_summary()
# res2.print_summary()