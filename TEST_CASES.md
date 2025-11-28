### Normal Case: Well-Conditioned System
**Description**: Standard well-conditioned system with unique solution.

**Input Matrix [A|b]:**
```
  4   -1    1  |  8
  2    5   -2  |  3
  1    2    4  | 11
```

### Tricky Case: Requires Pivoting
**Description**: System where initial pivot is zero, requires row swapping.

**Input Matrix [A|b]:**
```
  0    2   -1  |  1
  1   -1    2  |  4
  2    1    1  |  7
```
---

## LU Decomposition - Doolittle

### Normal Case: Positive Definite System
**Description**: Nice system suitable for LU decomposition.

**Input Matrix [A|b]:**
```
  4    2    1  |  7
  2    5    3  | 10
  1    3    6  | 10
```
---

### Tricky Case: Near-Singular Matrix
**Description**: Matrix very close to being singular (determinant near zero).

**Input Matrix [A|b]:**
```
  1    1    1  |  6
  1    1    2  |  9
  1    1  1.0001  | 6.0001
```

---

## LU Decomposition - Crout

### Normal Case: Standard System
**Description**: Regular system for Crout decomposition.

**Input Matrix [A|b]:**
```
  3   -1    2  |  7
  1    4   -1  |  8
  2   -2    5  |  9
```

---

### Tricky Case: Zeros in Matrix
**Description**: System with zeros that complicate decomposition.

**Input Matrix [A|b]:**
```
  2    0    1  |  3
  0    3    2  |  5
  1    2    4  |  7
```
---

## LU Decomposition - Cholesky

### Normal Case: Symmetric Positive Definite
**Description**: Properly conditioned SPD matrix (required for Cholesky).

**Input Matrix [A|b]:**
```
  4    2    1  |  7
  2    5    3  | 10
  1    3    6  | 10
```

---

### Tricky Case: Non-Symmetric Matrix
**Description**: Matrix that is NOT symmetric (should give error).

**Input Matrix [A|b]:**
```
  4    2    1  |  7
  1    5    3  | 10
  1    3    6  | 10
```
---

## Jacobi Iteration

### Normal Case: Diagonally Dominant
**Description**: Strictly diagonally dominant system (guaranteed convergence).

**Input Matrix [A|b]:**
```
  10    1    1  | 12
   1   10    1  | 12
   1    1   10  | 12
```
---

### Tricky Case: Not Diagonally Dominant
**Description**: System where Jacobi may not converge or converge slowly.

**Input Matrix [A|b]:**
```
  1    5    2  |  8
  3    1    4  |  8
  2    3    1  |  6
```
---

## Gauss-Seidel Iteration

### Normal Case: Diagonally Dominant
**Description**: Same system as Jacobi but should converge faster.

**Input Matrix [A|b]:**
```
  10    1    1  | 12
   1   10    1  | 12
   1    1   10  | 12
```

---

### Tricky Case: Poor Initial Guess
**Description**: Diagonally dominant but with initial guess far from solution.

**Input Matrix [A|b]:**
```
   8    1    1  | 10
   1    8    1  | 10
   1    1    8  | 10
```

**Settings**:
- Initial Guess: 100, 100, 100 (very far from solution)

---

## Additional Test Cases

### Universal Test: Simple Identity-Like System
**Description**: Works perfectly with all methods (good for quick verification).

**Input Matrix [A|b]:**
```
  3    0    0  |  6
  0    3    0  |  9
  0    0    3  | 12
```
---

### Challenge Test: Singular Matrix (Should Fail)
**Description**: System with no unique solution (determinant = 0).

**Input Matrix [A|b]:**
```
  1    2    3  |  6
  2    4    6  | 12
  1    1    1  |  3
```
---

### Challenge Test: Inconsistent System
**Description**: System with no solution (inconsistent equations).

**Input Matrix [A|b]:**
```
  1    2    3  |  6
  2    4    6  | 12
  1    2    3  |  5
```
