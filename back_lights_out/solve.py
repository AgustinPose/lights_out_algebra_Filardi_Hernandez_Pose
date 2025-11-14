# backend/game/solver.py

from typing import List, Tuple

Matrix = List[List[int]]
Coords = List[Tuple[int, int]]


def solve_lights_out(board: Matrix) -> Coords:
    """
    Recibe un tablero n x n de 0/1 y devuelve una lista de coordenadas (i, j)
    que indican qué luces hay que presionar para apagar todo el tablero.

    Las coordenadas son 0-based (i: fila, j: columna).
    """
    n = len(board)
    if n == 0:
        return []

    num_vars = n * n

    # Construimos la matriz A y el vector b del sistema A x = b en F2
    A, b = _build_system(board)

    # Aplicamos eliminación Gaussiana en mod 2 sobre la matriz aumentada [A | b]
    x = _gauss_elimination_mod2(A, b)

    # Convertimos el vector solución (flatten) a lista de coordenadas (i, j)
    coords: Coords = []
    for idx, val in enumerate(x):
        if val == 1:
            i = idx // n
            j = idx % n
            coords.append((i, j))

    return coords


def _build_system(board: Matrix) -> tuple[list[list[int]], list[int]]:
    """
    Construye la matriz A (num_ecuaciones x num_variables) y el vector b
    para el sistema lineal que modela Lights Out en F2.

    - Una ecuación por cada casilla (i, j).
    - Una variable por cada casilla presionada.
    - RHS = estado inicial de esa casilla (0 apagada, 1 encendida).
    """
    n = len(board)
    num_vars = n * n

    # Inicializamos A y b
    A = [[0 for _ in range(num_vars)] for _ in range(num_vars)]
    b = [0 for _ in range(num_vars)]

    # Direcciones que afectan una casilla cuando se presiona:
    # la propia y las adyacentes ortogonales
    dirs = [(0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)]

    for i in range(n):
        for j in range(n):
            eq_idx = i * n + j  # índice de la ecuación para la casilla (i, j)
            b[eq_idx] = board[i][j]  # RHS = estado inicial de esa luz

            # Cada presión en (ni, nj) que afecta a (i, j) suma 1 en esa ecuación
            for di, dj in dirs:
                ni, nj = i + di, j + dj
                if 0 <= ni < n and 0 <= nj < n:
                    var_idx = ni * n + nj  # variable asociada a casilla (ni, nj)
                    A[eq_idx][var_idx] ^= 1  # sumamos 1 en F2

    return A, b


def _gauss_elimination_mod2(A: list[list[int]], b: list[int]) -> list[int]:
    """
    Realiza eliminación Gaussiana en F2 sobre el sistema A x = b.

    - Solo usa operaciones del tipo: Fi <- Fi + Fj  (XOR de filas).
    - No hace multiplicaciones ni pivoteo por escala.
    - Devuelve un vector solución x (0/1). Si hay variables libres, las toma como 0.

    Asumimos que el sistema es consistente para los tableros válidos del juego.
    """
    n_eq = len(A)         # número de ecuaciones
    n_vars = len(A[0])    # número de incógnitas

    # Matriz aumentada [A | b]
    M = [row[:] + [rhs] for row, rhs in zip(A, b)]

    row = 0
    for col in range(n_vars):
        # Buscar pivote en esta columna
        pivot = None
        for r in range(row, n_eq):
            if M[r][col] == 1:
                pivot = r
                break

        if pivot is None:
            # Columna sin pivote → variable libre
            continue

        # Intercambiamos la fila actual con la fila del pivote
        if pivot != row:
            M[row], M[pivot] = M[pivot], M[row]

        # Eliminar los 1 por debajo del pivote
        for r in range(row + 1, n_eq):
            if M[r][col] == 1:
                # F_r <- F_r + F_row (XOR fila)
                for c in range(col, n_vars + 1):
                    M[r][c] ^= M[row][c]

        row += 1
        if row == n_eq:
            break

    # Back-substitution para obtener una solución
    x = [0] * n_vars

    for r in range(n_eq - 1, -1, -1):
        # Buscar primera columna con 1 (pivote)
        pivot_col = None
        for c in range(n_vars):
            if M[r][c] == 1:
                pivot_col = c
                break

        if pivot_col is None:
            # Fila del tipo [0 0 ... 0 | d]
            # si d = 1 → sistema inconsistente; acá asumimos que no pasa
            continue

        # sum_{j>pivot_col} a_rj * x_j
        acc = 0
        for j in range(pivot_col + 1, n_vars):
            if M[r][j] == 1:
                acc ^= x[j]  # suma en F2

        # x_pivot = b_r + acc  (en F2, resta = suma)
        x[pivot_col] = M[r][n_vars] ^ acc

    return x
