"""
Output display section component.
"""

import customtkinter as ctk


def create_output_section(parent, app):
    """Create the output display section"""
    # Header
    header = ctk.CTkLabel(parent, text="Output", font=ctk.CTkFont(size=20, weight="bold"))
    header.pack(pady=(15, 10), padx=15, anchor="w")

    # Output text box with monospace font for proper alignment
    app.output_text = ctk.CTkTextbox(parent, font=ctk.CTkFont(family="Courier New", size=16), corner_radius=8)
    app.output_text.pack(fill="both", expand=True, padx=15, pady=(0, 15))
