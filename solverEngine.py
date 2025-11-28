import time

from D import D, set_sig_figs
from methods.gaussElimination import gaussElimination
from methods.gaussJordan import gaussJordan
from methods.gaussSeidel import gaussSeidel
from methods.jacobi import jacobi
from methods.luCholesky import luCholesky
from methods.luCrout import luCrout
from methods.luDoolittle import luDoolittle
from utils.stepRecorder import StepRecorder


class SolverParameters:
    def __init__(self):
        self.coefficient_matrix = None
        self.constant_vector = None
        self.num_variables = 0
        self.significant_figures = 7
        self.selected_method = ""
        self.scaling_enabled = False
        self.step_by_step_mode = False
        self.lu_form = "Doolittle"
        self.initial_guess = None
        self.max_iterations = 100
        self.absolute_relative_error = 1e-6


class SolverResult:
    def __init__(self):
        self.solution = []
        self.execution_time = 0.0
        self.iterations = 0
        self.converged = None
        self.L_matrix = None
        self.U_matrix = None
        self.error_message = ""
        self.warning_message = ""
        self.steps = []


def solve(params: SolverParameters) -> SolverResult:
    result = SolverResult()

    set_sig_figs(params.significant_figures)

    a = D.from_matrix(params.coefficient_matrix)
    b = D.from_vector(params.constant_vector)

    recorder = StepRecorder(enabled=params.step_by_step_mode)

    try:
        start_time = time.time()

        if params.selected_method == "Gauss Elimination":
            result.solution = gaussElimination(
                a, b, params.num_variables, params.scaling_enabled, recorder
            )

        elif params.selected_method == "Gauss-Jordan":
            result.solution = gaussJordan(
                a, b, params.num_variables, params.scaling_enabled, recorder
            )

        elif params.selected_method == "LU Decomposition":
            if params.lu_form == "Doolittle":
                result.solution, result.L_matrix, result.U_matrix = luDoolittle(
                    a, b, params.num_variables, params.scaling_enabled, recorder
                )
            elif params.lu_form == "Crout":
                result.solution, result.L_matrix, result.U_matrix = luCrout(
                    a, b, params.num_variables, recorder
                )
            elif params.lu_form == "Cholesky":
                (
                    result.solution,
                    result.L_matrix,
                    result.U_matrix,
                    result.warning_message,
                ) = luCholesky(a, b, params.num_variables, recorder)
            else:
                raise ValueError(f"Unknown LU form: {params.lu_form}")

        elif params.selected_method == "Jacobi":
            x0 = D.from_vector(params.initial_guess)
            (
                result.solution,
                result.iterations,
                result.converged,
                result.warning_message,
            ) = jacobi(
                a,
                b,
                params.num_variables,
                x0,
                recorder,
                maxIterations=params.max_iterations,
                absRelError=params.absolute_relative_error,
            )

        elif params.selected_method == "Gauss-Seidel":
            x0 = D.from_vector(params.initial_guess)
            (
                result.solution,
                result.iterations,
                result.converged,
                result.warning_message,
            ) = gaussSeidel(
                a,
                b,
                params.num_variables,
                x0,
                recorder,
                maxIterations=params.max_iterations,
                absRelError=params.absolute_relative_error,
            )

        else:
            raise ValueError(f"Unknown method: {params.selected_method}")

        result.execution_time = time.time() - start_time
        result.steps = recorder.getSteps()

    except Exception as e:
        result.error_message = str(e)
        result.execution_time = 0.0
        result.steps = recorder.getSteps()

    return result
