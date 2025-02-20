<script lang="ts">
    export let favorites: {username: string; content: string}[];
  </script>
  
  <div class="box">
    <h3 class="favorites-title">Favorites</h3> <!-- Alterei a classe para 'favorites-title' -->
    <ul class="favorite-list">
      {#each favorites as fav}
        <li class="favorite-item box">
          <strong>{fav.username}</strong>: {fav.content}
        </li>
      {/each}
    </ul>
  </div>
  
  <style>
    .favorite-list {
        list-style-type: none;
        padding: 1px;
        max-height: 80vh; /* Limita a altura da lista */
        overflow-y: auto; /* Adiciona barra de rolagem se necessário */
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
      font-size: 1.0rem; /* Aumenta o tamanho do texto */
      color: rgb(50, 58, 90);
      font-weight: bold; /* Deixa o texto em negrito */
      margin-bottom: 10px; /* Espaçamento inferior */
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
        width: 12px;
    }

    .favorite-list::-webkit-scrollbar-thumb {
        background-color: var(--secondary-color);
        border-radius: 10px;
        border: 3px solid transparent;
    }

    .favorite-list::-webkit-scrollbar-track {
        background-color: rgba(0, 0, 0, 0.05);
    }

  </style>
  