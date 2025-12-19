from solverEngine2.methods.base_method import BaseRootFindingMethod
from solverEngine2.base.data_classes import RootFinderParameters, RootFinderResult
import sympy as sp
from D import D
import math

class SecantMethod(BaseRootFindingMethod):
    
    def real_odd_root(self, x, n):
        return math.copysign(abs(x) ** (1/n), x)

    def make_derivative(self, equation_str):
        equation_str = equation_str.replace("^", "**")
        x = sp.symbols("x")

        # tell sympy that 'e' is the constant
        expr = sp.sympify(equation_str, locals={"e": sp.E})

        expr = expr.replace(
            lambda e: isinstance(e, sp.Pow)
                    and e.exp.is_Rational
                    and e.exp.q % 2 == 1,
            lambda e: sp.Function('real_odd_root')(e.base, e.exp.q)**e.exp.p
        )

        f = sp.lambdify(x, expr, modules=[{"real_odd_root": self.real_odd_root}, "math"])

        def df_numeric(val):
            h = 1e-6
            x0 = float(val)
            return (f(x0 + h) - f(x0 - h)) / (2*h)

        return f, df_numeric

    def func_guard(self, x, f):
        try:
            x_float = float(x)
            y = f(x_float)
            if isinstance(y, complex):
                raise ValueError("Complex value encountered")
            return D(y)
        except Exception as e:
            raise ValueError(f"Error evaluating equation: {str(e)}")
    
    
    def validate_parameters(self) -> bool:
        """Validate that derivative equation is provided if needed"""
        # Derivative can be calculated numerically or provided
        return True
    
    def solve(self, params: RootFinderParameters) -> RootFinderResult:
        
        self.setup(params)
        
        steps = []
        significant_digits = None
        ea = float('inf')
        
        try:  
            f, df = self.make_derivative(params.equation)

            x0 = params.x0
            x1 = params.x1
            epsilon = params.epsilon
            
            for i in range(params.max_iterations):
                try:
                    f_x0 = self.func_guard(x0, f)
                    f_x1 = self.func_guard(x1, f)
                except:
                    raise ZeroDivisionError("Division by Zero When Evaluating f(x0) or f(x1)")
                
                try:                
                    factor = D((f_x1 * (x0 - x1)) / (f_x0 - f_x1))
                except:
                    raise ZeroDivisionError("Secant denominator near zero")
                
                x_next = D(x1 - factor)
                
                try:
                    f_xnext = self.func_guard(x_next, f)
                except:
                    raise ZeroDivisionError("Zero Division Error Evaluating f(xi+1).")
                
                if i > 0:
                    if not x_next.isNearZero():
                        ea = abs((x_next - x1) / x_next)
                        sig = self.calculate_significant_digits(ea)
                        significant_digits = sig if sig is not None else params.significant_figures
                    else:
                        ea = float('inf')
                        significant_digits = 0
                
                if params.step_by_step:
                    steps.append({
                        'type': 'iteration',
                        'iteration': str(i + 1),
                        'xi-1': str(x0),
                        'xi': str(x1),
                        'f(xi)Δx / Δf': str(factor),
                        'xi+1': str(x_next),
                        'error': ea if i > 0 else 'N/A'
                    })
            
                if f_xnext.isNearZero():
                    self.result.root = float(x_next)
                    self.result.f_root = float(f_xnext)
                    self.result.iterations = i + 1
                    self.result.approximate_error = ea if ea != float('inf') else 0.0
                    self.result.converged = True
                    self.result.significant_digits = significant_digits
                    if params.step_by_step:
                        steps.append({
                            'type': 'converged',
                            'message': 'f(xr) is near zero. Root found.',
                            'xr': str(x_next),
                            'f_xr': str(f_xnext),
                            'significant_digits': significant_digits
                        })
                    self.result.steps = steps
                    return self.finalize()
                
                if ea != float('inf') and ea < float(epsilon):
                    self.result.root = float(x_next)
                    self.result.iterations = i + 1
                    self.result.approximate_error = ea
                    self.result.converged = True
                    self.result.f_root = float(f_xnext)
                    self.result.significant_digits = significant_digits
                    self.result.steps = steps
                    return self.finalize()
                
                x0, x1 = x1, x_next
                
            self.result.root = float(x_next)
            self.result.iterations = params.max_iterations
            self.result.approximate_error = ea if ea != float('inf') else 0.0
            self.result.converged = False
            self.result.f_root = float(f_xnext)
            self.result.steps = steps
            self.result.significant_digits = significant_digits if significant_digits is not None else params.significant_figures
            self.result.error_message = "Maximum iterations reached without convergence"
            
        except Exception as e:
            self.result.error_message = f"Error in Secant method: {str(e)}"
            
        return self.finalize()
