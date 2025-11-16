# Numerical Methods For Linear Systems Phase 1
## 📌 Project Requirements

This project aims to **implement and compare different numerical methods** for solving systems of linear equations. The required methods are:

* **Gauss Elimination**
* **Gauss–Jordan**
* **LU Decomposition** (Doolittle, Crout, Cholesky forms)
* **Jacobi Iteration**
* **Gauss–Seidel Iteration**

### 🔧 Application Requirements

You must build an **interactive GUI application** that:

1. Accepts user input for a **system of linear equations**

   * Valid input format (any consistent structure)
   * Number of equations = number of variables
   * Numeric coefficients only (0 or missing allowed)

2. Allows selecting a **solving method** from a dropdown list.

3. Receives **method-specific parameters** where applicable:

   * **LU:** Choose decomposition form (Doolittle / Crout / Cholesky)
   * **Jacobi & Gauss-Seidel:** initial guess + stopping condition
     (max iterations or absolute relative error)

4. Accepts **precision (significant figures)**, or applies a default if not provided.

5. Displays:

   * Final **solution**
   * **Execution time**
   * **Number of iterations** (if applicable)

6. Properly handles special cases:

   * **No solution**
   * **Infinite solutions**

7. **Partial pivoting** must always be applied (Gauss, Gauss-Jordan, LU Doolittle).

---

### 🎯 Bonus Features

Extra points for implementing any of the following:

* Step-by-step algorithm simulation
* Symbolic coefficients and symbolic results
* Optional scaling feature

---

### 📑 Deliverables

1. Fully implemented, well-structured, **OOP-based commented code**
2. A detailed report containing:

   * Pseudo-code for each method
   * Sample runs (normal + edge cases)
   * Method comparison (time, convergence, error)
   * Explanation of chosen data structures
