import time

def pivot(a, b, n, k,s,scale):
    max_row = k
    if scale:
        max_ratio = abs(a[k][k]) / s[k]

        for i in range(k+1, n):
            dummy = abs(a[i][k]) / s[i]
            if dummy > max_ratio:
                max_ratio = dummy
                max_row = i
    else:
        max_pivot = abs(a[k][k] )
        for i in range(k+1, n):
            dummy = abs(a[i][k] )
            if dummy > max_pivot:
                max_pivot = dummy
                max_row = i

    if max_row != k:
        for j in range(k, n):
          dummy=  a[max_row][j]
          a[max_row][j] = a[k][j]
          a[k][j] = dummy
        dummy=  b[max_row]
        b[max_row] = b[k]
        b[k] = dummy
        if scale:
            dummy= s[max_row]
            s[max_row] = s[k]
            s[k] = dummy


def eliminate(a, b, n,s, scale,tol):
    for k in range(n - 1):
        pivot(a, b, n, k,s,scale)
        if scale and abs(a[k][k] / s[k]) < tol:
            return False
        else:
            if abs(a[k][k] ) < tol:
                return False

        for i in range(k + 1, n):
            factor = a[i][k] / a[k][k]
            for j in range(k, n):
                a[i][j] -= factor * a[k][j]
            b[i] -= factor * b[k]
    if scale and abs(a[n-1][n-1] / s[n-1]) < tol:
            return False
    else:   
        if abs(a[n-1][n-1]) < tol:
            return False

    return True


def substitute(a, b, n):
    x = [0] * n
    x[n-1] = b[n-1] / a[n-1][n-1]

    for i in range(n-2, -1, -1):
        s_val = sum(a[i][j] * x[j] for j in range(i+1, n))
        x[i] = (b[i] - s_val) / a[i][i]

    return x


def gauss_partial(A, B, scale, tol=1e-12 ):
    start = time.time()
    n = len(A)
    a = [row[:] for row in A]
    b = B[:]
    s = None
    if(scale):
        s = [max(abs(x) for x in row) for row in a]
        if any(si == 0 for si in s):
             return None, "1Singular system"
        
   

    ok = eliminate(a, b, n,s,scale, tol)
    if not ok:
        return None, "2System is singular"

    x = substitute(a, b, n)
    return x, time.time() - start