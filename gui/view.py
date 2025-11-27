"""
View - UI Layer
Handles all UI creation and display, no business logic.
"""

import customtkinter as ctk

from D import get_sig_figs
from gui.input_section import create_input_config_section, generate_matrix_inputs
from gui.method_section import (create_method_section, create_parameter_widgets, generate_initial_guess_inputs, )
from gui.output_section import create_output_section


class LinearSolverView:
    """View class handling UI display"""

    def __init__(self, root, controller):
        self.root = root
        self.controller = controller

        # UI references
        self.matrix_scroll = None
        self.output_text = None
        self.scaling_checkbox = None
        self.params_container = None

        # Parameter frames
        self.lu_frame = None
        self.iterative_frame = None
        self.initial_guess_container = None

        # Entry storage
        self.coefficient_entries = []
        self.constant_entries = []
        self.initial_guess_entries = []

        # Tkinter variables will be bound from outside before build_ui() is called
        self.lu_form = None

    def build_ui(self):
        """Build the entire UI"""
        # Main container
        main_container = ctk.CTkFrame(self.root, fg_color="#1a1a1a")
        main_container.pack(fill="both", expand=True, padx=10, pady=10)

        # Create 2 columns
        col1 = ctk.CTkFrame(main_container, fg_color=("#2b2b2b", "#1f1f1f"), corner_radius=10)
        col1.pack(side="left", fill="both", expand=True, padx=(0, 5))

        col2 = ctk.CTkFrame(main_container, fg_color=("#2b2b2b", "#1f1f1f"), corner_radius=10)
        col2.pack(side="left", fill="both", expand=True, padx=(5, 0))

        # Split column 1 into two rows
        # Row 1: Input Configuration - Set height and disable propagate
        input_row = ctk.CTkFrame(col1, fg_color="transparent", height=500)
        input_row.pack(fill="both", expand=True, pady=(0, 5))
        input_row.pack_propagate(False)  # Disable to respect height parameter

        # Row 2: Method Configuration - Set height and disable propagate
        method_row = ctk.CTkFrame(col1, fg_color="transparent", height=500)
        method_row.pack(fill="both", pady=(5, 0))
        method_row.pack_propagate(False)  # Keep fixed height

        # Build sections
        create_input_config_section(input_row, self)
        create_method_section(method_row, self)
        create_output_section(col2, self)

        # Initialize parameter widgets
        create_parameter_widgets(self)

        # Generate initial matrix
        self.generate_matrix_inputs()

    def generate_matrix_inputs(self):
        """Delegate to component function"""
        generate_matrix_inputs(self)

    def generate_initial_guess_inputs(self):
        """Delegate to component function"""
        generate_initial_guess_inputs(self)

    def display_output(self, model):
        """Display results from model"""
        self.output_text.delete("1.0", "end")

        self.output_text.insert("end", f"Method: {model.method}\n")
        self.output_text.insert("end", "=" * 70 + "\n\n")

        # Display step-by-step if enabled and steps exist
        if model.step_by_step and model.steps:
            self.display_steps(model.steps)
            self.output_text.insert("end", "\n" + "=" * 70 + "\n\n")

        # Display L and U matrices if available
        if model.L_matrix is not None and model.U_matrix is not None:
            self.output_text.insert("end", "L Matrix:\n")
            for row in model.L_matrix:
                formatted = "  ".join([str(v) for v in row])
                self.output_text.insert("end", f"  {formatted}\n")

            self.output_text.insert("end", "\nU Matrix:\n")
            for row in model.U_matrix:
                formatted = "  ".join([str(v) for v in row])
                self.output_text.insert("end", f"  {formatted}\n")

            self.output_text.insert("end", "\n")

        # Display solution
        if model.solution is not None:
            self.output_text.insert("end", "Solution:\n")
            for i, val in enumerate(model.solution):
                self.output_text.insert("end", f"  x{i + 1} = {val}\n")

            self.output_text.insert("end", f"\nExecution Time: {model.execution_time:.6f} seconds\n")

            if model.iterations is not None:
                self.output_text.insert("end", f"Iterations: {model.iterations}\n")

                if model.converged is not None:
                    status = ("CONVERGED" if model.converged else "DIVERGED (Max iterations reached)")
                    self.output_text.insert("end", f"Status: {status}\n")

    def display_steps(self, steps):
        """Display step-by-step solution"""
        self.output_text.insert("end", "STEP-BY-STEP SOLUTION\n\n")

        for step in steps:
            self.output_text.insert("end", f"Step {step.stepNumber}: {step.description}\n")

            if "augmented" in step.data:
                self.display_augmented_matrix(step.data["augmented"])

            if "matrix_a" in step.data:
                self.display_matrix("A", step.data["matrix_a"])

            if "matrix_L" in step.data:
                self.display_matrix("L", step.data["matrix_L"])

            if "matrix_U" in step.data:
                self.display_matrix("U", step.data["matrix_U"])

            if "vector_b" in step.data:
                self.display_vector("b", step.data["vector_b"])

            if "vector_y" in step.data:
                self.display_vector("y", step.data["vector_y"])

            if "vector_x" in step.data:
                self.display_iteration_vector(step.data["vector_x"])

            if "iteration" in step.data:
                self.output_text.insert("end", f"  Iteration: {step.data['iteration']}\n")

            if "error" in step.data:
                self.output_text.insert("end", f"  Error: {step.data['error']}\n")
                if "threshold" in step.data:
                    self.output_text.insert("end", f"  Threshold: {step.data['threshold']}\n")

            if "final_error" in step.data:
                self.output_text.insert("end", f"  Final Error: {step.data['final_error']}\n")

            self.output_text.insert("end", "\n")

    def display_augmented_matrix(self, aug_matrix):
        """Display augmented matrix with proper alignment and separator"""
        if not aug_matrix:
            return

        n_cols = len(aug_matrix[0])

        # Use width based on current significant figures setting + padding
        col_width = get_sig_figs() + 7

        # Convert all elements to strings
        str_matrix = [[str(elem) for elem in row] for row in aug_matrix]

        # Display each row with alignment
        for row_idx, row in enumerate(str_matrix):
            row_str = "  "

            # Display A matrix columns
            for col_idx in range(n_cols - 1):
                row_str += row[col_idx].rjust(col_width) + "  "

            # Add separator before b vector
            row_str += "| "

            # Display b vector (last column)
            row_str += row[-1].rjust(col_width)

            self.output_text.insert("end", row_str + "\n")

    def display_matrix(self, name, matrix):
        """Display a matrix with proper formatting"""
        if not matrix:
            return

        col_width = get_sig_figs() + 7
        self.output_text.insert("end", f"  {name} =\n")

        for row in matrix:
            row_str = "    "
            for val in row:
                row_str += str(val).rjust(col_width) + "  "
            self.output_text.insert("end", row_str + "\n")

    def display_vector(self, name, vector):
        """Display a vector with proper formatting"""
        if not vector:
            return

        col_width = get_sig_figs() + 5
        self.output_text.insert("end", f"  {name} = [ ")
        for i, val in enumerate(vector):
            if i > 0:
                self.output_text.insert("end", ", ")
            self.output_text.insert("end", str(val).rjust(col_width))
        self.output_text.insert("end", " ]\n")

    def display_iteration_vector(self, vector):
        """Display iteration vector for iterative methods"""
        col_width = get_sig_figs() + 5
        self.output_text.insert("end", "  x = [ ")
        for i, val in enumerate(vector):
            if i > 0:
                self.output_text.insert("end", ", ")
            self.output_text.insert("end", str(val).rjust(col_width))
        self.output_text.insert("end", " ]\n")

    def display_error(self, error_message: str):
        """Display error message"""
        self.output_text.delete("1.0", "end")
        self.output_text.insert("end", f"Error: {error_message}\n")

    def update_method_ui(self, model):
        """Update UI based on method selection"""
        # Hide all parameter frames
        self.lu_frame.pack_forget()
        self.iterative_frame.pack_forget()

        # Update scaling checkbox
        if model.get_method_requires_scaling():
            if model.get_method_is_lu():
                self.lu_frame.pack(fill="x", pady=5)
                # Update scaling based on current LU form
                self.update_lu_form_ui(model.lu_form)
            else:
                # For Gauss Elimination and Gauss-Jordan, enable scaling
                self.scaling_checkbox.configure(state="normal")
        else:
            self.scaling_checkbox.configure(state="disabled")

        # Show iterative parameters
        if model.get_method_is_iterative():
            self.iterative_frame.pack(fill="x", pady=5)
            self.generate_initial_guess_inputs()

    def update_lu_form_ui(self, lu_form: str):
        """Update scaling checkbox based on LU form selection"""
        if lu_form == "Doolittle":
            # Doolittle supports scaling
            self.scaling_checkbox.configure(state="normal")
        else:
            # Crout and Cholesky do not support scaling
            self.scaling_checkbox.configure(state="disabled")
