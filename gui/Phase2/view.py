# import customtkinter as ctk
# import numpy as np
# import matplotlib.pyplot as plt
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# from matplotlib.figure import Figure
# from solverEngine2.phase2_solver import parse_equation, RootFinderResult
# from D import D, get_sig_figs


# class Phase2View:
#     def __init__(self, root, controller):
#         self.root = root
#         self.controller = controller
        
#         # UI Components
#         self.equation_entry = None
#         self.output_text = None
#         self.plot_canvas = None
#         self.plot_figure = None

#     def build_ui(self):
        
#         # Main container
#         main_container = ctk.CTkFrame(self.root, fg_color="#1a1a1a")
#         main_container.pack(fill="both", expand=True, padx=10, pady=10)
        
#         # Left column - Input and parameters
#         left_col = ctk.CTkFrame(
#             main_container, 
#             fg_color=("#2b2b2b", "#1f1f1f"), 
#             corner_radius=10,
#             width=500
#         )
#         left_col.pack(side="left", fill="both", expand=False, padx=(0, 5))
#         left_col.pack_propagate(False)
        
#         # Right column - Plot and output
#         right_col = ctk.CTkFrame(
#             main_container, 
#             fg_color=("#2b2b2b", "#1f1f1f"), 
#             corner_radius=10
#         )
#         right_col.pack(side="left", fill="both", expand=True, padx=(5, 0))
        
#         # Build sections
#         self.create_input_section(left_col)
#         self.create_plot_section(right_col)
#         self.create_output_section(right_col)
    
#     def create_input_section(self, parent):
#         # Title
#         title = ctk.CTkLabel(
#             parent,
#             text="Root Finder - Bisection Method",
#             font=ctk.CTkFont(family="Courier New", size=18, weight="bold")
#         )
#         title.pack(pady=(15, 10), padx=15, anchor="w")
        
#         # Scrollable frame for inputs
#         scroll_frame = ctk.CTkScrollableFrame(
#             parent,
#             fg_color="transparent"
#         )
#         scroll_frame.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        
#         # Equation input
#         ctk.CTkLabel(
#             scroll_frame,
#             text="Equation (f(x) = 0):",
#             font=ctk.CTkFont(family="Courier New", size=14, weight="bold")
#         ).pack(anchor="w", pady=(10, 5))
        
#         self.equation_entry = ctk.CTkEntry(
#             scroll_frame,
#             textvariable=self.controller.equation_var,
#             height=40,
#             font=ctk.CTkFont(family="Courier New", size=14),
#             placeholder_text="e.g., x^3 - x - 2"
#         )
#         self.equation_entry.pack(fill="x", pady=(0, 5))
        
#         # Helper text
#         ctk.CTkLabel(
#             scroll_frame,
#             text="Supported: +, -, *, /, ^, exp(), sin(), cos(), ln(), log()",
#             font=ctk.CTkFont(family="Courier New", size=11),
#             text_color="gray"
#         ).pack(anchor="w", pady=(0, 10))
        
#         # Method (locked to Bisection for now)
#         ctk.CTkLabel(
#             scroll_frame,
#             text="Method:",
#             font=ctk.CTkFont(family="Courier New", size=14, weight="bold")
#         ).pack(anchor="w", pady=(5, 5))
        
#         ctk.CTkOptionMenu(
#             scroll_frame,
#             values=["Bisection"],
#             variable=self.controller.method_var,
#             height=35,
#             font=ctk.CTkFont(family="Courier New", size=13),
#             state="disabled"
#         ).pack(fill="x", pady=(0, 10))
        
#         # Interval inputs
#         ctk.CTkLabel(
#             scroll_frame,
#             text="Interval [Xl, Xu]:",
#             font=ctk.CTkFont(family="Courier New", size=14, weight="bold")
#         ).pack(anchor="w", pady=(5, 5))
        
#         interval_frame = ctk.CTkFrame(scroll_frame, fg_color="transparent")
#         interval_frame.pack(fill="x", pady=(0, 10))
        
#         ctk.CTkLabel(
#             interval_frame,
#             text="Xl:",
#             font=ctk.CTkFont(family="Courier New", size=13)
#         ).pack(side="left", padx=(0, 5))
        
#         ctk.CTkEntry(
#             interval_frame,
#             textvariable=self.controller.xl_var,
#             width=100,
#             height=35,
#             font=ctk.CTkFont(family="Courier New", size=13)
#         ).pack(side="left", padx=(0, 15))
        
#         ctk.CTkLabel(
#             interval_frame,
#             text="Xu:",
#             font=ctk.CTkFont(family="Courier New", size=13)
#         ).pack(side="left", padx=(0, 5))
        
#         ctk.CTkEntry(
#             interval_frame,
#             textvariable=self.controller.xu_var,
#             width=100,
#             height=35,
#             font=ctk.CTkFont(family="Courier New", size=13)
#         ).pack(side="left")
        
#         # Parameters section
#         ctk.CTkLabel(
#             scroll_frame,
#             text="Parameters:",
#             font=ctk.CTkFont(family="Courier New", size=14, weight="bold")
#         ).pack(anchor="w", pady=(10, 5))
        
#         # Max iterations
#         iter_frame = ctk.CTkFrame(scroll_frame, fg_color="transparent")
#         iter_frame.pack(fill="x", pady=5)
        
#         ctk.CTkLabel(
#             iter_frame,
#             text="Max Iterations:",
#             font=ctk.CTkFont(family="Courier New", size=13),
#             width=150
#         ).pack(side="left", padx=(0, 5))
        
#         ctk.CTkEntry(
#             iter_frame,
#             textvariable=self.controller.max_iterations_var,
#             width=100,
#             height=35,
#             font=ctk.CTkFont(family="Courier New", size=13)
#         ).pack(side="left")
        
#         # Epsilon
#         eps_frame = ctk.CTkFrame(scroll_frame, fg_color="transparent")
#         eps_frame.pack(fill="x", pady=5)
        
#         ctk.CTkLabel(
#             eps_frame,
#             text="Epsilon (ε):",
#             font=ctk.CTkFont(family="Courier New", size=13),
#             width=150
#         ).pack(side="left", padx=(0, 5))
        
#         ctk.CTkEntry(
#             eps_frame,
#             textvariable=self.controller.epsilon_var,
#             width=100,
#             height=35,
#             font=ctk.CTkFont(family="Courier New", size=13)
#         ).pack(side="left")
        
#         # Significant figures
#         sig_frame = ctk.CTkFrame(scroll_frame, fg_color="transparent")
#         sig_frame.pack(fill="x", pady=5)
        
#         ctk.CTkLabel(
#             sig_frame,
#             text="Significant Figures:",
#             font=ctk.CTkFont(family="Courier New", size=13),
#             width=150
#         ).pack(side="left", padx=(0, 5))
        
#         ctk.CTkEntry(
#             sig_frame,
#             textvariable=self.controller.sig_figs_var,
#             width=100,
#             height=35,
#             font=ctk.CTkFont(family="Courier New", size=13)
#         ).pack(side="left")
        
#         # Step by step checkbox
#         ctk.CTkCheckBox(
#             scroll_frame,
#             text="Step-by-Step Solution",
#             variable=self.controller.step_by_step_var,
#             font=ctk.CTkFont(family="Courier New", size=13, weight="bold")
#         ).pack(anchor="w", pady=(10, 10))
        
