import customtkinter as ctk


def create_method_section(parent, app):
    header = ctk.CTkLabel(
        parent,
        text="Method Configuration",
        font=ctk.CTkFont(family="Courier New", size=20, weight="bold"),
    )
    header.pack(pady=(15, 20), padx=15, anchor="w")

    method_frame = ctk.CTkFrame(parent, fg_color="transparent")
    method_frame.pack(fill="x", padx=15, pady=5)

    ctk.CTkLabel(
        method_frame,
        text="Algorithm:",
        font=ctk.CTkFont(family="Courier New", size=15, weight="bold"),
    ).pack(anchor="w", pady=(0, 5))

    methods = [
        "Gauss Elimination",
        "Gauss-Jordan",
        "LU Decomposition",
        "Jacobi",
        "Gauss-Seidel",
    ]

    ctk.CTkOptionMenu(
        method_frame,
        values=methods,
        variable=app.method,
        command=app.on_method_change,
        height=35,
        font=ctk.CTkFont(family="Courier New", size=14),
        dropdown_font=ctk.CTkFont(family="Courier New", size=13),
    ).pack(fill="x", pady=5)

    checkboxes_row = ctk.CTkFrame(parent, fg_color="transparent")
    checkboxes_row.pack(fill="x", padx=15, pady=10)

    app.scaling_checkbox = ctk.CTkCheckBox(
        checkboxes_row,
        text="Enable Scaling",
        variable=app.scaling_enabled,
        font=ctk.CTkFont(family="Courier New", size=15, weight="bold"),
    )
    app.scaling_checkbox.pack(side="left", padx=(0, 20))

    ctk.CTkCheckBox(
        checkboxes_row,
        text="Step by Step",
        variable=app.step_by_step,
        font=ctk.CTkFont(family="Courier New", size=15, weight="bold"),
    ).pack(side="left")

    app.params_container = ctk.CTkFrame(parent, fg_color="transparent")
    app.params_container.pack(fill="x", padx=15, pady=5)

    ctk.CTkButton(
        parent,
        text="SOLVE",
        command=app.solve_system,
        font=ctk.CTkFont(family="Courier New", size=18, weight="bold"),
        height=50,
        corner_radius=8,
    ).pack(fill="x", padx=15, pady=(10, 15))


def create_parameter_widgets(app):
    for widget in app.params_container.winfo_children():
        widget.destroy()

    app.lu_frame = ctk.CTkFrame(app.params_container, fg_color="transparent")

    ctk.CTkLabel(
        app.lu_frame,
        text="LU Form:",
        font=ctk.CTkFont(family="Courier New", size=15, weight="bold"),
    ).pack(anchor="w", pady=(5, 5))

    ctk.CTkOptionMenu(
        app.lu_frame,
        values=["Doolittle", "Crout", "Cholesky"],
        variable=app.lu_form,
        command=app.on_lu_form_change,
        height=35,
        font=ctk.CTkFont(family="Courier New", size=14),
    ).pack(fill="x", pady=5)

    app.iterative_frame = ctk.CTkFrame(app.params_container, fg_color="transparent")

    ctk.CTkLabel(
        app.iterative_frame,
        text="Initial Guess:",
        font=ctk.CTkFont(family="Courier New", size=15, weight="bold"),
    ).pack(anchor="w", pady=(5, 5))

    app.initial_guess_container = ctk.CTkFrame(
        app.iterative_frame, fg_color="transparent"
    )
    app.initial_guess_container.pack(fill="x", pady=5)

    stop_container = ctk.CTkFrame(app.iterative_frame, fg_color="transparent")
    stop_container.pack(fill="x", pady=(10, 5))

    ctk.CTkLabel(
        stop_container,
        text="Stopping Conditions:",
        font=ctk.CTkFont(family="Courier New", size=15, weight="bold"),
    ).pack(anchor="w", pady=(0, 5))

    inputs_row = ctk.CTkFrame(stop_container, fg_color="transparent")
    inputs_row.pack(fill="x", pady=(0, 5))

    ctk.CTkLabel(
        inputs_row,
        text="Max Iterations:",
        font=ctk.CTkFont(family="Courier New", size=13),
    ).pack(side="left", padx=(0, 5))

    ctk.CTkEntry(
        inputs_row,
        textvariable=app.max_iterations,
        width=100,
        height=35,
        font=ctk.CTkFont(family="Courier New", size=14),
        placeholder_text="100",
    ).pack(side="left", padx=(0, 15))

    ctk.CTkLabel(
        inputs_row,
        text="Error Tolerance:",
        font=ctk.CTkFont(family="Courier New", size=13),
    ).pack(side="left", padx=(0, 5))

    ctk.CTkEntry(
        inputs_row,
        textvariable=app.abs_error,
        width=100,
        height=35,
        font=ctk.CTkFont(family="Courier New", size=14),
        placeholder_text="1e-6",
    ).pack(side="left")

    app.lu_frame.pack_forget()
    app.iterative_frame.pack_forget()


def generate_initial_guess_inputs(app):
    for widget in app.initial_guess_container.winfo_children():
        widget.destroy()

    app.initial_guess_entries = []

    try:
        n = app.num_vars.get()
    except:
        return

    for i in range(n):
        col_frame = ctk.CTkFrame(app.initial_guess_container, fg_color="transparent")
        col_frame.pack(side="left", padx=3)

        ctk.CTkLabel(
            col_frame,
            text=f"x{i + 1}:",
            font=ctk.CTkFont(family="Courier New", size=13, weight="bold"),
        ).pack(anchor="w")

        entry = ctk.CTkEntry(
            col_frame,
            width=60,
            height=30,
            font=ctk.CTkFont(family="Courier New", size=13),
        )
        entry.insert(0, "0")
        entry.pack()
        app.initial_guess_entries.append(entry)
