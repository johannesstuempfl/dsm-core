"""
dsm_core -- a compact 2D plane-frame Direct Stiffness Method solver.

Supports Theory of 1st Order (linear) and Theory of 2nd Order
(via iterative geometric stiffness updates),
plus linear buckling (eigenvalue) analysis.
"""

from .node import Node
from .element import Element, TrussElement
from .structure import Structure
from .loads import NodeLoad, DistLoad
from .results import Results
from .solver_1st import Solver1stOrder
from .solver_2nd import Solver2ndOrder
from .buckling_analysis import BucklingAnalysis

__all__ = [
    "Node",
    "Element",
    "TrussElement",
    "Structure",
    "NodeLoad",
    "DistLoad",
    "Results",
    "Solver1stOrder",
    "Solver2ndOrder",
    "BucklingAnalysis",
]

__version__ = "0.1.0"
