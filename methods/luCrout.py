from D import D
from methods.luSubstitution import backwardSubstitution, forwardSubstitution
from utils.stepRecorder import copyMatrix


def luCrout(a, b, n, recorder):
    if recorder.isEnabled():
        recorder.record("initial", "Initial coefficient matrix", matrixA=copyMatrix(a))

    L = [[D.zero() for _ in range(n)] for _ in range(n)]
    U = [[D.zero() for _ in range(n)] for _ in range(n)]

    for j in range(n):
        U[j][j] = D.one()

        for i in range(j, n):
            sumValue = sum(L[i][k] * U[k][j] for k in range(j))
            L[i][j] = a[i][j] - sumValue

        if recorder.isEnabled():
            recorder.record("decompositionStep", f"Computing L column {j + 1}", matrixL=copyMatrix(L),
                            matrixU=copyMatrix(U), )

        for i in range(j + 1, n):
            if L[j][j].isNearZero():
                raise ValueError(f"Matrix is singular: zero pivot at position ({j + 1}, {j + 1})")
            sumValue = sum(L[j][k] * U[k][i] for k in range(j))
            U[j][i] = (a[j][i] - sumValue) / L[j][j]

        if recorder.isEnabled():
            recorder.record("decompositionStep", f"Computing U row {j + 1}", matrixL=copyMatrix(L),
                            matrixU=copyMatrix(U), )

    if recorder.isEnabled():
        recorder.record("decompositionComplete", "LU Decomposition complete (Crout form)", matrixL=copyMatrix(L),
                        matrixU=copyMatrix(U), )

    y = forwardSubstitution(L, b, n, recorder)
    x = backwardSubstitution(U, y, n, recorder)

    return x, L, U
