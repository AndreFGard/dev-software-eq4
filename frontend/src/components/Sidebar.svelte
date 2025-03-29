<script lang="ts">
  import { writable } from "svelte/store";
  import Login from './Login.svelte'; 
  import type { Activity } from "../api";
  export let favorites: Activity[] = [];
  export let removeFromFavorites: (username: string, act: Activity) => void; 
  export let isExpanded = writable(false);
  import { username } from "../api";
  username.set('User');
  function toggleSidebar() {
    isExpanded.update(value => !value);
  }
  
  import {marked} from "marked";
  marked.use({
      breaks: true,
      gfm: true,
  });
  function renderMarkdown(content: string) {
	  return marked(content);
	}

</script>

<div class="box">
  <button class="toggle-button" on:click={toggleSidebar}>☰</button>
  <h2 class="favorites-title">Favorites:</h2>
  <ul class="favorite-list">
    {#each favorites as act}
      <li class="message-box">
        <button class="remove-button" on:click={() => removeFromFavorites($username, act)}>✖</button>
        <h3 class="text-lg font-semibold text-gray-800">{act.name}:</h3>
        {@html renderMarkdown(act.short_description)}
      </li>
    {/each}
  </ul>
</div>

<style>
  .favorite-list {
    list-style-type: none;
    padding: 10px 0; 
    max-height: calc(100vh - 150px);
    overflow-y: auto;
    display: flex;
    flex-direction: column;
    gap: 10px;
    flex: 1;
  }
  
  .favorites-title {
    color: var(--accent-color);
    font-size: 1.5rem; 
    margin-top: 6px;
    padding-bottom: 14px;
    border-bottom: 2px solid var(--secondary-color);
    display: flex;
    align-items: center;
    text-shadow: 2px 2px 3px rgba(0, 0, 0, 0.2);
  }

  .box {
    background-color: rgb(163, 201, 241);
    border-radius: 25px;
    padding: 15px;
    width: 100%;
    height: 100%;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    display: flex;
    flex-direction: column;
    overflow: hidden;
    flex: 1;
    max-width: 100%;
    position: relative;
  }

  .favorite-list::-webkit-scrollbar {
    width: 10px;
  }

  .favorite-list::-webkit-scrollbar-thumb {
    background-color: rgb(191, 226, 245);
    border-radius: 10px;
    border: 3px solid transparent;
  }

  .favorite-list::-webkit-scrollbar-track {
    background-color: rgba(0, 0, 0, 0.05);
  }

  .remove-button {
    position: absolute;
    top: 4px;
    right: 4px;
    background: none;
    border: none;
    font-size: 14px;
    cursor: pointer;
    color: rgb(117, 169, 198);
  }

  .remove-button:hover {
    color: rgb(209, 18, 18);
  }

  .message-box {
    position: relative;
    padding: 10px;
    border-radius: 15px;
    max-width: 90%;
    word-wrap: break-word;
    background-color: white;
  }

  .toggle-button {
    position: absolute;
    top: 18px;
    right: 18px;
    background: var(--accent-color);
    color: white;
    border: none;
    padding: 8px 12px;
    font-size: 18px;
    border-radius: 15px;
    cursor: pointer;
    transition: 0.3s;
    box-shadow: 2px 2px 4px rgba(0, 0, 0, 0.1);
  }

  .toggle-button:hover {
    background: var(--button-active);
  }
  
  .login-register-container {
    display: flex;
    flex-direction: column;
    gap: 10px;
    width: 100%;
  }
  .button {
    width: 100%; 
    border-radius: 15px;
    font-size: 1.0rem;
    padding: 12px 24px;
    border: none;
    cursor: pointer;
    transition: background 0.3s ease;
  }
  @media (max-width: 768px) {
    .button {
      width: auto; 
    }
  }
</style>