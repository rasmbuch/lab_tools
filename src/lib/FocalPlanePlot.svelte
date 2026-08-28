<script lang="ts">
  import { Plot } from 'svelteplot';
  // @ts-ignore — svelteplot exports .svelte subpaths without type conditions
  import Contour from 'svelteplot/marks/Contour.svelte';
  // @ts-ignore
  import Frame from 'svelteplot/marks/Frame.svelte';
  // @ts-ignore
  import Rect from 'svelteplot/marks/Rect.svelte';
  import { interpolatePlasma } from 'd3-scale-chromatic';
  import { sigfigs } from './format';

  interface Props {
    fwhm_x_nm: number;
    fwhm_y_nm: number;
    fluence_phcm2: number;
    sigma_photo: number;
    etaPrimeRatio: number;
    mode: 'gaussian' | 'flat-top';
    heatmapMode: 'eta' | 'eta_prime';
  }

  let { fwhm_x_nm, fwhm_y_nm, fluence_phcm2, sigma_photo, etaPrimeRatio, mode, heatmapMode }: Props = $props();

  const LN2 = Math.log(2);
  const NSTOPS = 64;

  let extent_x = $derived(2 * fwhm_x_nm);
  let extent_y = $derived(2 * fwhm_y_nm);

  let valueFn = $derived((x: number, y: number): number => {
    let envelope: number;
    if (mode === 'gaussian') {
      envelope = Math.exp(
        -4 * LN2 * (x ** 2 / fwhm_x_nm ** 2 + y ** 2 / fwhm_y_nm ** 2)
      );
    } else {
      const rx = fwhm_x_nm / 2;
      const ry = fwhm_y_nm / 2;
      envelope = (x ** 2 / rx ** 2 + y ** 2 / ry ** 2) <= 1 ? 1 : 0;
    }
    const eta = sigma_photo * fluence_phcm2 * envelope;
    return heatmapMode === 'eta' ? eta : eta * etaPrimeRatio;
  });

  let peakVal = $derived(
    heatmapMode === 'eta'
      ? sigma_photo * fluence_phcm2
      : sigma_photo * fluence_phcm2 * etaPrimeRatio
  );

  let thresholds = $derived((): number[] => {
    if (peakVal <= 0) return [0];
    const levels: number[] = [];
    const nLevels = 12;
    for (let i = 1; i <= nLevels; i++) {
      levels.push((peakVal * i) / nLevels);
    }
    if (peakVal >= 1 && !levels.includes(1)) {
      levels.push(1);
    }
    return levels.sort((a, b) => a - b);
  });

  const zeroGrey = 'rgb(42,42,42)';

  function thresholdPlasma(t: number): string {
    if (peakVal <= 0) return zeroGrey;
    const val = t * peakVal;
    if (peakVal < 1 || val < 1) {
      const grey = Math.round(42 + t * 120);
      return `rgb(${grey},${grey},${grey})`;
    }
    const plasmaT = (val - 1) / (peakVal - 1);
    return interpolatePlasma(plasmaT);
  }

  let label = $derived(heatmapMode === 'eta' ? 'η' : "η'");

  let gradientStops = $derived((): string[] => {
    const stops: string[] = [];
    for (let i = 0; i <= NSTOPS; i++) {
      const t = i / NSTOPS;
      stops.push(thresholdPlasma(t));
    }
    return stops;
  });

  let etaOnePercent = $derived(
    peakVal > 1 ? (1 / peakVal) * 100 : -1
  );

  let colorbarTicks = $derived((): { val: number; pct: number }[] => {
    if (peakVal <= 0) return [];
    const n = 4;
    const ticks: { val: number; pct: number }[] = [];
    for (let i = 0; i <= n; i++) {
      const val = (peakVal * i) / n;
      ticks.push({ val, pct: (i / n) * 100 });
    }
    return ticks;
  });
</script>

