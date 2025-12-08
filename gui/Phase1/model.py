from typing import Optional

import numpy as np


class LinearSolverModel:
    def __init__(self):
        self.num_vars = 3
        self.sig_figs = 7
        self.scaling_enabled = False
        self.step_by_step = False

        self.method = "Gauss Elimination"
        self.lu_form = "Doolittle"

        self.max_iterations = 100
        self.abs_error = 1e-6

        self.matrix_A: Optional[np.ndarray] = None
        self.vector_b: Optional[np.ndarray] = None
        self.initial_guess: Optional[np.ndarray] = None

        self.solution: Optional[np.ndarray] = None
        self.L_matrix: Optional[np.ndarray] = None
        self.U_matrix: Optional[np.ndarray] = None
        self.iterations: Optional[int] = None
        self.converged: Optional[bool] = None
        self.execution_time: Optional[float] = None
        self.steps = []
        self.warning_message: Optional[str] = None

    def set_matrix_data(self, A: np.ndarray, b: np.ndarray):
        self.matrix_A = A
        self.vector_b = b

    def set_initial_guess(self, x0: np.ndarray):
        self.initial_guess = x0

    def set_solution(
        self,
        solution: np.ndarray,
        execution_time: float,
        iterations: Optional[int] = None,
        converged: Optional[bool] = None,
    ):
        self.solution = solution
        self.execution_time = execution_time
        self.iterations = iterations
        self.converged = converged

    def set_lu_matrices(self, L: np.ndarray, U: np.ndarray):
        self.L_matrix = L
        self.U_matrix = U

    def clear_results(self):
        self.solution = None
        self.L_matrix = None
        self.U_matrix = None
        self.iterations = None
        self.converged = None
        self.execution_time = None
        self.steps = []
        self.warning_message = None

    def get_method_requires_scaling(self) -> bool:
        return self.method in ["Gauss Elimination", "Gauss-Jordan", "LU Decomposition"]

    def get_method_is_iterative(self) -> bool:
        return self.method in ["Jacobi", "Gauss-Seidel"]

    def get_method_is_lu(self) -> bool:
        return self.method == "LU Decomposition"
