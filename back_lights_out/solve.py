# solver.py
from typing import List, Tuple

Matrix = List[List[int]]
Coords = List[Tuple[int, int]]

    """
    FUncion principal que resuelve lo que pide ña pregunta 6 del practico.
    Recibe un tablero n x n de 0/1 y devuelve un vector de 0/1
    que indica qué casillas hay que presionar para resolver el juego.
    """
def solve_lights_out_vector(board: Matrix) -> List[int]:

    n = len(board)
    if n == 0:
        return []

    A, b = _build_system(board)
    x = _gauss_mod2_sin_pivote(A, b)
    return x


# Versión cómoda para el juego (opcional, si la querés seguir usando)
def solve_lights_out(board: Matrix) -> Coords:
    n = len(board)
    x = solve_lights_out_vector(board)
    return _vector_to_coords(x, n)


def _build_system(board: Matrix) -> tuple[List[List[int]], List[int]]:
    """
    Construye la matriz A y el vector b del sistema A x = b en F2,
    """
    n = len(board)
    num_vars = n * n

    A = [[0 for _ in range(num_vars)] for _ in range(num_vars)]
    b = [0 for _ in range(num_vars)]

    # Casilla y adyacentes ortogonales
    dirs = [(0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)]

    for i in range(n):
        for j in range(n):
            eq_idx = i * n + j
            b[eq_idx] = board[i][j]

            for di, dj in dirs:
                ni, nj = i + di, j + dj
                if 0 <= ni < n and 0 <= nj < n:
                    var_idx = ni * n + nj
                    A[eq_idx][var_idx] ^= 1  # suma binaria (mod 2)

    return A, b


def _gauss_mod2_sin_pivote(A: List[List[int]], b: List[int]) -> List[int]:
    """
    Eliminación Gaussiana en {0,1}:
    - Solo usa transformaciones Fi <- Fi + Fj (XOR de filas)
    - No hace pivoteo ni multiplicar filas por escalares
    """
    n = len(A)  # n ecuaciones = n variables

    # Matriz aumentada [A | b]
    M = [row[:] + [rhs] for row, rhs in zip(A, b)]

    # Eliminación hacia adelante
    for k in range(n):  # pivote en la posición (k, k)
        # Por construcción del sistema, asumimos M[k][k] = 1
        for i in range(k + 1, n):
            if M[i][k] == 1:
                # Fi <- Fi + Fk (suma binaria fila a fila)
                for j in range(k, n + 1):
                    M[i][j] ^= M[k][j]

    # Back-substitution
    x = [0] * n
    for i in range(n - 1, -1, -1):
        acc = 0
        for j in range(i + 1, n):
            if M[i][j] == 1:
                acc ^= x[j]
        x[i] = M[i][n] ^ acc

    return x


def _vector_to_coords(x: List[int], n: int) -> Coords:
    coords: Coords = []
    for idx, val in enumerate(x):
        if val == 1:
            i = idx // n
            j = idx % n
            coords.append((i, j))
    return coords
