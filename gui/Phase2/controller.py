# import customtkinter as ctk
# from solverEngine2.phase2_solver import RootFinderParameters, solve_root
# from D import set_sig_figs


# class Phase2Controller:
#     def __init__(self):
#         self.view = None
        
#         # Tkinter variables
#         self.equation_var = None
#         self.method_var = None
#         self.xl_var = None
#         self.xu_var = None
#         self.max_iterations_var = None
#         self.epsilon_var = None
#         self.sig_figs_var = None
#         self.step_by_step_var = None
        
#     def initialize_tk_variables(self):
#         self.equation_var = ctk.StringVar(value="x^3 - x - 2")
#         self.method_var = ctk.StringVar(value="Bisection")
#         self.xl_var = ctk.DoubleVar(value=1.0)
#         self.xu_var = ctk.DoubleVar(value=2.0)
#         self.max_iterations_var = ctk.IntVar(value=50)
#         self.epsilon_var = ctk.DoubleVar(value=0.00001)
#         self.sig_figs_var = ctk.IntVar(value=5)
#         self.step_by_step_var = ctk.BooleanVar(value=False)

#     def set_view(self, view):
#         self.view = view
    
#     def solve(self):
#         try:
#             # Get parameters
#             params = RootFinderParameters()
#             params.equation = self.equation_var.get().strip()
#             params.method = self.method_var.get()
#             params.xl = self.xl_var.get()
#             params.xu = self.xu_var.get()
#             params.max_iterations = self.max_iterations_var.get()
#             params.epsilon = self.epsilon_var.get()
#             params.significant_figures = self.sig_figs_var.get()
#             params.step_by_step = self.step_by_step_var.get()
            
#             # Set global significant figures
#             set_sig_figs(params.significant_figures)
            
#             # Validate inputs
#             if not params.equation:
#                 self.view.display_error("Please enter an equation")
#                 return
            
#             if params.xl >= params.xu:
#                 self.view.display_error("Lower bound (Xl) must be less than upper bound (Xu)")
#                 return
            
#             # Solve
#             result = solve_root(params)
            
#             # Display results
#             if result.error_message and not result.root:
#                 self.view.display_error(result.error_message)
#             else:
#                 self.view.display_result(result)
                
#         except Exception as e:
#             self.view.display_error(f"Error: {str(e)}")
    
#     def plot_function(self):
#         try:
#             equation = self.equation_var.get().strip()
#             if not equation:
#                 self.view.display_error("Please enter an equation first")
#                 return
            
#             xl = self.xl_var.get()
#             xu = self.xu_var.get()
            
#             self.view.plot_equation(equation, xl, xu)
            
#         except Exception as e:
#             self.view.display_error(f"Error plotting: {str(e)}")

import customtkinter as ctk
from solverEngine2.solver import solve_root, get_available_methods
from solverEngine2.base.data_classes import RootFinderParameters
from D import set_sig_figs


