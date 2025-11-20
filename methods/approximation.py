class Approximation:
    
    def __init__(self, n, values, iteration, error):
        self.n = n
        self.values = values
        self.iteration = iteration
        self.error = error
        
    def __str__(self):
        print("k     | ", end="")
        for i in range(self.n - 1):
            print(f"x{i + 1}     | ", end="")
            
        print(f"x{self.n + 1}")
        print(f"{self.iteration}     | ", end="")
        for i in range(self.n - 1):
            print(f"{self.values[i]}     | ")
        print(f"{self.values[self.n]}     ")