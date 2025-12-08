# # solverEngine2/models.py
# from dataclasses import dataclass
# from typing import Optional, List

# @dataclass
# class RootFinderResult:
#     root: Optional[float] = None
#     iterations: int = 0
#     approximate_error: float = 0.0
#     execution_time: float = 0.0
#     converged: bool = False
#     error_message: Optional[str] = None
#     steps: List = None

#     def __post_init__(self):
#         if self.steps is None:
#             self.steps = []


# @dataclass
# class RootFinderParameters:
#     equation: str = ""
#     method: str = "Bisection"
#     xl: float = 0.0
#     xu: float = 1.0
#     max_iterations: int = 50
#     epsilon: float = 0.00001
#     significant_figures: int = 5
#     step_by_step: bool = False