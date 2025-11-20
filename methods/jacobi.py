from approximation import Approximation

def jacobi_by_iteration(matrix, n, guess, iterations, b):
    initial_approximation = Approximation(n, guess, 0, [0]*n)
    approximations = [initial_approximation]
    for k in range(iterations):
        last = approximations[k].values
        curr = [0]*n
        error = [0]*n
        
        #calculate current approximation
        # Xki = (bi - (j=0->n, j!=i)(sum(aij*X(k-1)j)))/ aii
        for i in range(0, n):
            aii = matrix[i][i]
            row_sum = 0
            for j in range(0, n):
                if j == i:
                    continue
                row_sum += matrix[i][j]*last[j]
            
            # calculate approximation and error
            curr[i] = (b[i] - row_sum) / aii
            error[i] = abs((curr[i] - last[i]) / curr[i]) * 100
            
        #create approximation data structure
        approximation = Approximation(n, curr, k, error)
        approximations.append(approximation)
        
    return approximations


def jacobi_by_error_bound(matrix, n, guess, bound, b):
    initial_approximation = Approximation(n, guess, 0, [0]*n)
    approximations = [initial_approximation]
    k = 0
    while(k < 100):
        last = approximations[k].values
        curr = [0]*n
        error = [0]*n
        
        #calculate current approximation
        # Xki = (bi - (j=0->n, j!=i)(sum(aij*X(k-1)j)))/ aii
        for i in range(0, n):
            aii = matrix[i][i]
            row_sum = 0
            for j in range(0, n):
                if j == i:
                    continue
                row_sum += matrix[i][j]*last[j]
            
            # calculate approximation and error
            curr[i] = (b[i] - row_sum) / aii
            error[i] = abs((curr[i] - last[i]) / curr[i]) * 100
            
        #create approximation data structure
        approximation = Approximation(n, curr, k, error)
        approximations.append(approximation)
        done = True
        for i in range(n):
            if(error[i] >= bound):
                done = False
                break
        
        if done: return approximations
        k+=1
            
    
    print("timeout")    
    return approximations

matrix = [[5, -1, 1], [2, 8, -1], [-1, 1, 4]]
b = [10, 11, 3]

a = jacobi_by_error_bound(matrix, 3, [1, 1, 1], 0.00000000001, b)
print(a[len(a) - 1].values)
print(a[len(a) -1].error)
print(a[len(a) -1].iteration)