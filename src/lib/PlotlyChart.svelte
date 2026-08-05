<script lang="ts">
  import Plotly from 'plotly.js-cartesian-dist-min';
  import type { Data, Layout, Config } from 'plotly.js';
  import { onMount } from 'svelte';
  import { labLayout, labConfig } from './plotly-theme';

  interface Props {
    data: Data[];
    layout?: Partial<Layout>;
    config?: Partial<Config>;
  }

  let { data, layout = {}, config = {} }: Props = $props();
  let container: HTMLDivElement;

  function mergedLayout(): Partial<Layout> {
    return { ...labLayout, ...layout };
  }

  function mergedConfig(): Partial<Config> {
    return { ...labConfig, ...config };
  }

  onMount(() => {
    Plotly.newPlot(container, data, mergedLayout(), mergedConfig());

    const ro = new ResizeObserver(() => {
      Plotly.Plots.resize(container);
    });
    ro.observe(container);

    return () => {
      Plotly.purge(container);
      ro.disconnect();
    };
  });

  $effect(() => {
    if (container) {
      Plotly.react(container, data, mergedLayout(), mergedConfig());
    }
  });
</script>

<div bind:this={container} class="plotly-chart"></div>

<style>
  .plotly-chart {
    width: 100%;
    min-height: 300px;
  }
</style>
