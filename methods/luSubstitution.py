from D import D
from utils.stepRecorder import copyMatrix, copyVector


def forwardSubstitution(L, b, n, recorder):
    if recorder.isEnabled():
        recorder.record("forwardSubstitutionStart", "Starting forward substitution: Ly = b", matrixL=copyMatrix(L),
            vectorB=copyVector(b), )

    y = D.zeros(n)

    for i in range(n):
        if L[i][i].isNearZero():
            raise ValueError(f"Matrix is singular: zero diagonal element at position ({i + 1}, {i + 1})")
        sumValue = sum(L[i][j] * y[j] for j in range(i))
        y[i] = (b[i] - sumValue) / L[i][i]

        if recorder.isEnabled():
            recorder.record("forwardSubstitutionStep", f"y[{i + 1}] = {y[i]}", vectorY=copyVector(y), )

    if recorder.isEnabled():
        recorder.record("forwardSubstitutionComplete", "Forward substitution complete", vectorY=copyVector(y), )

    return y


def backwardSubstitution(U, y, n, recorder):
    if recorder.isEnabled():
        recorder.record("backwardSubstitutionStart", "Starting backward substitution: Ux = y", matrixU=copyMatrix(U),
            vectorY=copyVector(y), )

    x = D.zeros(n)

    if U[n - 1][n - 1].isNearZero():
        raise ValueError(f"Matrix is singular: zero diagonal element at position ({n}, {n})")

    x[n - 1] = y[n - 1] / U[n - 1][n - 1]

    if recorder.isEnabled():
        recorder.record("backwardSubstitutionStep", f"x[{n}] = {x[n - 1]}", vectorX=copyVector(x), )

    for i in range(n - 2, -1, -1):
        if U[i][i].isNearZero():
            raise ValueError(f"Matrix is singular: zero diagonal element at position ({i + 1}, {i + 1})")
        sumValue = sum(U[i][j] * x[j] for j in range(i + 1, n))
        x[i] = (y[i] - sumValue) / U[i][i]

        if recorder.isEnabled():
            recorder.record("backwardSubstitutionStep", f"x[{i + 1}] = {x[i]}", vectorX=copyVector(x), )

    if recorder.isEnabled():
        recorder.record("backwardSubstitutionComplete", "Backward substitution complete - Solution found",
            vectorX=copyVector(x), )

    return x
