<script lang="ts">
  import Chat from './components/Chat.svelte';
  import Sidebar from './components/Sidebar.svelte';

  let messages = [
    { username: 'gpt', content: 'hello, I am gpt' },
    { username: 'fulano', content: 'my brother is ciclano' }
  ];
  let favorites: { username: string; content: string }[] = [];
  let username = 'Fulano';
  let message = '';

  async function handleAdd() {
    try {
      messages = [...messages, { username, content: message }];
      message = '';
    } catch (e) {
      console.error(e);
    }
  }

  function addToFavorites(msg: { username: string; content: string }) {
    if (!favorites.find(fav => fav.content === msg.content && fav.username === msg.username)) {
      favorites = [...favorites, msg];
      console.log('Favorites updated:', favorites); // Log para verificar o funcionamento
    }
  }
</script>

<main class="section">
  <div class="container" id="maincontainer">
    <h3 class="title has-text-centered">Chat component</h3>
    <div class="columns">
      <div class="column is-three-quarters">
        <Chat
          {handleAdd}
          bind:messages={messages}
          bind:message={message}
          {addToFavorites}
        />
      </div>
      <div class="column">
        <Sidebar {favorites} />
      </div>
    </div>
  </div>
</main>

<style>
  #maincontainer {
    max-width: 90vh;
  }
</style>