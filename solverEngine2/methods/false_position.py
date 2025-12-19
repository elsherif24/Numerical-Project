
import math
from solverEngine2.methods.base_method import BaseRootFindingMethod
from solverEngine2.base.data_classes import RootFinderParameters, RootFinderResult
from D import D
import sympy as sp


class FalsePositionMethod(BaseRootFindingMethod):
    def make_function(self, equation_str):

       equation_str = equation_str.replace("^", "**")
       x = sp.symbols("x", real=True)
       plot_locals = {
    "x": x,

    # Constants
    "e": sp.E,
    "pi": sp.pi,

    # Exponentials
    "exp": sp.exp,

    # Trigonometric
    "sin": sp.sin,
    "cos": sp.cos,
    "tan": sp.tan,

    # Logarithms
    "ln": sp.log,
    "log": sp.log,        # natural log
    "log10": sp.log,      # user writes log10(x)

    # Roots
    "sqrt": sp.sqrt,

    # Absolute & sign
    "abs": sp.Abs,
    "sign": sp.sign,

    # Power & real root
    "pow": sp.Pow,
    "real_root": sp.real_root
}
       expr = sp.sympify(
        equation_str,
        locals=plot_locals
    )


       expr = expr.replace(
        lambda e: (
        isinstance(e, sp.Pow)
        and e.exp.is_Rational
        and e.exp.q > 1        # ⬅ protects x^3
        and e.exp.q % 2 == 1
         ),
        lambda e: (
        sp.sign(e.base)
        * sp.real_root(sp.Abs(e.base), e.exp.q) ** e.exp.p
            )
         )
       f_numeric = sp.lambdify(x, expr, modules=["math"])

       def f(val):
        try:
            res = f_numeric(val)
            if isinstance(res, complex):
                raise ValueError("Complex value encountered")
            return float(res)
        except Exception as e:
            raise ValueError(str(e))

       return f
    def func_guard(self, x, f):

        try:
            x_float = float(x)
            result = f(x_float)

            if isinstance(result,complex):

                     raise ValueError("Complex value encountered")
                    
               
            return D(float(result)) if not isinstance(result, D) else result
        except Exception as e:
            raise ValueError(f"Error evaluating equation: {str(e)}")

    def validate_parameters(self) -> bool:
        if self.params.xl >= self.params.xu:
            self.result.error_message = "Lower bound (xl) must be less than upper bound (xu)"
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
            f = self.make_function(params.equation)
            try:
            # Convert to D objects for significant figure handling
              xl_float = float(params.xl)
              xu_float = float(params.xu)
              f_xl = self.func_guard(xl_float, f)
              f_xu = self.func_guard(xu_float, f)
            except Exception as e:
                self.result.error_message = f"Error evaluating initial points: {str(e)}"
                self.result.steps = steps 
                return self.finalize()
            epsilon_float = float(params.epsilon)

            xl = D(params.xl)
            xu = D(params.xu)
            epsilon = D(params.epsilon)
            

            if float(f_xl) * float(f_xu) > 0:
                self.result.error_message = (
                    f"No root exists in interval [{xl}, {xu}].\n"
                    f"f({xl}) = {f_xl}\n"
                    f"f({xu}) = {f_xu}\n"
                    f"Both values have the same sign."
                )
                return self.result
            
            if params.step_by_step:
                steps.append({
                    'type': 'info',
                    'message': f'Initial interval: [{xl}, {xu}]',
                    'xl': str(xl),
                    'xu': str(xu),
                    'f_xl': str(f_xl),
                    'f_xu': str(f_xu),
                    'method': 'False Position (Regula Falsi)'
                })
            
            xr_prev = None
            ea = float('inf')
            xr = None
            significant_digits = None
            f_xr = None
            # Main iteration loop
            for i in range(1, params.max_iterations + 1):
                # False Position formula: xr = (xl*f(xu) - xu*f(xl)) / (f(xu) - f(xl))
                # Alternative form: xr = xu - f(xu)*(xu - xl)/(f(xu) - f(xl))
                numerator = xl * f_xu - xu * f_xl
                denominator = f_xu - f_xl
                
                # Avoid division by zero
                if denominator.isNearZero():
                    if params.step_by_step:
                        steps.append({
                            'type': 'error',
                            'message': f'Division by zero at iteration {i}: denominator f(xu)-f(xl) = {denominator} ≈ 0',
                            'iteration': i,
                            'xl': str(xl),
                            'xu': str(xu),
                            'f_xl': str(f_xl),
                            'f_xu': str(f_xu),
                            'method': 'False Position'
                        })
                    self.result.error_message = f"Division by zero at iteration {i}"
                    
                    # Record partial results
                    self.result.root = float(xr) if xr is not None else None
                    self.result.f_root = float(f_xr) if 'f_xr' in locals() else None
                    self.result.iterations = i - 1 if i > 1 else 0
                    self.result.approximate_error = ea if ea != float('inf') else 0.0
                    self.result.significant_digits = significant_digits if xr_prev is not None else None
                    self.result.converged = False
                    self.result.steps = steps
                    return self.finalize()    
                
                xr = numerator / denominator
                # f_xr = self.func(xr)
                try:
                  f_xr = self.func_guard(float(xr), f)
                  if not isinstance(f_xr, D): 
                    f_xr = D(f_xr)
                except Exception as e:
                    self.result.error_message = f"Error evaluating f(x) at iteration {i}: {str(e)}"
                    self.result.steps = steps
                    return self.finalize()
                    
                # Calculate approximate relative error
                if xr_prev is not None:
                    if xr != D(0):
                        ea = float(abs((xr - xr_prev)  / xr))
                        significant_digits = self.calculate_significant_digits(ea)  # Inherited method

                    else:
                        ea = 0.0
                
                if params.step_by_step:
                    steps.append({
                        'type': 'iteration',
                        'iteration': i,
                        'xl': str(xl),
                        'xu': str(xu),
                        'xr': str(xr),
                        'f_xr': str(f_xr),
                        'f_xl': str(f_xl),
                        'f_xu': str(f_xu),
                        'error': str(D((ea*100.0))) if ea != float('inf') else None,
                        'method': 'False Position'
                    })
                
                # Check if function value is near zero (root found)
                if f_xr == 0:
                    self.result.root = float(xr)
                    self.result.f_root=float(f_xr)

                    self.result.iterations = i
                    self.result.approximate_error = ea if ea != float('inf') else 0.0
                    self.result.converged = True
                    self.result.significant_digits = significant_digits if xr_prev is not None else None

                    if params.step_by_step:
                        steps.append({
                            'type': 'converged',
                            'message': 'f(xr) is near zero. Root found.',
                            'xr': str(xr),
                            'f_xr': str(f_xr),
                            'iterations': i,
                            'significant_digits': significant_digits if xr_prev is not None else None

                            
                        })
                    self.result.steps = steps
                    return self.finalize()
                
                # Check convergence based on error
                if ea != float('inf') and ea < float(params.epsilon):
                    self.result.root = float(xr)
                    self.result.f_root=float(f_xr)
                    self.result.iterations = i
                    self.result.approximate_error = ea
                    self.result.converged = True
                    self.result.significant_digits = significant_digits if xr_prev is not None else None

                    if params.step_by_step:
                        steps.append({
                            'type': 'converged',
                            'message': f'Approximate error ({ea:.6f}) below tolerance ({float(params.epsilon):.6f})',
                            'xr': str(xr),
                            'f_xr': str(f_xr),
                            'iterations': i,
                            'significant_digits': significant_digits if xr_prev is not None else None

                        })
                    self.result.steps = steps
                    return self.finalize()
                
                # Update interval based on sign change
                # If f(xl) and f(xr) have opposite signs, root is between xl and xr
                # Otherwise, root is between xr and xu
                if f_xl * f_xr < D(0):
                    xu = xr
                    f_xu = f_xr
                else:
                    xl = xr
                    f_xl = f_xr
                
                xr_prev = xr
            
            # Max iterations reached
            self.result.root = float(xr)
            self.result.f_root=float(f_xr)
            self.result.iterations = params.max_iterations
            self.result.approximate_error = ea if ea != float('inf') else 0.0
            self.result.significant_digits = significant_digits if xr_prev is not None else None

            self.result.converged = False
           
            
            if params.step_by_step:
                steps.append({
                    'type': 'warning',
                    'message': f'Maximum iterations ({params.max_iterations}) reached',
                    'final_xr': str(xr),
                    'final_error': ea if ea != float('inf') else 'N/A',
                            'significant_digits': significant_digits  

                })
            self.result.steps = steps
            self.result.error_message = "Maximum iterations reached without convergence"
        except ZeroDivisionError:
            self.result.error_message = f"Division by zero occurred: {str(e)}"
            self.result.steps = steps
        except Exception as e:
            self.result.error_message = f"Error in False Position method: {str(e)}"
            self.result.steps = steps
        
        return self.finalize()