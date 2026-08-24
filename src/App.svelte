<script lang="ts">
  import { parseHash, type Route } from './lib/router';
  import Sidebar from './Sidebar.svelte';
  import Dashboard from './Dashboard.svelte';
  import EnergyConverter from './EnergyConverter.svelte';
  import IntensityCalculator from './IntensityCalculator.svelte';
  import SolidAngleCalculator from './SolidAngleCalculator.svelte';
  import EtaCalculator from './EtaCalculator.svelte';
  import MathsReference from './MathsReference.svelte';

  let currentRoute: Route = $state(parseHash());

  $effect(() => {
    const onHashChange = () => { currentRoute = parseHash(); };
    window.addEventListener('hashchange', onHashChange);
    return () => window.removeEventListener('hashchange', onHashChange);
  });
</script>

<div class="shell">
  <Sidebar {currentRoute} />

  <main>
    {#if currentRoute === 'dashboard'}
      <Dashboard />
    {:else if currentRoute === 'energy'}
      <EnergyConverter />
    {:else if currentRoute === 'intensity'}
      <IntensityCalculator />
    {:else if currentRoute === 'eta'}
      <EtaCalculator />
    {:else if currentRoute === 'omega'}
      <SolidAngleCalculator />
    {:else if currentRoute === 'about'}
      <MathsReference />
    {/if}
  </main>
</div>

<style>
  .shell {
    display: flex;
    min-height: 100vh;
  }

  main {
    flex: 1;
    min-width: 0;
  }
</style>
