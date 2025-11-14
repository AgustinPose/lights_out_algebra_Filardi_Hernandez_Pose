from fastapi import FastAPI
from config import setup_cors
from models import InitRequest, BoardRequest, MoveRequest
from board import generate_board, apply_move
from solve import solve_lights_out

app = FastAPI()
setup_cors(app)


@app.get("/")
def home():
    return {"message": "Lights Out API funcionando"}


@app.post("/init")
def init(req: InitRequest):
    board = generate_board(req.n)
    return {"board": board}


@app.post("/press")
def press(req: MoveRequest):
    new_board = apply_move(req.board, req.i, req.j)
    return {"board": new_board}


@app.post("/solve")
def solve(req: BoardRequest):
    sol = solve_lights_out(req.board)
    return {"solution": sol}


@app.post("/reset")
def reset(req: InitRequest):
    board = generate_board(req.n)
    return {"board": board}