#         # Buttons
#         button_frame = ctk.CTkFrame(scroll_frame, fg_color="transparent")
#         button_frame.pack(fill="x", pady=(10, 5))
        
#         ctk.CTkButton(
#             button_frame,
#             text="Plot Function",
#             command=self.controller.plot_function,
#             font=ctk.CTkFont(family="Courier New", size=14, weight="bold"),
#             height=45,
#             corner_radius=8,
#             fg_color="#2563eb",
#             hover_color="#1d4ed8"
#         ).pack(fill="x", pady=(0, 10))
        
#         ctk.CTkButton(
#             button_frame,
#             text="SOLVE",
#             command=self.controller.solve,
#             font=ctk.CTkFont(family="Courier New", size=16, weight="bold"),
#             height=50,
#             corner_radius=8,
#             fg_color="#16a34a",
#             hover_color="#15803d"
#         ).pack(fill="x")
    
#     def create_plot_section(self, parent):
#         plot_container = ctk.CTkFrame(parent, fg_color="transparent")
#         plot_container.pack(fill="both", expand=True, padx=15, pady=(15, 5))
        
#         ctk.CTkLabel(
#             plot_container,
#             text="Function Plot",
#             font=ctk.CTkFont(family="Courier New", size=16, weight="bold")
#         ).pack(anchor="w", pady=(0, 10))
        
#         # Create matplotlib figure
#         self.plot_figure = Figure(figsize=(8, 4), dpi=100, facecolor='#2b2b2b')
#         self.plot_canvas = FigureCanvasTkAgg(self.plot_figure, plot_container)
#         self.plot_canvas.get_tk_widget().pack(fill="both", expand=True)
        
#         # Initial empty plot
#         ax = self.plot_figure.add_subplot(111)
#         ax.set_facecolor('#1f1f1f')
#         ax.grid(True, alpha=0.3, color='gray')
#         ax.set_xlabel('x', color='white', fontsize=12)
#         ax.set_ylabel('f(x)', color='white', fontsize=12)
#         ax.tick_params(colors='white')
#         ax.spines['bottom'].set_color('white')
#         ax.spines['top'].set_color('white')
#         ax.spines['left'].set_color('white')
#         ax.spines['right'].set_color('white')
#         ax.text(0.5, 0.5, 'Click "Plot Function" to visualize', 
#                 ha='center', va='center', transform=ax.transAxes,
#                 color='gray', fontsize=14)
#         self.plot_canvas.draw()
    
#     def create_output_section(self, parent):
#         output_container = ctk.CTkFrame(parent, fg_color="transparent")
#         output_container.pack(fill="both", expand=True, padx=15, pady=(5, 15))
        
#         ctk.CTkLabel(
#             output_container,
#             text="Results",
#             font=ctk.CTkFont(family="Courier New", size=16, weight="bold")
#         ).pack(anchor="w", pady=(0, 10))
        
#         self.output_text = ctk.CTkTextbox(
#             output_container,
#             font=ctk.CTkFont(family="Courier New", size=13),
#             corner_radius=8
#         )
#         self.output_text.pack(fill="both", expand=True)
    
#     def plot_equation(self, equation: str, xl: float, xu: float):
       
#         try:
#             func = parse_equation(equation)
            
#             # Generate x values
#             margin = (xu - xl) * 0.2
#             x_min = xl - margin
#             x_max = xu + margin
#             x_vals = np.linspace(x_min, x_max, 500)
            
#             # Calculate y values
#             y_vals = [func(x) for x in x_vals]
            
#             # Clear and create new plot
#             self.plot_figure.clear()
#             ax = self.plot_figure.add_subplot(111)
#             ax.set_facecolor('#1f1f1f')
            
#             # Plot function
#             ax.plot(x_vals, y_vals, 'cyan', linewidth=2, label='f(x)')
#             ax.axhline(y=0, color='white', linestyle='--', linewidth=1, alpha=0.5)
#             ax.axvline(x=0, color='white', linestyle='--', linewidth=1, alpha=0.5)
            
#             # Highlight interval
#             ax.axvline(x=xl, color='yellow', linestyle='--', linewidth=1.5, alpha=0.7, label=f'Xl = {xl}')
#             ax.axvline(x=xu, color='orange', linestyle='--', linewidth=1.5, alpha=0.7, label=f'Xu = {xu}')
            
#             # Styling
#             ax.grid(True, alpha=0.3, color='gray')
#             ax.set_xlabel('x', color='white', fontsize=12)
#             ax.set_ylabel('f(x)', color='white', fontsize=12)
#             ax.set_title(f'f(x) = {equation}', color='white', fontsize=14)
#             ax.tick_params(colors='white')
#             ax.spines['bottom'].set_color('white')
#             ax.spines['top'].set_color('white')
#             ax.spines['left'].set_color('white')
#             ax.spines['right'].set_color('white')
#             ax.legend(facecolor='#2b2b2b', edgecolor='white', labelcolor='white')
            
#             self.plot_figure.tight_layout()
#             self.plot_canvas.draw()
            
#         except Exception as e:
#             self.display_error(f"Error plotting function: {str(e)}")
    
       
    
#     def display_result(self, result: RootFinderResult):
#       self.output_text.delete("1.0", "end")
    
#       self.output_text.insert("end", "="*70 + "\n")
#       self.output_text.insert("end", "BISECTION METHOD RESULTS\n")
#       self.output_text.insert("end", "="*70 + "\n\n")
    
#       if result.error_message:
#         self.output_text.insert("end", f"⚠ Warning: {result.error_message}\n\n")
    
#       if result.root is not None:
#         # Get significant figures
#            sig_figs = get_sig_figs()
#            root_d = D(result.root)
#            self.output_text.insert("end", f"Approximate Root: {root_d}\n")
#            self.output_text.insert("end", f"Number of Iterations: {result.iterations}\n")
#            self.output_text.insert("end", f"Approximate Relative Error: {result.approximate_error:.6f}%\n")
#            self.output_text.insert("end", f"Execution Time: {result.execution_time:.6f} seconds\n")
#            self.output_text.insert("end", f"Significant Figures: {sig_figs}\n")
#            self.output_text.insert("end", f"Status: {'✓ Converged' if result.converged else '✗ Did not converge'}\n")
        
#            if result.steps:
#               self.output_text.insert("end", "\n" + "="*70 + "\n")
#               self.output_text.insert("end", "STEP-BY-STEP SOLUTION\n")
#               self.output_text.insert("end", "="*70 + "\n\n")
            
#               for step in result.steps:
#                   if step['type'] == 'info':
#                     self.output_text.insert("end", f"{step['message']}\n")
#                     # Remove .6f formatting - these are already strings
#                     self.output_text.insert("end", f"f(Xl) = f({step['xl']}) = {step['f_xl']}\n")
#                     self.output_text.insert("end", f"f(Xu) = f({step['xu']}) = {step['f_xu']}\n")
#                     self.output_text.insert("end", f"Required iterations: {step['required_iterations']}\n\n")
                    
#                     # Create table header with proper column widths
#                     col_width = sig_figs + 7
#                     self.output_text.insert("end", f"{'Iter':<6} {'Xl':<{col_width}} {'Xu':<{col_width}} {'Xr':<{col_width}} {'f(Xr)':<15} {'Error %':<15}\n")
#                     self.output_text.insert("end", "-"*100 + "\n")
                
#                   elif step['type'] == 'iteration':
#                       error_str = f"{step['error']:.6f}" if step['error'] is not None else "N/A"
#                       col_width = max(15, sig_figs + 7)
                    
