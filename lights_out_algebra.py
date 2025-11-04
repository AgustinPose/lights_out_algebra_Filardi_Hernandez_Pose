# Lights Out - Álgebra Aplicada
# Agustín Pose / Mateo Hernández / Franco Filardi

import numpy as np

# arma la matriz que muestra qué luces se afectan entre sí
def matriz_influencia(n):
    A = np.zeros((n*n, n*n), dtype=int)
    for i in range(n):
        for j in range(n):
            pos = i*n + j
            A[pos, pos] = 1
            if i > 0: A[pos, (i-1)*n + j] = 1
            if i < n-1: A[pos, (i+1)*n + j] = 1
            if j > 0: A[pos, i*n + (j-1)] = 1
            if j < n-1: A[pos, i*n + (j+1)] = 1
    return A

# eliminación gaussiana pero mod 2 (0/1)
def gauss_binario(A, b):
    A = A.copy()
    b = b.copy()
    n = len(b)
    fila = 0
    for col in range(n):
        for i in range(fila, n):
            if A[i, col] == 1:
                if i != fila:
                    A[[fila, i]] = A[[i, fila]]
                    b[[fila, i]] = b[[i, fila]]
                break
        else:
            continue
        for j in range(fila + 1, n):
            if A[j, col] == 1:
                A[j] = (A[j] + A[fila]) % 2
                b[j] = (b[j] + b[fila]) % 2
        fila += 1

    x = np.zeros(n, dtype=int)
    for i in range(n - 1, -1, -1):
        suma = np.dot(A[i], x) % 2
        x[i] = (b[i] + suma) % 2
    return x

# función principal
def lights_out(tablero):
    n = len(tablero)
    A = matriz_influencia(n)
    b = tablero.flatten() % 2
    x = gauss_binario(A, b)
    return x.reshape((n, n))

# 
tablero = np.array([
    [0, 1, 0],
    [1, 1, 0],
    [0, 0, 1]
])

sol = lights_out(tablero)
print("Solución (1 = presionar):")
print(sol)