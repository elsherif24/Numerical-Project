"""
System Classifier - Debug Helper
This module is used to classify linear systems and determine whether they have:
no solution, one unique solution, or infinitely many solutions.

This is a standalone helper used strictly for debugging purposes and does not affect
the main solver's time measurement or output.
"""


def classifySystem(coefficientMatrix, constantVector):
    """
    Classifies a linear system as having no solution, one solution, or infinitely many solutions.

    Args:
        coefficientMatrix: The coefficient matrix A (as list of lists of floats/ints)
        constantVector: The constant vector b (as list of floats/ints)

    Returns:
        str: "No solution", "One unique solution", or "Infinitely many solutions"
    """
    # Convert to native Python types to avoid D class dependencies
    A = [
        [float(val) if hasattr(val, "val") else float(val) for val in row]
        for row in coefficientMatrix
    ]
    b = [float(val) if hasattr(val, "val") else float(val) for val in constantVector]

    n = len(A)
    m = len(A[0]) if n > 0 else 0

    # Calculate rank of coefficient matrix A
    matrixA = [row[:] for row in A]
    rankA = computeRank(matrixA)

    # Calculate rank of augmented matrix [A|b]
    augmented = [A[i][:] + [b[i]] for i in range(n)]
    rankAb = computeRank(augmented)

    # Rouché-Capelli theorem:
    # - If rank(A) < rank([A|b]): No solution (inconsistent)
    # - If rank(A) = rank([A|b]) = m: One unique solution
    # - If rank(A) = rank([A|b]) < m: Infinitely many solutions

    if rankAb > rankA:
        return "No solution"
    elif rankA == rankAb == m:
        return "One unique solution"
    else:
        return "Infinitely many solutions"


def computeRank(matrix):
    """
    Computes the rank of a matrix using Gaussian elimination.

    Args:
        matrix: The matrix (will be modified during computation)

    Returns:
        int: The rank of the matrix (number of non-zero rows after reduction)
    """
    if not matrix or not matrix[0]:
        return 0

    n = len(matrix)
    m = len(matrix[0])
    tolerance = 1e-10

    # Perform Gaussian elimination to row echelon form
    currentRow = 0

    for col in range(m):
        # Find the pivot (row with largest absolute value in this column)
        pivotRow = -1
        maxVal = 0.0

        for row in range(currentRow, n):
            absVal = abs(matrix[row][col])
            if absVal > maxVal:
                maxVal = absVal
                pivotRow = row

        # If no suitable pivot found, move to next column
        if maxVal < tolerance:
            continue

        # Swap rows if needed
        if pivotRow != currentRow:
            matrix[currentRow], matrix[pivotRow] = matrix[pivotRow], matrix[currentRow]

        # Eliminate all entries below the pivot
        for row in range(currentRow + 1, n):
            if abs(matrix[currentRow][col]) < tolerance:
                continue

            factor = matrix[row][col] / matrix[currentRow][col]

            for c in range(col, m):
                matrix[row][c] -= factor * matrix[currentRow][c]

        currentRow += 1

        # If we've processed all rows, we're done
        if currentRow >= n:
            break

    # Count non-zero rows
    rank = 0
    for row in range(n):
        # Check if row has any non-zero element
        hasNonZero = False
        for col in range(m):
            if abs(matrix[row][col]) > tolerance:
                hasNonZero = True
                break
        if hasNonZero:
            rank += 1

    return rank


def debugSystemType(coefficientMatrix, constantVector):
    """
    Public interface to classify and print the system type.

    Args:
        coefficientMatrix: The coefficient matrix A
        constantVector: The constant vector b

    Returns:
        str: Classification result
    """
    systemType = classifySystem(coefficientMatrix, constantVector)
    return systemType
