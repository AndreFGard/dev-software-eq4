<script lang="ts">
  export let favorites = []; // Recebe a lista de favoritos do componente pai
  export let removeFromFavorites: (msg: { username: string; content: string }) => void; // Função para remover favoritos
</script>

<div class="box">
  <h3 class="favorites-title">Favorites</h3>
  <ul class="favorite-list">
    {#each favorites as msg}
      <li class="message-box">
        <!-- Botão de remover com posicionamento absoluto -->
        <button class="remove-button" on:click={() => removeFromFavorites(msg)}>✖</button>
        <strong>{msg.username}:</strong> {@html msg.content}
      </li>
    {/each}
  </ul>
</div>

<style>
  .favorite-list {
    list-style-type: none;
    padding: 10px 0; /* Correção do erro de digitação */
    max-height: calc(100vh - 150px);
    overflow-y: auto;
    display: flex;
    flex-direction: column;
    gap: 10px;
    flex: 1;
  }

  .box {
    background-color: rgb(163, 201, 241);
    border-radius: 25px;
    padding: 15px;
    width: 100%;
    height: 100%;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    display: flex;
    flex-direction: column;
    overflow: hidden;
    flex: 1;
    max-width: 100%;
  }

  .favorite-list::-webkit-scrollbar {
    width: 10px;
  }

  .favorite-list::-webkit-scrollbar-thumb {
    background-color: rgb(191, 226, 245);
    border-radius: 10px;
    border: 3px solid transparent;
  }

  .favorite-list::-webkit-scrollbar-track {
    background-color: rgba(0, 0, 0, 0.05);
  }

  .remove-button {
    position: absolute;
    top: 4px;
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
    padding: 10px;
    border-radius: 15px;
    max-width: 90%;
    word-wrap: break-word;
    background-color: white;
  }

  .favorites-title {
    font-size: 1rem;
    color: rgb(50, 58, 90);
    font-weight: bold;
    margin-bottom: 10px;
  }
</style>