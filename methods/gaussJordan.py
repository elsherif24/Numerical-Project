from D import D
from methods.gaussElimination import forwardElimination
from utils.pivoting import computeScaleFactors
from utils.stepRecorder import createAugmentedMatrix


def gaussJordan(a, b, n, scalingEnabled, recorder):
    if recorder.isEnabled():
        augmented = createAugmentedMatrix(a, b)
        recorder.record("initial", "Initial augmented matrix", augmented=augmented)

    scalers = computeScaleFactors(a, n) if scalingEnabled else None

    forwardElimination(a, b, n, scalers, recorder)

    backwardElimination(a, b, n, recorder)

    return b


def backwardElimination(a, b, n, recorder):
    for k in range(n - 1, -1, -1):
        pivot = a[k][k]
        a[k][k] = D.one()

        for col in range(k + 1, n):
            a[k][col] /= pivot
        b[k] /= pivot

        if recorder.isEnabled():
            augmented = createAugmentedMatrix(a, b)
            recorder.record("normalize", f"R{k + 1} = R{k + 1} / {pivot}", augmented=augmented, )

        for row in range(k - 1, -1, -1):
            eliminateRowBackward(a, b, k, row, n, recorder)


def eliminateRowBackward(a, b, pivotRow, targetRow, n, recorder):
    multiplier = a[targetRow][pivotRow]
    a[targetRow][pivotRow] = D.zero()

    for col in range(pivotRow + 1, n):
        a[targetRow][col] -= multiplier * a[pivotRow][col]

    b[targetRow] -= multiplier * b[pivotRow]

    if recorder.isEnabled():
        augmented = createAugmentedMatrix(a, b)
        recorder.record("backward_elimination", f"R{targetRow + 1} = R{targetRow + 1} - ({multiplier})R{pivotRow + 1}",
            augmented=augmented, )
