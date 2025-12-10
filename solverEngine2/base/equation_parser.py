
import math
import re
from typing import Callable
from D import D


def parse_equation(equation_str: str) -> Callable:
    # Replace common math operators
    equation_str = equation_str.replace('^', '**')
    
    # Add implicit multiplication
    equation_str = re.sub(r'(\d)([a-zA-Z(])', r'\1*\2', equation_str)
    equation_str = re.sub(r'(\))(\d)', r'\1*\2', equation_str)
    equation_str = re.sub(r'(\))(\()', r'\1*\2', equation_str)
    
    # Create namespace with math functions that work with D class
    namespace = {
        "x": D(0),
        "exp": lambda d: d.exp() if isinstance(d, D) else D(math.exp(float(d))),
        "sin": lambda d: D(math.sin(float(d))),
        "cos": lambda d: D(math.cos(float(d))),
        "tan": lambda d: D(math.tan(float(d))),
        "log": lambda d: d.log10() if isinstance(d, D) else D(math.log10(float(d))),
        "ln": lambda d: d.ln() if isinstance(d, D) else D(math.log(float(d))),
        "sqrt": lambda d: d.sqrt() if isinstance(d, D) else D(math.sqrt(float(d))),
        "abs": lambda d: abs(d) if isinstance(d, D) else D(abs(float(d))),
        "pi": D(math.pi),
        "e": D(math.e)
    }
    
    def func(x):
     
        ns = dict(namespace)
        ns["x"] = x if isinstance(x, D) else D(x)
        try:
            return eval(equation_str, {"__builtins__": {}}, ns)
        except Exception as e:
            raise ValueError(f"Error evaluating equation: {str(e)}")
    
    return func