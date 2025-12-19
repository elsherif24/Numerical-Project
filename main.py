
import customtkinter as ctk

from gui.Phase1.controller import LinearSolverController
from gui.Phase1.view import LinearSolverView
from gui.Phase2.controller import Phase2Controller
from gui.Phase2.view import Phase2View

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")


class PhaseSelectionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Numerical Methods Solver")
        self.root.geometry("1920x1080")
        
        self.show_phase_selection()
    
    def show_phase_selection(self):
        """Show the main menu for phase selection"""
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Main container
        main_container = ctk.CTkFrame(self.root, fg_color="transparent")
        main_container.pack(fill="both", expand=True)
        
        # Center content
        center_frame = ctk.CTkFrame(main_container, fg_color="transparent")
        center_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        # Title
        ctk.CTkLabel(
            center_frame,
            text="Numerical Methods Solver",
            font=ctk.CTkFont(family="Courier New", size=36, weight="bold")
        ).pack(pady=(0, 60))
        
        # Subtitle
        ctk.CTkLabel(
            center_frame,
            text="Select a Phase",
            font=ctk.CTkFont(family="Courier New", size=24)
        ).pack(pady=(0, 40))
        
        # Phase 1 button
        ctk.CTkButton(
            center_frame,
            text="Phase 1: Linear Equation Solver",
            command=self.open_phase1,
            font=ctk.CTkFont(family="Courier New", size=20, weight="bold"),
            width=350,
            height=70,
            corner_radius=10
        ).pack(pady=20)
        
        # Phase 2 button
        ctk.CTkButton(
            center_frame,
            text="Phase 2: Root Finding Methods",
            command=self.open_phase2,
            font=ctk.CTkFont(family="Courier New", size=20, weight="bold"),
            width=350,
            height=70,
            corner_radius=10
        ).pack(pady=20)
    
    def open_phase1(self):
        """Open Phase 1 Linear Equation Solver"""
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Create Phase 1 application
        Phase1App(self.root, self.show_phase_selection)
    
    def open_phase2(self):
        """Open Phase 2"""
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Create Phase 2 application
        Phase2App(self.root, self.show_phase_selection)


class Phase1App:
    """Phase 1 Linear Equation Solver Application"""
    def __init__(self, root, back_callback):
        self.root = root
        self.back_callback = back_callback
        
        # Initialize controller
        self.controller = LinearSolverController()
        self.controller.initialize_tk_variables()

        # Initialize view
        self.view = LinearSolverView(root, self.controller)
        self.bind_variables()
        self.controller.set_view(self.view)
        
        # Build UI
        self.view.build_ui()
        
        # Add back button
        self.add_back_button()

    def bind_variables(self):
        """Bind controller variables to view"""
        self.view.num_vars = self.controller.num_vars_var
        self.view.sig_figs = self.controller.sig_figs_var
        self.view.scaling_enabled = self.controller.scaling_var
        self.view.step_by_step = self.controller.step_by_step_var
        self.view.method = self.controller.method_var
        self.view.lu_form = self.controller.lu_form_var
        self.view.max_iterations = self.controller.max_iterations_var
        self.view.abs_error = self.controller.abs_error_var
        
        self.view.on_method_change = self.controller.on_method_change
        self.view.on_lu_form_change = self.controller.on_lu_form_change
        self.view.solve_system = self.controller.solve
    
    def add_back_button(self):
        """Add back button to return to main menu"""
        back_btn = ctk.CTkButton(
            self.root,
            text="← Back to Main Menu",
            command=self.back_callback,
            font=ctk.CTkFont(family="Courier New", size=14),
            width=180,
            height=40,
            corner_radius=8,
            fg_color="transparent",
            border_width=2
        )
        back_btn.place(x=15, y=15)


class Phase2App:
    """Phase 2 Root Finding Application"""
    def __init__(self, root, back_callback):
        self.root = root
        self.back_callback = back_callback
        
        # Initialize controller
        self.controller = Phase2Controller()
        self.controller.initialize_tk_variables()
        
        # Initialize view
        self.view = Phase2View(root, self.controller)
        self.controller.set_view(self.view)
        
        # Build UI
        self.view.build_ui()
        
        # Add back button
        self.add_back_button()
    
    def add_back_button(self):
        """Add back button to return to main menu"""
        back_btn = ctk.CTkButton(
            self.root,
            text="← Back to Main Menu",
            command=self.back_callback,
            font=ctk.CTkFont(family="Courier New", size=14),
            width=180,
            height=40,
            corner_radius=8,
            fg_color="transparent",
            border_width=2,
            
        )
        back_btn.place(x=1100, y=15)


def main():
    """Main entry point"""
    root = ctk.CTk()
    app = PhaseSelectionApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
