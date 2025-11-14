from pydantic import BaseModel
from typing import List

#La request para iniciar el juego solo necesita el tamaño del tablero n x n
class InitRequest(BaseModel):
    n: int

#La response a una jugada es un nuevo tablero con las casillas afectadas cambiadas
class BoardRequest(BaseModel):
    board: List[List[int]]

#la reques de jugada es el tablero con las coordenadas de la casilla (luz) que apreto
class MoveRequest(BaseModel):
    board: List[List[int]]
    i: int
    j: int
