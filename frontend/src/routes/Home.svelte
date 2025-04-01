  <script>
    import { link } from 'svelte-routing'
    import Topbar from '../components/Topbar.svelte'
    import agenda  from '../assets/agenda.png'
    import search from '../assets/search.png'
  </script>
  
  <main>
    <Topbar></Topbar>
    <div class="w-full max-w-[60%] mx-auto mt-32">
      <h1 class="text-center text-3xl font-bold text-sky-600">Introducing Mape.ia✈️</h1>
      <br>
      <br>
      <p class="text-center max-w-[60%] mx-auto">"Your journey, your way"</p>
      <br>
      <br>
      <div class="flex items-center justify-center">
        <a href="/app" use:link class="inline-flex justify-center px-6 py-3 bg-purple-600 text-white font-semibold rounded-lg hover:bg-purple-800 transition">Test the AI</a>
    </div>
  </div>
  <div class="w-full max-w-[60%] mx-auto mt-24">
    <h2 class="text-2xl font-bold text-sky-600 text-center">Explore the Features</h2>
    <p class="text-justify mt-10 mx-auto max-w-[80%]">Our chatbot system leverages advanced artificial intelligence to retrieve up-to-date travel information from reliable sources. Using Retrieval-Augmented Generation (RAG), we ensure that all data is accurate and contextually relevant, providing users with precise and optimized travel planning. Additionally, the system personalizes itineraries based on user preferences, offering tailored recommendations for a seamless travel experience.

    </p>
  </div>

  <div class="w-full max-w-[60%] mx-auto mt-32 grid grid-cols-1 md:grid-cols-2 gap-16">
    <div>
      <h3 class="text-xl font-bold text-sky-600">Accurate & Updated Information</h3>
      <p class="mt-2">Using Retrieval-Augmented Generation (RAG), our system ensures that travel details are always current, pulling data from reliable sources in real time.</p>
    </div>
    <div class="h-[120px]"> <img src={search} alt="SearchWebsites" class="ml-auto w-[200px] h-auto" ></div>
    <div class="h-[120px]"> <img src={agenda} alt="Agenda" style="width: 200px; height: auto;"></div>
    <div>
      <h3 class="text-xl font-bold text-sky-600">Personalized Itineraries</h3>
      <p class="mt-2">Based on user preferences, the AI crafts tailored travel plans, optimizing schedules and recommendations for a seamless experience.</p>
    </div>
  </div>

  <div class="h-20"></div>
</main> 
  
  <style></style>