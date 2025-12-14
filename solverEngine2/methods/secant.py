from solverEngine2.methods.base_method import BaseRootFindingMethod
from solverEngine2.base.data_classes import RootFinderParameters, RootFinderResult
import sympy as sp
from D import D


class SecantMethod(BaseRootFindingMethod):
    
    def make_derivative(self, equation_str):
        equation_str = equation_str.replace("^", "**")


        x = sp.symbols("x")

        expr = sp.sympify(equation_str)

        d_expr = sp.diff(expr, x)

        f = sp.lambdify(x, expr, "math")          
        df = sp.lambdify(x, d_expr, "math")       

        return f, df

    def func_guard(self, x, f):
        if not isinstance(x, D): x = D(x)
        try:
            return f(x)
        except Exception as e:
            raise ValueError(f"Error evaluating equation: {str(e)}")
    
    
    def validate_parameters(self) -> bool:
        """Validate that derivative equation is provided if needed"""
        # Derivative can be calculated numerically or provided
        return True
    
    def solve(self, params: RootFinderParameters) -> RootFinderResult:
        
        self.setup(params)
        
        steps = []
        
        try:  
            f, df = self.make_derivative(params.equation)


            x0 = params.x0
            x1 = params.x1
            epsilon = params.epsilon
            ea = float('inf')
            
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
                    else:
                        ea = float('inf')
                    
                
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
                    if params.step_by_step:
                        steps.append({
                            'type': 'converged',
                            'message': 'f(xr) is near zero. Root found.',
                            'xr': str(x1),
                            'f_xr': str(f_x1)
                        })
                    self.result.steps = steps
                    return self.finalize()
                
                if ea != float('inf') and ea < float(epsilon):
                    self.result.root = float(x_next)
                    self.result.iterations = i + 1
                    self.result.approximate_error = ea
                    self.result.converged = True
                    self.result.steps = steps
                    self.result.f_root = float(f_xnext)

                    return self.finalize()
                
                x0, x1 = x1, x_next
                
                
            self.result.root = float(x_next)
            self.result.iterations = params.max_iterations
            self.result.approximate_error = ea if ea != float('inf') else 0.0
            self.result.converged = False
            self.result.f_root = float(f_xnext)
            self.result.steps = steps
            self.result.error_message = "Maximum iterations reached without convergence"
            
            
        except Exception as e:
            self.result.error_message = f"Error in Secant method: {str(e)}"
            
        return self.finalize()