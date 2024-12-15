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

	/* Estilo para os itens de mensagem (caixas interno) */
	.message-box {
		background-color: var(--secondary-color); /*cor das caixas menores*/
		color: var(--text-color); /*Cor do texto*/
		padding: 25px; /*Tamanho das caixas menores*/
		border-radius: 15px; /*Arredondamento das caixas internas*/
		margin-bottom: 15px; /*espaço entre as caixas internas*/
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
		max-height: 80vh; /*Ajuste para usar 80% da altura da tela */
		overflow-y: auto; /*Adiciona barra de rolagem se necessário*/
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
<div class="box"> 
	<h3>Messages:</h3>
	<ul class="messages-list">
		{#each messages as msg}
			<li class="message-box">
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

