# dsm_core

A compact, dependency-light 2D plane-frame **Direct Stiffness Method** (DSM) solver in Python. Supports Theory of 1st Order (linear elastic), Theory of 2nd Order (geometrically non-linear, via iterative geometric-stiffness updates), and linear buckling (eigenvalue) analysis.

It was originally developed as part of the Master's thesis *"Safety Level Homogenization for Geometrically Non-linear Structures under Multi-Dimensional Loading"* (TUM, Chair of Engineering Risk Analysis) — see the [companion analysis repository](https://github.com/johannesstuempfl/nonlinear-structural-reliability-and-homogenization) for the full reliability workflow it was used in. This repository is the standalone, general-purpose solver.

## Installation

```bash
git clone https://github.com/johannesstuempfl/dsm-core.git
cd dsm-core
pip install -e .
```

This installs `dsm_core` and its one dependency, `numpy`.

## Quick example: Cantilever beam

```python
from dsm_core import Structure, Solver1stOrder

s = Structure()
n1 = s.add_node(x=0.0, z=0.0, support={"u": True, "w": True, "phi": True})   # fixed
n2 = s.add_node(x=5.0, z=0.0)                                                # free

s.add_element(node_i=n1, node_j=n2, E=210000, A=1000, I=8356)
s.add_node_load(n2, Fz=1000)   # downward point load at the tip

res = Solver1stOrder().solve(s)
res.print_summary()
```

See `examples/quickstart.py` for a slightly larger portal-frame example.

## API overview

| Class | Purpose |
|---|---|
| `Node` | A point in the 2D frame; `kind="frame"` (3 DOF: `u`, `w`, `phi`) or `kind="truss"` (2 DOF: `u`, `w`). |
| `Element` | Euler-Bernoulli beam element (6 DOF), created automatically by `Structure.add_element`. |
| `TrussElement` | Axial-only truss element (4 DOF). **Not production ready** -- not benchmarked or validated against known analytical solutions, and its interaction with `Structure` (mixed frame/truss assemblies, 2nd-order geometric stiffness) has not been verified. Use with caution. |
| `Structure` | Collects nodes, elements, and loads; assembles the global stiffness matrix, geometric stiffness matrix, and load vector. |
| `NodeLoad` / `DistLoad` | Point loads/moments at a node, or a uniformly distributed load on an element (local or global direction). |
| `Solver1stOrder` | Linear elastic solve: `K · u = f`. |
| `Solver2ndOrder` | Geometrically non-linear solve: iterates `(K + Kg(N)) · u = f` until the displacement increment converges. |
| `BucklingAnalysis` | Linear buckling (eigenvalue) analysis: smallest load multiplier `λ` for which `K + λ·Kg` becomes singular. |
| `Results` | Displacements, internal forces (`N`, `Q`, `M`), and support reactions from a solved structure. |

### Sign convention

The global `z`-axis points **downward**, so a downward point load is `Fz > 0` and a resulting downward deflection is `w > 0`. Node DOF order is `[u, w, phi]` (axial, transverse, rotation); truss nodes have no `phi`.

## Validation

The solver is checked against classical closed-form beam theory solutions. Each case lives in its own script in `benchmarks/`:

| # | Script | Case | Compared against | Result |
|---|---|---|---|---|
| BM1 | `bm1_simply_supported_point_load.py` | Simply supported beam, midspan point load | Deflection & moment (Euler-Bernoulli) | exact to machine precision |
| BM2 | `bm2_cantilever_tip_load.py` | Cantilever, tip point load | Tip deflection & fixed-end moment | exact to machine precision |
| BM3 | `bm3_cantilever_tip_moment.py` | Cantilever, tip moment | Tip deflection, tip rotation, fixed-end moment | exact to machine precision |
| BM4 | `bm4_fixed_fixed_point_load.py` | Fixed-fixed beam, midspan point load | Deflection & end/midspan moments | exact to machine precision |
| BM5 | `bm5_simply_supported_udl.py` | Simply supported beam, uniform distributed load | Midspan deflection & moment | exact to machine precision |
| BM6 | `bm6_euler_buckling.py` | Euler buckling, pinned-pinned column | Critical load `Pcr = pi^2 EI / L^2` | ~1e-5 relative error (10-element mesh) |
| BM7 | `bm7_beam_column_amplification.py` | Beam-column under axial + transverse load | 2nd-order moment amplification factor `1/(1-N/Pcr)` | ~5% (approximate reference formula; see note below) |

Each benchmark is a standalone script and can be run individually, e.g.:

```bash
python3 benchmarks/bm1_simply_supported_point_load.py
```

Or run all of them at once:

```bash
python3 benchmarks/run_all.py
```

## Limitations

- 2D plane-frame only (no 3D structures, no shear deformation).
- `Solver2ndOrder` uses a fixed-point iteration on the geometric stiffness matrix; it is accurate for moderate axial-load ratios but is not an exact large-displacement/large-rotation formulation.
- `BucklingAnalysis` is a linear eigenvalue analysis (small-deformation prebuckling assumption).
- `TrussElement` is **not production ready** -- it has not been benchmarked or validated (see the API table above). All benchmarks in `benchmarks/` cover the frame `Element` only.

## License

<!-- TODO: add a license (e.g. MIT) and a LICENSE file if you want others to freely reuse this code. -->
