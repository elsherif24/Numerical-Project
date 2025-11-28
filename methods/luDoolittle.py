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

    # Perform decomposition with pivoting
    for k in range(n - 1):
        # Find pivot row
        pivotRow = findPivotRow(a, k, n, scalers)

        # Swap rows if needed
        if pivotRow != k:
            swapRows(a, b, k, pivotRow)
            if scalers is not None:
                swapScalers(scalers, k, pivotRow)

            if recorder.isEnabled():
                recorder.record(
                    "pivot",
                    f"Partial pivoting: Swap R{k + 1} ↔ R{pivotRow + 1}",
                    matrixA=copyMatrix(a),
                )

        # Check for singular matrix
        if a[k][k].isNearZero():
            raise ValueError(
                f"Matrix is singular: zero pivot at position ({k + 1}, {k + 1})"
            )

        # Elimination - store L factors in lower part of a
        for i in range(k + 1, n):
            factor = a[i][k] / a[k][k]
            a[i][k] = factor  # Store L coefficient in place

            for j in range(k + 1, n):
                a[i][j] = a[i][j] - factor * a[k][j]

        if recorder.isEnabled():
            recorder.record(
                "decompositionStep", f"Elimination step {k + 1}", matrixA=copyMatrix(a)
            )

    # Check last pivot
    if a[n - 1][n - 1].isNearZero():
        raise ValueError(f"Matrix is singular: zero pivot at position ({n}, {n})")

    # Extract L and U from the combined matrix
    for i in range(n):
        for j in range(n):
            if i > j:
                L[i][j] = a[i][j]  # Lower part
            elif i == j:
                L[i][j] = D.one()  # Diagonal of L is 1
                U[i][j] = a[i][j]  # Diagonal of U
            else:
                U[i][j] = a[i][j]  # Upper part

    if recorder.isEnabled():
        recorder.record(
            "decompositionComplete",
            "LU Decomposition complete (Doolittle with partial pivoting form)",
            matrixL=copyMatrix(L),
            matrixU=copyMatrix(U),
        )

    # Solve using forward and backward substitution
    y = forwardSubstitution(L, b, n, recorder)
    x = backwardSubstitution(U, y, n, recorder)

    return x, L, U
