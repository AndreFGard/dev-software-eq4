<script lang="ts">
    import "../app.css";
    
    import Chat from '../components/Chat.svelte';
    import Sidebar from '../components/Sidebar.svelte';
    import { addMessage, getMessages, addToFavoritesBack, getFavorites } from '../api.js';
    import type { Message, Activity } from '../api.js';
    
    import { onMount } from 'svelte';
    import { removeFromFavoritesBack } from '../api';
    import { writable } from "svelte/store";
    
    let favorites: Activity[] = [];
    let error: string;
    
    let messages: (Message | null)[] = [
      { username: 'assistant', content: 'Hello! Im GPT.' },
      { username: 'User', content: "Can you help me?" }
    ];
    let username = 'User';
    let message = '';
    
    let isExpanded = writable(false);
    
    onMount(async () => {
      try {
        messages = await getMessages(username);
        favorites = await getFavorites(username);
      } catch (e: any) {
        error = e.message || e;
      }
    });
    
    async function handleAdd() {
      if (!message.trim()) {
        error = 'Message cannot be empty';
        return;
      }
      try {
        messages = messages.concat([{ username, content: message }, null]);
        messages = await addMessage({ username, content: message});
        message = '';
      } catch (e) {
        console.error(e);
      }
    }
    
    export async function addToFavorites(msg: Message) {
      console.log(`sending request to add ${msg} to favorites`);
      favorites = await addToFavoritesBack(username, msg);
    }
    
    async function removeFromFavorites(_username:string, act: Activity) {
    
      favorites = await removeFromFavoritesBack(username, act);
    
    }
  </script>
  
  <main id="chat-cont">
    <div class="content-wrapper">
      <Sidebar {favorites} {username} class="{isExpanded ? 'sidebar expanded' : 'sidebar collapsed'}" removeFromFavorites={removeFromFavorites} bind:isExpanded />
      <Chat {handleAdd} bind:messages={messages} bind:message={message} addToFavorites={addToFavorites} />
    </div>
  </main>
  
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
      --background-color: rgb(245, 245, 245);
      --border-radius: 15px;
      --box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
    }
  
  #chat-cont {
      height: 100vh;
      padding: 20px;
      background: var(--background-color);
      box-sizing: border-box;
      display: flex;
      justify-content: center;
    }
  
    .content-wrapper {
      display: flex;
      height: 100%;
      width: 100%; 
      gap: 20px;
    }
  
    .sidebar {
      width: 33.33%; /* Força 1/3 da tela */
      min-width: 0;
    }
  
    .chat {
      width: 66.66%; /* Força 2/3 da tela */
      min-width: 0; /* Permite encolhimento */
    }
    
    @media (max-width: 768px) {
      .sidebar, .chat {
        max-width: 100%;
        min-width: 100%;
      }
      .header {
        flex-direction: column;
        align-items: flex-start;
      }
      .login-register-container {
        margin-left: 0;
        margin-top: 10px;
      }
    }
  </style>
  