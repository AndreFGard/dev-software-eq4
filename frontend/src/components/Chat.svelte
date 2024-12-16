<script lang="ts"> //indica que o código dentro dessa tag está em TypeScript
	//exporta as variáveis que serão usadas fora do componente Svelte
	export let messages: { username: string; content: string }[] = []; //Lista de mensagens exibidas no chat
	export let message = "Hello sir"; //Mensagem inicial de exemplo
	export let handleAdd: () => void; //Função que será chamada ao clicar no botão de enviar mensagem
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
  	}

	/* Estilo para a caixa principal */
	.box{
		background-color: var(--primary-color); /*Cor da caixa maior */
		box-shadow: 0 4px 1px var(--black); /*Sombras das caixas*/
		color:var(--white); /*Cor de "Messages:"*/
		padding: 35px; /*Tamanho ou espaçamento das bordas*/
		width: 100%; /*Tamanho da caixa de texto*/
		max-width: 600; /*Largura da caixa*/
		border-radius: 30px; /*Arredondamento das bordas*/
		
	}

	/* Estilo para os itens de mensagem (caixas internas) */
	.message-box {
		background-color: var(--secondary-color); /*cor das caixas menores*/
		color: var(--text-color); /*Cor do texto*/
		padding: 25px; /*Tamanho das caixas menores*/
		border-radius: 15px; /*Arredondamento das caixas internas*/
		margin-bottom: 15px; /*espaço entre as caixas internas*/
		max-width: 70%; /* Define a largura máxima da mensagem em relação à caixa principal */
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
		max-height: 60vh; /* Altura máxima da lista de mensagens */
		overflow-y: auto; /* Adiciona barra de rolagem se necessário */
		gap: 10px; /* Espaçamento entre as mensagens */

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
		display: flex; /*organizar os elementos horizontalmente */
		align-items: center; /*Alinha os itens ao centro verticalmente */
		justify-content: center; /*Alinha os itens ao centro horizontalmente */
	}
</style>

<!--Estrutura HTML principal-->
<div class="box" style="max-height:30%;"> 
	<h3>Messages:</h3>
	<ul class="messages-list">
		{#each messages as msg}
			<li class="message-box {msg.username === 'GPT' ? 'left' : 'right'}">
				<strong>{msg.username}:</strong>
				{msg.content}
			</li>
		{/each}
	</ul>

	<div class="field">
		<input
			class="input"
			type="text"
			placeholder="Type your message"
			bind:value={message}
		/>
		<button class="button" on:click={handleAdd}>Send</button>
	</div>
</div>

