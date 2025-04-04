<script lang="ts">
	import type { Activity, Message } from "../api";
	export let addToFavorites: (msg: Message) => Promise<Activity[]>;
	import { marked } from "marked";
	import Login from "./Login.svelte";
	export let messages: (Message | null)[] = [];
	export let message = "";
	export let handleAdd: () => void;
	import Cronogram from "./Cronogram.svelte";
	let isLoading = false;

	async function handleSend() {
		isLoading = true;
		await handleAdd();
		isLoading = false;
	}

	import { afterUpdate } from "svelte";
	let messagesList: HTMLUListElement;
	function scrollToBottom() {
		if (messagesList) {
			messagesList.scrollTo({
				top: messagesList.scrollHeight,
				behavior: "smooth",
			});
		}
	}

	// Trigger scroll after updates
	afterUpdate(() => {
		scrollToBottom();
	});

	marked.use({
		breaks: true,
		gfm: true,
	});

	function renderMarkdown(content: string) {
		return marked(content);
	}

	import { Skeleton } from "$lib/components/ui/skeleton";
	import { username } from "../api";
	let storedUsername: string | null = "";
	import { onMount } from 'svelte';

	// Watch for changes to the username store and update localStorage
	$: if ($username) {
		localStorage.setItem("username", $username);
	}


	function generateRandomUsername() {
		return "user_" + Math.random().toString(36).substring(2, 8);
	}
	
	function initUsername() {
		storedUsername = localStorage.getItem("username");
		if (!storedUsername) {
			storedUsername = generateRandomUsername();
			localStorage.setItem("username", storedUsername);
		}
		username.set(storedUsername);
	}

	initUsername();
	console.log($username);
</script>

<div class="box">
	<div class="header-wrapper">
		<div class="header-content">
			<h2 class="app-title">Mape.ia✈️</h2>
			<Login />
			<Cronogram></Cronogram>
		</div>
	</div>
	<ul class="messages-list" bind:this={messagesList}>
		{#each messages as msg}
			{#if msg === null}
				<strong>assistant:</strong>
				<li class="message-box left skeleton-block">
					<Skeleton
						class="h-[20px] bg-black/10 w-full max-w-[60rem] rounded-full"
					></Skeleton>
					<Skeleton
						class="h-[20px] bg-black/10 w-[30rem] rounded-full"
					></Skeleton>
					<Skeleton
						class="h-[20px] bg-black/10 w-[35rem] rounded-full"
					></Skeleton>
				</li>
			{:else}
				<li
					class="message-box {msg.username === 'assistant'
						? 'left'
						: 'right'}"
				>
					<div style="display: flex; align-items: center; gap: 10px;">
						<strong>{msg.username}:</strong>
						{#if msg.id !== null}
							<button
								class="button is-primary favorite-button"
								on:click={() => addToFavorites(msg)}
								>Add to Favorites
							</button>
						{/if}
					</div>
					{@html renderMarkdown(msg.content)}
				</li>
			{/if}
		{/each}
	</ul>

	<div class="field {isLoading ? 'placeholder' : ''}">
		<input
			class="input"
			type="text"
			placeholder="Type your message"
			bind:value={message}
		/>
		<button
			class="button {isLoading ? 'is-loading' : ''}"
			on:click={handleSend}>Send</button
		>
	</div>
</div>

<style>
	:root {
		--primary-color: rgb(163, 201, 241);
		--secondary-color: rgb(191, 226, 245);
		--text-color: rgb(47, 49, 91);
		--button-text-color: rgb(47, 49, 91);
		--button-active: rgb(117, 169, 198);
		--black: rgba(0, 0, 0, 0.1);
		--white: rgb(255, 255, 255);
		--accent-color: rgb(39, 121, 168);
	}

	.header-wrapper {
		width: 100%;
		position: relative;
		margin-bottom: 15px;
		padding-bottom: 14px;
		border-bottom: 2px solid var(--secondary-color);
	}

	.header-content {
		display: flex;
		justify-content: space-between;
		align-items: flex-end;
		width: 100%;
	}

	.app-title {
		color: var(--accent-color);
		font-size: 2.2rem;
		margin: 0; /* Reset de margens */
		padding-bottom: 0;
		display: flex;
		align-items: center;
		text-shadow: 2px 2px 3px rgba(0, 0, 0, 0.2);
		line-height: 1; /* Garante alinhamento preciso */
	}

	.box {
		background-color: var(--primary-color);
		box-shadow: 0 4px 10px var(--black);
		color: var(--white);
		padding: 25px;
		height: 100%;
		width: 66%;
		border-radius: 25px;
		display: flex;
		flex-direction: column;
		overflow: hidden;
		position: relative;
	}

	.message-box {
		background-color: var(--secondary-color);
		color: var(--text-color);
		padding: 1.1rem;
		border-radius: 15px;
		max-width: 80%;
		min-width: 30%;
		word-wrap: break-word;
		word-break: break-word;
	}

	.message-box.left {
		align-self: flex-start;
		background-color: var(--white);
	}

	.message-box.right {
		align-self: flex-end;
		background-color: var(--secondary-color);
		color: var(--text-color);
	}

	.input,
	.button {
		background-color: var(--white);
		color: var(--button-text-color);
		box-shadow: 3px 3px 3px var(--black);
		border-radius: 15px;
		padding: 20px;
		transition: 0.3s;
	}

	.messages-list {
		display: flex;
		flex-direction: column;
		align-items: flex-start;
		height: calc(100% - 120px);
		overflow-y: auto;
		gap: 15px;
		flex-grow: 1;
		margin-bottom: 15px;
	}

	.messages-list::-webkit-scrollbar {
		width: 10px;
	}

	.messages-list::-webkit-scrollbar-thumb {
		background-color: var(--secondary-color);
		border-radius: 10px;
		border: 3px solid transparent;
	}

	.messages-list::-webkit-scrollbar-track {
		background-color: rgba(0, 0, 0, 0.05);
	}

	.button:hover {
		background-color: var(--button-active);
	}

	.button:active {
		outline: 4px solid var(--button-active);
	}

	.input {
		flex: 1;
		min-width: 0;
	}

	.field {
		display: flex;
		gap: 10px;
		align-items: center;
		position: sticky;
		background: var(--primary-color);
	}

	.message-box strong {
		color: var(--accent-color);
		font-weight: bold;
		margin-right: 5px;
	}

	.favorite-button {
		padding: 12px;
		font-size: 12px;
		background-color: var(--accent-color);
		color: var(--white);
		border-radius: 15px;
		cursor: pointer;
	}
</style>
