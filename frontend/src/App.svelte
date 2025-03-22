<script lang="ts">
  import Chat from './components/Chat.svelte';
  import Sidebar from './components/Sidebar.svelte';
  import { addMessage, getMessages, addToFavoritesBack, getFavorites } from './api.js';
  import type { Message } from './api.js';
  import { onMount } from 'svelte';
  import { removeFromFavoritesBack } from './api';
  
  let favorites: Message[] = [];
  let error: string;
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
    favorites = favorites.filter(fav => fav.content !== msg.content);
    await removeFromFavoritesBack(username, msg);
  }
</script>

<main id="chat-cont">
  <div class="content-wrapper">
    <Sidebar {favorites} class="sidebar" removeFromFavorites={removeFromFavorites} />
    <Chat {handleAdd} bind:messages={messages} bind:message={message} addToFavorites={addToFavorites} />
  </div>
</main>

<style>

#chat-cont {
    height: 100vh;
    padding: 20px;
    background: rgb(245, 245, 245);
    box-sizing: border-box;
    display: flex;
    justify-content: center;
  }

  .content-wrapper {
    display: flex;
    height: 100%;
    width: 100%; 
    gap: 15px;
  }

  .sidebar {
    width: 33.33%; /* Força 1/3 da tela */
    min-width: 0;
  }

  .chat {
    width: 66.66%; /* Força 2/3 da tela */
    min-width: 0; /* Permite encolhimento */
  }


  @media (max-width: 768px) {
    .container {
      max-width: 100%;
      padding: 1rem;
    }
    .sidebar, .chat {
      max-width: 100%;
      min-width: 100%;
    }
  }
</style>
