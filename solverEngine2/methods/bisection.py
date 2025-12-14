
import math
from solverEngine2.methods.base_method import BaseRootFindingMethod
from solverEngine2.base.data_classes import RootFinderParameters, RootFinderResult
from D import D


class BisectionMethod(BaseRootFindingMethod):
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
            
            # Check if root exists in interval
            f_xl = self.func(xl)
            f_xu = self.func(xu)
            if not isinstance(f_xl, D): 
                f_xl = D(f_xl)
            if not isinstance(f_xu, D): 
                f_xu = D(f_xu)
            
            if f_xl * f_xu > D(0):
                self.result.error_message = (
                    f"No root exists in interval [{xl}, {xu}].\n"
                    f"f({xl}) = {f_xl}\n"
                    f"f({xu}) = {f_xu}\n"
                    f"Both values have the same sign."
                )
                return self.result
            
            # Calculate required iterations
            L0 = abs(xu - xl)
            k_required = math.ceil(math.log2(float(L0 / epsilon))) if float(L0) > 0 and float(epsilon) > 0 else 0
            
            if params.step_by_step:
                steps.append({
                    'type': 'info',
                    'message': f'Initial interval: [{xl}, {xu}]',
                    'xl': str(xl),
                    'xu': str(xu),
                    'f_xl': str(f_xl),
                    'f_xu': str(f_xu),
                    'required_iterations': k_required
                })
            
            xr_prev = None
            ea = float('inf')
            xr = None
        
            # Main iteration loop
            for i in range(1, k_required+ 1):
                if(i>params.max_iterations):
                    self.result.root = float(xr)
                    self.result.f_root=float(f_xr)
                    self.result.iterations = params.max_iterations
                    self.result.significant_digits = significant_digits if xr_prev is not None else None

                    self.result.approximate_error = ea if ea != float('inf') else 0.0
                    self.result.converged = False
                    if params.step_by_step:
                       steps.append({
                'type': 'warning',
                'message': f'Maximum iterations ({params.max_iterations}) reached, but {k_required} required',
                'final_xr': str(xr) if xr is not None else 'N/A',
                'final_error': str(D(ea * 100)) if ea != float('inf') else 'N/A',
                'significant_digits': significant_digits
                   })
                    self.result.steps = steps
                    self.result.error_message = f"Maximum iterations reached without convergence, Required {k_required} iterations."

                    return self.finalize()
            
                    
                
                # Calculate midpoint
                xr = (xl + xu) / D(2)
                f_xr = self.func(xr)
                if not isinstance(f_xr, D): 
                    f_xr = D(f_xr)
                
                # Calculate approximate relative error
                if xr_prev is not None:
                    if xr != D(0):
                        # ea = float(abs((xr - xr_prev) / xr) * D(100))
                        ea = float(abs((xr - xr_prev) )/xr )
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
                        'error': str(D((ea*100.0))) if ea != float('inf') else None
                    })
                
                # Check if function value is near zero (root found)
                if f_xr == 0 :
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
                            'significant_digits': significant_digits if xr_prev is not None else None
                        })
                    self.result.steps = steps
                    return self.finalize()
                
                # Check convergence based on error
                # if ea != float('inf') and ea < float(params.epsilon):
                #     self.result.root = float(xr)
                #     self.result.f_root=float(f_xr)

                #     self.result.iterations = i
                #     self.result.approximate_error = ea
                #     self.result.converged = True
                #     if params.step_by_step:
                #         steps.append({
                #             'type': 'converged',
                #             'message': f'Approximate error ({ea:.6f}%) below tolerance ({float(params.epsilon):.6f}%)',
                #             'xr': str(xr),
                #             'f_xr': str(f_xr),
                #             'iterations': i
                #         })
                #     self.result.steps = steps
                #     return self.finalize()
                
                # Update interval
                f_xl_current = self.func(xl)
                if not isinstance(f_xl_current, D): 
                    f_xl_current = D(f_xl_current)
                
                if f_xl_current * f_xr < D(0):
                    xu = xr
                    f_xu = f_xr
                else:
                    xl = xr
                    f_xl = f_xr
                
                xr_prev = xr
            self.result.root = float(xr)
            self.result.f_root=float(f_xr)
            self.result.significant_digits = significant_digits if xr_prev is not None else None

            self.result.iterations = k_required
            self.result.approximate_error = ea if ea != float('inf') else 0.0
            self.result.converged = True
            # Max iterations reached
            if params.step_by_step:
                        steps.append({
                            'type': 'converged',
                            'message': f'Completed all {k_required} iterations. Final error: {ea:.6f}',

                            'xr': str(xr),
                            'f_xr': str(f_xr),
                            'iterations':k_required,
                            'significant_digits': significant_digits if xr_prev is not None else None

                        })
            self.result.steps = steps
        except Exception as e:
            self.result.error_message = f"Error in Bisection method: {str(e)}"
        
        return self.finalize()