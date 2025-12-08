# import math
# import time
# from typing import List, Dict, Any
# from dataclasses import dataclass
# from D import D, set_sig_figs

# @dataclass
# class RootFinderResult:
#     root: float = None
#     iterations: int = 0
#     approximate_error: float = 0.0
#     execution_time: float = 0.0
#     converged: bool = False
#     error_message: str = None
#     steps: List[Dict[str, Any]] = None
    
#     def __post_init__(self):
#         if self.steps is None:
#             self.steps = []


# class BisectionMethod:
#     """Bisection method for finding roots of equations."""
    
#     def __init__(self, equation_func, params):
#         """
#         Initialize the Bisection method.
        
#         Args:
#             equation_func: Function to evaluate the equation
#             params: RootFinderParameters object with method parameters
#         """
#         self.func = equation_func
#         self.params = params
#         self.result = RootFinderResult()
#         self.steps = []
        
#     def _check_initial_conditions(self, xl: D, xu: D) -> bool:
#         """Check if root exists in the interval."""
#         try:
#             f_xl = self.func(xl)
#             f_xu = self.func(xu)
            
#             if not isinstance(f_xl, D): 
#                 f_xl = D(f_xl)
#             if not isinstance(f_xu, D): 
#                 f_xu = D(f_xu)
            
#             if f_xl * f_xu > D(0):
#                 self.result.error_message = (
#                     f"No root exists in interval [{xl}, {xu}].\n"
#                     f"f({xl}) = {f_xl}\n"
#                     f"f({xu}) = {f_xu}\n"
#                     "Both values have the same sign."
#                 )
#                 return False
#             return True
            
#         except Exception as e:
#             self.result.error_message = f"Error checking initial conditions: {str(e)}"
#             return False
    
#     def _calculate_required_iterations(self, xl: D, xu: D, epsilon: D) -> int:
#         """Calculate the required number of iterations."""
#         L0 = abs((xu) - (xl))
#         if float(L0) > 0 and float(epsilon) > 0:
#             return math.ceil(math.log2(float(L0 / epsilon)))
#         return 0
    
#     def _record_initial_step(self, xl: D, xu: D, k_required: int):
#         """Record initial step information."""
#         if self.params.step_by_step:
#             f_xl = self.func(xl)
#             f_xu = self.func(xu)
            
#             if not isinstance(f_xl, D): f_xl = D(f_xl)
#             if not isinstance(f_xu, D): f_xu = D(f_xu)
            
#             self.steps.append({
#                 'type': 'info',
#                 'message': f'Initial interval: [{xl}, {xu}]',
#                 'xl': str(xl),
#                 'xu': str(xu),
#                 'f_xl': str(f_xl),
#                 'f_xu': str(f_xu),
#                 'required_iterations': k_required
#             })
    
#     def _update_interval(self, xl: D, xu: D, f_xl: D, f_xu: D, 
#                         xr: D, f_xr: D) -> tuple:
#         """Update the interval based on the bisection rule."""
#         f_xl_current = self.func(xl)
#         if not isinstance(f_xl_current, D): 
#             f_xl_current = D(f_xl_current)
            
#         if f_xl_current * f_xr < D(0):
#             xu = xr
#             f_xu = f_xr
#         else:
#             xl = xr
#             f_xl = f_xr
            
#         return xl, xu, f_xl, f_xu
    
#     def _record_iteration_step(self, iteration: int, xl: D, xu: D, 
#                               xr: D, f_xr: D, f_xl: D, f_xu: D, 
#                               error: float):
#         """Record iteration step information."""
#         if self.params.step_by_step:
#             self.steps.append({
#                 'type': 'iteration',
#                 'iteration': iteration,
#                 'xl': str(xl),
#                 'xu': str(xu),
#                 'xr': str(xr),
#                 'f_xr': str(f_xr),
#                 'f_xl': str(f_xl),
#                 'f_xu': str(f_xu),
#                 'error': error if error != float('inf') else None
#             })
    
#     def _check_convergence(self, f_xr: D, xr: D, xr_prev: D, 
#                           iteration: int, start_time: float) -> bool:
#         """Check if convergence criteria are met."""
#         # Check if f(xr) is near zero
#         if f_xr.isNearZero():
#             self.result.root = float(xr)
#             self.result.iterations = iteration
#             self.result.approximate_error = 0.0
#             self.result.execution_time = time.time() - start_time
#             self.result.converged = True
            
#             if self.params.step_by_step:
#                 self.steps.append({
#                     'type': 'converged',
#                     'message': 'f(xr) is near zero. Root found.',
#                     'xr': str(xr),
#                     'f_xr': str(f_xr)
#                 })
#             return True
            
#         # Check approximate relative error
#         if xr_prev is not None and xr != D(0):
#             ea = float(abs((xr - xr_prev) / xr) * D(100))
            
#             if ea < float(self.params.epsilon):
#                 self.result.root = float(xr)
#                 self.result.iterations = iteration
#                 self.result.approximate_error = ea
#                 self.result.execution_time = time.time() - start_time
#                 self.result.converged = True
#                 return True
                
#         return False
    
#     def solve(self) -> RootFinderResult:
#         """Execute the Bisection method to find the root."""
#         try:
#             # Set significant figures
#             set_sig_figs(self.params.significant_figures)
            
#             # Convert to D objects for significant figure handling
#             xl = D(self.params.xl)
#             xu = D(self.params.xu)
            
#             # Check initial conditions
#             if not self._check_initial_conditions(xl, xu):
#                 return self.result
            
#             # Calculate required iterations
#             epsilon = D(self.params.epsilon)
#             k_required = self._calculate_required_iterations(xl, xu, epsilon)
            
#             # Record initial step
#             self._record_initial_step(xl, xu, k_required)
            
#             # Initialize variables
#             start_time = time.time()
#             xr_prev = None
#             ea = float('inf')
#             f_xl = self.func(xl)
#             f_xu = self.func(xu)
            
#             if not isinstance(f_xl, D): f_xl = D(f_xl)
#             if not isinstance(f_xu, D): f_xu = D(f_xu)
            
#             # Main iteration loop
#             for i in range(1, self.params.max_iterations + 1):
#                 # Calculate midpoint
#                 xr = (xl + xu) / D(2)
#                 f_xr = self.func(xr)
#                 if not isinstance(f_xr, D): 
#                     f_xr = D(f_xr)
                
#                 # Record iteration step
#                 current_error = ea if ea != float('inf') else None
#                 self._record_iteration_step(i, xl, xu, xr, f_xr, f_xl, f_xu, current_error)
                
#                 # Check for convergence
#                 if self._check_convergence(f_xr, xr, xr_prev, i, start_time):
#                     self.result.steps = self.steps
#                     return self.result
                
#                 # Update interval
#                 xl, xu, f_xl, f_xu = self._update_interval(xl, xu, f_xl, f_xu, xr, f_xr)
#                 xr_prev = xr
                
#                 # Calculate approximate error for next iteration
#                 if xr_prev is not None and not xr.isNearZero():
#                     ea = float(abs((xr - xr_prev) / xr) * D(100))
            
#             # Maximum iterations reached
#             self.result.root = float(xr_prev) if xr_prev is not None else float((xl + xu) / D(2))
#             self.result.iterations = self.params.max_iterations
#             self.result.approximate_error = ea if ea != float('inf') else 0.0
#             self.result.execution_time = time.time() - start_time
#             self.result.converged = False
#             self.result.error_message = "Maximum iterations reached without convergence"
#             self.result.steps = self.steps
            
#         except Exception as e:
#             self.result.error_message = f"Error in Bisection method: {str(e)}"
        
#         return self.result