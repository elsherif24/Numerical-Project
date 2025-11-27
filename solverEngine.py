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
        self.stopping_condition = "Max Iterations"
        self.max_iterations = 100
        self.absolute_relative_error = 1e-6


class SolverResult:
    def __init__(self):
        self.solution = []
        self.execution_time = 0.0
        self.iterations = 0
        self.L_matrix = None
        self.U_matrix = None
        self.error_message = ""
        self.steps = []


def solve(params: SolverParameters) -> SolverResult:
    result = SolverResult()

    # Set significant figures globally
    set_sig_figs(params.significant_figures)

    a = D.from_matrix(params.coefficient_matrix)
    b = D.from_vector(params.constant_vector)

    # Create step recorder with enabled flag based on step-by-step mode
    recorder = StepRecorder(enabled=params.step_by_step_mode)

    try:
        # Start timing only for actual method computation
        start_time = time.time()

        if params.selected_method == "Gauss Elimination":
            result.solution = gaussElimination(a, b, params.num_variables, params.scaling_enabled, recorder)

        elif params.selected_method == "Gauss-Jordan":
            result.solution = gaussJordan(a, b, params.num_variables, params.scaling_enabled, recorder)

        elif params.selected_method == "LU Decomposition":
            if params.lu_form == "Doolittle":
                result.solution, result.L_matrix, result.U_matrix = luDoolittle(a, b, params.num_variables,
                    params.scaling_enabled, recorder)
            elif params.lu_form == "Crout":
                result.solution, result.L_matrix, result.U_matrix = luCrout(a, b, params.num_variables, recorder)
            elif params.lu_form == "Cholesky":
                result.solution, result.L_matrix, result.U_matrix = luCholesky(a, b, params.num_variables, recorder)
            else:
                raise ValueError(f"Unknown LU form: {params.lu_form}")

        elif params.selected_method == "Jacobi":
            x0 = D.from_vector(params.initial_guess)
            absRelError = (None if params.stopping_condition == "Max Iterations" else params.absolute_relative_error)
            result.solution, result.iterations = jacobi(a, b, params.num_variables, x0, recorder,
                maxIterations=params.max_iterations, absRelError=absRelError, )

        elif params.selected_method == "Gauss-Seidel":
            x0 = D.from_vector(params.initial_guess)
            absRelError = (None if params.stopping_condition == "Max Iterations" else params.absolute_relative_error)
            result.solution, result.iterations = gaussSeidel(a, b, params.num_variables, x0, recorder,
                maxIterations=params.max_iterations, absRelError=absRelError, )

        else:
            raise ValueError(f"Unknown method: {params.selected_method}")

        # End timing after method completes
        result.execution_time = time.time() - start_time
        result.steps = recorder.getSteps()

    except Exception as e:
        result.error_message = str(e)
        result.execution_time = 0.0

    return result
