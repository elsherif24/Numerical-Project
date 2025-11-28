from tkinter import messagebox
from typing import Optional, Tuple

import numpy as np


def get_matrix_and_constants(app) -> Tuple[Optional[np.ndarray], Optional[np.ndarray]]:
    try:
        n = app.num_vars.get()
        A = np.zeros((n, n))
        b = np.zeros(n)

        for i in range(n):
            for j in range(n):
                val = app.coefficient_entries[i][j].get().strip()
                A[i, j] = float(val) if val else 0.0

            val = app.constant_entries[i].get().strip()
            b[i] = float(val) if val else 0.0

        return A, b
    except Exception as e:
        messagebox.showerror("Error", f"Invalid input: {str(e)}")
        return None, None


def get_initial_guess(app) -> Optional[np.ndarray]:
    try:
        n = app.num_vars.get()
        x0 = np.zeros(n)

        for i in range(n):
            val = app.initial_guess_entries[i].get().strip()
            x0[i] = float(val) if val else 0.0

        return x0
    except Exception as e:
        messagebox.showerror("Error", f"Invalid initial guess: {str(e)}")
        return None


def format_number(num, sig_figs):
    if hasattr(num, "__float__"):
        num = float(num)
    return f"{num:.{sig_figs}g}"
