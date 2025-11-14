<script lang="ts">
  import { board, size, gameStarted } from "./stores/game";
  import { applyMove } from "./utils/api";

  let won = false;

  $: b = $board;
  $: n = $size;

  function checkWin(board: number[][]): boolean {
    return board.every(row => row.every(cell => cell === 0));
  }

  async function press(i: number, j: number) {
    if (won) return; // si ya ganó, no permitir más jugadas

    const newBoard = await applyMove(b, i, j);
    board.set(newBoard);

    if (checkWin(newBoard)) {
      won = true;
    }
  }

  function backToHome() {
    won = false;
    gameStarted.set(false); // vuelve a la pantalla principal
  }
</script>

<h2>Tablero {n}×{n}</h2>

<div class="grid" style={`grid-template-columns: repeat(${n}, 50px);`}>
  {#each b as row, i}
    {#each row as cell, j}
      <button
        title={cell ? "Encendida" : "Apagada"}
        class="cell {cell ? 'on' : 'off'}"
        on:click={() => press(i, j)}
        disabled={won}
      ></button>
    {/each}
  {/each}
</div>

{#if won}
  <div class="win-box">
    <h3>🎉 ¡Felicidades! ¡Has ganado! 🎉</h3>
    <button class="back-btn" on:click={backToHome}>
      Volver al inicio
    </button>
  </div>
{/if}

<style>
  .grid {
    display: grid;
    gap: 6px;
    margin-top: 20px;
  }

  .cell {
    width: 50px;
    height: 50px;
    border-radius: 6px;
    border: none;
    cursor: pointer;
    transition: 0.2s;
  }

  .cell:disabled {
    cursor: not-allowed;
    opacity: 0.6;
  }

  .cell.on {
    background: #facc15;
  }

  .cell.off {
    background: #0f172a;
    border: 1px solid #475569;
  }

  .win-box {
    margin-top: 25px;
    background: #1e293b;
    padding: 20px;
    border-radius: 10px;
    color: #f1f5f9;
    text-align: center;
    border: 1px solid #334155;
    max-width: 250px;
    margin-left: auto;
    margin-right: auto;
  }

  .back-btn {
    margin-top: 15px;
    padding: 10px 18px;
    background: #f97316;
    border: none;
    color: white;
    font-weight: bold;
    border-radius: 8px;
    cursor: pointer;
    width: 100%;
  }

  .back-btn:hover {
    background: #fb923c;
  }
</style>
