from solverEngine2.methods.base_method import BaseRootFindingMethod
from solverEngine2.base.data_classes import RootFinderParameters, RootFinderResult
import sympy as sp
from D import D


class NewtonRaphsonMethod(BaseRootFindingMethod):
    """
    Newton-Raphson method.
    Uses the formula: x_{n+1} = x_n - f(x_n)/f'(x_n)
    """
    
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
        """Execute Newton-Raphson method - TO BE IMPLEMENTED"""
        self.setup(params)
        
        steps = []
        
        try:  
            f, df = self.make_derivative(params.equation)
            
            x_prev = params.x0
            epsilon = params.epsilon
            ea = float('inf')
            
            for i in range(params.max_iterations):
                f_x_prev = self.func_guard(x_prev, f)
                df_x_prev = self.func_guard(x_prev, df)
                
                if not isinstance(f_x_prev, D): f_x_prev = D(f_x_prev)
                if not isinstance(df_x_prev, D): df_x_prev = D(df_x_prev)
                
                x_next = D(x_prev - f_x_prev / df_x_prev)
                f_xnext = self.func_guard(x_next, f)
                
                if i > 0:
                    ea = abs((x_next - x_prev) / x_next)
                
                if params.step_by_step:
                    steps.append({
                        'type': 'iteration',
                        'iteration': str(i + 1),
                        'xi': x_prev,
                        'f(xi)': f_x_prev,
                        'df(xi)': df_x_prev,
                        'xi+1': x_next,
                        'error': ea if i > 0 else 'N/A'
                    })
                    
                if f_xnext.isNearZero():
                    self.result.root = x_next
                    self.result.f_root = f_xnext
                    self.result.iterations = i
                    self.result.approximate_error = ea if ea != float('inf') else 0.0
                    self.result.converged = True
                    if params.step_by_step:
                        steps.append({
                            'type': 'converged',
                            'message': 'f(xr) is near zero. Root found.',
                            'xr': x_next,
                            'f_xr': f_xnext
                        })
                    self.result.steps = steps
                    return self.finalize()
                
                if ea != float('inf') and ea < float(params.epsilon):
                    self.result.root = x_next
                    self.result.iterations = i
                    self.result.approximate_error = ea
                    self.result.converged = True
                    self.result.steps = steps
                    self.result.f_root = f_xnext

                    return self.finalize()
                
                x_prev = x_next
                
            self.result.root = x_next
            self.result.iterations = params.max_iterations
            self.result.approximate_error = ea if ea != float('inf') else 0.0
            self.result.converged = False
            self.result.f_root = f_xnext
            self.result.steps = steps
            self.result.error_message = "Maximum iterations reached without convergence"
            
            
        except Exception as e:
            self.result.error_message = f"Error in Newton-Raphson method: {str(e)}"
            
        return self.finalize()