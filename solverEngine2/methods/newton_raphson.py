from solverEngine2.methods.base_method import BaseRootFindingMethod
from solverEngine2.base.data_classes import RootFinderParameters, RootFinderResult
import sympy as sp
from D import D
import math


class NewtonRaphsonMethod(BaseRootFindingMethod):
    """
    Newton-Raphson method.
    Uses the formula: x_{n+1} = x_n - f(x_n)/f'(x_n)
    """
    
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
            x_prev = params.x0
            epsilon = params.epsilon
            
            for i in range(params.max_iterations):
                f_x_prev = self.func_guard(x_prev, f)
                df_x_prev = self.func_guard(x_prev, df)
                
                if not isinstance(f_x_prev, D): f_x_prev = D(f_x_prev)
                if not isinstance(df_x_prev, D): df_x_prev = D(df_x_prev)
                
                try:
                    x_next = D(x_prev - f_x_prev / df_x_prev)
                except:
                    raise ZeroDivisionError("Division By Zero Error in Newton-Raphson Method. f'(xi) is Equal to Zero")
                
                try:
                    f_xnext = self.func_guard(x_next, f)
                except:
                    raise ZeroDivisionError("Division by Zero Error Evaluating f(xi+1)")
                
                if i > 0:
                    if not x_next.isNearZero():
                        ea = abs((x_next - x_prev) / x_next)
                        sig = self.calculate_significant_digits(ea)
                        significant_digits = sig if sig is not None else params.significant_figures
                    else:
                        ea = float('inf')
                        significant_digits = 0
                
                if params.step_by_step:
                    steps.append({
                        'type': 'iteration',
                        'iteration': str(i + 1),
                        'xi': x_prev,
                        'f(xi)': f_x_prev,
                        'df(xi)': df_x_prev,
                        'xi+1': x_next,
                        'error': ea if i > 0 and ea != float('inf') else 'N/A'
                    })
                
                if f_xnext.isNearZero() or (ea != float('inf') and ea < float(epsilon)):
                    self.result.root = x_next
                    self.result.f_root = f_xnext
                    self.result.iterations = i + 1
                    self.result.approximate_error = ea
                    self.result.converged = True
                    self.result.significant_digits = significant_digits
                    self.result.steps = steps
                    return self.finalize()
                
                x_prev = x_next
            
            if params.step_by_step:
                steps.append({
                    'type': 'warning',
                    'message': f'Maximum iterations reached without convergence',
                    'xr': x_next,
                    'f_xr': f_xnext,
                    'error': ea,
                    'iteration': str(params.max_iterations)
                })
            
            self.result.root = x_next
            self.result.iterations = params.max_iterations
            self.result.approximate_error = ea
            self.result.converged = False
            self.result.significant_digits = significant_digits if significant_digits is not None else params.significant_figures
            self.result.f_root = f_xnext
            self.result.steps = steps
            self.result.error_message = "Maximum iterations reached without convergence"
        
        except Exception as e:
            self.result.error_message = f"Error in Newton-Raphson method: {str(e)}"
        
        return self.finalize()