<script lang="ts">
	export let messages: { username: string; content: string }[];
	export let message = "";
	export let handleAdd: () => void;
	export let addToFavorites: (msg: { username: string; content: string }) => void;
  </script>
  
  <div class="box">
	<h3>Messages:</h3>
	<ul class="messages-list">
	  {#each messages as msg}
		<li class="message-item box">
		  <strong>{msg.username}:</strong> {msg.content}
		  <button
			class="button is-small is-primary"
			on:click={() => addToFavorites(msg)}
		  >
			Add to Favorites
		  </button>
		</li>
	  {/each}
	</ul>
	<div class="field is-flex is-align-items-center is-justify-content-center">
	  <input
		class="input"
		type="text"
		placeholder="Type your message"
		bind:value={message}
	  />
	  <button class="button" on:click={handleAdd}>Send</button>
	</div>
  </div>
  