<script lang="ts">
  import svelteLogo from './assets/svelte.svg'
  import viteLogo from '/vite.svg'
  import Counter from './Counter.svelte'
  import Chat from './components/Chat.svelte'
  import { apiUrl, addMessage, getMessages, addToFavoritesBack, getFavorites } from './api.js'
  import type { Message } from './api.js'
  import { onMount } from 'svelte';
  let favorites: Message[] = [];
  let error: string;
  import Sidebar from './components/Sidebar.svelte';

  import { removeFromFavoritesBack } from './api';

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
    margin: auto;
    display: flex; /* Aplica o Flexbox */
    flex-direction: column;
    align-items: center; /* Centraliza os itens horizontalmente */
  }

  .container {
    max-width: 90vh;
    margin: auto;
    text-align: left; /* Garante que o título siga para a esquerda */
  }

  .content-wrapper {
    display: flex; /* Flex layout para alinhar os dois componentes horizontalmente */
    flex-direction: row; /* Alinha os componentes lado a lado */
    justify-content: space-between; /* Espaço uniforme entre os dois */
    align-items: stretch; /* Garante que ambos os boxes tenham a mesma altura */
    gap: 15px; /* Espaçamento entre os dois boxes */
    max-height: 78vh; /* Limita a altura total */
  }

  .sidebar,
  .chat {
    flex: 1; /* Faz com que ambos ocupem o mesmo espaço */
    max-height: 78vh; /* Garante que ambos respeitem a mesma altura */
    overflow-y: auto; /* Adiciona barra de rolagem quando o conteúdo ultrapassar a altura */
  }

  .title {
    text-align: left; /* Alinha o título à esquerda */
    margin-top: -10px; /* Espaçamento acima */
    margin-bottom: 20px; /* Espaçamento abaixo */
    font-size: 2.0rem; /* Tamanho do título */
    color: rgb(39, 121, 168); /* Cor do título */
  }

  .error {
    color: rgb(207, 55, 55);
    font-size: 0.9rem;
    margin-top: 10px;
  }

  /* Estilo global para a Sidebar */
  :global(.sidebar) {
    background-color: rgb(163, 201, 241); /* Cor de fundo */
    border-radius: 10px;
    padding: 10px;
    width: 300px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  }

  @media (max-width: 768px) {
    .container {
      max-width: 100%;
      padding: 1rem;
    }
  }
</style>
