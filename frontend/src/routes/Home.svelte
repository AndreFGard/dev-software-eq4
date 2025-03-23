<script>
    import { link } from 'svelte-routing';
  </script>
  
  <main>
    <h1>Bem-vindo ao Mape.ia✈️</h1>
    <p>Este é um assistente de chat. Clique no botão abaixo para acessar a aplicação.</p>
    <a href="/app" use:link class="button">Ir para a aplicação</a>
  </main>
  
  <style>
    main {
      text-align: center;
      padding: 2rem;
    }
    .button {
      display: inline-block;
      padding: 10px 20px;
      background-color: #007bff;
      color: white;
      border-radius: 5px;
      text-decoration: none;
      font-weight: bold;
    }
    .button:hover {
      background-color: #0056b3;
    }
  </style>