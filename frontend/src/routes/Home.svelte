  <script>
    import { link } from 'svelte-routing'
    import Topbar from '../components/Topbar.svelte'
  </script>
  
  <main>
    <Topbar></Topbar>
    <div class="w-full max-w-[60%] mx-auto mt-32">
      <h1 class="text-center text-3xl font-bold text-sky-600">Introducing Mape.ia✈️</h1>
      <br>
      <p class="text-center max-w-[60%] mx-auto">Lorem ipsum dolor, sit amet consectetur adipisicing elit. Quam nobis eius aliquid, quis saepe expedita dolore adipisci sit dicta sunt tenetur, est nesciunt iusto non! Dolores tenetur molestiae praesentium recusandae.</p>
      <br>
      <div class="flex items-center justify-center">
        <a href="/app" use:link class="inline-flex justify-center px-6 py-3 bg-purple-600 text-white font-semibold rounded-lg hover:bg-purple-800 transition">Test the AI</a>
    </div>
  </div>
  <div class="w-full max-w-[60%] mx-auto mt-32">
    <h2 class="text-2xl font-bold text-sky-600 text-center">Explore the Features</h2>
    <p class="text-center mt-10">Descrição da IA</p>
  </div>

  <div class="w-full max-w-[60%] mx-auto mt-32 grid grid-cols-1 md:grid-cols-2 gap-16">
    <div>
      <h3 class="text-xl font-bold text-sky-600">Vantagem 1</h3>
      <p class="mt-2">Descrição da vantagem 1</p>
    </div>
    <div class="h-40 bg-gray-200 rounded-lg"></div>
    <div class="h-40 bg-gray-200 rounded-lg"></div>
    <div>
      <h3 class="text-xl font-bold text-sky-600">Vantagem 2</h3>
      <p class="mt-2">Descrição da vantagem 2</p>
    </div>
  </div>

  <div class="h-20"></div>
</main>
  
  <style></style>