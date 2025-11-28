from D import D
from utils.matrixChecks import isDiagonallyDominant, isSymmetricPositiveDefinite
from utils.stepRecorder import copyVector


def gaussSeidel(a, b, n, initialGuess, recorder, maxIterations=100, absRelError=1e-6):
    warning_message = None

    diagonallyDominant = isDiagonallyDominant(a, n)
    spd = isSymmetricPositiveDefinite(a, n)

    if not diagonallyDominant and not spd:
        warning_message = "Warning: Matrix is neither diagonally dominant nor SPD - method may not converge"
        if recorder.isEnabled():
            recorder.record("warning", warning_message)

    x = initialGuess[:]
    iteration = 0
    converged = False

    while iteration < maxIterations:
        xOld = x[:]
        iteration += 1

        for i in range(n):
            sumBefore = sum(a[i][j] * x[j] for j in range(i))
            sumAfter = sum(a[i][j] * xOld[j] for j in range(i + 1, n))
            x[i] = (b[i] - sumBefore - sumAfter) / a[i][i]

        # Calculate error for this iteration
        error = calculateError(x, xOld, n)

        if recorder.isEnabled():
            recorder.record(
                "iteration",
                f"Iteration {iteration}",
                vectorX=copyVector(x),
                iteration=iteration,
            )
            recorder.record(
                "error", f"Error = {error}", error=error, threshold=absRelError
            )

        # Check convergence condition
        if error < absRelError:
            converged = True
            break

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
