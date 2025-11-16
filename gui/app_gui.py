import tkinter as tk
from tkinter import messagebox  
from methods.gauss_elimination import gauss_partial
from gui.input import create_matrix_inputs

def start_app():
    root = tk.Tk()
    root.title("Gauss Elimination with Partial Pivoting")
    root.geometry("400x600")

    tk.Label(root, text="Enter number of variables (n):", font=("Arial", 12)).pack()
    n_entry = tk.Entry(root)
    n_entry.pack()

    frame = tk.Frame(root)
    frame.pack(pady=5)

    def create_fields():
        for w in frame.winfo_children():
            w.destroy()
        n = int(n_entry.get())
        nonlocal coeff_entries, b_entries
        coeff_entries, b_entries = create_matrix_inputs(n, frame)

    coeff_entries = []
    b_entries = []

    tk.Button(root, text="Create Matrix",font = ("Arial", 9), command=create_fields).pack(pady=5)

    def solve():
        try:
            n = len(coeff_entries)
            A = []
            B = []

            for i in range(n):
                row = []
                for j in range(n):
                    row.append(float(coeff_entries[i][j].get()))
                A.append(row)
                B.append(float(b_entries[i].get()))

            solution, t = gauss_partial(A, B)

            if solution is None:
                messagebox.showerror("Error", t)
            else:
                messagebox.showinfo("Solution", f"X = {solution}\nTime = {t:.6f} sec")

        except Exception as e:
            messagebox.showerror("Error", str(e))

    tk.Button(root, text="Solve",font = ("Arial", 9), command=solve).pack(pady=5)

    root.mainloop()