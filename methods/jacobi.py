from D import D
from utils.matrixChecks import isDiagonallyDominant
from utils.stepRecorder import copyVector


def jacobi(a, b, n, initialGuess, recorder, maxIterations=100, absRelError=1e-6):
    for i in range(n):
        if a[i][i].isNearZero():
            raise ValueError(
                f"Error: Zero diagonal element at position ({i + 1}, {i + 1}) - Jacobi method requires non-zero diagonal elements"
            )

    warning_message = None

    if isDiagonallyDominant(a, n):
        warning_message = "Matrix is diagonally dominant - method should converge"
        if recorder.isEnabled():
            recorder.record("info", warning_message)
    else:
        warning_message = (
            "Warning: Matrix is not diagonally dominant - method may not converge"
        )
        if recorder.isEnabled():
            recorder.record("warning", warning_message)

    x = initialGuess[:]
    xNew = [D.zero() for _ in range(n)]
    iteration = 0

    converged = False

    while iteration < maxIterations:
        iteration += 1

        for i in range(n):
            sumValue = sum(a[i][j] * x[j] for j in range(n) if j != i)
            xNew[i] = (b[i] - sumValue) / a[i][i]

        # Calculate error for this iteration
        error = calculateError(xNew, x, n)

        if recorder.isEnabled():
            recorder.record(
                "iteration",
                f"Iteration {iteration}",
                vectorX=copyVector(xNew),
                iteration=iteration,
            )
            recorder.record(
                "error", f"Error = {error}", error=error, threshold=absRelError
            )

        # Check convergence condition
        if error < absRelError:
            x = xNew[:]
            converged = True
            break

        x = xNew[:]

    if recorder.isEnabled():
        if converged:
            recorder.record("convergence", "Solution converged successfully")
        else:
            recorder.record(
                "convergence",
                f"Solution did not converge after {maxIterations} iterations",
            )

    return x, iteration, converged, warning_message


def calculateError(xNew, xOld, n):
    maxError = D.zero()
    for i in range(n):
        if not xNew[i].isNearZero():
            error = abs((xNew[i] - xOld[i]) / xNew[i])
            if error > maxError:
                maxError = error
    return maxError
