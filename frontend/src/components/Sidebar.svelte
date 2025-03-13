<script lang="ts">
  export let favorites = [];
  export let removeFromFavorites: (msg: { username: string; content: string }) => void;
</script>

<div class="box">
  <h3 class="favorites-title">Favorites</h3>
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
    list-style-type: none;
    padding: 1px;
    max-height: 60vh; /* Limita a altura da lista */
    overflow-y: auto; /* Adiciona barra de rolagem se necessário */
    display: flex;
    flex-direction: column;
    gap: 10px; /* Espaçamento entre as mensagens */
  }
      
  .favorite-item {
    word-wrap: break-word;
    word-break: break-word;
    color: var(--text-color);
    max-width: 100%; /* Garante que os itens de favoritos respeitem a largura da sidebar */
    padding: 10px; /* Ajuste de espaçamento interno */
    margin-bottom: 5px;
  }

  /* Estilos do título de Favorites */
  .favorites-title {
    font-size: 1rem;
    color: rgb(50, 58, 90);
    font-weight: bold;
    margin-bottom: 10px;
  }

  /* Estilo do box */
  .box {
    background-color: rgb(163, 201, 241); /* Cor de fundo */
    border-radius: 25px; /* Bordas arredondadas */
    padding: 20px;
    width: 300px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  }

  /* Estilização da barra de rolagem para a lista de favoritos */
  .favorite-list::-webkit-scrollbar {
    width: 10px;
  }

  .favorite-list::-webkit-scrollbar-thumb {
    background-color: var(--secondary-color);
    border-radius: 10px;
    border: 3px solid transparent;
  }

  .favorite-list::-webkit-scrollbar-track {
    background-color: rgba(0, 0, 0, 0.05);
  }

  .remove-button {
  position: absolute;
  top: 4px; /* Antes estava 8px, agora está mais para cima */
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
    padding: 1.1rem;
    border-radius: 15px;
    max-width: 85%;
    word-wrap: break-word;
    word-break: break-word;
  }

  .message-box.left {
    background-color: white; /* Mensagem do assistente */
  }

  .message-box.right {
    background-color: rgb(191, 226, 245); /* Mensagem do usuário */
  }

</style>
