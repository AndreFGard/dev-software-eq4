

<script lang="ts"> //indica que o código dentro dessa tag está em TypeScript
	export let addToFavorites: (msg: { username: string; content: string }) => void;
  	import { apiUrl } from "../api";
	//exporta as variáveis que serão usadas fora do componente Svelte
	import type { Message } from "../api";
	import {marked} from 'marked';
	export let messages: Message[] = []; //Lista de mensagens exibidas no chat
	export let message = "Hello sir"; //Mensagem inicial de exemplo
	export let handleAdd: () => void; //Função que será chamada ao clicar no botão de enviar mensagem
	
	let isLoading = false;
	async function handleSend() {
		isLoading = true;
		
		await handleAdd();
		isLoading = false;
	}

	 function renderMarkdown(content: string) {
		return  marked(content);
	}
	
</script>

<style>
	/* Definição das cores mais usadas */
	:root{
		--primary-color: rgb(163, 201, 241); 
		--secondary-color: rgb(191, 226, 245);
		--text-color: rgb(47, 49, 91);
		--button-text-color: rgb(47, 49, 91);
		--button-active: rgb(117, 169, 198);
		--black: rgba(0, 0, 0, 0.1);
		--white: rgb(255, 255, 255);

	/*Cores exatas do emoji de avião*/
		--cor-1: rgb(0, 132, 206);
		--cor-2: rgb(205, 196, 214);
		--cor-3: rgb(0, 166, 237);
		--cor-4: rgb(155, 155, 155);
  	}

	/* Estilo para a caixa principal */
	/* No seu código de estilo de .box para a caixa de favoritos */
	.box {
		background-color: var(--primary-color);
		box-shadow: 0 4px 1px var(--black);
		color: var(--white);
		padding: 35px;
		height: 78vh;
		border-radius: 25px;
		position: relative;
		display: flex;
		flex-direction: column;
		justify-content: flex-end;
		margin-bottom: 20px; /* Adiciona o espaçamento abaixo do box de favoritos */
	}

	h3{
        margin-top: -10px; /* Ajuste a distância do topo */
        margin-bottom: 10px; /* Ajuste a distância abaixo do título */
        font-size: 1.1rem; /* Tamanho da fonte */
    }

	/* Estilo para os itens de mensagem (caixas internas) */
	.message-box {
		background-color: var(--secondary-color); /*cor das caixas menores*/
		color: var(--text-color); /*Cor do texto*/
		padding: 1.1rem; /*Tamanho das caixas menores*/
		border-radius: 15px; /*Arredondamento das caixas internas*/
		max-width: 80%; /* Define a largura máxima da mensagem em relação à caixa principal */
		word-wrap: break-word; /* Garante que palavras longas sejam quebradas */
    	word-break: break-word; /* Compatibilidade adicional com navegadores antigos */
	}

	.message-box.left {
		align-self: flex-start; /* Alinha mensagens do lado esquerdo */
		background-color: var(--white); /* Cor da mensagem da GPT */
	}

	.message-box.right {
		align-self: flex-end; /* Alinha mensagens do lado direito */
		background-color: var(--secondary-color); /* Cor da mensagem do usuário */
		color: var(--text-color); /* Cor do texto da mensagem do usuário */
	}

	.message-box.activity {
		font-style: italic; /* Estilo de fonte itálico para mensagens de atividade */
	}
	/* Caixa de entrada de texto e botão */
	.input, 
	.button {
		background-color: var(--white); /*Cor do botão*/
   		color: var(--button-text-color); /*cor do texto nos botões*/
		box-shadow: 0 4px 1px var(--black); /*Sombras das caixas*/
		margin-top: 5px; /*Distância das mensagens já enviadas*/
		border-radius: 10px; /*Arredondamento das bordas*/
	}

	/* Para as mensagens (box internos) não ultrapassarem a largura da caixa maior */
	.messages-list {
		display: flex;
		flex-direction: column; /* Empilha as mensagens verticalmente */
		align-items: flex-start; /* Por padrão, mensagens começam alinhadas à esquerda */
		max-height: 75vh; /* Altura máxima da lista de mensagens */
		overflow-y: auto; /* Adiciona barra de rolagem se necessário */
		gap: 10px; /* Espaçamento entre as mensagens */
		flex-grow: 1;
	}

	/* Estilização das barras de rolagem */
	.messages-list::-webkit-scrollbar {
		width: 12px; /* Largura da barra */
	}

	.messages-list::-webkit-scrollbar-thumb {
		background-color: var(--secondary-color); /* Cor da barra de rolagem */
		border-radius: 10px; /* Arredondamento */
		border: 3px solid transparent; /* Espaço entre a barra e o conteúdo */
	}

	.messages-list::-webkit-scrollbar-track {
		background-color: rgba(0, 0, 0, 0.05); /* Cor do track */
	}

	/*Efeito no botão*/
	.button:hover {
		background-color: var(--secondary-color); /*Muda a cor do botão quando selecionado*/
	}
	/* Foco no botão */
	.button:active{
		outline: 7px solid var(--button-active); /* Indicador visual ao focar no botão */
	}

	/* Estilo do input de mensagem */
	.input {
		margin-right: 8px; /*Espaço entre o input e o botão */
	}
	
	/*Alinhamento da entrada de texto e botão*/
	.field {
		display: flex; /* Organiza os elementos horizontalmente */
    	align-items: center; /* Alinha os itens ao centro verticalmente */
    	justify-content: space-between; /* Espaço entre o input e o botão */
    	width: 100%; /* Garante que o campo de entrada e o botão ocupem toda a largura */
	}

	.message-box strong {
		color: rgb(19, 82, 119);
		font-weight: bold;
	}

	

</style>

<!--Estrutura HTML principal-->
<div class="box"> 
	
	<ul class="messages-list">
		{#each messages as msg}
			<li class="message-box {msg.username === 'assistant' ? 'left' : 'right'} {msg.is_activity ? 'activity' : ''}">
				<strong>{msg.username}:</strong> 
          <button
			    class="button is-small is-primary"
			    on:click={() => addToFavorites(msg)}
		      >
			      Add to Favorites
		    </button>
				{@html renderMarkdown(msg.content)}
			</li>
		{/each}
	</ul>

	<div class="field {isLoading ? 'placeholder' : ''}">
		<input
			class="input"
			type="text"
			placeholder="Type your message"
			bind:value={message}
		/>
		<button class="button {isLoading ? 'is-loading' : ''}" on:click={handleSend}>Send</button>
	</div>
</div>

