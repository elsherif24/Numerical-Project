from D import D


def isDiagonallyDominant(a, n):
    for i in range(n):
        diagonal = abs(a[i][i])
        rowSum = sum(abs(a[i][j]) for j in range(n) if j != i)
        if diagonal <= rowSum:
            return False
    return True


def isSymmetricPositiveDefinite(a, n):
    if not isSymmetric(a, n):
        return False

    for k in range(1, n + 1):
        det = calculateLeadingMinorDeterminant(a, k)
        if det <= 0:
            return False

    return True


def isSymmetric(a, n):
    for i in range(n):
        for j in range(i + 1, n):
            if abs(a[i][j] - a[j][i]) > 1e-10:
                return False
    return True


def calculateLeadingMinorDeterminant(a, k):
    if k == 1:
        return a[0][0]

    submatrix = [[a[i][j] for j in range(k)] for i in range(k)]

    return calculateDeterminant(submatrix, k)


def calculateDeterminant(matrix, n):
    if n == 1:
        return matrix[0][0]

    if n == 2:
        return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]

    det = D.zero()
    for j in range(n):
        minor = []
        for i in range(1, n):
            minorRow = []
            for k in range(n):
                if k != j:
                    minorRow.append(matrix[i][k])
            minor.append(minorRow)

        cofactor = matrix[0][j] * calculateDeterminant(minor, n - 1)

        if j % 2 == 0:
            det = det + cofactor
        else:
            det = det - cofactor

    return det
