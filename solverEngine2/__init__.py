"""
=== solverEngine2/__init__.py ===
"""
from solverEngine2.solver import solve_root, get_available_methods
from solverEngine2.base.data_classes import RootFinderParameters, RootFinderResult
from solverEngine2.base.equation_parser import parse_equation

__all__ = [
    'solve_root',
    'get_available_methods',
    'RootFinderParameters',
    'RootFinderResult',
    'parse_equation'
]


"""
=== solverEngine2/base/__init__.py ===
"""
from solverEngine2.base.data_classes import RootFinderParameters, RootFinderResult
from solverEngine2.base.equation_parser import parse_equation

__all__ = [
    'RootFinderParameters',
    'RootFinderResult',
    'parse_equation'
]


"""
=== solverEngine2/methods/__init__.py ===
"""
from solverEngine2.methods.bisection import BisectionMethod
from solverEngine2.methods.false_position import FalsePositionMethod
from solverEngine2.methods.fixed_point import FixedPointMethod
from solverEngine2.methods.newton_raphson import NewtonRaphsonMethod
from solverEngine2.methods.modified_newton import ModifiedNewtonMethod
from solverEngine2.methods.secant import SecantMethod

__all__ = [
    'BisectionMethod',
    'FalsePositionMethod',
    'FixedPointMethod',
    'NewtonRaphsonMethod',
    'ModifiedNewtonMethod',
    'SecantMethod'
]