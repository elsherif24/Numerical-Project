# import math
# from dataclasses import dataclass
# from typing import Optional, Callable, List
# import time
# import re
# from D import D, set_sig_figs, get_sig_figs


# @dataclass
# class RootFinderResult:
    
#     root: Optional[float] = None
#     iterations: int = 0
#     approximate_error: float = 0.0
#     execution_time: float = 0.0
#     converged: bool = False
#     error_message: Optional[str] = None
#     steps: List = None
    
#     def __post_init__(self):
#         if self.steps is None:
#             self.steps = []


# @dataclass
# class RootFinderParameters:
#     equation: str = ""
#     method: str = "Bisection"
#     xl: float = 0.0  # Lower bound
#     xu: float = 1.0  # Upper bound
#     max_iterations: int = 50
#     epsilon: float = 0.00001
#     significant_figures: int = 5
#     step_by_step: bool = False


# def parse_equation(equation_str: str) -> Callable:

#     # Replace common math functions
#     equation_str = equation_str.replace('^', '**')
#     equation_str = re.sub(r'(\d)([a-zA-Z(])', r'\1*\2', equation_str)  # Add implicit multiplication
#     equation_str = re.sub(r'(\))(\d)', r'\1*\2', equation_str)
#     equation_str = re.sub(r'(\))(\()', r'\1*\2', equation_str)
    
#     # Create namespace with math functions
#     # namespace = {
#     #     'x': 0,
#     #     'exp': np.exp,
#     #     'sin': np.sin,
#     #     'cos': np.cos,
#     #     'tan': np.tan,
#     #     'log': np.log10,
#     #     'ln': np.log,
#     #     'sqrt': np.sqrt,
#     #     'abs': np.abs,
#     #     'pi': np.pi,
#     #     'e': np.e
#     # }
#     namespace = {
#         "x": D(0),
#         "exp": lambda d: d.exp() if isinstance(d, D) else D(math.exp(float(d))),
#         "sin": lambda d: D(math.sin(float(d))),
#         "cos": lambda d: D(math.cos(float(d))),
#         "tan": lambda d: D(math.tan(float(d))),

#         "log": lambda d: d.log10() if isinstance(d, D) else D(math.log10(float(d))),
#         "ln": lambda d: d.ln() if isinstance(d, D) else D(math.log(float(d))),
#         "sqrt": lambda d: d.sqrt() if isinstance(d, D) else D(math.sqrt(float(d))),
#         "abs": lambda d: abs(d) if isinstance(d, D) else D(abs(float(d))),
#         "pi": D(math.pi),
#         "e": D(math.e)
#     }
    
#     def func(x):
#         ns = dict(namespace)
#         ns["x"] = x if isinstance(x, D) else D(x)      
#         try:
#             return (eval(equation_str, {"__builtins__": {}}, ns))
#         except Exception as e:
#             raise ValueError(f"Error evaluating equation: {str(e)}")
    
#     return func


# def bisection_method(params: RootFinderParameters) -> RootFinderResult:
#     result = RootFinderResult()
#     steps = []
    
#     try:
#         # Set significant figures
#         set_sig_figs(params.significant_figures)    
#         func = parse_equation(params.equation)
        
#         # Convert to D objects for significant figure handling
#         xl = D(params.xl)
#         xu = D(params.xu)
#         epsilon = D(params.epsilon)     
#         start_time = time.time()
        
#         # Check if root exists
#         # f_xl = func(float(xl))
#         # f_xu = func(float(xu))
#         f_xl = func(xl)
#         f_xu = func(xu)
#         if not isinstance(f_xl, D): f_xl = D(f_xl)
#         if not isinstance(f_xu, D): f_xu = D(f_xu)
#         if f_xl * f_xu > D(0):
#             result.error_message = f"No root exists in interval [{xl}, {xu}].\nf({xl}) = {f_xl}\nf({xu}) = {f_xu}\nBoth values have the same sign."
#             return result
        
#         L0 = abs((xu) - (xl))
#         k_required = math.ceil(math.log2(float(L0 / epsilon))) if float(L0) > 0 and float(epsilon) > 0 else 0

       
#         if params.step_by_step:
#             steps.append({
#                 'type': 'info',
#                 'message': f'Initial interval: [{xl}, {xu}]',
#                 'xl': str(xl),
#                 'xu': str(xu),
#                 'f_xl': str(f_xl),
#                 'f_xu': str(f_xu),
#                 'required_iterations': k_required
#             })
        
#         xr_prev = None
#         ea = float('inf')
#         xr=None
        
#         for i in range(1, params.max_iterations + 1):
#             # Calculate midpoint with D class
#             xr = (xl + xu) / D(2)
#             f_xr = func((xr))
#             if not isinstance(f_xr, D): f_xr = D(f_xr)
#             if xr_prev is not None:
#                 if xr != D(0):
#                     ea = float(abs((xr - xr_prev) / xr) * D(100))
#                 else:
#                     ea = 0.0
#             if params.step_by_step:
#                 steps.append({
#                     'type': 'iteration',
#                     'iteration': i,
#                     'xl': str(xl),
#                     'xu': str(xu),
#                     'xr': str(xr),
#                     'f_xr': str(f_xr),
#                     'f_xl': str(f_xl),
#                     'f_xu': str(f_xu),
#                     'error': ea if ea != float('inf') else None
#                 })
#             if f_xr.isNearZero():
#                 result.root = float(xr)
#                 result.iterations = i
#                 result.approximate_error = ea if ea != float('inf') else 0.0
#                 result.execution_time = time.time() - start_time
#                 result.converged = True
#                 if params.step_by_step:
#                  steps.append({
#                        'type': 'converged',
#                        'message': 'f(xr) is near zero. Root found.',
#                        'xr': str(xr),
#                         'f_xr': str(f_xr)
#                    })
#                 result.steps = steps
#                 return result    
#             # Check if function value is near zero (root found)
            
#             # Calculate approximate relative error
#             if xr_prev is not None:
#                 if (xr) != D(0):
#                     ea = float(abs((xr - xr_prev) / xr) * D(100))

#                 else:
#                     ea = 0
            
#             # Check convergence
#             if ea != float('inf') and ea < float(params.epsilon):
#                 result.root = float(xr)
#                 result.iterations = i
#                 result.approximate_error = ea
#                 result.execution_time = time.time() - start_time
#                 result.converged = True
#                 result.steps = steps
#                 return result
            
#             # Update interval with D objects
#             f_xl_current = func((xl))
#             if not isinstance(f_xl_current, D): f_xl_current = D(f_xl_current)

#             if f_xl_current * f_xr < D(0):
#                 xu = xr
#                 f_xu = f_xr
#             else:
#                 xl = xr
#                 f_xl = f_xr
            
#             xr_prev = xr
        
#         # Max iterations reached
#         result.root = float(xr)
#         result.iterations = params.max_iterations
#         result.approximate_error = ea if ea != float('inf') else 0.0
#         result.execution_time = time.time() - start_time
#         result.converged = False
#         result.steps = steps
#         result.error_message = "Maximum iterations reached without convergence"
        
#     except Exception as e:
#         result.error_message = f"Error in Bisection method: {str(e)}"
    
#     return result


# def solve_root(params: RootFinderParameters) -> RootFinderResult:
#     if params.method == "Bisection":
#         return bisection_method(params)
#     else:
#         result = RootFinderResult()
#         result.error_message = f"Unknown method: {params.method}"
#         return result
