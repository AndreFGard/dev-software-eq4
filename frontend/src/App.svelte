<script lang="ts">
  import { Router, Route } from 'svelte-routing';
  import Home from './routes/Home.svelte';
  import Application from './routes/Application.svelte';
</script>
<Router>
  <Route path="/" component={Home} />
  <Route path="/app" component={Application} />
</Router>