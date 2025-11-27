"""
Controller - Business Logic Layer
Coordinates between Model and View, handles user actions.
Updated to use solver_engine for method dispatch.
"""

import customtkinter as ctk

from gui.input_handlers import get_initial_guess, get_matrix_and_constants
from gui.model import LinearSolverModel
from solverEngine import SolverParameters
from solverEngine import solve as solve_system


class LinearSolverController:
    """Controller class handling business logic"""

    def __init__(self):
        self.model = LinearSolverModel()
        self.view = None

        # Tkinter variables (needed for UI binding)
        self.num_vars_var = None
        self.sig_figs_var = None
        self.scaling_var = None
        self.step_by_step_var = None
        self.method_var = None
        self.lu_form_var = None
        self.max_iterations_var = None
        self.abs_error_var = None

    def initialize_tk_variables(self):
        """Initialize Tkinter variables"""
        self.num_vars_var = ctk.IntVar(value=self.model.num_vars)
        self.sig_figs_var = ctk.IntVar(value=self.model.sig_figs)
        self.scaling_var = ctk.BooleanVar(value=self.model.scaling_enabled)
        self.step_by_step_var = ctk.BooleanVar(value=self.model.step_by_step)
        self.method_var = ctk.StringVar(value=self.model.method)
        self.lu_form_var = ctk.StringVar(value=self.model.lu_form)
        self.max_iterations_var = ctk.IntVar(value=self.model.max_iterations)
        self.abs_error_var = ctk.DoubleVar(value=self.model.abs_error)

    def set_view(self, view):
        """Set the view reference"""
        self.view = view

    def sync_model_from_ui(self):
        """Sync model from UI variables"""
        self.model.num_vars = self.num_vars_var.get()
        self.model.sig_figs = self.sig_figs_var.get()
        self.model.scaling_enabled = self.scaling_var.get()
        self.model.step_by_step = self.step_by_step_var.get()
        self.model.method = self.method_var.get()
        self.model.lu_form = self.lu_form_var.get()
        self.model.max_iterations = self.max_iterations_var.get()
        self.model.abs_error = self.abs_error_var.get()

    def on_method_change(self, choice):
        """Handle method selection change"""
        self.model.method = choice
        self.view.update_method_ui(self.model)

    def on_lu_form_change(self, choice):
        """Handle LU form selection change"""
        self.model.lu_form = choice
        self.view.update_lu_form_ui(choice)

    def solve(self):
        """Main solve operation - uses solver_engine"""
        # Sync UI to model
        self.sync_model_from_ui()

        # Extract data from UI
        A, b = get_matrix_and_constants(self.view)
        if A is None or b is None:
            return

        # Prepare parameters for solver engine
        params = SolverParameters()
        params.coefficient_matrix = A
        params.constant_vector = b
        params.num_variables = self.model.num_vars
        params.significant_figures = self.model.sig_figs
        params.selected_method = self.model.method
        params.scaling_enabled = self.model.scaling_enabled
        params.step_by_step_mode = self.model.step_by_step
        params.lu_form = self.model.lu_form
        params.max_iterations = self.model.max_iterations
        params.absolute_relative_error = self.model.abs_error

        # Get initial guess for iterative methods
        if self.model.get_method_is_iterative():
            x0 = get_initial_guess(self.view)
            if x0 is None:
                return
            params.initial_guess = x0

        # Call solver engine (pure logic, no GUI)
        result = solve_system(params)

        # Update model with results
        self.model.clear_results()
        if result.error_message:
            self.view.display_error(result.error_message)
        else:
            self.model.set_solution(result.solution, result.execution_time, result.iterations, result.converged, )
            if result.L_matrix is not None:
                self.model.set_lu_matrices(result.L_matrix, result.U_matrix)
            self.model.steps = result.steps
            self.view.display_output(self.model)
