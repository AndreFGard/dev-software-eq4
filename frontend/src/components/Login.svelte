<script lang="ts">
    let activeTab = "";
</script>

<div class="login-register-container">
    <button class="button is-primary" on:click={() => activeTab = "login"}>Login</button>
    <button class="button is-link" on:click={() => activeTab = "register"}>Register</button>
</div>

<style>
    .login-register-container {
        display: flex;
        gap: 10px;
        margin-left: 20px;
        margin-bottom: -5px; /* Ajuste fino para alinhar com a linha */
    }
    
    .button {
        border-radius: 15px;
        font-size: 1.0rem;
        padding: 8px 16px;
        height: 38px;
        border: none;
        cursor: pointer;
        transition: background 0.3s ease;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 2px 2px 4px rgba(0, 0, 0, 0.1);
        margin-bottom: 2px; /* Alinhamento fino com a linha */
    }


    .button.is-primary {
        background-color: var(--accent-color);
        color: white;
    }

    .button.is-primary:hover {
        background-color: var(--button-active);
    }

    .button.is-link {
        background-color: var(--secondary-color);
        color: var(--text-color);
    }

    .button.is-link:hover {
        background-color: var(--button-active);
    }
</style>