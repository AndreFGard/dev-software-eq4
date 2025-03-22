<script lang="ts">
	export let addToFavorites: (msg: { username: string; content: string }) => void;
	import type { Message } from "../api";
	import { marked } from "marked";
	export let messages: Message[] = [];
	export let message = "";
	export let handleAdd: () => void;
	
	let isLoading = false;
	async function handleSend() {
	  isLoading = true;
	  await handleAdd();
	  isLoading = false;
	}
	
	function renderMarkdown(content: string) {
	  return marked(content);
	}
  </script>
  
  <style>
	:root {
	  --primary-color: rgb(163, 201, 241); 
	  --secondary-color: rgb(191, 226, 245);
	  --text-color: rgb(47, 49, 91);
	  --button-text-color: rgb(47, 49, 91);
	  --button-active: rgb(117, 169, 198);
	  --black: rgba(0, 0, 0, 0.1);
	  --white: rgb(255, 255, 255);
	}
  
	.box {
	  background-color: var(--primary-color);
	  box-shadow: 0 4px 1px var(--black);
	  color: var(--white);
	  padding: 25px;
	  height: 100%;
	  width: 66%;
	  border-radius: 25px;
	  display: flex;
	  flex-direction: column;
	  overflow: hidden;
	  position: relative;
	}
  
	.app-title {
	  color: rgb(39, 121, 168);
	  font-size: 1.8rem;
	  margin: 0 0 25px 0;
	  padding-bottom: 10px;
	  border-bottom: 2px solid var(--secondary-color);
	  margin-bottom: 15px;
	}
  
	.message-box {
	  background-color: var(--secondary-color);
	  color: var(--text-color);
	  padding: 1.1rem;
	  border-radius: 15px;
	  max-width: 80%;
	  min-width: 30%;
	  word-wrap: break-word;
	  word-break: break-word;
	}
  
	.message-box.left {
	  align-self: flex-start;
	  background-color: var(--white);
	}
  
	.message-box.right {
	  align-self: flex-end;
	  background-color: var(--secondary-color);
	  color: var(--text-color);
	}
  
	.input, 
	.button {
	  background-color: var(--white);
	  color: var(--button-text-color);
	  box-shadow: 0 4px 1px var(--black);
	  margin-top: 5px;
	  border-radius: 10px;
	  flex: 0 0 auto;
	  padding: 0 20px;
	}
  
	.messages-list {
	  display: flex;
	  flex-direction: column;
	  align-items: flex-start;
	  height: calc(100% - 120px);
	  overflow-y: auto;
	  gap: 10px;
	  flex-grow: 1;
	  margin-bottom: 15px;
	}
  
	.messages-list::-webkit-scrollbar {
	  width: 10px;
	}
  
	.messages-list::-webkit-scrollbar-thumb {
	  background-color: var(--secondary-color);
	  border-radius: 10px;
	  border: 3px solid transparent;
	}
  
	.messages-list::-webkit-scrollbar-track {
	  background-color: rgba(0, 0, 0, 0.05);
	}
  
	.button:hover {
	  background-color: var(--secondary-color);
	}
  
	.button:active {
	  outline: 7px solid var(--button-active);
	}
  
	.input {
	  flex: 1;
	  min-width: 0;
	}
  
	.field {
	  display: flex;
	  gap: 8px;
	  align-items: center;
	  position: sticky;
	  bottom: 0;
	  background: var(--primary-color);
	  padding: 10px 0;
	  margin-top: auto;
	}
  
	.message-box strong {
	  color: rgb(19, 82, 119);
	  font-weight: bold;
	}
  
	.favorite-button {
	  height: 25px;
	  padding: 5px 12px;
	  font-size: 12px;
	}
  </style>
  
  <div class="box"> 
	<h2 class="app-title">Mape.ia</h2>
	<ul class="messages-list">
	  {#each messages as msg}
		<li class="message-box {msg.username === 'assistant' ? 'left' : 'right'}">
		  <strong>{msg.username}:</strong> 
		  <button
			class="button is-small is-primary favorite-button"
			on:click={() => addToFavorites(msg)}
		  >
			Add to Favorites
		  </button>
		  {@html renderMarkdown(msg.content)}
		</li>
	  {/each}
	</ul>
  
	<div class="field {isLoading ? 'placeholder' : ''}">
	  <input
		class="input"
		type="text"
		placeholder="Type your message"
		bind:value={message}
	  />
	  <button class="button {isLoading ? 'is-loading' : ''}" on:click={handleSend}>Send</button>
	</div>
  </div>