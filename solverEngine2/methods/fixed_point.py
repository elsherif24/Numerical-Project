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

        expr = sp.sympify(
            equation_str,
            locals={"real_root": sp.real_root}
        )

        # Automatically replace fractional powers x**(1/3)
        # expr = expr.replace(
        #     lambda e: isinstance(e, sp.Pow)
        #               and e.exp.is_Rational
        #               and e.exp.q % 2 == 1,
        #     lambda e: sp.real_root(e.base, e.exp.q)
        # )
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

        # def f(val):
        #     res = expr.subs(x, val).evalf()
        #     if res.is_real:
        #         return float(res)
        #     raise ValueError("Complex value encountered")

        # return f
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
    
    # def analyze_convergence_simple(self, g_equation: str, x0: float) -> str:
    #     """
    #     Simple convergence analysis using symbolic derivative at x0.
    #     Returns a string describing the convergence behavior.
    #     """
    #     try:
    #         # Get symbolic derivative
    #         x = sp.symbols('x')
    #         g_expr = sp.sympify(g_equation.replace('^', '**'))
    #         derivative = sp.diff(g_expr, x)
            
    #         # Evaluate at x0
    #         g_prime = float(derivative.subs(x, x0))
    #         abs_g_prime = abs(g_prime)
            
    #         # Simple classification
    #         if abs_g_prime < 1:
    #             if g_prime >= 0:
    #                 return f"Converges monotonically (|g'|={abs_g_prime:.3f} < 1, g' ≥ 0)"
    #             else:
    #                 return f"Converges oscillatory (|g'|={abs_g_prime:.3f} < 1, g' < 0)"
    #         elif abs_g_prime > 1:
    #             if g_prime >= 0:
    #                 return f"Diverges monotonically (|g'|={abs_g_prime:.3f} > 1)"
    #             else:
    #                 return f"Diverges oscillatory (|g'|={abs_g_prime:.3f} > 1)"
    #         else:
    #             return f"Marginal convergence (|g'| ≈ 1)"
                
    #     except:
    #         # If sympy fails, give generic message
    #         return "Convergence analysis not available"
    def analyze_convergence_simple(self, g_equation: str, x0: float) -> str:
     try:
        import re
        import sympy as sp

        # 🔒 same sanitization as make_function
        eq = g_equation.replace("^", "**")
        eq = eq.replace(" ", "")

        x = sp.symbols("x", real=True)

        # 🔒 same sympify as make_function
        expr = sp.sympify(
            eq,
            locals={"real_root": sp.real_root}
        )

        # 🔒 same odd-root handling
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
        g_prime = float(derivative.subs(x, x0))
        abs_g = abs(g_prime)

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

    # def analyze_convergence_simple(self, g_equation: str, x0: float) -> str:
    #     """
    #     Simple convergence analysis using symbolic derivative at x0.
    #     Returns a string describing the convergence behavior.
    #     """
    #     try:
            
    #         # Get symbolic derivative
    #         x = sp.symbols('x')
    #         expr = sp.sympify(g_equation.replace('^', '**'))
    #         derivative = sp.diff(expr, x)
            
    #         # Evaluate at x0
    #         g_prime = float(derivative.subs(x, x0))
    #         abs_g_prime = abs(g_prime)
            
    #         # Simple classification
    #         if abs_g_prime < 1:
    #             if g_prime >= 0:
    #                 return f"Converges monotonically (|g'|={abs_g_prime:.3f} < 1, g' ≥ 0)"
    #             else:
    #                 return f"Converges oscillatory (|g'|={abs_g_prime:.3f} < 1, g' < 0)"
    #         elif abs_g_prime > 1:
    #             if g_prime >= 0:
    #                 return f"Diverges monotonically (|g'|={abs_g_prime:.3f} > 1)"
    #             else:
    #                 return f"Diverges oscillatory (|g'|={abs_g_prime:.3f} > 1)"
    #         else:
    #             return f"Marginal convergence (|g'| ≈ 1)"
                
    #     except:
    #         # If sympy fails, give generic message
    #         return "Convergence analysis not available"
     
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
            # try:
            #     # from solverEngine2.base.equation_parser import parse_equation
            #     # g_func = parse_equation(params.g_equation)
            #     print(g_func)
            # except ImportError:
            #     g_func = lambda x: eval(params.g_equation.replace('^', '**'), 
            #                             {"x": x, "exp": math.exp, "sin": math.sin, 
            #                              "cos": math.cos, "ln": math.log, "log10": math.log10,
            #                              "sqrt": math.sqrt, "pi": math.pi, "e": math.e})
            # except Exception as e:
            #     self.result.error_message = f"Error parsing g(x) equation: {str(e)}"
            #     return self.result
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
                    # Evaluate g(x)
                    # g_value = g_func(xr_prev)
                    g_value = self.func_guard(float(xr_prev), g_func)
                    # if not isinstance(g_value, D):
                    #     g_value = D(g_value)
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
                
                # Calculate absolute error (not relative)
                # if xr_prev is not None:
                #     ea = float(abs(xr - xr_prev)/xr)
                if xr_prev is not None:
                    if xr != D(0):
                        # ea = float(abs((xr - xr_prev) / xr) * D(100))
                        ea = float(abs((xr - xr_prev) /xr) )
                        significant_digits = self.calculate_significant_digits(ea)  # Inherited method

                    else:
                        ea = 0.0
                try:
                # Evaluate f(x) at current approximation
                    # f_xr = self.func(xr)
                    f_xr = self.func_guard(float(xr), f_func)
                    # if not isinstance(f_xr, D):
                    #   f_xr = D(f_xr)
                # except (ValueError, Overflow) as e:
                #     self.result.error_message = f"Error evaluating f(x) at iteration {i}: Overflow/Divergence"
                #     break
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
                        # 'x_current': str(xr),
                        # 'g_x': str(xr),  # g(x) = current x
                        # 'f_x': str(f_xr),
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
                
                # if i > 2:
                #     if ea > 1e10:  # Diverging to infinity
                #         self.result.error_message = f"Divergence detected after {i} iterations"
                #         break
                #     if abs(float(f_xr)) > 1e10:  # Function value blowing up
                #         self.result.error_message = f"Function value too large after {i} iterations"
                #         break
            
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