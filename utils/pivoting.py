def computeScaleFactors(a, n):
    scaleFactors = []
    for i in range(n):
        rowMaxValue = max(abs(x) for x in a[i][:n])

        if rowMaxValue.isNearZero():
            raise ValueError(f'Row {i + 1} "numerically" all zeros. Scaling is not possible.')

        scaleFactors.append(rowMaxValue)

    return scaleFactors


def findPivotRow(a, k, n, scalers):
    if scalers is None:
        return max(range(k, n), key=lambda r: abs(a[r][k]))
    else:
        return max(range(k, n), key=lambda r: abs(a[r][k]) / scalers[r])


def swapRows(a, b, row1, row2):
    a[row1], a[row2] = a[row2], a[row1]
    b[row1], b[row2] = b[row2], b[row1]


def swapScalers(scalers, row1, row2):
    if scalers is not None:
        scalers[row1], scalers[row2] = scalers[row2], scalers[row1]
