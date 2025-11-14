import { writable } from "svelte/store";

export const board = writable<number[][]>([]);
export const size = writable<number>(0);
export const gameStarted = writable<boolean>(false);
