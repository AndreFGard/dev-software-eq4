<script lang="ts">
  import svelteLogo from './assets/svelte.svg'
  import viteLogo from '/vite.svg'
  import Counter from './Counter.svelte'
  import Chat from './components/Chat.svelte'
  import { apiUrl, addMessage } from './api.js'

  let messages = [{ username: 'gpt', content: 'hello, im gpt' }, {username:'fulano', content:"my brother is ciclano"}];
  let username = 'Fulano';
  let message = '';
  let error = '';

  //again, this function is purely an example.
  async function handleAdd() {
    try {
      messages = await addMessage({ username: username, content: message });
      console.log(`messages: ${messages}`);
      message = '';
    } catch (e: any) {
      error = e.message || e;
    }
  }
</script>

<main class="section">
  <div class="container" id="maincontainer">
    <h3 class="title  has-text-centered">Chat component</h3>
    <!--  Repare que passamos pro chat a função handleAdd definida aqui que sera chamada quando o botao for apertado-->
    <Chat {handleAdd} bind:messages={messages} bind:message={message} />
  </div>
</main>

<style>
  #maincontainer{
    max-width: 90vh;
  }
</style>
