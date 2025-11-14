import random

def generate_board(n: int):
    return [[random.randint(0,1) for _ in range(n)] for _ in range(n)]

def apply_move(board, i, j):
    n = len(board)
    new = [row[:] for row in board]

    # dr, dc: cambio en fila y columna (dr>0 = abajo, dc>0 = derecha)
    offsets = [(0,0),(1,0),(-1,0),(0,1),(0,-1)]

    for dr,dc in offsets:
        ni, nj = i + dr, j + dc
        if 0 <= ni < n and 0 <= nj < n:
            new[ni][nj] = 1 - new[ni][nj]
    return new
