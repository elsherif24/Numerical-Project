from tkinter import messagebox

import customtkinter as ctk


def create_input_config_section(parent, app):
    header = ctk.CTkLabel(
        parent,
        text="Input Configuration",
        font=ctk.CTkFont(family="Courier New", size=20, weight="bold"),
    )
    header.pack(pady=(15, 20), padx=15, anchor="w")

    config_frame = ctk.CTkFrame(parent, fg_color="transparent")
    config_frame.pack(fill="x", padx=15, pady=5)

    var_row = ctk.CTkFrame(config_frame, fg_color="transparent")
    var_row.pack(fill="x", pady=5)

    ctk.CTkLabel(
        var_row,
        text="Number of Variables:",
        font=ctk.CTkFont(family="Courier New", size=15, weight="bold"),
    ).pack(side="left", padx=5)

    ctk.CTkEntry(
        var_row,
        textvariable=app.num_vars,
        width=80,
        height=35,
        font=ctk.CTkFont(family="Courier New", size=14),
    ).pack(side="left", padx=5)

    ctk.CTkButton(
        var_row,
        text="Generate",
        command=app.generate_matrix_inputs,
        width=100,
        height=35,
        font=ctk.CTkFont(family="Courier New", size=14, weight="bold"),
    ).pack(side="left", padx=5)

    sig_row = ctk.CTkFrame(config_frame, fg_color="transparent")
    sig_row.pack(fill="x", pady=5)

    ctk.CTkLabel(
        sig_row,
        text="Significant Figures:",
        font=ctk.CTkFont(family="Courier New", size=15, weight="bold"),
    ).pack(side="left", padx=5)

    ctk.CTkEntry(
        sig_row,
        textvariable=app.sig_figs,
        width=80,
        height=35,
        font=ctk.CTkFont(family="Courier New", size=14),
    ).pack(side="left", padx=5)

    app.matrix_scroll = ctk.CTkScrollableFrame(
        parent,
        fg_color=("#242424", "#1a1a1a"),
        corner_radius=8,
        height=500,
    )
    app.matrix_scroll.pack(fill="both", expand=True, padx=15, pady=(10, 15))


def generate_matrix_inputs(app):
    for widget in app.matrix_scroll.winfo_children():
        widget.destroy()

    app.coefficient_entries = []
    app.constant_entries = []

    try:
        n = app.num_vars.get()
        if n < 1 or n > 10:
            messagebox.showerror(
                "Error", "Number of variables must be between 1 and 10"
            )
            return
    except:
        messagebox.showerror("Error", "Invalid number of variables")
        return

    header = ctk.CTkFrame(app.matrix_scroll, fg_color="transparent")
    header.pack(fill="x", pady=8)

    ctk.CTkLabel(
        header,
        text="Coefficients",
        font=ctk.CTkFont(family="Courier New", size=16, weight="bold"),
        width=500,
    ).pack(side="left", padx=10)

    ctk.CTkLabel(
        header,
        text="Constant",
        font=ctk.CTkFont(family="Courier New", size=16, weight="bold"),
        width=100,
    ).pack(side="left")

    for i in range(n):
        eq_frame = ctk.CTkFrame(app.matrix_scroll, fg_color="transparent")
        eq_frame.pack(fill="x", pady=3)

        ctk.CTkLabel(
            eq_frame,
            text=f"Eq {i + 1}:",
            width=60,
            font=ctk.CTkFont(family="Courier New", size=14, weight="bold"),
        ).pack(side="left", padx=5)

        row_entries = []
        for j in range(n):
            entry = ctk.CTkEntry(
                eq_frame,
                width=75,
                height=32,
                placeholder_text=f"a{i + 1}{j + 1}",
                font=ctk.CTkFont(family="Courier New", size=13),
            )
            entry.pack(side="left", padx=2)
            row_entries.append(entry)

        app.coefficient_entries.append(row_entries)

        const_entry = ctk.CTkEntry(
            eq_frame,
            width=75,
            height=32,
            placeholder_text=f"b{i + 1}",
            font=ctk.CTkFont(family="Courier New", size=13),
        )
        const_entry.pack(side="left", padx=8)
        app.constant_entries.append(const_entry)
