import { writable } from 'svelte/store';

// Store to manage drawer open/close state
export const isDrawerOpen = writable(false);