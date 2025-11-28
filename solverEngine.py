import time

from D import D, set_sig_figs
from debug.systemClassifier import debugSystemType
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

    # First pass: measure execution time with steps DISABLED
    measured_time = 0.0
    first_pass_success = False

    try:
        # Create fresh matrices for first pass (no steps)
        a_timing = D.from_matrix(params.coefficient_matrix)
        b_timing = D.from_vector(params.constant_vector)
        recorder_timing = StepRecorder(enabled=False)  # Always disabled for timing

        start_time = time.time()

        # Execute method without step recording
        if params.selected_method == "Gauss Elimination":
            _ = gaussElimination(
                a_timing,
                b_timing,
                params.num_variables,
                params.scaling_enabled,
                recorder_timing,
            )

        elif params.selected_method == "Gauss-Jordan":
            _ = gaussJordan(
                a_timing,
                b_timing,
                params.num_variables,
                params.scaling_enabled,
                recorder_timing,
            )

        elif params.selected_method == "LU Decomposition":
            if params.lu_form == "Doolittle":
                _, _, _ = luDoolittle(
                    a_timing,
                    b_timing,
                    params.num_variables,
                    params.scaling_enabled,
                    recorder_timing,
                )
            elif params.lu_form == "Crout":
                _, _, _ = luCrout(
                    a_timing, b_timing, params.num_variables, recorder_timing
                )
            elif params.lu_form == "Cholesky":
                _, _, _, _ = luCholesky(
                    a_timing, b_timing, params.num_variables, recorder_timing
                )
            else:
                raise ValueError(f"Unknown LU form: {params.lu_form}")

        elif params.selected_method == "Jacobi":
            x0_timing = D.from_vector(params.initial_guess)
            _, _, _, _ = jacobi(
                a_timing,
                b_timing,
                params.num_variables,
                x0_timing,
                recorder_timing,
                maxIterations=params.max_iterations,
                absRelError=params.absolute_relative_error,
            )

        elif params.selected_method == "Gauss-Seidel":
            x0_timing = D.from_vector(params.initial_guess)
            _, _, _, _ = gaussSeidel(
                a_timing,
                b_timing,
                params.num_variables,
                x0_timing,
                recorder_timing,
                maxIterations=params.max_iterations,
                absRelError=params.absolute_relative_error,
            )

        else:
            raise ValueError(f"Unknown method: {params.selected_method}")

        measured_time = time.time() - start_time
        first_pass_success = True

    except Exception:
        # If timing pass fails, we'll handle it after the second pass attempt
        measured_time = 0.0
        first_pass_success = False

    # Second pass: execute with actual step recording settings
    a = D.from_matrix(params.coefficient_matrix)
    b = D.from_vector(params.constant_vector)
    recorder = StepRecorder(enabled=params.step_by_step_mode)

    try:
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

        # Use the measured time from the first pass
        result.execution_time = measured_time
        result.steps = recorder.getSteps()

    except Exception as e:
        result.error_message = str(e)
        result.execution_time = measured_time if first_pass_success else 0.0
        result.steps = recorder.getSteps()

        # Classify the system type when an error occurs
        try:
            system_type = debugSystemType(
                params.coefficient_matrix, params.constant_vector
            )
            result.error_message += f'\n\nThe system actually is: "{system_type}"'
        except Exception as classify_error:
            # If classification fails, just append a note
            result.error_message += (
                f"\n\n(Could not classify system type: {str(classify_error)})"
            )

    return result
