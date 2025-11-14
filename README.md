# Lights Out – Proyecto de Álgebra Aplicada

Este proyecto implementa el juego **Lights Out** como parte del práctico de **Álgebra Aplicada**.  
Incluye un **backend en FastAPI** que resuelve el juego usando un modelo matemático en `{0,1}`  
y un **frontend en Svelte** que permite jugar de forma interactiva.

---

## Funcionalidades principales

- Selección del **tamaño del tablero** (`n × n`).
- Generación de un tablero aleatorio con 0s y 1s.
- Interacción clickeando casillas:
  - Se invierte la casilla clickeada y sus adyacentes (arriba, abajo, izquierda, derecha).
- Detección automática de victoria (cuando todas las luces quedan en 0).
- Mensaje de **“¡Felicidades, has ganado!”** y opción de volver al inicio.
- Endpoint `/solve` que devuelve el **vector de solución** en formato de 0 y 1 como se solicito en la consigna.

---

## Tecnologías utilizadas

### Backend (API)
- Python
- FastAPI
- Uvicorn

### Frontend
- Svelte
- Vite

---

# Levantar el backend (FastAPI)

1. Abrir una terminal e ir a la carpeta del backend:

   ```bash
   cd back_lights_out
   ```

2. Crear un entorno virtual:

   ### Windows (PowerShell)
   ```bash
   py -m venv venv
   venv\Scripts\Activate.ps1
   ```

   ### Windows (CMD)
   ```bash
   py -m venv venv
   venv\Scripts\activate.bat
   ```

3. Instalar dependencias:

   ```bash
   pip install -r requirements.txt
   ```

4. Levantar el servidor de desarrollo:

   ```bash
   uvicorn main:app --reload
   ```

5. API disponible en:

   - http://127.0.0.1:8000/
   - Documentación Swagger: http://127.0.0.1:8000/docs

---

# Levantar el frontend (Svelte)

1. Ir a la carpeta del frontend:

   ```bash
   cd front_lights_out
   ```

2. Instalar dependencias:

   ```bash
   npm install
   ```

3. Ejecutar el servidor de desarrollo:

   ```bash
   npm run dev
   ```

4. Abrir en el navegador:

   http://localhost:5173/

---

# Flujo de uso

1. Iniciar el backend con Uvicorn.
2. Iniciar el frontend con `npm run dev`.
3. Abrir la página del juego en el navegador.
4. Seleccionar el tamaño del tablero.
5. Jugar clickeando las luces hasta apagarlas todas.
6. Si se gana:
   - Aparece un mensaje de victoria.
   - Opción de volver al menú principal.

---

# 🧑‍💻 Autores

- Franco Filardi  
- Mateo Hernández  
- Agustín Pose
