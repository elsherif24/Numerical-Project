from solverEngine2.base.data_classes import RootFinderParameters, RootFinderResult
from solverEngine2.methods.bisection import BisectionMethod
from solverEngine2.methods.false_position import FalsePositionMethod
from solverEngine2.methods.fixed_point import FixedPointMethod
from solverEngine2.methods.newton_raphson import NewtonRaphsonMethod
from solverEngine2.methods.modified_newton import ModifiedNewtonMethod
from solverEngine2.methods.secant import SecantMethod


# Method registry mapping method names to classes
METHOD_REGISTRY = {
    "Bisection": BisectionMethod,
    "False-Position": FalsePositionMethod,
    "Fixed Point": FixedPointMethod,
    "Newton-Raphson": NewtonRaphsonMethod,
    "Modified Newton-Raphson": ModifiedNewtonMethod,
    "Secant": SecantMethod,
}


def solve_root(params: RootFinderParameters) -> RootFinderResult:
    # Get the appropriate method class
    method_class = METHOD_REGISTRY.get(params.method)
    
    if method_class is None:
        result = RootFinderResult()
        result.error_message = f"Unknown method: {params.method}. Available: {list(METHOD_REGISTRY.keys())}"
        return result
    
    # Instantiate and execute the method
    method = method_class()
    return method.solve(params)


def get_available_methods():
    return list(METHOD_REGISTRY.keys())