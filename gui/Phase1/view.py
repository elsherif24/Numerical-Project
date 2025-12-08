import customtkinter as ctk

from D import get_sig_figs
from gui.Phase1.input_section import create_input_config_section, generate_matrix_inputs
from gui.Phase1.method_section import (
    create_method_section,
    create_parameter_widgets,
    generate_initial_guess_inputs,
)
from gui.Phase1.output_section import create_output_section


class LinearSolverView:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller

        self.matrix_scroll = None
        self.output_text = None
        self.scaling_checkbox = None
        self.params_container = None

        self.lu_frame = None
        self.iterative_frame = None
        self.initial_guess_container = None

        self.coefficient_entries = []
        self.constant_entries = []
        self.initial_guess_entries = []
        self.current_steps = []

        self.lu_form = None

    def build_ui(self):
        main_container = ctk.CTkFrame(self.root, fg_color="#1a1a1a")
        main_container.pack(fill="both", expand=True, padx=10, pady=10)

        col1 = ctk.CTkFrame(
            main_container, fg_color=("#2b2b2b", "#1f1f1f"), corner_radius=10
        )
        col1.pack(side="left", fill="both", expand=True, padx=(0, 5))

        col2 = ctk.CTkFrame(
            main_container, fg_color=("#2b2b2b", "#1f1f1f"), corner_radius=10
        )
        col2.pack(side="left", fill="both", expand=True, padx=(5, 0))

        input_row = ctk.CTkFrame(col1, fg_color="transparent", height=500)
        input_row.pack(fill="both", expand=True, pady=(0, 5))
        input_row.pack_propagate(False)

        method_row = ctk.CTkFrame(col1, fg_color="transparent", height=500)
        method_row.pack(fill="both", pady=(5, 0))
        method_row.pack_propagate(False)

        create_input_config_section(input_row, self)
        create_method_section(method_row, self)
        create_output_section(col2, self)

        create_parameter_widgets(self)

        self.generate_matrix_inputs()

    def generate_matrix_inputs(self):
        generate_matrix_inputs(self)

    def generate_initial_guess_inputs(self):
        generate_initial_guess_inputs(self)

    def display_output(self, model):
        self.output_text.delete("1.0", "end")

        self.output_text.insert("end", f"Method: {model.method}\n")
        self.output_text.insert("end", "=" * 70 + "\n\n")

        if model.warning_message:
            self.output_text.insert("end", f"{model.warning_message}\n\n")

        if model.step_by_step and model.steps:
            self.current_steps = model.steps
            self.display_steps(model.steps)
            self.output_text.insert("end", "\n" + "=" * 70 + "\n\n")

        if model.L_matrix is not None and model.U_matrix is not None:
            self.output_text.insert("end", "L Matrix:\n")
            self.display_aligned_matrix(model.L_matrix)

            self.output_text.insert("end", "\nU Matrix:\n")
            self.display_aligned_matrix(model.U_matrix)

            self.output_text.insert("end", "\n")

        if model.solution is not None:
            self.output_text.insert("end", "Solution:\n")
            for i, val in enumerate(model.solution):
                self.output_text.insert("end", f"  x{i + 1} = {val}\n")

            self.output_text.insert(
                "end", f"\nExecution Time: {model.execution_time:.6f} seconds\n"
            )

            if model.iterations is not None:
                self.output_text.insert("end", f"Iterations: {model.iterations}\n")

                if model.converged is not None:
                    status = (
                        "CONVERGED"
                        if model.converged
                        else "DIVERGED (Max iterations reached)"
                    )
                    self.output_text.insert("end", f"Status: {status}\n")

    def display_steps(self, steps):
        self.output_text.insert("end", "STEP-BY-STEP SOLUTION\n\n")

        for step in steps:
            if step.operation == "iteration":
                iteration_num = step.data.get("iteration", 0)
                self.output_text.insert("end", f"Iteration {iteration_num}:\n")
                if "vectorX" in step.data:
                    self.display_iteration_vector(step.data["vectorX"])
                continue

            if step.operation == "error":
                if "error" in step.data:
                    self.output_text.insert(
                        "end", f"Absolute Relative Error = {step.data['error']}\n\n"
                    )
                continue

            if step.operation == "convergence":
                self.output_text.insert("end", f"{step.description}\n\n")
                continue

            if step.operation == "warning":
                self.output_text.insert("end", f"{step.description}\n\n")
                continue

            if step.operation == "validation":
                self.output_text.insert("end", f"✓ {step.description}\n\n")
                continue

            if step.operation == "info":
                self.output_text.insert("end", f"{step.description}\n\n")
                continue

            self.output_text.insert(
                "end", f"Step {step.stepNumber}: {step.description}\n"
            )

            if "augmented" in step.data:
                self.display_augmented_matrix(step.data["augmented"])

            if "matrixA" in step.data:
                self.display_matrix("A", step.data["matrixA"])

            if "matrixL" in step.data and "matrixU" in step.data:
                self.display_lu_matrices_combined(
                    step.data["matrixL"], step.data["matrixU"]
                )
            elif "matrixL" in step.data:
                self.display_matrix("L", step.data["matrixL"])
            elif "matrixU" in step.data:
                self.display_matrix("U", step.data["matrixU"])

            if "vectorB" in step.data:
                self.display_vector("b", step.data["vectorB"])

            if "vectorY" in step.data:
                self.display_vector("y", step.data["vectorY"])

            if "vectorX" in step.data and step.operation not in ["iteration", "error"]:
                self.display_vector("x", step.data["vectorX"])

            self.output_text.insert("end", "\n")

    def display_lu_matrices_combined(self, L, U):
        if not L or not U:
            return

        col_width = get_sig_figs() + 7

        str_L = [[str(elem) for elem in row] for row in L]
        str_U = [[str(elem) for elem in row] for row in U]

        self.output_text.insert("end", "  L Matrix:\n")
        for row in str_L:
            row_str = "    "
            for val in row:
                row_str += val.rjust(col_width) + "  "
            self.output_text.insert("end", row_str + "\n")

        self.output_text.insert("end", "\n  U Matrix:\n")
        for row in str_U:
            row_str = "    "
            for val in row:
                row_str += val.rjust(col_width) + "  "
            self.output_text.insert("end", row_str + "\n")

    def display_augmented_matrix(self, aug_matrix):
        if not aug_matrix:
            return

        n_cols = len(aug_matrix[0])
        col_width = get_sig_figs() + 7

        str_matrix = [[str(elem) for elem in row] for row in aug_matrix]

        for row in str_matrix:
            row_str = "  "
            for col_idx in range(n_cols - 1):
                row_str += row[col_idx].rjust(col_width) + "  "
            row_str += "| "
            row_str += row[-1].rjust(col_width)
            self.output_text.insert("end", row_str + "\n")

    def display_matrix(self, name, matrix):
        if not matrix:
            return

        col_width = get_sig_figs() + 7
        self.output_text.insert("end", f"  {name} =\n")

        for row in matrix:
            row_str = "    "
            for val in row:
                row_str += str(val).rjust(col_width) + "  "
            self.output_text.insert("end", row_str + "\n")

    def display_aligned_matrix(self, matrix):
        if not matrix:
            return

        col_width = get_sig_figs() + 7

        for row in matrix:
            row_str = "  "
            for val in row:
                row_str += str(val).rjust(col_width) + "  "
            self.output_text.insert("end", row_str + "\n")

    def display_vector(self, name, vector):
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
        self.output_text.insert("end", "x = [")
        for i, val in enumerate(vector):
            if i > 0:
                self.output_text.insert("end", ", ")
            self.output_text.insert("end", str(val))
        self.output_text.insert("end", "]\n")

    def display_output_with_error(self, model, error_message: str):
        self.output_text.delete("1.0", "end")

        self.output_text.insert("end", f"Method: {model.method}\n")
        self.output_text.insert("end", "=" * 70 + "\n\n")

        if model.step_by_step and model.steps:
            self.current_steps = model.steps
            self.display_steps(model.steps)
            self.output_text.insert("end", "\n" + "=" * 70 + "\n\n")

        self.output_text.insert("end", "ERROR OCCURRED:\n")
        self.output_text.insert("end", f"{error_message}\n")

    def display_error(self, error_message: str):
        self.output_text.delete("1.0", "end")
        self.output_text.insert("end", f"Error: {error_message}\n")

    def update_method_ui(self, model):
        self.lu_frame.pack_forget()
        self.iterative_frame.pack_forget()

        if model.get_method_requires_scaling():
            if model.get_method_is_lu():
                self.lu_frame.pack(fill="x", pady=5)
                self.update_lu_form_ui(model.lu_form)
            else:
                self.scaling_checkbox.configure(state="normal")
        else:
            self.scaling_checkbox.configure(state="disabled")

        if model.get_method_is_iterative():
            self.iterative_frame.pack(fill="x", pady=5)
            self.generate_initial_guess_inputs()

    def update_lu_form_ui(self, lu_form: str):
        if lu_form == "Doolittle":
            self.scaling_checkbox.configure(state="normal")
        else:
            self.scaling_checkbox.configure(state="disabled")
