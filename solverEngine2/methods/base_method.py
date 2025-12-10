
from abc import ABC, abstractmethod
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