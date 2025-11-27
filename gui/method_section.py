"""
Method configuration section component.
"""
import customtkinter as ctk


def create_method_section(parent, app):
    """Create the method selection and parameters section"""
    # Header
    header = ctk.CTkLabel(parent, text="Method Configuration", font=ctk.CTkFont(size=20, weight="bold"))
    header.pack(pady=(15, 20), padx=15, anchor="w")

    # Method selection
    method_frame = ctk.CTkFrame(parent, fg_color="transparent")
    method_frame.pack(fill="x", padx=15, pady=5)

    ctk.CTkLabel(method_frame, text="Algorithm:", font=ctk.CTkFont(size=15, weight="bold")).pack(anchor="w",
                                                                                                 pady=(0, 5))

    methods = ["Gauss Elimination", "Gauss-Jordan", "LU Decomposition", "Jacobi", "Gauss-Seidel"]

    ctk.CTkOptionMenu(method_frame, values=methods, variable=app.method, command=app.on_method_change, height=35,
        font=ctk.CTkFont(size=14), dropdown_font=ctk.CTkFont(size=13)).pack(fill="x", pady=5)

    # Checkboxes in one row (Enable Scaling and Step by Step side by side)
    checkboxes_row = ctk.CTkFrame(parent, fg_color="transparent")
    checkboxes_row.pack(fill="x", padx=15, pady=10)

    app.scaling_checkbox = ctk.CTkCheckBox(checkboxes_row, text="Enable Scaling", variable=app.scaling_enabled,
        font=ctk.CTkFont(size=15, weight="bold"))
    app.scaling_checkbox.pack(side="left", padx=(0, 20))

    ctk.CTkCheckBox(checkboxes_row, text="Step by Step", variable=app.step_by_step,
        font=ctk.CTkFont(size=15, weight="bold")).pack(side="left")

    # Parameters container
    app.params_container = ctk.CTkFrame(parent, fg_color="transparent")
    app.params_container.pack(fill="x", padx=15, pady=5)

    # Solve button
    ctk.CTkButton(parent, text="SOLVE", command=app.solve_system, font=ctk.CTkFont(size=18, weight="bold"), height=50,
        corner_radius=8).pack(fill="x", padx=15, pady=(10, 15))


def create_parameter_widgets(app):
    """Create method parameter input widgets"""
    # Clear existing
    for widget in app.params_container.winfo_children():
        widget.destroy()

    # LU Form
    app.lu_frame = ctk.CTkFrame(app.params_container, fg_color="transparent")

    ctk.CTkLabel(app.lu_frame, text="LU Form:", font=ctk.CTkFont(size=15, weight="bold")).pack(anchor="w", pady=(5, 5))

    ctk.CTkOptionMenu(app.lu_frame, values=["Doolittle", "Crout", "Cholesky"], variable=app.lu_form, height=35,
        font=ctk.CTkFont(size=14)).pack(fill="x", pady=5)

    # Iterative methods parameters
    app.iterative_frame = ctk.CTkFrame(app.params_container, fg_color="transparent")

    # Initial guess (horizontal row instead of vertical)
    ctk.CTkLabel(app.iterative_frame, text="Initial Guess:", font=ctk.CTkFont(size=15, weight="bold")).pack(anchor="w",
                                                                                                            pady=(5, 5))

    app.initial_guess_container = ctk.CTkFrame(app.iterative_frame, fg_color="transparent")
    app.initial_guess_container.pack(fill="x", pady=5)

    # Stopping condition - dropdown and input in same row
    stop_container = ctk.CTkFrame(app.iterative_frame, fg_color="transparent")
    stop_container.pack(fill="x", pady=(10, 5))

    ctk.CTkLabel(stop_container, text="Stop Condition:", font=ctk.CTkFont(size=15, weight="bold")).pack(anchor="w",
                                                                                                        pady=(0, 5))

    # Row with dropdown and input side by side
    stop_row = ctk.CTkFrame(stop_container, fg_color="transparent")
    stop_row.pack(fill="x")

    # Left side: dropdown
    dropdown_frame = ctk.CTkFrame(stop_row, fg_color="transparent")
    dropdown_frame.pack(side="left", fill="x", expand=True, padx=(0, 5))

    ctk.CTkOptionMenu(dropdown_frame, values=["Max Iterations", "Absolute Relative Error"],
        variable=app.stopping_condition, command=app.on_stopping_condition_change, height=35,
        font=ctk.CTkFont(size=14)).pack(fill="x")

    # Right side: input (will be swapped based on selection)
    app.stop_input_container = ctk.CTkFrame(stop_row, fg_color="transparent")
    app.stop_input_container.pack(side="left", fill="x", expand=True, padx=(5, 0))

    # Max iterations input
    app.max_iter_frame = ctk.CTkFrame(app.stop_input_container, fg_color="transparent")

    ctk.CTkEntry(app.max_iter_frame, textvariable=app.max_iterations, width=150, height=35, font=ctk.CTkFont(size=14),
        placeholder_text="Max Iterations").pack(fill="x")

    # Absolute error input
    app.abs_error_frame = ctk.CTkFrame(app.stop_input_container, fg_color="transparent")

    ctk.CTkEntry(app.abs_error_frame, textvariable=app.abs_error, width=150, height=35, font=ctk.CTkFont(size=14),
        placeholder_text="Tolerance").pack(fill="x")

    # Initially hide all
    app.lu_frame.pack_forget()
    app.iterative_frame.pack_forget()

    # Show max iterations by default
    app.max_iter_frame.pack(fill="x")
    app.abs_error_frame.pack_forget()


def generate_initial_guess_inputs(app):
    """Generate initial guess input fields as a horizontal row"""
    for widget in app.initial_guess_container.winfo_children():
        widget.destroy()

    app.initial_guess_entries = []

    try:
        n = app.num_vars.get()
    except:
        return

    # Create a single row for all initial guess values
    for i in range(n):
        col_frame = ctk.CTkFrame(app.initial_guess_container, fg_color="transparent")
        col_frame.pack(side="left", padx=3)

        ctk.CTkLabel(col_frame, text=f"x{i + 1}:", font=ctk.CTkFont(size=13, weight="bold")).pack(anchor="w")

        entry = ctk.CTkEntry(col_frame, width=60, height=30, font=ctk.CTkFont(size=13))
        entry.insert(0, "0")
        entry.pack()
        app.initial_guess_entries.append(entry)