class Phase2Controller: 
    def __init__(self):
        self.view = None
        
        # Tkinter variables
        self.equation_var = None
        self.method_var = None
        
        # Interval-based parameters (Bisection, False Position)
        self.xl_var = None
        self.xu_var = None
        
        # Fixed Point parameters
        self.x0_var = None
        self.g_equation_var = None
        
        # Newton-Raphson parameters
        self.derivative_var = None
        
        # Secant parameters
        self.x1_var = None
        
        # Modified Newton parameters
        self.multiplicity_var = None
        
        # Common parameters
        self.max_iterations_var = None
        self.epsilon_var = None
        self.sig_figs_var = None
        self.step_by_step_var = None
        
    def initialize_tk_variables(self):
        self.equation_var = ctk.StringVar(value="x^3 - x - 2")
        self.method_var = ctk.StringVar(value="Bisection")
        
        # Interval-based
        self.xl_var = ctk.DoubleVar(value=1.0)
        self.xu_var = ctk.DoubleVar(value=3.0)
        
        # Fixed Point
        self.x0_var = ctk.DoubleVar(value=1.0)
        self.g_equation_var = ctk.StringVar(value="")
        
        # Newton-Raphson
        self.derivative_var = ctk.StringVar(value="")
        
        # Secant
        self.x1_var = ctk.DoubleVar(value=1.5)
        
        # Modified Newton
        self.multiplicity_var = ctk.IntVar(value=1)
        
        # Common
        self.max_iterations_var = ctk.IntVar(value=50)
        self.epsilon_var = ctk.DoubleVar(value=0.00001)
        self.sig_figs_var = ctk.IntVar(value=5)
        self.step_by_step_var = ctk.BooleanVar(value=False)

    def set_view(self, view):
        self.view = view
    
    def on_method_change(self, method: str):
        if self.view:
            self.view.update_parameter_visibility(method)
    
    def solve(self):
        try:
            # Create parameters object
            params = RootFinderParameters()
            params.equation = self.equation_var.get().strip()
            params.method = self.method_var.get()
            
            # Method-specific parameters
            if params.method in ["Bisection", "False-Position"]:
                try:
                    params.xl = self.xl_var.get()

                except:
                    self.view.display_error ("Lower bound (xl) is required Bisection/False-Position methods")
                    return
                try:
                    params.xu = self.xu_var.get()
                except:
                    self.view.display_error ("Upper bound (xu) is required Bisection/False-Position methods")   
                    return 
            
            if params.method == "Fixed Point":
                try:
                  params.x0 = self.x0_var.get()
                except:
                  self.view.display_error ("Initial guess (x0) is required for Fixed Point method")
                  return 
                params.g_equation = self.g_equation_var.get().strip()

            
            if params.method in ["Newton-Raphson", "Modified Newton-Raphson"]:
                # try:
                #   params.x0 = self.x0_var.get()
                # except:
                #   self.view.display_error ("Initial guess (x0) is required for Secant method")
                #   return
                params.x0 = self.x0_var.get()
                params.derivative_equation = self.derivative_var.get().strip()
            
            if params.method == "Modified Newton-Raphson":
                params.multiplicity = self.multiplicity_var.get()
            
            if params.method == "Secant":
                # try:
                #   params.x0 = self.x0_var.get()
                # except:
                #   self.view.display_error ("Initial guess (x0) is required for Secant method")
                #   return
                # try:
                #   params.x1 = self.x1_var.get()
                # except:
                #   self.view.display_error ("Initial guess (x1) is required for Secant method")
                #   return
                params.x0 = self.x0_var.get()
                params.x1 = self.x1_var.get()
            
            # Common parameters
            params.max_iterations = self.max_iterations_var.get()
            params.epsilon = self.epsilon_var.get()
            params.significant_figures = self.sig_figs_var.get()
            params.step_by_step = self.step_by_step_var.get()
            
            # Set global significant figures
            set_sig_figs(params.significant_figures)
            
            # Validate inputs
            if not params.equation:
                self.view.display_error("Please enter an equation")
                return
            
            if params.method in ["Bisection", "False-Position"] and params.xl >= params.xu:
                self.view.display_error("Lower bound (Xl) must be less than upper bound (Xu)")
                return
            
            # Solve using the orchestrator
            result = solve_root(params)
            
            # Display results
            if result.error_message and not result.root:
                self.view.display_error(result.error_message)
            else:
                self.view.display_result(result)
                
        except Exception as e:
            self.view.display_error(f"Error: {str(e)}")
    
    def plot_function(self):
        try:
            equation = self.equation_var.get().strip()
            if not equation:
                self.view.display_error("Please enter an equation first")
                return
            
            method = self.method_var.get()
            
            # Get appropriate range based on method
            if method in ["Bisection", "False-Position"]:
                xl = self.xl_var.get()
                xu = self.xu_var.get()
                self.view.plot_equation(equation, xl, xu, method)
            else:
                x0 = self.x0_var.get()
                # Use a range around x0
                xl = x0 - 5
                xu = x0 + 5
                
                # For Fixed Point, also pass g(x)
                g_eq = self.g_equation_var.get().strip() if method == "Fixed Point" else None
                self.view.plot_equation(equation, xl, xu, method, g_equation=g_eq)
            
        except Exception as e:
            self.view.display_error(f"Error plotting: {str(e)}")
    
    def get_available_methods(self):
        return get_available_methods()