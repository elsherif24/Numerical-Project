from D import D
from utils.matrixChecks import isDiagonallyDominant, isSymmetricPositiveDefinite
from utils.stepRecorder import copyVector


def gaussSeidel(a, b, n, initialGuess, recorder, maxIterations=100, absRelError=None):
    if recorder.isEnabled():
        recorder.record("initial", "Initial system and guess", vectorX=copyVector(initialGuess), iteration=0, )

    diagonallyDominant = isDiagonallyDominant(a, n)
    spd = isSymmetricPositiveDefinite(a, n)

    if not diagonallyDominant and not spd:
        if recorder.isEnabled():
            recorder.record("warning",
                            "Warning: Matrix is neither diagonally dominant nor SPD - method may not converge", )

    x = initialGuess[:]
    iteration = 0

    while iteration < maxIterations:
        xOld = x[:]
        iteration += 1

        for i in range(n):
            sumBefore = sum(a[i][j] * x[j] for j in range(i))
            sumAfter = sum(a[i][j] * xOld[j] for j in range(i + 1, n))
            x[i] = (b[i] - sumBefore - sumAfter) / a[i][i]

        if recorder.isEnabled():
            recorder.record("iteration", f"Iteration {iteration}", vectorX=copyVector(x), iteration=iteration, )

        if absRelError is not None:
            if checkConvergence(x, xOld, n, absRelError, recorder):
                break

    return x, iteration


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
