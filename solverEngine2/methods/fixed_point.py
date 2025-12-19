"""
Fixed Point Iteration method implementation.
Solves x = g(x) by iterating x_{n+1} = g(x_n).
"""
from decimal import Overflow
import math
from solverEngine2.methods.base_method import BaseRootFindingMethod
from solverEngine2.base.data_classes import RootFinderParameters, RootFinderResult
from D import D
import sympy as sp



class FixedPointMethod(BaseRootFindingMethod):
    def make_function(self, equation_str):
        """Parse equation using SymPy for any function (f(x) or g(x))"""
        equation_str = equation_str.replace("^", "**")
        x = sp.symbols("x")
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
        """Safe function evaluation with D class support"""
        try:
            x_float = float(x)
            result = f(x_float)
            
            if isinstance(result, complex):
                raise ValueError("Complex value encountered")
                    
            return D(float(result)) if not isinstance(result, D) else result
        except Exception as e:
            raise ValueError(f"Error evaluating equation: {str(e)}")
    

    def analyze_convergence_simple(self, g_equation: str, x0: float) -> str:
     try:
        import re
        import sympy as sp

        # 🔒 same sanitization as make_function
        eq = g_equation.replace("^", "**")
        eq = eq.replace(" ", "")

        x = sp.symbols("x", real=True)
        plot_locals = {
            "x": x,
            "e": sp.E,
            "pi": sp.pi,
            "exp": sp.exp,
            "sin": sp.sin,
            "cos": sp.cos,
            "tan": sp.tan,
            "ln": sp.log,
            "log": sp.log,
            "log10": sp.log,
            "sqrt": sp.sqrt,
            "abs": sp.Abs,
            "sign": sp.sign,
            "pow": sp.Pow,
            "real_root": sp.real_root
        }
        expr = sp.sympify(
            eq,
            locals=plot_locals
        )

        expr = expr.replace(
            lambda e: (
                isinstance(e, sp.Pow)
                and e.exp.is_Rational
                and e.exp.q > 1
                and e.exp.q % 2 == 1
            ),
            lambda e: (
                sp.sign(e.base)
                * sp.real_root(sp.Abs(e.base), e.exp.q) ** e.exp.p
            )
        )

        derivative = sp.diff(expr, x)
        g_prime_sym = derivative.subs(x, x0)

        if not g_prime_sym.is_real:
           return "Convergence analysis not available"

        g_prime = float(g_prime_sym.evalf())
        abs_g = abs(g_prime)
        print("DEBUG g(x)      =", expr)
        print("DEBUG g'(x)     =", derivative)
        print("DEBUG x0        =", x0, type(x0))
        print("DEBUG g'(x0)sym =", g_prime_sym, type(g_prime_sym))
        if abs_g < 1:
            return (
                f"Converges monotonically (|g'|={abs_g:.3f} < 1)"
                if g_prime >= 0
                else f"Converges oscillatory (|g'|={abs_g:.3f} < 1)"
            )
        elif abs_g > 1:
            return (
                f"Diverges monotonically (|g'|={abs_g:.3f} > 1)"
                if g_prime >= 0
                else f"Diverges oscillatory (|g'|={abs_g:.3f} > 1)"
            )
        else:
            return "Marginal convergence (|g'| ≈ 1)"

     except Exception:
        return "Convergence analysis not available"

     
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
 
            f_func = self.make_function(params.equation)
            
            # Create g(x) function for Fixed Point iteration using the same method
            g_func = self.make_function(params.g_equation)
            
            # Convert to D objects for significant figure handling
            x0 = D(params.x0)
            epsilon = D(params.epsilon)
            convergence_prediction = self.analyze_convergence_simple(
               params.g_equation, 
               float(params.x0)
              )

            if params.step_by_step:
                steps.append({
                    'type': 'info',
                    'message': f'Fixed Point Iteration: x = g(x)',
                    'equation': params.equation,
                    'g_equation': params.g_equation,
                    'x0': str(x0),
                    'epsilon': str(epsilon),
                    'convergence_prediction': convergence_prediction
                })
            
            xr = x0  # Current approximation
            xr_prev = None
            ea = float('inf')  # Absolute error
            iteration_count = 0
            significant_digits = None
            # Main iteration loop
            for i in range(1, params.max_iterations + 1):
                iteration_count = i
                xr_prev = xr
                
                # Fixed Point iteration: x_{n+1} = g(x_n)
                try:

                    g_value = self.func_guard(float(xr_prev), g_func)

                    xr = g_value
                except ValueError  as e:
                    if "Overflow" in str(e) or "too large" in str(e).lower():
                       self.result.error_message = f"Overflow at iteration {i}: Method is diverging (values too large)"
                       self.result.root = float(xr_prev) if xr_prev is not None else float(x0)
                       self.result.iterations = i - 1
                       self.result.converged = False
                       self.result.significant_digits = significant_digits if xr_prev is not None else None

                       if params.step_by_step:
                            steps.append({
                    'type': 'error',
                    'message': f'Overflow detected at iteration {i}',
                    'last_valid_x': str(xr_prev)
                        })
                       self.result.steps = steps
                       return self.finalize()
                    else:
                         self.result.error_message = f"Error evaluating g(x) at iteration {i}: {str(e)}"
                         break
                except Exception as e:
                         self.result.error_message = f"Error evaluating g(x) at iteration {i}: {str(e)}"
                         break

                if xr_prev is not None:
                    if xr != D(0):
                        ea = float(abs((xr - xr_prev) /xr) )
                        significant_digits = self.calculate_significant_digits(ea)  # Inherited method

                    else:
                        ea = 0.0
                try:

                    f_xr = self.func_guard(float(xr), f_func)
  
                except ValueError as e:

                    if "Overflow" in str(e) or "too large" in str(e).lower():
                        self.result.error_message = f"Error evaluating f(x) at iteration {i}: Overflow/Divergence"
                        break
                    else:
                        self.result.error_message = f"Error evaluating f(x) at iteration {i}: {str(e)}"
                        break
                if params.step_by_step:
                    steps.append({
                        'type': 'iteration',
                        'iteration': i,
                        'x_current': str(xr_prev),
                        "g_x_current":str(g_value),
                        "f_x_next":str(f_xr),

                        'error': str(D(ea*100 ))if ea != float('inf') else None,
                        'method': 'Fixed Point'
                    })
                
                if float(f_xr) == 0 :
                    self.result.root = float(xr)
                    self.result.f_root = float(f_xr)
                    self.result.iterations = i
                    self.result.approximate_error = ea if ea != float('inf') else 0.0
                    self.result.converged = True
                    self.result.significant_digits = significant_digits if xr_prev is not None else None

                    
                    if params.step_by_step:
                        steps.append({
                            'type': 'converged',
                            'message': f'f(x) is near zero. Root found.',
                            'xr': str(xr),
                            'f_xr': str(f_xr),
                            'iterations': i,
                            'significant_digits': significant_digits if xr_prev is not None else None

                        })
                    self.result.steps = steps
                    return self.finalize()
                
                if ea != float('inf') and ea < float(params.epsilon):
                    self.result.root = float(xr)
                    self.result.f_root = float(f_xr)
                    self.result.iterations = i
                    self.result.approximate_error = ea
                    self.result.converged = True
                    
                    self.result.significant_digits = significant_digits if xr_prev is not None else None

                    
                    if params.step_by_step:
                        steps.append({
                            'type': 'converged',
                            'message': f'Absolute error ({ea:.6f}) below epsilon ({float(params.epsilon):.6f})',
                            'xr': str(xr),
                            'f_xr': str(f_xr),
                            'iterations': i,
                            'significant_digits': significant_digits if xr_prev is not None else None

                        })
                    self.result.steps = steps
                    return self.finalize()
                
      
            # Max iterations reached or divergence
            self.result.root = float(xr)
            self.result.f_root = float(f_xr)
            self.result.iterations = iteration_count
            self.result.approximate_error = ea if ea != float('inf') else 0.0
            self.result.significant_digits = significant_digits if xr_prev is not None else None

            self.result.converged = False
            self.result.steps = steps
            
            if not self.result.error_message:
                self.result.error_message = "Maximum iterations reached without convergence"
            
            if params.step_by_step:
                if iteration_count >= params.max_iterations:
                  steps.append({
                    'type': 'warning',
                    'message': f'Maximum iterations ({params.max_iterations}) reached without convergence',
                    'final_x': str(xr),
                    'final_f_x': str(f_xr),
                    'final_error': ea if ea != float('inf') else 'N/A',
                    'significant_digits': significant_digits 

                })
            
        except ZeroDivisionError:
            self.result.error_message = "Division by zero occurred in Fixed Point calculation"
        except Exception as e:
            self.result.error_message = f"Error in Fixed Point method: {str(e)}"
        
        return self.finalize()