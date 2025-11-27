from D import D
from methods.luSubstitution import backwardSubstitution, forwardSubstitution
from utils.pivoting import computeScaleFactors, findPivotRow, swapRows, swapScalers
from utils.stepRecorder import copyMatrix


def luDoolittle(a, b, n, scalingEnabled, recorder):
    if recorder.isEnabled():
        recorder.record("initial", "Initial coefficient matrix", matrixA=copyMatrix(a))

    scalers = computeScaleFactors(a, n) if scalingEnabled else None

    L = [[D.zero() for _ in range(n)] for _ in range(n)]
    U = [[D.zero() for _ in range(n)] for _ in range(n)]

    for i in range(n):
        pivotRow = findPivotRow(a, i, n, scalers)

        if pivotRow != i:
            swapRows(a, b, i, pivotRow)
            swapRows(U, [D.zero()] * n, i, pivotRow)
            swapScalers(scalers, i, pivotRow)

            for j in range(i):
                L[i][j], L[pivotRow][j] = L[pivotRow][j], L[i][j]

            if recorder.isEnabled():
                recorder.record("pivot", f"Partial pivoting: Swap R{i + 1} ↔ R{pivotRow + 1}", matrixL=copyMatrix(L),
                    matrixU=copyMatrix(U), )

        for k in range(i, n):
            sumValue = sum(L[i][j] * U[j][k] for j in range(i))
            U[i][k] = a[i][k] - sumValue

        if recorder.isEnabled():
            recorder.record("decompositionStep", f"Computing U row {i + 1}", matrixL=copyMatrix(L),
                matrixU=copyMatrix(U), )

        if U[i][i].isNearZero():
            raise ValueError(f"Matrix is singular: zero pivot at position ({i + 1}, {i + 1})")

        L[i][i] = D.one()
        for k in range(i + 1, n):
            sumValue = sum(L[k][j] * U[j][i] for j in range(i))
            L[k][i] = (a[k][i] - sumValue) / U[i][i]

        if recorder.isEnabled():
            recorder.record("decompositionStep", f"Computing L column {i + 1}", matrixL=copyMatrix(L),
                matrixU=copyMatrix(U), )

    if recorder.isEnabled():
        recorder.record("decompositionComplete", "LU Decomposition complete (Doolittle with partial pivoting form)",
            matrixL=copyMatrix(L), matrixU=copyMatrix(U), )

    y = forwardSubstitution(L, b, n, recorder)
    x = backwardSubstitution(U, y, n, recorder)

    return x, L, U
