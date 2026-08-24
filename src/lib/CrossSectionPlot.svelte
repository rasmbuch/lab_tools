<script lang="ts">
  import { Plot } from 'svelteplot';
  // @ts-ignore — svelteplot exports .svelte subpaths without type conditions
  import Line from 'svelteplot/marks/Line.svelte';
  // @ts-ignore
  import Dot from 'svelteplot/marks/Dot.svelte';
  // @ts-ignore
  import RuleX from 'svelteplot/marks/RuleX.svelte';
  // @ts-ignore
  import Frame from 'svelteplot/marks/Frame.svelte';
  // @ts-ignore
  import Pointer from 'svelteplot/marks/Pointer.svelte';
  import { sigfigs } from './format';
  import type { EnergyScanPoint } from './eta';

  interface Props {
    data: EnergyScanPoint[];
    currentKeV: number;
  }

  let { data, currentKeV }: Props = $props();

  let currentSigma = $derived(
    data.find(p => Math.abs(p.energy_keV - currentKeV) / currentKeV < 0.05)?.sigma_barn ?? 0
  );

  let markerData = $derived([{ energy_keV: currentKeV, sigma_barn: currentSigma }]);
  let ruleData = $derived([currentKeV]);

  let hovered: EnergyScanPoint | null = $state(null);

  function onPointerUpdate(pts: EnergyScanPoint[]) {
    hovered = pts.length > 0 ? pts[0] : null;
  }
</script>

<div class="cs-plot">
  <Plot
    height={220}
    x={{ type: 'log', label: 'photon energy [keV]', nice: false }}
    y={{ type: 'log', label: 'σ_photo [barn]', nice: false }}
    grid={false}
  >
    <Line
      data={data}
      x="energy_keV"
      y="sigma_barn"
      stroke="#16225C"
      strokeWidth={1.8}
      curve="linear"
    />
    <RuleX
      data={ruleData}
      stroke="#D4351F"
      strokeWidth={0.7}
      strokeDasharray="4 3"
      strokeOpacity={0.5}
    />
    {#if currentSigma > 0}
      <Dot
        data={markerData}
        x="energy_keV"
        y="sigma_barn"
        r={4}
        fill="#D4351F"
        stroke="#FBF9F4"
        strokeWidth={1.5}
      />
    {/if}
    <Pointer data={data} x="energy_keV" y="sigma_barn" onupdate={onPointerUpdate}>
      {#snippet children({ data: pts }: { data: EnergyScanPoint[] })}
        {#if pts.length > 0}
          <Dot data={pts} x="energy_keV" y="sigma_barn" r={3} fill="none" stroke="#16225C" strokeWidth={1.5} />
          <RuleX data={[pts[0].energy_keV]} stroke="#16225C" strokeWidth={0.5} strokeDasharray="2 2" strokeOpacity={0.4} />
        {/if}
      {/snippet}
    </Pointer>
    <Frame stroke="var(--color-text)" strokeOpacity={0.6} />
  </Plot>
  <div class="cs-readout">
    {#if hovered}
      {sigfigs(hovered.energy_keV, 4)} keV &middot; {sigfigs(hovered.sigma_barn, 4)} barn
    {/if}
  </div>
</div>

<style>
  .cs-plot {
    width: 100%;
    min-height: 220px;
    font-family: var(--font-mono);
    font-size: 10px;
    color: var(--color-text);
  }

  .cs-plot :global(figure) {
    margin: 0;
  }

  .cs-plot :global([aria-label="x-axis"] text),
  .cs-plot :global([aria-label="y-axis"] text) {
    font-family: var(--font-mono);
    font-size: 10px;
    fill: var(--color-text);
  }

  .cs-plot :global([aria-label="x-axis label"] text),
  .cs-plot :global([aria-label="y-axis label"] text) {
    font-family: var(--font-ui);
    font-size: 11px;
    fill: var(--color-text);
  }

  .cs-plot :global([aria-label="x-axis"] line),
  .cs-plot :global([aria-label="y-axis"] line) {
    stroke: var(--color-text);
    stroke-opacity: 0.3;
  }

  .cs-readout {
    font-family: var(--font-mono);
    font-size: 10px;
    color: var(--color-text-faint);
    text-align: right;
    height: 16px;
    padding-right: 4px;
    margin-top: 2px;
  }
</style>
