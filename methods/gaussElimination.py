from D import D
from utils.pivoting import computeScaleFactors, findPivotRow, swapRows, swapScalers
from utils.stepRecorder import createAugmentedMatrix


def gaussElimination(a, b, n, scalingEnabled, recorder):
    if recorder.isEnabled():
        augmented = createAugmentedMatrix(a, b)
        recorder.record("initial", "Initial augmented matrix", augmented=augmented)

    scalers = computeScaleFactors(a, n) if scalingEnabled else None

    forwardElimination(a, b, n, scalers, recorder)

    x = substitution(a, b, n)

    return x


def ensureNonSingularPivot(a, k, scalers):
    if scalers is None:
        if a[k][k].isNearZero():
            raise ValueError(f"Matrix is singular: zero pivot encountered at row {k + 1}")
    else:
        if (a[k][k] / scalers[k]).isNearZero():
            raise ValueError(f"Matrix is singular: zero pivot encountered at row {k + 1}")


def forwardElimination(a, b, n, scalers, recorder):
    for k in range(n - 1):
        pivoting(a, b, k, n, scalers, recorder)
        ensureNonSingularPivot(a, k, scalers)

        for row in range(k + 1, n):
            eliminateRow(a, b, k, row, n, recorder)
    ensureNonSingularPivot(a, n - 1, scalers)


def pivoting(a, b, k, n, scalers, recorder):
    pivot = findPivotRow(a, k, n, scalers)

    if pivot != k:
        swapRows(a, b, k, pivot)
        swapScalers(scalers, k, pivot)

        if recorder.isEnabled():
            augmented = createAugmentedMatrix(a, b)
            recorder.record("swap", f"Swap R{k + 1} ↔ R{pivot + 1}", augmented=augmented)

    return pivot


def eliminateRow(a, b, pivotRow, targetRow, n, recorder):
    multiplier = a[targetRow][pivotRow] / a[pivotRow][pivotRow]

    a[targetRow][pivotRow] = D.zero()

    for col in range(pivotRow + 1, n):
        a[targetRow][col] -= multiplier * a[pivotRow][col]

    b[targetRow] -= multiplier * b[pivotRow]

    if recorder.isEnabled():
        augmented = createAugmentedMatrix(a, b)
        recorder.record("elimination", f"R{targetRow + 1} = R{targetRow + 1} - ({multiplier})R{pivotRow + 1}",
            augmented=augmented, )


def substitution(a, b, n):
    x = D.zeros(n)
    x[n - 1] = b[n - 1] / a[n - 1][n - 1]

    for row in range(n - 2, -1, -1):
        sumValue = sum(a[row][col] * x[col] for col in range(row + 1, n))
        x[row] = (b[row] - sumValue) / a[row][row]

    return x
