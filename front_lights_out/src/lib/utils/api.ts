export async function applyMove(board: number[][], i: number, j: number) {
  try {
    const res = await fetch("http://127.0.0.1:8000/press", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        board,
        i,
        j
      })
    });

    if (!res.ok) {
      throw new Error("Error al aplicar movimiento");
    }

    const data = await res.json();
    return data.board; // el backend devuelve el tablero ya modificado

  } catch (error) {
    console.error("applyMove error:", error);
    return board; // fallback: no cambia nada si hubo error
  }
}
