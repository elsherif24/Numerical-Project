"""
Fixed Point Iteration method implementation.
Solves x = g(x) by iterating x_{n+1} = g(x_n).
"""
import math
from solverEngine2.methods.base_method import BaseRootFindingMethod
from solverEngine2.base.data_classes import RootFinderParameters, RootFinderResult
from D import D


class FixedPointMethod(BaseRootFindingMethod):
  
    def validate_parameters(self) -> bool:
        if not self.params.g_equation:
            self.result.error_message = "g(x) equation is required for Fixed Point method"
            return False
        
        # Check if initial guess is provided
        if self.params.x0 is None:
            self.result.error_message = "Initial guess (x0) is required for Fixed Point method"
            return False
            
        return True
    
    def solve(self, params: RootFinderParameters) -> RootFinderResult:
        # Setup
        self.setup(params)
        
        if self.result.error_message:
            return self.result
        
        # Validate parameters
        if not self.validate_parameters():
            return self.result
        
        steps = []
        
        try:
            # Parse the g(x) equation for Fixed Point iteration
            g_func = None
            try:
                # Try to import equation parser from your codebase
                from solverEngine2.base.equation_parser import parse_equation
                g_func = parse_equation(params.g_equation)
            except ImportError:
                # Fallback: Use lambda with eval (less secure)
                g_func = lambda x: eval(params.g_equation.replace('^', '**'), 
                                        {"x": x, "exp": math.exp, "sin": math.sin, 
                                         "cos": math.cos, "ln": math.log, "log10": math.log10,
                                         "sqrt": math.sqrt, "pi": math.pi, "e": math.e})
            except Exception as e:
                self.result.error_message = f"Error parsing g(x) equation: {str(e)}"
                return self.result
            
            # Convert to D objects for significant figure handling
            x0 = D(params.x0)
            epsilon = D(params.epsilon)
            
            if params.step_by_step:
                steps.append({
                    'type': 'info',
                    'message': f'Fixed Point Iteration: x = g(x)',
                    'equation': params.equation,
                    'g_equation': params.g_equation,
                    'x0': str(x0),
                    'epsilon': str(epsilon)
                })
            
            xr = x0  # Current approximation
            xr_prev = None
            ea = float('inf')  # Absolute error
            iteration_count = 0
            
            # Main iteration loop
            for i in range(1, params.max_iterations + 1):
                iteration_count = i
                xr_prev = xr
                
                # Fixed Point iteration: x_{n+1} = g(x_n)
                try:
                    # Evaluate g(x)
                    g_value = g_func(xr_prev)
                    if not isinstance(g_value, D):
                        g_value = D(g_value)
                    xr = g_value
                except Exception as e:
                    self.result.error_message = f"Error evaluating g(x) at iteration {i}: {str(e)}"
                    break
                
                # Calculate absolute error (not relative)
                if xr_prev is not None:
                    ea = float(abs(xr - xr_prev))
                
                # Evaluate f(x) at current approximation
                f_xr = self.func(xr)
                if not isinstance(f_xr, D):
                    f_xr = D(f_xr)
                
                if params.step_by_step:
                    steps.append({
                        'type': 'iteration',
                        'iteration': i,
                        'x_current': str(xr_prev),
                        "g_x_current":str(g_value),
                        "f_x_next":str(f_xr),
                        # 'x_current': str(xr),
                        # 'g_x': str(xr),  # g(x) = current x
                        # 'f_x': str(f_xr),
                        'error': ea*100 if ea != float('inf') else None,
                        'method': 'Fixed Point'
                    })
                
                # Check if function value is near zero (root found)
                if f_xr.isNearZero():
                    self.result.root = float(xr)
                    self.result.f_root = float(f_xr)
                    self.result.iterations = i
                    self.result.approximate_error = ea if ea != float('inf') else 0.0
                    self.result.converged = True
                    
                    if params.step_by_step:
                        steps.append({
                            'type': 'converged',
                            'message': f'f(x) is near zero. Root found.',
                            'xr': str(xr),
                            'f_xr': str(f_xr),
                            'iterations': i
                        })
                    self.result.steps = steps
                    return self.finalize()
                
                # Check convergence based on absolute error (not relative)
                if ea != float('inf') and ea < float(params.epsilon):
                    self.result.root = float(xr)
                    self.result.f_root = float(f_xr)
                    self.result.iterations = i
                    self.result.approximate_error = ea
                    self.result.converged = True
                    
                    if params.step_by_step:
                        steps.append({
                            'type': 'converged',
                            'message': f'Absolute error ({ea:.6f}) below epsilon ({float(params.epsilon):.6f})',
                            'xr': str(xr),
                            'f_xr': str(f_xr),
                            'iterations': i
                        })
                    self.result.steps = steps
                    return self.finalize()
                
                # Check for divergence (stagnation or oscillation)
                if i > 2:
                    # Check if error is increasing or not decreasing
                    if ea > 1e10:  # Diverging to infinity
                        self.result.error_message = f"Divergence detected after {i} iterations"
                        break
                    if abs(float(f_xr)) > 1e10:  # Function value blowing up
                        self.result.error_message = f"Function value too large after {i} iterations"
                        break
            
            # Max iterations reached or divergence
            self.result.root = float(xr)
            self.result.f_root = float(f_xr)
            self.result.iterations = iteration_count
            self.result.approximate_error = ea if ea != float('inf') else 0.0
            self.result.converged = False
            self.result.steps = steps
            
            if not self.result.error_message:
                self.result.error_message = "Maximum iterations reached without convergence"
            
            if params.step_by_step:
                steps.append({
                    'type': 'warning',
                    'message': f'Maximum iterations ({params.max_iterations}) reached without convergence',
                    'final_x': str(xr),
                    'final_f_x': str(f_xr),
                    'final_error': ea if ea != float('inf') else 'N/A'
                })
            
        except ZeroDivisionError:
            self.result.error_message = "Division by zero occurred in Fixed Point calculation"
        except Exception as e:
            self.result.error_message = f"Error in Fixed Point method: {str(e)}"
        
        return self.finalize()