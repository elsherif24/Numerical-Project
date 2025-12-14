
from abc import ABC, abstractmethod
import math
import time
from solverEngine2.base.data_classes import RootFinderParameters, RootFinderResult
from solverEngine2.base.equation_parser import parse_equation
from D import set_sig_figs


class BaseRootFindingMethod(ABC):
    # Abstract base class for root-finding methods.
    # All methods must inherit from this class and implement the solve method.
   
    
    def __init__(self):
        self.result = RootFinderResult()
        self.params = None
        self.func = None
        self.start_time = None
    
    def setup(self, params: RootFinderParameters) -> None:
        self.params = params
        self.result = RootFinderResult()
        
        # Set significant figures globally
        set_sig_figs(params.significant_figures)
        
        # Parse the equation
        try:
            self.func = parse_equation(params.equation)
        except Exception as e:
            self.result.error_message = f"Error parsing equation: {str(e)}"
            return
        
        # Start timing
        self.start_time = time.time()
    
    def finalize(self) -> RootFinderResult:
        if self.start_time:
            self.result.execution_time = time.time() - self.start_time
        return self.result
    
    @abstractmethod
    def solve(self, params: RootFinderParameters) -> RootFinderResult:
        pass
    
    @abstractmethod
    def validate_parameters(self) -> bool:
        pass
    def calculate_significant_digits(self, ea):
        """
        Calculate number of significant digits at least correct.
        ea: approximate relative error (as decimal, not percentage)
        Returns: number of significant digits (m)
        
        Formula: m ≤ 2 - log₁₀(0.5 × εₐ)
        This gives the number of significant digits guaranteed to be correct.
        """
        if ea == 0:
            return  None  # Perfect accuracy
        
        if ea == float('inf') or ea < 0:
            return None
        
        try:
            # Formula: m ≤ 2 - log₁₀(0.5 × εₐ)
            ea_percent = ea * 100
            m = 2 - math.log10( ea_percent/0.5)
            return math.floor(m)  # Round down to get "at least" correct digits
        except (ValueError, OverflowError):
            return 0