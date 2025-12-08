import customtkinter as ctk
from solverEngine2.phase2_solver import RootFinderParameters, solve_root
from D import set_sig_figs


class Phase2Controller:
    def __init__(self):
        self.view = None
        
        # Tkinter variables
        self.equation_var = None
        self.method_var = None
        self.xl_var = None
        self.xu_var = None
        self.max_iterations_var = None
        self.epsilon_var = None
        self.sig_figs_var = None
        self.step_by_step_var = None
        
    def initialize_tk_variables(self):
        self.equation_var = ctk.StringVar(value="x^3 - x - 2")
        self.method_var = ctk.StringVar(value="Bisection")
        self.xl_var = ctk.DoubleVar(value=1.0)
        self.xu_var = ctk.DoubleVar(value=2.0)
        self.max_iterations_var = ctk.IntVar(value=50)
        self.epsilon_var = ctk.DoubleVar(value=0.00001)
        self.sig_figs_var = ctk.IntVar(value=5)
        self.step_by_step_var = ctk.BooleanVar(value=False)

    def set_view(self, view):
        self.view = view
    
    def solve(self):
        try:
            # Get parameters
            params = RootFinderParameters()
            params.equation = self.equation_var.get().strip()
            params.method = self.method_var.get()
            params.xl = self.xl_var.get()
            params.xu = self.xu_var.get()
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
            
            if params.xl >= params.xu:
                self.view.display_error("Lower bound (Xl) must be less than upper bound (Xu)")
                return
            
            # Solve
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
            
            xl = self.xl_var.get()
            xu = self.xu_var.get()
            
            self.view.plot_equation(equation, xl, xu)
            
        except Exception as e:
            self.view.display_error(f"Error plotting: {str(e)}")