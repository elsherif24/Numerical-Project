from D import D
from utils.matrixChecks import isDiagonallyDominant
from utils.stepRecorder import copyVector


def jacobi(a, b, n, initialGuess, recorder, maxIterations=100, absRelError=1e-6):
    if recorder.isEnabled():
        recorder.record("initial", "Initial system and guess", vectorX=copyVector(initialGuess), iteration=0, )

    if not isDiagonallyDominant(a, n):
        if recorder.isEnabled():
            recorder.record("warning", "Warning: Matrix is not diagonally dominant - method may not converge", )

    x = initialGuess[:]
    xNew = [D.zero() for _ in range(n)]
    iteration = 0

    converged = False

    while iteration < maxIterations:
        iteration += 1

        for i in range(n):
            sumValue = sum(a[i][j] * x[j] for j in range(n) if j != i)
            xNew[i] = (b[i] - sumValue) / a[i][i]

        if recorder.isEnabled():
            recorder.record("iteration", f"Iteration {iteration}", vectorX=copyVector(xNew), iteration=iteration, )

        # Check convergence condition
        if checkConvergence(xNew, x, n, absRelError, recorder):
            x = xNew[:]
            converged = True
            break

        x = xNew[:]

    if recorder.isEnabled():
        if converged:
            recorder.record("convergence", "Solution converged successfully")
        else:
            recorder.record("convergence", f"Solution did not converge after {maxIterations} iterations", )

    return x, iteration, converged


def checkConvergence(xNew, xOld, n, threshold, recorder):
    error = calculateError(xNew, xOld, n)

    if recorder.isEnabled():
        recorder.record("error", f"Error = {error}", error=error, threshold=threshold)

    return error < threshold


def calculateError(xNew, xOld, n):
    maxError = D.zero()
    for i in range(n):
        if not xNew[i].isNearZero():
            error = abs((xNew[i] - xOld[i]) / xNew[i])
            if error > maxError:
                maxError = error
    return maxError
