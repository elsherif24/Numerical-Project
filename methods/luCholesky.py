from D import D
from methods.luSubstitution import backwardSubstitution, forwardSubstitution
from utils.matrixChecks import isSymmetricPositiveDefinite
from utils.stepRecorder import copyMatrix


def luCholesky(a, b, n, recorder):
    if recorder.isEnabled():
        recorder.record("initial", "Initial coefficient matrix", matrixA=copyMatrix(a))

    if not isSymmetricPositiveDefinite(a, n):
        errorMsg = "Error: Matrix is not Symmetric Positive Definite (SPD) - Cholesky decomposition cannot proceed"
        if recorder.isEnabled():
            recorder.record("error", errorMsg)
        raise ValueError(errorMsg)

    L = [[D.zero() for _ in range(n)] for _ in range(n)]

    for i in range(n):
        for j in range(i + 1):
            if i == j:
                sumValue = sum(L[i][k] * L[i][k] for k in range(j))
                value = a[i][i] - sumValue

                if value <= D.zero():
                    raise ValueError(
                        f"Matrix is not positive definite: non-positive value at position ({i + 1}, {i + 1})")

                L[i][j] = value.sqrt()
            else:
                if L[j][j].isNearZero():
                    raise ValueError(f"Matrix is singular: zero diagonal at position ({j + 1}, {j + 1})")
                sumValue = sum(L[i][k] * L[j][k] for k in range(j))
                L[i][j] = (a[i][j] - sumValue) / L[j][j]

        if recorder.isEnabled():
            recorder.record("decompositionStep", f"Computing L row {i + 1}", matrixL=copyMatrix(L))

    U = [[L[j][i] for j in range(n)] for i in range(n)]

    if recorder.isEnabled():
        recorder.record("decompositionComplete", "LU Decomposition complete (Cholesky form)", matrixL=copyMatrix(L),
                        matrixU=copyMatrix(U), )

    y = forwardSubstitution(L, b, n, recorder)
    x = backwardSubstitution(U, y, n, recorder)

    return x, L, U
