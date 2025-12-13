
import math
from solverEngine2.methods.base_method import BaseRootFindingMethod
from solverEngine2.base.data_classes import RootFinderParameters, RootFinderResult
from D import D


class FalsePositionMethod(BaseRootFindingMethod):

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
            # Convert to D objects for significant figure handling
            xl = D(params.xl)
            xu = D(params.xu)
            epsilon = D(params.epsilon)
            
            # Calculate initial function values
            f_xl = self.func(xl)
            f_xu = self.func(xu)
            if not isinstance(f_xl, D): 
                f_xl = D(f_xl)
            if not isinstance(f_xu, D): 
                f_xu = D(f_xu)
            
            # Check if root exists in interval (Bracketing condition)
            if f_xl * f_xu > D(0):
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
            
            # Main iteration loop
            for i in range(1, params.max_iterations + 1):
                # False Position formula: xr = (xl*f(xu) - xu*f(xl)) / (f(xu) - f(xl))
                # Alternative form: xr = xu - f(xu)*(xu - xl)/(f(xu) - f(xl))
                numerator = xl * f_xu - xu * f_xl
                denominator = f_xu - f_xl
                
                # Avoid division by zero
                if denominator.isNearZero():
                    self.result.error_message = "Division by zero in false position formula"
                    return self.result
                
                xr = numerator / denominator
                f_xr = self.func(xr)
                if not isinstance(f_xr, D): 
                    f_xr = D(f_xr)
                
                # Calculate approximate relative error
                if xr_prev is not None:
                    if xr != D(0):
                        # ea = float(abs((xr - xr_prev) / xr) * D(100))
                        ea = float(abs(xr - xr_prev ) / xr)
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
                if f_xr.isNearZero():
                    self.result.root = float(xr)
                    self.result.f_root=float(f_xr)

                    self.result.iterations = i
                    self.result.approximate_error = ea if ea != float('inf') else 0.0
                    self.result.converged = True
                    if params.step_by_step:
                        steps.append({
                            'type': 'converged',
                            'message': 'f(xr) is near zero. Root found.',
                            'xr': str(xr),
                            'f_xr': str(f_xr),
                            'iterations': i
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
                    if params.step_by_step:
                        steps.append({
                            'type': 'converged',
                            'message': f'Approximate error ({ea:.6f}%) below tolerance ({float(params.epsilon):.6f}%)',
                            'xr': str(xr),
                            'f_xr': str(f_xr),
                            'iterations': i
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
            self.result.converged = False
            self.result.steps = steps
            self.result.error_message = "Maximum iterations reached without convergence"
            
            if params.step_by_step:
                steps.append({
                    'type': 'warning',
                    'message': f'Maximum iterations ({params.max_iterations}) reached',
                    'final_xr': str(xr),
                    'final_error': ea if ea != float('inf') else 'N/A'
                })
            
        except ZeroDivisionError:
            self.result.error_message = "Division by zero occurred in false position calculation"
        except Exception as e:
            self.result.error_message = f"Error in False Position method: {str(e)}"
        
        return self.finalize()