#                     # Remove .6f formatting from f_xr - it's already a string
#                       self.output_text.insert("end", 
#                         f"{step['iteration']:<6} "
#                         f"{step['xl']:<{col_width}} "
#                         f"{step['xu']:<{col_width}} "
#                         f"{step['xr']:<{col_width}} "
#                         f"{step['f_xr']:<{col_width}} "
#                         f"{error_str:<15}\n"
#                       )
    
#     def display_error(self, message: str):
#         self.output_text.delete("1.0", "end")
#         self.output_text.insert("end", "="*70 + "\n")
#         self.output_text.insert("end", "ERROR\n")
#         self.output_text.insert("end", "="*70 + "\n\n")
#         self.output_text.insert("end", f"{message}\n")
import customtkinter as ctk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from solverEngine2.base.equation_parser import parse_equation
from solverEngine2.base.data_classes import RootFinderResult
from D import D, get_sig_figs


class Phase2View:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller
        
        # UI Components
        self.equation_entry = None
        self.output_text = None
        self.plot_canvas = None
        self.plot_figure = None
        
        # Method-specific parameter frames
        self.interval_frame = None      # For Bisection, False Position
        self.fixed_point_frame = None   # For Fixed Point
        self.newton_frame = None        # For Newton-Raphson, Modified Newton
        self.secant_frame = None        # For Secant
        self.modified_newton_frame = None  # For Modified Newton only

    def build_ui(self):
        # Main container
        main_container = ctk.CTkFrame(self.root, fg_color="#1a1a1a")
        main_container.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Left column - Input and parameters
        left_col = ctk.CTkFrame(
            main_container, 
            fg_color=("#2b2b2b", "#1f1f1f"), 
            corner_radius=10,
            width=500
        )
        left_col.pack(side="left", fill="both", expand=False, padx=(0, 5))
        left_col.pack_propagate(False)
        
        # Right column - Plot and output
        right_col = ctk.CTkFrame(
            main_container, 
            fg_color=("#2b2b2b", "#1f1f1f"), 
            corner_radius=10
        )
        right_col.pack(side="left", fill="both", expand=True, padx=(5, 0))
        
        # Build sections
        self.create_input_section(left_col)
        self.create_plot_section(right_col)
        self.create_output_section(right_col)
    
    def create_input_section(self, parent):
        # Title
        title = ctk.CTkLabel(
            parent,
            text="Root Finder - All Methods",
            font=ctk.CTkFont(family="Courier New", size=18, weight="bold")
        )
        title.pack(pady=(15, 10), padx=15, anchor="w")
        
        # Scrollable frame for inputs
        scroll_frame = ctk.CTkScrollableFrame(
            parent,
            fg_color="transparent"
        )
        scroll_frame.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        
        # ========== EQUATION INPUT ==========
        ctk.CTkLabel(
            scroll_frame,
            text="Equation (f(x) = 0):",
            font=ctk.CTkFont(family="Courier New", size=14, weight="bold")
        ).pack(anchor="w", pady=(10, 5))
        
        self.equation_entry = ctk.CTkEntry(
            scroll_frame,
            textvariable=self.controller.equation_var,
            height=40,
            font=ctk.CTkFont(family="Courier New", size=14),
            placeholder_text="e.g., x^3 - x - 2"
        )
        self.equation_entry.pack(fill="x", pady=(0, 5))
        
        # Helper text
        ctk.CTkLabel(
            scroll_frame,
            text="Supported: +, -, *, /, ^, exp(), sin(), cos(), ln(), log(), sqrt()",
            font=ctk.CTkFont(family="Courier New", size=11),
            text_color="gray"
        ).pack(anchor="w", pady=(0, 10))
        
        # ========== METHOD SELECTION ==========
        ctk.CTkLabel(
            scroll_frame,
            text="Method:",
            font=ctk.CTkFont(family="Courier New", size=14, weight="bold")
        ).pack(anchor="w", pady=(5, 5))
        
        # Get available methods from controller
        available_methods = self.controller.get_available_methods()
        
        method_menu = ctk.CTkOptionMenu(
            scroll_frame,
            values=available_methods,
            variable=self.controller.method_var,
            command=self.controller.on_method_change,  # Callback when method changes
            height=35,
            font=ctk.CTkFont(family="Courier New", size=13)
        )
        method_menu.pack(fill="x", pady=(0, 10))
        
        # ========== METHOD-SPECIFIC PARAMETERS ==========
        # These frames will be shown/hidden based on selected method
        
        # 1. INTERVAL FRAME (Bisection, False Position)
        self.interval_frame = ctk.CTkFrame(scroll_frame, fg_color="transparent")
        
        ctk.CTkLabel(
            self.interval_frame,
            text="Interval [Xl, Xu]:",
            font=ctk.CTkFont(family="Courier New", size=14, weight="bold")
        ).pack(anchor="w", pady=(5, 5))
        
        interval_inputs = ctk.CTkFrame(self.interval_frame, fg_color="transparent")
        interval_inputs.pack(fill="x", pady=(0, 10))
        
        ctk.CTkLabel(
            interval_inputs,
            text="Xl:",
            font=ctk.CTkFont(family="Courier New", size=13)
        ).pack(side="left", padx=(0, 5))
        
        ctk.CTkEntry(
            interval_inputs,
            textvariable=self.controller.xl_var,
            width=100,
            height=35,
            font=ctk.CTkFont(family="Courier New", size=13)
        ).pack(side="left", padx=(0, 15))
        
        ctk.CTkLabel(
            interval_inputs,
            text="Xu:",
            font=ctk.CTkFont(family="Courier New", size=13)
        ).pack(side="left", padx=(0, 5))
        
        ctk.CTkEntry(
            interval_inputs,
            textvariable=self.controller.xu_var,
            width=100,
            height=35,
            font=ctk.CTkFont(family="Courier New", size=13)
        ).pack(side="left")
        
        # 2. FIXED POINT FRAME
        self.fixed_point_frame = ctk.CTkFrame(scroll_frame, fg_color="transparent")
        
        ctk.CTkLabel(
            self.fixed_point_frame,
            text="Fixed Point Parameters:",
            font=ctk.CTkFont(family="Courier New", size=14, weight="bold")
        ).pack(anchor="w", pady=(5, 5))
        
        # g(x) equation
        ctk.CTkLabel(
            self.fixed_point_frame,
            text="g(x) equation (x = g(x)):",
            font=ctk.CTkFont(family="Courier New", size=13)
        ).pack(anchor="w", pady=(0, 3))
        
        ctk.CTkEntry(
            self.fixed_point_frame,
            textvariable=self.controller.g_equation_var,
            height=35,
            font=ctk.CTkFont(family="Courier New", size=13),
            placeholder_text="e.g., (x + 2)^(1/3)"
        ).pack(fill="x", pady=(0, 8))
        
        # Initial guess x0
        x0_frame = ctk.CTkFrame(self.fixed_point_frame, fg_color="transparent")
        x0_frame.pack(fill="x", pady=(0, 10))
        
        ctk.CTkLabel(
            x0_frame,
            text="Initial Guess (x₀):",
            font=ctk.CTkFont(family="Courier New", size=13),
            width=150
        ).pack(side="left", padx=(0, 5))
        
        ctk.CTkEntry(
            x0_frame,
            textvariable=self.controller.x0_var,
            width=120,
            height=35,
            font=ctk.CTkFont(family="Courier New", size=13)
        ).pack(side="left")
        
        # 3. NEWTON FRAME (Newton-Raphson, Modified Newton)
        self.newton_frame = ctk.CTkFrame(scroll_frame, fg_color="transparent")
        
        ctk.CTkLabel(
            self.newton_frame,
            text="Newton Method Parameters:",
            font=ctk.CTkFont(family="Courier New", size=14, weight="bold")
        ).pack(anchor="w", pady=(5, 5))
        
        # Derivative equation (optional)
        ctk.CTkLabel(
            self.newton_frame,
            text="f'(x) - Derivative (optional, will use numerical if empty):",
            font=ctk.CTkFont(family="Courier New", size=11),
            text_color="gray"
        ).pack(anchor="w", pady=(0, 3))
        
        ctk.CTkEntry(
            self.newton_frame,
            textvariable=self.controller.derivative_var,
            height=35,
            font=ctk.CTkFont(family="Courier New", size=13),
            placeholder_text="e.g., 3*x^2 - 1"
        ).pack(fill="x", pady=(0, 8))
        
        # Initial guess x0
        newton_x0_frame = ctk.CTkFrame(self.newton_frame, fg_color="transparent")
        newton_x0_frame.pack(fill="x", pady=(0, 10))
        
        ctk.CTkLabel(
            newton_x0_frame,
            text="Initial Guess (x₀):",
            font=ctk.CTkFont(family="Courier New", size=13),
            width=150
        ).pack(side="left", padx=(0, 5))
        
        ctk.CTkEntry(
            newton_x0_frame,
            textvariable=self.controller.x0_var,
            width=120,
            height=35,
            font=ctk.CTkFont(family="Courier New", size=13)
        ).pack(side="left")
        
        # 4. MODIFIED NEWTON FRAME (additional parameter)
        self.modified_newton_frame = ctk.CTkFrame(scroll_frame, fg_color="transparent")
        
        mult_frame = ctk.CTkFrame(self.modified_newton_frame, fg_color="transparent")
        mult_frame.pack(fill="x", pady=(0, 10))
        
        ctk.CTkLabel(
            mult_frame,
            text="Root Multiplicity (m):",
            font=ctk.CTkFont(family="Courier New", size=13),
            width=150
        ).pack(side="left", padx=(0, 5))
        
        ctk.CTkEntry(
            mult_frame,
            textvariable=self.controller.multiplicity_var,
            width=120,
            height=35,
            font=ctk.CTkFont(family="Courier New", size=13)
        ).pack(side="left")
        
        # 5. SECANT FRAME
        self.secant_frame = ctk.CTkFrame(scroll_frame, fg_color="transparent")
        
        ctk.CTkLabel(
            self.secant_frame,
            text="Secant Method Parameters:",
            font=ctk.CTkFont(family="Courier New", size=14, weight="bold")
        ).pack(anchor="w", pady=(5, 5))
        
        # Two initial guesses
        secant_x0_frame = ctk.CTkFrame(self.secant_frame, fg_color="transparent")
        secant_x0_frame.pack(fill="x", pady=5)
        
        ctk.CTkLabel(
            secant_x0_frame,
            text="First Guess (x₀):",
            font=ctk.CTkFont(family="Courier New", size=13),
            width=150
        ).pack(side="left", padx=(0, 5))
        
        ctk.CTkEntry(
            secant_x0_frame,
            textvariable=self.controller.x0_var,
            width=120,
            height=35,
            font=ctk.CTkFont(family="Courier New", size=13)
        ).pack(side="left")
        
        secant_x1_frame = ctk.CTkFrame(self.secant_frame, fg_color="transparent")
        secant_x1_frame.pack(fill="x", pady=(0, 10))
        
        ctk.CTkLabel(
            secant_x1_frame,
            text="Second Guess (x₁):",
            font=ctk.CTkFont(family="Courier New", size=13),
            width=150
        ).pack(side="left", padx=(0, 5))
        
        ctk.CTkEntry(
            secant_x1_frame,
            textvariable=self.controller.x1_var,
            width=120,
            height=35,
            font=ctk.CTkFont(family="Courier New", size=13)
        ).pack(side="left")
        
        # ========== COMMON PARAMETERS ==========
        ctk.CTkLabel(
            scroll_frame,
            text="Common Parameters:",
            font=ctk.CTkFont(family="Courier New", size=14, weight="bold")
        ).pack(anchor="w", pady=(10, 5))
        
        # Max iterations
        iter_frame = ctk.CTkFrame(scroll_frame, fg_color="transparent")
        iter_frame.pack(fill="x", pady=5)
        
        ctk.CTkLabel(
            iter_frame,
            text="Max Iterations:",
            font=ctk.CTkFont(family="Courier New", size=13),
            width=150
        ).pack(side="left", padx=(0, 5))
        
        ctk.CTkEntry(
            iter_frame,
            textvariable=self.controller.max_iterations_var,
            width=100,
            height=35,
            font=ctk.CTkFont(family="Courier New", size=13)
        ).pack(side="left")
        
        # Epsilon
        eps_frame = ctk.CTkFrame(scroll_frame, fg_color="transparent")
        eps_frame.pack(fill="x", pady=5)
        
        ctk.CTkLabel(
            eps_frame,
            text="Epsilon (ε):",
            font=ctk.CTkFont(family="Courier New", size=13),
            width=150
        ).pack(side="left", padx=(0, 5))
        
        ctk.CTkEntry(
            eps_frame,
            textvariable=self.controller.epsilon_var,
            width=100,
            height=35,
            font=ctk.CTkFont(family="Courier New", size=13)
        ).pack(side="left")
        
        # Significant figures
        sig_frame = ctk.CTkFrame(scroll_frame, fg_color="transparent")
        sig_frame.pack(fill="x", pady=5)
        
        ctk.CTkLabel(
            sig_frame,
            text="Significant Figures:",
            font=ctk.CTkFont(family="Courier New", size=13),
            width=150
        ).pack(side="left", padx=(0, 5))
        
        ctk.CTkEntry(
            sig_frame,
            textvariable=self.controller.sig_figs_var,
            width=100,
            height=35,
            font=ctk.CTkFont(family="Courier New", size=13)
        ).pack(side="left")
        
        # Step by step checkbox
        ctk.CTkCheckBox(
            scroll_frame,
            text="Step-by-Step Solution",
            variable=self.controller.step_by_step_var,
            font=ctk.CTkFont(family="Courier New", size=13, weight="bold")
        ).pack(anchor="w", pady=(10, 10))
        
        # ========== BUTTONS ==========
        button_frame = ctk.CTkFrame(scroll_frame, fg_color="transparent")
        button_frame.pack(fill="x", pady=(10, 5))
        
        ctk.CTkButton(
            button_frame,
            text="Plot Function",
            command=self.controller.plot_function,
            font=ctk.CTkFont(family="Courier New", size=14, weight="bold"),
            height=45,
            corner_radius=8,
            fg_color="#2563eb",
            hover_color="#1d4ed8"
        ).pack(fill="x", pady=(0, 10))
        
        ctk.CTkButton(
            button_frame,
            text="SOLVE",
            command=self.controller.solve,
            font=ctk.CTkFont(family="Courier New", size=16, weight="bold"),
            height=50,
            corner_radius=8,
            fg_color="#16a34a",
            hover_color="#15803d"
        ).pack(fill="x")
        
        # Initialize with Bisection method visible
        self.update_parameter_visibility("Bisection")
    
    def update_parameter_visibility(self, method: str):
        """
        Show/hide parameter input frames based on selected method.
        Called by controller when method changes.
        """
        # Hide all method-specific frames first
        self.interval_frame.pack_forget()
        self.fixed_point_frame.pack_forget()
        self.newton_frame.pack_forget()
        self.modified_newton_frame.pack_forget()
        self.secant_frame.pack_forget()
        
        # Show relevant frames based on method
        if method in ["Bisection", "False-Position"]:
            self.interval_frame.pack(fill="x", pady=(0, 10), before=self.interval_frame.master.winfo_children()[-6])
        
        elif method == "Fixed Point":
            self.fixed_point_frame.pack(fill="x", pady=(0, 10), before=self.fixed_point_frame.master.winfo_children()[-6])
        
        elif method == "Newton-Raphson":
            self.newton_frame.pack(fill="x", pady=(0, 10), before=self.newton_frame.master.winfo_children()[-6])
        
        elif method == "Modified Newton-Raphson":
            self.newton_frame.pack(fill="x", pady=(0, 10), before=self.newton_frame.master.winfo_children()[-6])
            self.modified_newton_frame.pack(fill="x", pady=(0, 10), before=self.modified_newton_frame.master.winfo_children()[-6])
        
        elif method == "Secant":
            self.secant_frame.pack(fill="x", pady=(0, 10), before=self.secant_frame.master.winfo_children()[-6])
    
    def create_plot_section(self, parent):
        plot_container = ctk.CTkFrame(parent, fg_color="transparent")
        plot_container.pack(fill="both", expand=True, padx=15, pady=(15, 5))
        
        ctk.CTkLabel(
            plot_container,
            text="Function Plot",
            font=ctk.CTkFont(family="Courier New", size=16, weight="bold")
        ).pack(anchor="w", pady=(0, 10))
        
        # Create matplotlib figure
        # self.plot_figure = Figure(figsize=(8, 4), dpi=100, facecolor='#2b2b2b')
        # self.plot_canvas = FigureCanvasTkAgg(self.plot_figure, plot_container)
        # self.plot_canvas.get_tk_widget().pack(fill="both", expand=True)
        self.plot_figure = Figure(figsize=(10, 4), dpi=100, facecolor='#2b2b2b')
        self.plot_canvas = FigureCanvasTkAgg(self.plot_figure, plot_container)
        self.plot_canvas.get_tk_widget().pack(fill="both", expand=True)
        
        # Initial empty plot
        ax = self.plot_figure.add_subplot(111)
        ax.set_facecolor('#1f1f1f')
        ax.grid(True, alpha=0.3, color='gray')
        ax.set_xlabel('x', color='white', fontsize=12)
        ax.set_ylabel('f(x)', color='white', fontsize=12)
        ax.tick_params(colors='white')
        ax.spines['bottom'].set_color('white')
        ax.spines['top'].set_color('white')
        ax.spines['left'].set_color('white')
        ax.spines['right'].set_color('white')
        ax.text(0.5, 0.5, 'Click "Plot Function" to visualize', 
                ha='center', va='center', transform=ax.transAxes,
                color='gray', fontsize=14)
        self.plot_canvas.draw()
    
    def create_output_section(self, parent):
        output_container = ctk.CTkFrame(parent, fg_color="transparent")
        output_container.pack(fill="both", expand=True, padx=15, pady=(5, 15))
        
        ctk.CTkLabel(
            output_container,
            text="Results",
            font=ctk.CTkFont(family="Courier New", size=16, weight="bold")
        ).pack(anchor="w", pady=(0, 10))
        
        self.output_text = ctk.CTkTextbox(
            output_container,
            font=ctk.CTkFont(family="Courier New", size=13),
            corner_radius=8
        )
        self.output_text.pack(fill="both", expand=True)
    
    def plot_equation(self, equation: str, xl: float, xu: float, method: str, g_equation: str = None):
        """
        Plot the equation(s) based on the selected method.
        For Fixed Point, also plots g(x) and y=x line.
        """
        try:
            func = parse_equation(equation)
            
            # Generate x values
            margin = (xu - xl) * 0.2
            x_min = xl - margin
            x_max = xu + margin
            x_vals = np.linspace(x_min, x_max, 500)
            
            # Calculate y values for f(x)
            y_vals = [float(func(x)) for x in x_vals]
            
            # Clear and create new plot
            self.plot_figure.clear()
            
            # ax = self.plot_figure.add_subplot(111)
            # ax.set_facecolor('#1f1f1f')
            
            # Plot based on method
            # if method == "Fixed Point" and g_equation:
            #     # For Fixed Point: plot both f(x), g(x), and y=x
            #     try:
            #         g_func = parse_equation(g_equation)
            #         g_vals = [float(g_func(x)) for x in x_vals]
                    
            #         ax.plot(x_vals, g_vals, 'cyan', linewidth=2, label='g(x)')
            #         ax.plot(x_vals, x_vals, 'yellow', linewidth=2, linestyle='--', label='y = x', alpha=0.7)
            #         ax.set_title(f'Fixed Point: x = g(x)', color='white', fontsize=14)
            #         ax.set_ylabel('y', color='white', fontsize=12)
            #     except:
            #         # If g(x) fails, just plot f(x)
            #         ax.plot(x_vals, y_vals, 'cyan', linewidth=2, label='f(x)')
            #         ax.axhline(y=0, color='white', linestyle='--', linewidth=1, alpha=0.5)
            #         ax.set_title(f'f(x) = {equation}', color='white', fontsize=14)
            #         ax.set_ylabel('f(x)', color='white', fontsize=12)
            # else:
            #     # For all other methods: plot f(x)
            #     ax.plot(x_vals, y_vals, 'cyan', linewidth=2, label='f(x)')
            #     ax.axhline(y=0, color='white', linestyle='--', linewidth=1, alpha=0.5)
            #     ax.set_title(f'f(x) = {equation}', color='white', fontsize=14)
            #     ax.set_ylabel('f(x)', color='white', fontsize=12)
            
            # # Add x and y axes
            # ax.axvline(x=0, color='white', linestyle='--', linewidth=1, alpha=0.5)
            if method == "Fixed Point" and g_equation:
                try:
                    g_func = parse_equation(g_equation)
                    g_vals = [float(g_func(x)) for x in x_vals]
                    
                    # Create two subplots side by side
                    ax1 = self.plot_figure.add_subplot(121)  # Left plot
                    ax2 = self.plot_figure.add_subplot(122)  # Right plot
                    
                    # LEFT PLOT: g(x) and y=x
                    ax1.set_facecolor('#1f1f1f')
                    ax1.plot(x_vals, g_vals, 'cyan', linewidth=2, label='g(x)')
                    ax1.plot(x_vals, x_vals, 'yellow', linewidth=2, linestyle='--', label='y = x', alpha=0.7)
                    ax1.axhline(y=0, color='white', linestyle='--', linewidth=1, alpha=0.3)
                    ax1.axvline(x=0, color='white', linestyle='--', linewidth=1, alpha=0.3)
                    ax1.grid(True, alpha=0.3, color='gray')
                    ax1.set_xlabel('x', color='white', fontsize=11)
                    ax1.set_ylabel('y', color='white', fontsize=11)
                    ax1.set_title('Fixed Point: x = g(x)', color='white', fontsize=12)
                    ax1.tick_params(colors='white', labelsize=9)
                    for spine in ax1.spines.values():
                        spine.set_color('white')
                    ax1.legend(facecolor='#2b2b2b', edgecolor='white', labelcolor='white', fontsize=9)
                    
                    # RIGHT PLOT: Original function f(x)
                    ax2.set_facecolor('#1f1f1f')
                    ax2.plot(x_vals, y_vals, 'lime', linewidth=2, label='f(x)')
                    ax2.axhline(y=0, color='white', linestyle='--', linewidth=1, alpha=0.5)
                    ax2.axvline(x=0, color='white', linestyle='--', linewidth=1, alpha=0.3)
                    ax2.grid(True, alpha=0.3, color='gray')
                    ax2.set_xlabel('x', color='white', fontsize=11)
                    ax2.set_ylabel('f(x)', color='white', fontsize=11)
                    ax2.set_title(f'Original: f(x) = {equation}', color='white', fontsize=12)
                    ax2.tick_params(colors='white', labelsize=9)
                    for spine in ax2.spines.values():
                        spine.set_color('white')
                    ax2.legend(facecolor='#2b2b2b', edgecolor='white', labelcolor='white', fontsize=9)
                    
                except Exception as e:
                    # If g(x) parsing fails, show error and just plot f(x)
                    ax = self.plot_figure.add_subplot(111)
                    ax.set_facecolor('#1f1f1f')
                    ax.plot(x_vals, y_vals, 'cyan', linewidth=2, label='f(x)')
                    ax.axhline(y=0, color='white', linestyle='--', linewidth=1, alpha=0.5)
                    ax.axvline(x=0, color='white', linestyle='--', linewidth=1, alpha=0.5)
                    ax.set_title(f'f(x) = {equation} (g(x) error)', color='white', fontsize=14)
                    ax.set_xlabel('x', color='white', fontsize=12)
                    ax.set_ylabel('f(x)', color='white', fontsize=12)
                    ax.grid(True, alpha=0.3, color='gray')
                    ax.tick_params(colors='white')
                    for spine in ax.spines.values():
                        spine.set_color('white')
            
            # ALL OTHER METHODS - SINGLE PLOT
            else:
                ax = self.plot_figure.add_subplot(111)
                ax.set_facecolor('#1f1f1f')
                
                # Plot f(x)
                ax.plot(x_vals, y_vals, 'cyan', linewidth=2, label='f(x)')
                ax.axhline(y=0, color='white', linestyle='--', linewidth=1, alpha=0.5)
                ax.axvline(x=0, color='white', linestyle='--', linewidth=1, alpha=0.5)
                
                # Highlight interval for interval-based methods
                if method in ["Bisection", "False-Position"]:
                    ax.axvline(x=xl, color='yellow', linestyle='--', linewidth=1.5, alpha=0.7, label=f'Xl = {xl}')
                    ax.axvline(x=xu, color='orange', linestyle='--', linewidth=1.5, alpha=0.7, label=f'Xu = {xu}')
                
                # Styling
                ax.grid(True, alpha=0.3, color='gray')
                ax.set_xlabel('x', color='white', fontsize=12)
                ax.set_ylabel('f(x)', color='white', fontsize=12)
                ax.set_title(f'f(x) = {equation}', color='white', fontsize=14)
                ax.tick_params(colors='white')
                for spine in ax.spines.values():
                    spine.set_color('white')
                ax.legend(facecolor='#2b2b2b', edgecolor='white', labelcolor='white')
            
            self.plot_figure.tight_layout()
            self.plot_canvas.draw()
            
        except Exception as e:
            self.display_error(f"Error plotting function: {str(e)}")
            # Highlight interval for interval-based methods
        #     if method in ["Bisection", "False-Position"]:
        #         ax.axvline(x=xl, color='yellow', linestyle='--', linewidth=1.5, alpha=0.7, label=f'Xl = {xl}')
        #         ax.axvline(x=xu, color='orange', linestyle='--', linewidth=1.5, alpha=0.7, label=f'Xu = {xu}')
            
        #     # Styling
        #     ax.grid(True, alpha=0.3, color='gray')
        #     ax.set_xlabel('x', color='white', fontsize=12)
        #     ax.tick_params(colors='white')
        #     ax.spines['bottom'].set_color('white')
        #     ax.spines['top'].set_color('white')
        #     ax.spines['left'].set_color('white')
        #     ax.spines['right'].set_color('white')
        #     ax.legend(facecolor='#2b2b2b', edgecolor='white', labelcolor='white')
            
        #     self.plot_figure.tight_layout()
        #     self.plot_canvas.draw()
            
        # except Exception as e:
        #     self.display_error(f"Error plotting function: {str(e)}")
    
    def display_result(self, result: RootFinderResult):
        self.output_text.delete("1.0", "end")
        
        # Get method name from controller
        method = self.controller.method_var.get()
        
        if (method == "Newton-Raphson"):
            self.display_result_newton(result)
            return
        elif (method == "Modified Newton-Raphson"):
            self.display_result_modified_newton(result)
            return
        elif (method == "Secant"):
            self.display_result_secant(result)
            return
        self.output_text.insert("end", "="*70 + "\n")
        self.output_text.insert("end", f"{method.upper()} METHOD RESULTS\n")
        self.output_text.insert("end", "="*70 + "\n\n")
        
        if result.error_message:
            self.output_text.insert("end", f"⚠ Warning: {result.error_message}\n\n")
        
        if result.root is not None:
            sig_figs = get_sig_figs()
            root_d = D(result.root)
            f_root_d = D(result.f_root)
            approximate_error = D(result.approximate_error)
            
            self.output_text.insert("end", f"Approximate Root: {root_d}\n")
            self.output_text.insert("end", f"Function value at root f(xr): {f_root_d}\n")
            self.output_text.insert("end", f"Number of Iterations: {result.iterations}\n")
            self.output_text.insert("end", f"Approximate Relative Error: {approximate_error}\n")
            self.output_text.insert("end", f"Execution Time: {result.execution_time:.6f} seconds\n")
            self.output_text.insert("end", f"Significant Figures: {sig_figs}\n")
            self.output_text.insert("end", f"Status: {'✓ Converged' if result.converged else '✗ Did not converge'}\n")
            
            if result.steps:
                self.output_text.insert("end", "\n" + "="*70 + "\n")
                self.output_text.insert("end", "STEP-BY-STEP SOLUTION\n")
                self.output_text.insert("end", "="*70 + "\n\n")
                if method in ["Bisection", "False-Position"]:
                  self.display_interval_steps(result.steps, sig_figs)
                elif method == "Fixed Point":
                  self.display_fixed_point_steps(result.steps, sig_figs)
        # self.output_text.insert("end", "="*70 + "\n")
        # self.output_text.insert("end", f"{method.upper()} METHOD RESULTS\n")
        # self.output_text.insert("end", "="*70 + "\n\n")
        
        # if result.error_message:
        #     self.output_text.insert("end", f"⚠ Warning: {result.error_message}\n\n")
        
        # if result.root is not None:
        #     # Get significant figures
        #     sig_figs = get_sig_figs()
        #     root_d = D(result.root)
        #     f_root_d=D(result.f_root)
            
        #     self.output_text.insert("end", f"Approximate Root: {root_d}\n")
        #     self.output_text.insert("end", f"Function value at root f(xr): {f_root_d}\n")

        #     self.output_text.insert("end", f"Number of Iterations: {result.iterations}\n")
        #     self.output_text.insert("end", f"Approximate Relative Error: {result.approximate_error:.6f}%\n")
        #     self.output_text.insert("end", f"Execution Time: {result.execution_time:.6f} seconds\n")
        #     self.output_text.insert("end", f"Significant Figures: {sig_figs}\n")
        #     self.output_text.insert("end", f"Status: {'✓ Converged' if result.converged else '✗ Did not converge'}\n")
            
        #     # Display step-by-step if available
        #     if result.steps:
        #         self.output_text.insert("end", "\n" + "="*70 + "\n")
        #         self.output_text.insert("end", "STEP-BY-STEP SOLUTION\n")
        #         self.output_text.insert("end", "="*70 + "\n\n")
                
        #         for step in result.steps:
        #             if step['type'] == 'info':
        #                 self.output_text.insert("end", f"{step['message']}\n")
        #                 if 'xl' in step:
        #                     self.output_text.insert("end", f"f(Xl) = f({step['xl']}) = {step['f_xl']}\n")
        #                     self.output_text.insert("end", f"f(Xu) = f({step['xu']}) = {step['f_xu']}\n")
        #                 if 'required_iterations' in step:
        #                     self.output_text.insert("end", f"Required iterations: {step['required_iterations']}\n\n")
                        
        #                 # Create table header
        #                 col_width = sig_figs + 7
        #                 self.output_text.insert("end", f"{'Iter':<6} {'Xl':<{col_width}} {'Xu':<{col_width}} {'Xr':<{col_width}} {'f(Xr)':<15} {'Error %':<15}\n")
        #                 self.output_text.insert("end", "-"*100 + "\n")
                    
        #             elif step['type'] == 'iteration':
        #                 error_str = f"{step['error']:.6f}" if step['error'] is not None else "N/A"
        #                 col_width = max(15, sig_figs + 7)
                        
        #                 self.output_text.insert("end", 
        #                     f"{step['iteration']:<6} "
        #                     f"{step.get('xl', 'N/A'):<{col_width}} "
        #                     f"{step.get('xu', 'N/A'):<{col_width}} "
        #                     f"{step.get('xr', 'N/A'):<{col_width}} "
        #                     f"{step.get('f_xr', 'N/A'):<{col_width}} "
        #                     f"{error_str:<15}\n"
        #                 )
                    
        #             elif step['type'] == 'converged':
        #                 self.output_text.insert("end", f"\n{step['message']}\n")
        #                 if 'xr' in step:
        #                     self.output_text.insert("end", f"Final xr: {step['xr']}\n")
        #                 if 'f_xr' in step:
        #                     self.output_text.insert("end", f"f(xr): {step['f_xr']}\n")
    
    def display_error(self, message: str):
        """Display an error message"""
        self.output_text.delete("1.0", "end")
        self.output_text.insert("end", "="*70 + "\n")
        self.output_text.insert("end", "ERROR\n")
        self.output_text.insert("end", "="*70 + "\n\n")
        self.output_text.insert("end", f"{message}\n")
        
    def display_interval_steps(self, steps: list, sig_figs: int):
      col_width = sig_figs + 7
    
    # Find the first info step for initial values
      for step in steps:
        if step['type'] == 'info':
            if 'xl' in step and 'xu' in step:
                self.output_text.insert("end", f"Initial interval: [{step['xl']}, {step['xu']}]\n")
                if 'f_xl' in step and 'f_xu' in step:
                    self.output_text.insert("end", f"f(Xl) = f({step['xl']}) = {step['f_xl']}\n")
                    self.output_text.insert("end", f"f(Xu) = f({step['xu']}) = {step['f_xu']}\n")
            if 'required_iterations' in step:
                self.output_text.insert("end", f"Required iterations: {step['required_iterations']}\n\n")
            break
    
    # Print table header
      self.output_text.insert("end", 
        f"{'Iter':<6} {'Xl':<{col_width}} {'Xu':<{col_width}} "
        f"{'Xr':<{col_width}} {'f(Xr)':<{col_width}} {'Error %':<15}\n"
      )
      self.output_text.insert("end", "-"*100 + "\n")
    
    # Print iteration steps
      for step in steps:
        if step['type'] == 'iteration':
            error_str = step['error'] if step['error'] is not None else "N/A"
            self.output_text.insert("end", 
                f"{step['iteration']:<6} "
                f"{step.get('xl', 'N/A'):<{col_width}} "
                f"{step.get('xu', 'N/A'):<{col_width}} "
                f"{step.get('xr', 'N/A'):<{col_width}} "
                f"{step.get('f_xr', 'N/A'):<{col_width}} "
                f"{error_str}\n"
            )
        elif step['type'] == 'converged':
            self.output_text.insert("end", f"\n{step['message']}\n")
            if 'xr' in step:
                self.output_text.insert("end", f"Final xr: {step['xr']}\n")
            if 'f_xr' in step:
                self.output_text.insert("end", f"f(xr): {step['f_xr']}\n")

    def display_fixed_point_steps(self, steps: list, sig_figs: int):
      col_width = sig_figs + 7
    
    # Find the first info step for initial values
      for step in steps:
        if step['type'] == 'info':
            self.output_text.insert("end", f"{step['message']}\n")
            self.output_text.insert("end", f"Equation: x = {step['g_equation']}\n")
            self.output_text.insert("end", f"x₀ = {step['x0']}\n")
            self.output_text.insert("end", f"ε = {step['epsilon']}\n")
            if 'convergence_prediction' in step:
                self.output_text.insert("end", f"Prediction: {step['convergence_prediction']}\n\n")
            
            
            
            break
    
    # Print table header for Fixed Point
      self.output_text.insert("end", 
        f"{'Iter':<6} {'x_current':<{col_width}} "
        f"{'g(x_current)':<{col_width}} {'f(x_next)':<{col_width}} {'Error %':<15}\n"
      )
      self.output_text.insert("end", "-"*100 + "\n")
    
    # Print iteration steps
      for step in steps:
        if step['type'] == 'iteration':
            error_str = step['error'] if step['error'] is not None else "N/A"
            x_current = step.get('x_current', 'N/A')
            g_x_current=step.get('g_x_current','N/A')
            f_x_next=step.get('f_x_next','N/A')
            if x_current is not None and g_x_current is not None and f_x_next is not None  :     
                self.output_text.insert("end", 
                    f"{step['iteration']-1:<6} "
                    f"{x_current:<{col_width}} "
                    f"{g_x_current:<{col_width}} "
                    f"{f_x_next:<{col_width}} "
                    
                    f"{error_str}\n"
                )
        elif step['type'] == 'converged':
            self.output_text.insert("end", f"\n{step['message']}\n")
            if 'xr' in step:
                self.output_text.insert("end", f"Final xr: {step['xr']}\n")
            if 'f_xr' in step:
                self.output_text.insert("end", f"f(xr): {step['f_xr']}\n") 

    def display_result_newton(self, result: RootFinderResult):
        self.output_text.delete("1.0", "end")

        self.output_text.insert("end", "="*70 + "\n")
        self.output_text.insert("end", "NEWTON–RAPHSON METHOD RESULTS\n")
        self.output_text.insert("end", "="*70 + "\n\n")

        if result.error_message:
            self.output_text.insert("end", f"⚠ Warning: {result.error_message}\n\n")

        if result.root is not None:

            sig_figs = get_sig_figs()
            root_d = D(result.root)
            f_root_d = D(result.f_root)
            
            self.output_text.insert("end", f"Approximate Root: {root_d}\n")
            self.output_text.insert("end", f"Function value at root f(xr): {f_root_d}\n")
            self.output_text.insert("end", f"Number of Iterations: {result.iterations}\n")
            self.output_text.insert("end", f"Approximate Relative Error: {result.approximate_error}%\n")
            self.output_text.insert("end", f"Execution Time: {result.execution_time:.6} seconds\n")
            self.output_text.insert("end", f"Significant Figures: {sig_figs}\n")
            self.output_text.insert("end", f"Status: {'✓ Converged' if result.converged else '✗ Did not converge'}\n")

            if result.steps:
                self.output_text.insert("end", "\n" + "="*70 + "\n")
                self.output_text.insert("end", "STEP-BY-STEP SOLUTION\n")
                self.output_text.insert("end", "="*70 + "\n\n")

                col_width = max(15, sig_figs + 7)

                # Table header
                self.output_text.insert(
                    "end",
                    f"{'Iter':<6} {'Xi':<{col_width}} {'f(Xi)':<{col_width}} {'df(Xi)':<{col_width}} {'Xi+1':<{col_width}} {'Error %':<15}\n"
                )
                self.output_text.insert("end", "-"*100 + "\n")

                for step in result.steps:
                    if step["type"] == "iteration":
                        xi = step['xi']
                        fxi = step['f(xi)']
                        dfxi = step['df(xi)']
                        xi1 = step['xi+1']
                        error_val = step['error']
                        error_str = f"{error_val}" if error_val is not None else "N/A"

                        self.output_text.insert(
                            "end",
                            f"{step['iteration']:<6} "
                            f"{xi:<{col_width}} "
                            f"{fxi:<{col_width}} "
                            f"{dfxi:<{col_width}} "
                            f"{xi1:<{col_width}} "
                            f"{error_str:<15}\n"
                        )
                    elif step["type"] == "converged":
                        self.output_text.insert("end", f"\n{step['message']}\n")
                        if 'xr' in step:
                            xr_val = float(step['xr']) if isinstance(step['xr'], D) else step['xr']
                            self.output_text.insert("end", f"Final xr: {xr_val}\n")
                        if 'f_xr' in step:
                            fxr_val = float(step['f_xr']) if isinstance(step['f_xr'], D) else step['f_xr']
                            self.output_text.insert("end", f"f(xr): {fxr_val}\n")


    def display_result_modified_newton(self, result: RootFinderResult):
        self.output_text.delete("1.0", "end")

        self.output_text.insert("end", "="*70 + "\n")
        self.output_text.insert("end", "MODIFIED NEWTON–RAPHSON METHOD RESULTS\n")
        self.output_text.insert("end", "="*70 + "\n\n")

        if result.error_message:
            self.output_text.insert("end", f"⚠ Warning: {result.error_message}\n\n")

        if result.root is not None:
            sig_figs = get_sig_figs()

            self.output_text.insert("end", f"Approximate Root: {result.root}\n")
            self.output_text.insert("end", f"Function value at root f(xr): {result.f_root}\n")
            self.output_text.insert("end", f"Number of Iterations: {result.iterations}\n")
            self.output_text.insert("end", f"Approximate Relative Error: {result.approximate_error}\n")
            self.output_text.insert("end", f"Execution Time: {result.execution_time:.6}\n")
            self.output_text.insert("end", f"Significant Figures: {sig_figs}\n")
            self.output_text.insert("end", f"Status: {'✓ Converged' if result.converged else '✗ Did not converge'}\n")

            if result.steps:
                self.output_text.insert("end", "\n" + "="*70 + "\n")
                self.output_text.insert("end", "STEP-BY-STEP SOLUTION\n")
                self.output_text.insert("end", "="*70 + "\n\n")

                # Table header
                self.output_text.insert(
                    "end",
                    f"{'Iter':<6} {'Xi':<15} {'f(Xi)':<15} {'df(Xi)':<15} {'mf/df':<12} {'Xi+1':<15} {'Error':<15}\n"
                )
                self.output_text.insert("end", "-"*100 + "\n")

                for step in result.steps:
                    if step["type"] == "iteration":
                        self.output_text.insert(
                            "end",
                            f"{step['iteration']:<6} "
                            f"{step['xi']:<15} "
                            f"{step['f(xi)']:<15} "
                            f"{step['df(xi)']:<15} "
                            f"{step['mf(xi)/df(xi)']:<12} "
                            f"{step['xi+1']:<15} "
                            f"{step['error']:<15}\n"
                        )
                    elif step["type"] == "converged":
                        self.output_text.insert("end", f"\n{step['message']}\n")
                        if 'xr' in step:
                            self.output_text.insert("end", f"Final xr: {step['xr']}\n")
                        if 'f_xr' in step:
                            self.output_text.insert("end", f"f(xr): {step['f_xr']}\n")

    def display_result_secant(self, result: RootFinderResult):
        self.output_text.delete("1.0", "end")

        sep = "=" * 80
        sub_sep = "-" * 80

        self.output_text.insert("end", f"{sep}\n")
        self.output_text.insert("end", "SECANT METHOD RESULTS\n")
        self.output_text.insert("end", f"{sep}\n\n")

        if result.error_message:
            self.output_text.insert(
                "end", f"⚠  Warning: {result.error_message}\n\n"
            )

        if result.root is not None:
            sig_figs = get_sig_figs()

            self.output_text.insert("end", f"Approximate Root (xr)        : {result.root}\n")
            self.output_text.insert("end", f"f(xr)                       : {result.f_root}\n")
            self.output_text.insert("end", f"Iterations                  : {result.iterations}\n")
            self.output_text.insert("end", f"Approx. Relative Error      : {result.approximate_error}\n")
            self.output_text.insert("end", f"Execution Time              : {result.execution_time:.6}\n")
            self.output_text.insert("end", f"Significant Figures         : {sig_figs}\n")
            self.output_text.insert(
                "end",
                f"Status                      : "
                f"{'✓ Converged' if result.converged else '✗ Did not converge'}\n"
            )

            if result.steps:
                self.output_text.insert("end", f"\n{sep}\n")
                self.output_text.insert("end", "STEP-BY-STEP ITERATIONS\n")
                self.output_text.insert("end", f"{sep}\n\n")

                headers = ["Iter", "Xi-1", "Xi", "f(xi)Δx / Δf", "Xi+1", "Error"]
                col_widths = [6, 14, 14, 16, 14, 14]

                # Header row
                header_row = "".join(f"{h:<{w}}" for h, w in zip(headers, col_widths))
                self.output_text.insert("end", header_row + "\n")
                self.output_text.insert("end", sub_sep + "\n")

                for step in result.steps:
                    if step["type"] == "iteration":
                        row = "".join(
                            f"{step[k]:<{w}}"
                            for k, w in zip(
                                [
                                    "iteration",
                                    "xi-1",
                                    "xi",
                                    "f(xi)Δx / Δf",
                                    "xi+1",
                                    "error",
                                ],
                                col_widths,
                            )
                        )
                        self.output_text.insert("end", row + "\n")

                    elif step["type"] == "converged":
                        self.output_text.insert("end", f"\n✓ {step['message']}\n")
                        if "xr" in step:
                            self.output_text.insert("end", f"Final xr : {step['xr']}\n")
                        if "f_xr" in step:
                            self.output_text.insert("end", f"f(xr)    : {step['f_xr']}\n")