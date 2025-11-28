import customtkinter as ctk


def create_output_section(parent, app):
    output_container = ctk.CTkFrame(parent, fg_color="transparent")
    output_container.pack(fill="both", expand=True, padx=15, pady=15)

    header = ctk.CTkLabel(
        output_container,
        text="Output",
        font=ctk.CTkFont(family="Courier New", size=20, weight="bold"),
    )
    header.pack(pady=(0, 10), anchor="w")

    content_frame = ctk.CTkFrame(output_container, fg_color="transparent")
    content_frame.pack(fill="both", expand=True)

    app.output_text = ctk.CTkTextbox(
        content_frame, font=ctk.CTkFont(family="Courier New", size=14), corner_radius=8
    )
    app.output_text.pack(side="left", fill="both", expand=True)

    app.current_steps = []
