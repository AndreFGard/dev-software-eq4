<script lang="ts">
    import { loginStatus, setLoggedIn } from "../api";
    import { Dialog, DialogContent, DialogTrigger, DialogTitle, DialogDescription, DialogClose } from '../lib/components/ui/dialog';
    let activeTab = "";
    import { username } from "../api";

    let showLoginDialog = false;
    let showRegisterDialog = false;

    const handleLogIn = () => {
    showLoginDialog = true;};

  const handleRegister = () => {
    showRegisterDialog = true;};

    const confirmLogin = () => {
    setLoggedIn(true);
    showLoginDialog = false;
  };
  let tname='';
  const confirmRegister = () => {
    setLoggedIn(true);
    showRegisterDialog = false;
    username.set(tname);
  };

  const handleSignOut = () => {
    setLoggedIn(false);
    showRegisterDialog = false;
    showLoginDialog = false;

  };


</script>

<div class="login-register-container">
    {#if $loginStatus == false}

<Dialog bind:open={showLoginDialog}>
    <DialogTrigger>
    <button class="button is-primary" on:click={handleLogIn}>Login</button>  
    </DialogTrigger>
<DialogContent>
<DialogTitle>Login</DialogTitle>
<DialogDescription>Fill the blanks with your credentials</DialogDescription>
        <input type="text" placeholder="Username" class="border p-2 w-full rounded" />
        <input type="password" placeholder="Password" class="border p-2 w-full rounded mt-2" />
  <DialogClose>
    <button on:click={confirmLogin} class="bg-purple-600 text-white px-4 py-2 rounded w-full mt-4">
      Login
    </button>
        </DialogClose>
</DialogContent>
</Dialog>


    <Dialog bind:open={showRegisterDialog}>
     <DialogTrigger>
        <button class="button is-link" on:click={handleRegister}>Register</button>
    </DialogTrigger>
    <DialogContent>
      <DialogTitle>Register</DialogTitle>
      <DialogDescription>Create an account</DialogDescription>
      <input type="text" placeholder="Username" class="border p-2 w-full rounded" bind:value={tname}/>
      <input type="password" placeholder="Password" class="border p-2 w-full rounded mt-2" />
      <DialogClose>
        <button on:click={confirmRegister} class="bg-purple-600 text-white px-4 py-2 rounded w-full mt-4">
          Create account
        </button>
      </DialogClose>
    </DialogContent>
  </Dialog>
  
    {:else}

    <button class="button is-link" on:click={handleSignOut}>Sign Out</button>

    {/if}
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