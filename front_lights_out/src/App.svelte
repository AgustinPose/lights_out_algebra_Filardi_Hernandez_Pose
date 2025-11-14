<script lang="ts">
  import Board from "./lib/Board.svelte";
  import { board, size, gameStarted } from "./lib/stores/game";

  let n: number = 5; // tamaño válido actual
  let nInput: string = "3"; // lo que escribe el usuario (string)
  let showHelp = false;
  let errorMsg = "";

  function validateCampos(): boolean {
    // Solo dígitos
    if (!/^\d+$/.test(nInput)) {
      errorMsg = "El tamaño debe ser un número entero.";
      return false;
    }

    const value = Number(nInput);

    if (!Number.isInteger(value) || value < 2 || value > 15) {
      errorMsg = "El tamaño debe ser un entero entre 2 y 15.";
      return false;
    }

    errorMsg = "";
    n = value;
    return true;
  }

  async function generateBoard() {
    if (!validateCampos()) return;

    try {
      const res = await fetch("http://127.0.0.1:8000/init", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ n }),
      });

      const data = await res.json();

      size.set(n);
      board.set(data.board);
      gameStarted.set(true);
    } catch (e) {
      console.error("Error:", e);
    }
  }

  $: started = $gameStarted;
</script>

<button class="help-button" on:click={() => (showHelp = true)}> Ayuda </button>

<main>
  <h1>Lights Out 💡</h1>

  {#if !started}
    <div class="config-container">
      <div class="size-container">
        <label for="size">Tamaño del tablero</label>
        <input id="size" type="text" bind:value={nInput} inputmode="numeric" />
      </div>

      {#if errorMsg}
        <p class="error">{errorMsg}</p>
      {/if}

      <button class="generate-btn" on:click={generateBoard}>
        Generar tablero
      </button>
    </div>
  {:else}
    <Board />
  {/if}
</main>

{#if showHelp}
  <button title="Help" class="modal-overlay" on:click={() => (showHelp = false)}
  ></button>

  <div class="modal">
    <h2>Cómo jugar</h2>
    <ul>
      <li>
        Lights Out es un juego de lógica donde cada luz puede estar encendida o
        apagada.
      </li>
      <li>
        Al presionar una luz, esa luz y sus adyacentes (arriba, abajo,
        izquierda, derecha) cambian de estado.
      </li>
      <li>El objetivo es dejar todas las luces apagadas.</li>
    </ul>

    <button on:click={() => (showHelp = false)}>Cerrar</button>
  </div>
{/if}
