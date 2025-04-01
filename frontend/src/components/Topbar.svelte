<script>
  import { loginStatus, setLoggedIn } from "../api"

  import { Dialog, DialogContent, DialogTrigger, DialogTitle, DialogDescription, DialogClose } from '../lib/components/ui/dialog';

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

  const confirmRegister = () => {
    setLoggedIn(true);
    showRegisterDialog = false;
  };

  const handleSignOut = () => {
    setLoggedIn(false);
    showRegisterDialog = false;
    showLoginDialog = false;

  };
</script>

<div class="topbar flex items-center justify-between bg-white-900 text-white p-4 border-b-2 border-sky-600">
  <div class="w-[60%] mx-auto flex justify-between items-center">
    <h1 class="text-3xl font-bold text-sky-600">Mape.ia✈️</h1>
    <div class="flex space-x-2 ml-auto">
      {#if $loginStatus == false}

      <Dialog bind:open={showLoginDialog}>
        <DialogTrigger>
        <button 
          on:click={handleLogIn} 
          class="px-4 py-2 text-blue-500 border-2 border-blue-500 rounded-lg hover:bg-blue-100 transition font-bold">
          Login
        </button>
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
        <button 
          on:click={handleRegister} 
          class="px-4 py-2 text-white font-bold bg-sky-600 hover:bg-sky-700 transition rounded-lg">
          Register
        </button>
      </DialogTrigger>
      <DialogContent>
        <DialogTitle>Register</DialogTitle>
        <DialogDescription>Create an account</DialogDescription>
        <input type="text" placeholder="Username" class="border p-2 w-full rounded" />
        <input type="password" placeholder="Password" class="border p-2 w-full rounded mt-2" />
        <DialogClose>
          <button on:click={confirmRegister} class="bg-purple-600 text-white px-4 py-2 rounded w-full mt-4">
            Create account
          </button>
        </DialogClose>
      </DialogContent>
    </Dialog>
      {:else}
        <button 
          on:click={handleSignOut} 
          class="px-4 py-2 text-white font-bold bg-gray-500 hover:bg-gray-600 transition rounded-lg">
          Sign Out
        </button>
      {/if}
    </div>
  </div>
</div>
