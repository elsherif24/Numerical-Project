import tkinter as tk

def create_matrix_inputs(n, frame):
    coeff_entries = []
    b_entries = []

    for i in range(n):
        row_list = []
        tk.Label(frame, text=f"Eq {i+1}:").grid(row=i, column=0)

        for j in range(n):
            e = tk.Entry(frame, width=5)
            e.grid(row=i, column=1 + j)
            row_list.append(e)

        coeff_entries.append(row_list)

        tk.Label(frame, text="=").grid(row=i, column=n + 1)

        e_b = tk.Entry(frame, width=5)
        e_b.grid(row=i, column=n + 2)
        b_entries.append(e_b)

    return coeff_entries, b_entries