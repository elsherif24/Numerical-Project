import tkinter as tk
from tkinter import ttk, messagebox  
from methods.gauss_elimination import gauss_partial
from gui.input import create_matrix_inputs
from methods.lu_decomposition import lu
def start_app():
    root = tk.Tk()
    root.title("Linear System Solver")
    root.geometry("500x650")

    main_frame = ttk.Frame(root, padding="15")
    main_frame.pack(fill=tk.BOTH, expand=True)

    tk.Label(main_frame, text="Select Method:", font=("Arial", 12)).pack(anchor='w', pady=(0, 5))
    
    method_var = tk.StringVar(value="Gauss Elimination")
    method_combo = ttk.Combobox(
        main_frame, 
        textvariable=method_var,
        values=[
            "Gauss Elimination",
            "Gauss Jordan", 
            "LU Decomposition",
            "Jacobi",
            "Gauss Seidel"
        ],
        state="readonly",
        font=("Arial", 10)
    )
    method_combo.pack(fill=tk.X, pady=(0, 10))

    lu_frame = ttk.Frame(main_frame)
    
    tk.Label(lu_frame, text="LU Decomposition Form:", font=("Arial", 10)).pack(anchor='w', pady=(0, 5))
    
    lu_method_var = tk.StringVar(value="Doolittle Form")
    lu_method_combo = ttk.Combobox(
        lu_frame, 
        textvariable=lu_method_var,
        values=[
            "Doolittle Form",
            "Crout Form", 
            "Cholesky Form"
        ],
        state="readonly",
        font=("Arial", 9)
    )
    lu_method_combo.pack(fill=tk.X, pady=(0, 5))

    tk.Label(main_frame, text="Enter number of variables (n):", font=("Arial", 12)).pack(anchor='w', pady=(10, 5))
    n_entry = tk.Entry(main_frame, font=("Arial", 10))
    n_entry.pack(fill=tk.X, pady=(0, 10))

    scaling_var = tk.BooleanVar(value=False)
    scaling_checkbox = tk.Checkbutton(
        main_frame, 
        text="Use Scaling",
        variable=scaling_var,
        font=("Arial", 10)
    )

    matrix_frame = ttk.LabelFrame(main_frame, text="Equations", padding="10")
    matrix_frame.pack(fill=tk.BOTH, expand=True, pady=10)

    button_frame = ttk.Frame(main_frame)
    button_frame.pack(fill=tk.X, pady=10)

    coeff_entries = []
    b_entries = []

    def update_ui_based_on_method():
        method = method_var.get()
        
        scaling_checkbox.pack(anchor='w', pady=5)

        
        if method == "LU Decomposition":
            lu_frame.pack(fill=tk.X, pady=5, after=method_combo)
        else:
            lu_frame.pack_forget()

    def create_fields():
        try:
            n = int(n_entry.get())
            if n <= 0:
                messagebox.showerror("Error", "Number of variables must be positive")
                return
            
            # Clear existing matrix inputs
            for widget in matrix_frame.winfo_children():
                widget.destroy()
            
            nonlocal coeff_entries, b_entries
            coeff_entries, b_entries = create_matrix_inputs(n, matrix_frame)
            
            method = method_var.get()
            matrix_frame.configure(text=f"Equations for {method} (n={n})")
            
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number for n")

    def solve():
        try:
            if not coeff_entries:
                messagebox.showwarning("Please create the equations first")
                return

            n = len(coeff_entries)
            A = []
            B = []

            # Read matrix values
            for i in range(n):
                row = []
                for j in range(n):
                    value = coeff_entries[i][j].get()
                    if value == "":
                        messagebox.showerror("Error", f"Missing value at A[{i+1}][{j+1}]")
                        return
                    row.append(float(value))
                A.append(row)
                
                b_value = b_entries[i].get()
                if b_value == "":
                    messagebox.showerror("Error", f"Missing value at B[{i+1}]")
                    return
                B.append(float(b_value))

            method = method_var.get()
            use_scaling = scaling_var.get()

            # Call specific method
            if method == "Gauss Elimination":
                solution, t = gauss_partial(A, B, scale=use_scaling)
                method_used = f"Gauss Elimination {'with Scaling' if use_scaling else 'without Scaling'}"
                
            elif method == "Gauss Jordan":
                method_used = "Gauss Jordan"
                
            elif method == "LU Decomposition":
                lu_form = lu_method_var.get()
                solution, t = lu(A, B, scale=use_scaling, form=lu_form)

                method_used = f"LU Decomposition ({lu_form}) {'with Scaling' if use_scaling else 'without Scaling'}"
                
            elif method == "Jacobi":
                method_used = "Jacobi"
                
            elif method == "Gauss Seidel":
                method_used = "Gauss Seidel"
            
            else:
                messagebox.showerror("Error", "Unknown method selected")
                return

            if solution is None:
                messagebox.showerror("Error", t)
            else:
                result_text = f"Method: {method_used}\n\n"
                result_text += "Solution:\n"
                for i, x in enumerate(solution):
                    result_text += f"x{i+1} = {x:.6f}\n"
                result_text += f"\nTime: {t:.6f} seconds"
                
                messagebox.showinfo("Solution", result_text)

        except ValueError as e:
            messagebox.showerror("Error", "Please enter valid numbers in all fields")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    # Create buttons
    ttk.Button(button_frame, text="Create Equations", command=create_fields).pack(side=tk.LEFT, padx=(0, 10))
    ttk.Button(button_frame, text="Solve System", command=solve).pack(side=tk.LEFT)

    # Bind method change event
    method_combo.bind('<<ComboboxSelected>>', lambda e: update_ui_based_on_method())

    # Initial UI update
    update_ui_based_on_method()

    root.mainloop()
