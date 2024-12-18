<script lang="ts">
  import svelteLogo from './assets/svelte.svg'
  import viteLogo from '/vite.svg'
  import Counter from './Counter.svelte'
  import Chat from './components/Chat.svelte'
  import { apiUrl, addMessage, getMessages } from './api.js'
  import type {Message} from './api.js'
  import { onMount } from 'svelte';

  let messages = [
    { username: 'assistant', content: 'Hello! Im GPT.' },
    {username:'User', content:"Can you help me?"}
  ];
  let username = 'User';
  let message = '';
  let error = '';

  onMount(async () => {
    try {
      messages = await getMessages(username);
    } catch (e: any) {
      error = e.message || e;
    }
  });


  //conferir se a mensagem está vazia
  async function handleAdd() {
    if (!message.trim()){
    error = 'Message cannot be empty';
    return;
    }
    try{
      messages = await addMessage({ username, content: message, is_activity:false });
      message = '';
    } catch (e: any) {
      error = e.message || e;
    }
  }

</script>

<main class="section">
  <div class="container" id='chat-cont'>
    <h3 class="title  has-text-centered" >Mape.ia✈️</h3>
    <Chat {handleAdd} bind:messages={messages} bind:message={message}/>
    {#if error}
      <p class="error">{error}</p>
    {/if}
  </div>
</main>

<style>
  #chat-cont {
    max-width: 1000; /*Largura da caixa*/

  }
   .container {
    max-width: 90vh;
    margin: auto;
    text-align: left; /* Garante que o título siga para a esquerda */
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

  @media (max-width: 768px) {
    .container {
      max-width: 100%;
      padding: 1rem;
    }
  }
</style>
