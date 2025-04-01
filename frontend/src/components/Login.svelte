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