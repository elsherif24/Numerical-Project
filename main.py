"""
Main Application Entry Point
Initializes MVC components and runs the application.
"""

import customtkinter as ctk

from gui.controller import LinearSolverController
from gui.view import LinearSolverView

# Set appearance mode and color theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")


class LinearEquationSolverApp:
    """Main Application class"""

    def __init__(self, root):
        self.root = root
        self.root.title("Linear Equation Solver")
        self.root.geometry("1920x1080")

        # Initialize MVC components
        self.controller = LinearSolverController()
        self.controller.initialize_tk_variables()

        # Create view with controller reference
        self.view = LinearSolverView(root, self.controller)

        # Bind Tkinter variables to view BEFORE building UI
        self.bind_variables()

        # Set view reference in controller
        self.controller.set_view(self.view)

        # NOW build the UI with variables bound
        self.view.build_ui()

    def bind_variables(self):
        """Bind controller's Tkinter variables to view's UI needs"""
        self.view.num_vars = self.controller.num_vars_var
        self.view.sig_figs = self.controller.sig_figs_var
        self.view.scaling_enabled = self.controller.scaling_var
        self.view.step_by_step = self.controller.step_by_step_var
        self.view.method = self.controller.method_var
        self.view.lu_form = self.controller.lu_form_var
        self.view.max_iterations = self.controller.max_iterations_var
        self.view.abs_error = self.controller.abs_error_var

        # Bind methods
        self.view.generate_matrix_inputs = self.view.generate_matrix_inputs
        self.view.generate_initial_guess_inputs = (self.view.generate_initial_guess_inputs)
        self.view.on_method_change = self.controller.on_method_change
        self.view.on_lu_form_change = self.controller.on_lu_form_change
        self.view.solve_system = self.controller.solve


def main():
    root = ctk.CTk()
    _ = LinearEquationSolverApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
