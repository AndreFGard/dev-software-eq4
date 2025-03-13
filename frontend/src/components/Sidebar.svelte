<script lang="ts">
  export let favorites = [];
  export let removeFromFavorites: (msg: { username: string; content: string }) => void;
</script>

<div class="box">
  <h3 class="favorites-title">Favorites:</h3>
  <ul class="favorite-list">
    {#each favorites as msg}
      <li class="message-box {msg.username === 'assistant' ? 'left' : 'right'}">
        <button class="remove-button" on:click={() => removeFromFavorites(msg)}>✖</button>
        <strong>{msg.username}:</strong> {@html msg.content}
      </li>    
    {/each}
  </ul>
</div>

<style>
  .favorite-list {
    max-height: 70vh; /* Limita a altura da lista */
    overflow-y: auto; /* Adiciona barra de rolagem se necessário */
    display: flex;
    flex-direction: column;
    gap: 10px; /* Espaçamento entre as mensagens */
  }

  /* Estilos do título de Favorites */
  .favorites-title {
    color: rgb(50, 58, 90);
    font-weight: bold;
    margin-bottom: 7px;
  }

  /* Estilo do box */
  .box {
    background-color: rgb(163, 201, 241); /* Cor de fundo */
    border-radius: 25px; /* Bordas arredondadas */
    padding: 20px;
    width: 300px;
		box-shadow: 0 4px 1px var(--black);
  }

  /* Estilização da barra de rolagem para a lista de favoritos */
  .favorite-list::-webkit-scrollbar {
    width: 10px;
  }

  .favorite-list::-webkit-scrollbar-thumb {
    background-color: var(--secondary-color);
    border-radius: 10px;
  }

  .favorite-list::-webkit-scrollbar-track {
    background-color: rgba(0, 0, 0, 0.05);
  }

  .remove-button {
  position: absolute;
  top: 3px; 
  right: 3px;
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
    padding: 1.1rem;
    border-radius: 15px;
    max-width: 90%;
  }

  .message-box.left {
    background-color: white; /* Mensagem do assistente */
  }

  .message-box.right {
    background-color: rgb(191, 226, 245); /* Mensagem do usuário */
  }
</style>