<div class="focal-plot">
  <div class="plot-row">
    <div class="plot-area">
      <Plot
        height={250}
        x={{ label: 'x [nm]', domain: [-extent_x, extent_x], nice: false }}
        y={{ label: 'y [nm]', domain: [-extent_y, extent_y], nice: false }}
        color={{
          type: 'linear',
          domain: [0, peakVal],
          interpolate: thresholdPlasma,
          legend: false,
          label: label,
        }}
        grid={false}
      >
        <Rect
          data={[{ x1: -extent_x, x2: extent_x, y1: -extent_y, y2: extent_y }]}
          x1="x1" x2="x2" y1="y1" y2="y2"
          fill={zeroGrey}
        />
        <Contour
          value={valueFn}
          fill="value"
          stroke="none"
          thresholds={thresholds()}
          x1={-extent_x}
          x2={extent_x}
          y1={-extent_y}
          y2={extent_y}
        />
        {#if peakVal >= 1}
          <Contour
            value={valueFn}
            fill="none"
            stroke="#D4351F"
            strokeWidth={1.5}
            thresholds={[1]}
            x1={-extent_x}
            x2={extent_x}
            y1={-extent_y}
            y2={extent_y}
          />
        {/if}
        <Frame stroke="var(--color-text)" strokeOpacity={0.5} />
      </Plot>
    </div>

    <div class="colorbar">
      <div class="colorbar-label">{label}</div>
      <div class="colorbar-body">
        <svg class="colorbar-svg" viewBox="0 0 12 200" preserveAspectRatio="none">
          <defs>
            <linearGradient id="focal-cbar-grad" x1="0" x2="0" y1="1" y2="0">
              {#each gradientStops() as color, i}
                <stop offset="{(i / NSTOPS) * 100}%" stop-color={color} />
              {/each}
            </linearGradient>
          </defs>
          <rect x="0" y="0" width="12" height="200" fill="url(#focal-cbar-grad)" />
          {#if etaOnePercent > 0 && etaOnePercent < 100}
            <line
              x1="0" x2="12"
              y1={200 - etaOnePercent * 2} y2={200 - etaOnePercent * 2}
              stroke="#D4351F" stroke-width="2"
            />
          {/if}
        </svg>
        <div class="colorbar-ticks">
          {#each colorbarTicks() as tick}
            <span class="colorbar-tick" style="bottom:{tick.pct}%">
              {sigfigs(tick.val, 2)}
            </span>
          {/each}
          {#if etaOnePercent > 0 && etaOnePercent < 100}
            <span class="colorbar-tick eta-one-tick" style="bottom:{etaOnePercent}%">1</span>
          {/if}
        </div>
      </div>
    </div>
  </div>
</div>

<style>
  .focal-plot {
    width: 100%;
    font-family: var(--font-mono);
    font-size: 10px;
    color: var(--color-text);
  }

  .plot-row {
    display: flex;
    align-items: stretch;
    gap: 6px;
  }

  .plot-area {
    flex: 1;
    min-width: 0;
    width: 100%;
  }
  .plot-area :global(figure),
  .plot-area :global(svg),
  .plot-area :global(canvas) {
    width: 100%;
    height: 100%;
  }

  .focal-plot :global(figure) {
    margin: 0;
  }

  .focal-plot :global([aria-label="x-axis"] text),
  .focal-plot :global([aria-label="y-axis"] text) {
    font-family: var(--font-mono);
    font-size: 10px;
    fill: var(--color-text);
  }

  .focal-plot :global([aria-label="x-axis label"] text),
  .focal-plot :global([aria-label="y-axis label"] text) {
    font-family: var(--font-ui);
    font-size: 11px;
    fill: var(--color-text);
  }

  .focal-plot :global([aria-label="x-axis"] line),
  .focal-plot :global([aria-label="y-axis"] line) {
    stroke: var(--color-text);
    stroke-opacity: 0.3;
  }

  /* ── Colorbar (vertical, right side) ───────────────────────── */

  .colorbar {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding-top: 4px;
    width: 40px;
    flex-shrink: 0;
  }

  .colorbar-label {
    font-family: var(--font-ui);
    font-size: 10px;
    color: var(--color-text-faint);
    margin-bottom: 4px;
  }

  .colorbar-body {
    flex: 1;
    display: flex;
    align-items: stretch;
    gap: 3px;
    min-height: 0;
  }

  .colorbar-svg {
    width: 12px;
    height: 100%;
    display: block;
    border: 1px solid rgba(23, 21, 18, 0.4);
  }

  .colorbar-ticks {
    position: relative;
    width: 24px;
  }

  .colorbar-tick {
    position: absolute;
    transform: translateY(50%);
    font-family: var(--font-mono);
    font-size: 8px;
    color: var(--color-text-faint);
    white-space: nowrap;
    line-height: 1;
  }

  .colorbar-tick.eta-one-tick {
    color: #D4351F;
    font-weight: 600;
    font-size: 9px;
  }
</style>
