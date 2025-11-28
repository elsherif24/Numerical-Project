# Numerical Methods For Linear Systems

## ✅ Project Status: COMPLETE & ENHANCED

This project is **fully functional** with all requirements implemented and additional enhancements applied.

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

1. ✅ Fully implemented, well-structured, **OOP-based code**
2. ✅ Comprehensive documentation in `DOCUMENTATION.md`

---

## 🎨 Project Enhancements

This implementation includes the following improvements:

### Code Quality
* **Clean Architecture**: Strict MVC pattern separation
* **Monospace Fonts**: Courier New throughout for perfect alignment
* **Code Cleanup**: Removed unnecessary comments, simplified logic
* **Java-style Casing**: Consistent methodName convention
* **Type Safety**: Full type hints in Python code

### Features Implemented
* ✅ All 5 numerical methods working perfectly
* ✅ Step-by-step algorithm visualization
* ✅ Partial pivoting with optional scaling
* ✅ Precision control via significant figures
* ✅ Real-time execution timing
* ✅ Convergence detection for iterative methods
* ✅ Comprehensive error handling
* ✅ Matrix alignment in all outputs
* ✅ Support for systems up to 10×10

### Documentation
* Complete project documentation in `DOCUMENTATION.md`
* Detailed explanation of all components
* Workflow diagrams and usage guide
* Technical details and best practices

---

## 🚀 Quick Start

### Installation
```bash
pip install customtkinter numpy
```

### Running the Application
```bash
python main.py
```

### Basic Usage
1. Set number of variables (1-10)
2. Enter matrix coefficients and constants
3. Select solving method from dropdown
4. Configure method-specific parameters
5. Click SOLVE

---

## 📚 Documentation

See **DOCUMENTATION.md** for comprehensive information about:
* Project structure and architecture
* Core components (D class, Recorder, Solver Engine)
* All numerical methods with algorithms
* GUI architecture and MVC pattern
* Complete workflow explanation
* Usage guide and tips

---

## 🏗️ Architecture

* **MVC Pattern**: Clean separation of Model, View, Controller
* **D Class**: Precise arithmetic with configurable significant figures
* **Recorder System**: Captures step-by-step execution
* **Solver Engine**: Central dispatch for all methods
* **Modular Design**: Easy to extend with new methods

---

## 📊 Implemented Methods

| Method | Type | Features |
|--------|------|----------|
| Gauss Elimination | Direct | Partial pivoting, scaling |
| Gauss-Jordan | Direct | Reduced row echelon form |
| LU Doolittle | Decomposition | Pivoting, scaling |
| LU Crout | Decomposition | Standard form |
| LU Cholesky | Decomposition | Symmetric positive definite |
| Jacobi | Iterative | Convergence detection |
| Gauss-Seidel | Iterative | Faster convergence |

---

## 🎯 Key Features

* **Precise Arithmetic**: Using Python's Decimal class
* **Numerical Stability**: Scaled partial pivoting
* **User-Friendly**: Intuitive GUI with dark theme
* **Educational**: Step-by-step mode for learning
* **Robust**: Comprehensive error handling
* **Fast**: Optimized algorithms with timing
* **Flexible**: Configurable precision and parameters

---

## 📝 Notes

* All numerical methods in `methods/` folder are production-ready
* The D class provides automatic precision management
* Step recorder captures all operations for visualization
* GUI uses monospace fonts for perfect matrix alignment
* Supports both direct and iterative solution methods
