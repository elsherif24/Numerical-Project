
from dataclasses import dataclass
from typing import Optional, List


@dataclass
class RootFinderResult:

    root: Optional[float] = None
    f_root: Optional[float] = None
    iterations: int = 0
    approximate_error: float = 0.0
    execution_time: float = 0.0
    converged: bool = False
    error_message: Optional[str] = None
    steps: List = None
    
    def __post_init__(self):
        if self.steps is None:
            self.steps = []


@dataclass
class RootFinderParameters:

    equation: str = ""
    method: str = "Bisection"
    
    # Interval-based methods (Bisection, False Position)
    xl: float = 0.0  # Lower bound
    xu: float = 1.0  # Upper bound
    
    # Fixed point
    x0: float = 0.0  # Initial guess for fixed point, Newton, Modified Newton
    g_equation: str = ""  # g(x) for fixed point iteration
    
    # Newton-Raphson
    derivative_equation: str = ""  # f'(x) for Newton methods
    
    # Secant
    x1: float = 0.0  # Second initial guess for Secant
    
    # Modified Newton-Raphson
    multiplicity: int = 1  # Root multiplicity for Modified Newton
    
    # Common parameters
    max_iterations: int = 50
    epsilon: float = 0.00001
    significant_figures: int = 5
    step_by_step: bool = False