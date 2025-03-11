<script lang="ts">
  import Chat from './components/Chat.svelte'
  import { apiUrl, addMessage, getMessages, addToFavoritesBack, getFavorites } from './api.js'
  import type { Message } from './api.js'
  import { onMount } from 'svelte';
  let favorites: Message[] = [];
  let error: string;
  import Sidebar from './components/Sidebar.svelte';

  let messages = [
    { username: 'assistant', content: 'Hello! Im GPT.' },
    { username: 'User', content: "Can you help me?" }
  ];
  let username = 'User';
  let message = '';

  onMount(async () => {
    try {
      messages = await getMessages(username);
      favorites = await getFavorites(username);
    } catch (e: any) {
      error = e.message || e;
    }
  });

  // Conferir se a mensagem está vazia
  async function handleAdd() {
    if (!message.trim()) {
      error = 'Message cannot be empty';
      return;
    }
    try {
      messages = await addMessage({ username, content: message, is_activity: false });
      message = '';
    } catch (e) {
      console.error(e);
    }
  }

  export async function addToFavorites(msg: Message) {
    favorites = await addToFavoritesBack(username, msg);
  }

  async function removeFromFavorites(msg: Message) {
  favorites = favorites.filter(fav => fav.content !== msg.content); // Remove localmente
  await removeFromFavoritesBack(username, msg); // Remove no backend
}

</script>

<main class="section">
  <div class="container" id="chat-cont">
    <h3 class="title has-text-centered">Mape.ia✈️</h3>
    <div class="is-flex is-flex-direction-row is-justify-content-center" style="gap: 15px;"> <!-- Centraliza a sidebar e o chat -->
      <Sidebar {favorites} class="sidebar" removeFromFavorites={removeFromFavorites} />
      <Chat {handleAdd} bind:messages={messages} bind:message={message} addToFavorites={addToFavorites} />
    </div>
    {#if error}
      <p class="error">{error}</p>
    {/if}
  </div>
</main>

<style>
  #chat-cont {
    max-width: 1000px; /* Largura da caixa */
  }

  .title {
    margin-bottom: 20px; /* Espaçamento abaixo */
    font-size: 2.0rem; /* Tamanho do título */
    color: rgb(39, 121, 168); /* Cor do título */
  }

  .error {
    color: rgb(207, 55, 55);
    font-size: 0.9rem;
  }
</style>
