"""
Model - Application State and Data
Stores all application state and provides methods to access/modify it.
"""

from typing import Optional

import numpy as np


class LinearSolverModel:
    """Model class storing application state"""

    def __init__(self):
        # Configuration
        self.num_vars = 3
        self.sig_figs = 7
        self.scaling_enabled = False
        self.step_by_step = False

        # Method selection
        self.method = "Gauss Elimination"
        self.lu_form = "Doolittle"

        # Iterative method parameters
        self.max_iterations = 100
        self.abs_error = 1e-6

        # Data
        self.matrix_A: Optional[np.ndarray] = None
        self.vector_b: Optional[np.ndarray] = None
        self.initial_guess: Optional[np.ndarray] = None

        # Results
        self.solution: Optional[np.ndarray] = None
        self.L_matrix: Optional[np.ndarray] = None
        self.U_matrix: Optional[np.ndarray] = None
        self.iterations: Optional[int] = None
        self.converged: Optional[bool] = (
            None  # None for non-iterative, True/False for iterative
        )
        self.execution_time: Optional[float] = None
        self.steps = []
        self.warning_message: Optional[str] = None

    def set_matrix_data(self, A: np.ndarray, b: np.ndarray):
        """Store matrix and constant vector"""
        self.matrix_A = A
        self.vector_b = b

    def set_initial_guess(self, x0: np.ndarray):
        """Store initial guess for iterative methods"""
        self.initial_guess = x0

    def set_solution(
        self,
        solution: np.ndarray,
        execution_time: float,
        iterations: Optional[int] = None,
        converged: Optional[bool] = None,
    ):
        """Store solution and statistics"""
        self.solution = solution
        self.execution_time = execution_time
        self.iterations = iterations
        self.converged = converged

    def set_lu_matrices(self, L: np.ndarray, U: np.ndarray):
        """Store L and U matrices for LU decomposition"""
        self.L_matrix = L
        self.U_matrix = U

    def clear_results(self):
        """Clear previous results"""
        self.solution = None
        self.L_matrix = None
        self.U_matrix = None
        self.iterations = None
        self.converged = None
        self.execution_time = None
        self.steps = []
        self.warning_message = None

    def get_method_requires_scaling(self) -> bool:
        """Check if current method supports scaling"""
        return self.method in ["Gauss Elimination", "Gauss-Jordan", "LU Decomposition"]

    def get_method_is_iterative(self) -> bool:
        """Check if current method is iterative"""
        return self.method in ["Jacobi", "Gauss-Seidel"]

    def get_method_is_lu(self) -> bool:
        """Check if current method is LU decomposition"""
        return self.method == "LU Decomposition"
