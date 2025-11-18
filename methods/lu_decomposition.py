import time

def lu(A, B, scale,form="Doolittle Form",  tol=1e-12):
    start = time.time()
    n = len(A)
    a = [row[:] for row in A]
    b = B[:]
    
    # Initialize L and U matrices
    L = [[0.0] * n for _ in range(n)]
    U = [[0.0] * n for _ in range(n)]
    
    o = list(range(n))
    s=None
    if(scale):
        s = [max(abs(x) for x in row) for row in a]
    
    if form == "Doolittle Form":
        return doolittle_decomposition(a, b, n, L, U, o, s,scale, tol, start)


def doolittle_decomposition(a, b, n, L, U, o, s,scale, tol, start_time):
    er = 0
    
        
    for k in range(n-1):
        # Pivot
        p = k
        if scale:
            big = abs(a[o[k]][k]) / s[o[k]]
        else:
            big = abs(a[o[k]][k])
        
        for i in range(k+1, n):
            if scale:
                dummy = abs(a[o[i]][k]) / s[o[i]]
            else:
                dummy = abs(a[o[i]][k])
            if dummy > big:
                big = dummy
                p = i
        
        if p != k:
            o[p], o[k] = o[k], o[p]
        
        if scale:
            if abs(a[o[k]][k]) / s[o[k]] < tol:
                return None, "Matrix is singular or nearly singular", None, None
        else:
            if abs(a[o[k]][k]) < tol:
                return None, "Matrix is singular or nearly singular", None, None
        
        # Elimination
        for i in range(k+1, n):
            factor = a[o[i]][k] / a[o[k]][k]
            a[o[i]][k] = factor  # Store L coefficient
            for j in range(k+1, n):
                a[o[i]][j] = a[o[i]][j] - factor * a[o[k]][j]
    
    if scale:
        if abs(a[o[n-1]][n-1]) / s[o[n-1]] < tol:
            return None, "Matrix is singular or nearly singular", None, None
    else:
        if abs(a[o[n-1]][n-1]) < tol:
            return None, "Matrix is singular or nearly singular", None, None
    
    # # Extract L and U matrices
    # for i in range(n):
    #     for j in range(n):
    #         if i > j:
    #             L[i][j] = a[o[i]][j]
    #         elif i == j:
    #             L[i][j] = 1.0
    #             U[i][j] = a[o[i]][j]
    #         else:
    #             U[i][j] = a[o[i]][j]
    
    # Solve the system
    x = substitute(a, o, n, b)
    return x, time.time() - start_time,


def substitute(a, o, n, b):
    """Solve the system using forward and backward substitution"""
    # Forward substitution for Lz = b
    z = [0.0] * n
    z[0] = b[o[0]]
    for i in range(1, n):
        sum_val = b[o[i]]
        for j in range(0,i):
            sum_val -= a[o[i]][j] * z[j]
        z[i] = sum_val
    
    # Backward substitution for Ux = z
    x = [0.0] * n
    x[n-1] = z[n-1] / a[o[n-1]][n-1]
    for i in range(n-2, -1, -1):
        sum_val = 0.0
        for j in range(i+1, n):
            sum_val += a[o[i]][j] * x[j]
        x[i] = (z[i] - sum_val) / a[o[i]][i]
    
    return x
