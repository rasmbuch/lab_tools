<script lang="ts">
  import { photonEnergy, pulseEnergy, fwhm, pulseDuration, spatialMode, transmission } from './lib/stores.svelte';
  import { ELEMENTS, getElementInfo, getCrossSections, type ElementSymbol } from './lib/xray';
  import { computeEta, computeEnergyScan } from './lib/eta';
  import { sigfigs } from './lib/format';
  import BeamInputs from './lib/BeamInputs.svelte';
  import CrossSectionPlot from './lib/CrossSectionPlot.svelte';
  import FocalPlanePlot from './lib/FocalPlanePlot.svelte';

  let element: ElementSymbol = $state('Au');
  let heatmapMode: 'eta' | 'eta_prime' = $state('eta');
  let shellTableOpen = $state(false);
  let tauOverride_fs: string = $state('');
  let tauOverride_s = $derived(
    tauOverride_fs !== '' ? parseFloat(tauOverride_fs) * 1e-15 : undefined
  );
  type SigmaUnit = 'barn' | 'cm²' | 'm²';
  let sigmaUnit: SigmaUnit = $state('barn');

  function fmt(v: number): string {
    if (!Number.isFinite(v) || v <= 0) return '—';
    return sigfigs(v, 4);
  }

  function fmtLarge(v: number): string {
    if (!Number.isFinite(v) || v <= 0) return '0';
    return sigfigs(v, 3);
  }

  let beamParams = $derived({
    photonEnergy_eV: photonEnergy.eV,
    pulseEnergy_J: pulseEnergy.J * transmission.value,
    fwhm_x_m: fwhm.x_m,
    fwhm_y_m: fwhm.y_m,
    pulseDuration_s: pulseDuration.s,
    mode: spatialMode.value,
  });

  let etaResult = $derived(computeEta(beamParams, element, tauOverride_s));
  let crossSections = $derived(getCrossSections(element, photonEnergy.eV / 1e3));
  let energyScan = $derived(computeEnergyScan(beamParams, element));

  let etaPrimeRatio = $derived(
    etaResult.eta_photo > 0 ? etaResult.eta_prime_val / etaResult.eta_photo : 0
  );

  let isNonlinear = $derived(etaResult.eta_photo >= 1);

  let sigmaDisplay = $derived(() => {
    const sigma_cm2 = crossSections.sigma_total;
    if (sigmaUnit === 'barn') return fmt(sigma_cm2 * 1e24);
    if (sigmaUnit === 'cm²') return sigfigs(sigma_cm2, 4);
    return sigfigs(sigma_cm2 * 1e-4, 4); // m²
  });


  function tauDisplay(tau_s: number): string {
    if (!Number.isFinite(tau_s) || tau_s <= 0) return '—';
    const tau_as = tau_s * 1e18;
    if (tau_as < 1000) return `${sigfigs(tau_as, 3)} as`;
    const tau_fs = tau_s * 1e15;
    return `${sigfigs(tau_fs, 3)} fs`;
  }

  function elementZ(sym: ElementSymbol): number {
    return getElementInfo(sym).Z;
  }
</script>

<div class="calculator">
  <div class="tool-header">
    <div class="tool-header-top">
      <span class="tool-number">03</span>
      <span class="tool-category">focal map</span>
    </div>
    <h1>Photons per atom — η and η′</h1>
    <p class="tool-description">
      η = σ<sub>photo</sub>·Φ₀ over the whole pulse.
      η′ counts only what arrives inside the dominant core-hole lifetime.
    </p>
  </div>

  <div class="main-layout">
    <div class="col-left">
      <div class="section-label">Beam parameters</div>
      <BeamInputs />
    </div>

    <div class="col-right">
      <div class="result-band" class:nonlinear={isNonlinear}>
        <div class="result-block">
          <div class="result-label">η — photons per atom per pulse</div>
          <div class="result-number">{fmtLarge(etaResult.eta_photo)}</div>
        </div>
        <div class="result-block">
          <div class="result-label">η′ — within {etaResult.eta_prime_shell || '—'} hole ({tauDisplay(etaResult.eta_prime_tau_s)})</div>
          <div class="result-number">{fmtLarge(etaResult.eta_prime_val)}</div>
        </div>
        <div class="result-regime">
          <div class="result-label">regime</div>
          <div class="regime-name">{isNonlinear ? 'nonlinear' : 'linear'}</div>
          <div class="regime-note">{isNonlinear ? 'multiple hits per atom' : 'single-hit regime'}</div>
        </div>
      </div>

      <div class="grid-2x2">
        <div class="grid-cell">
          <div class="plot-header">
            <span class="section-label" style="margin-bottom:0">Focal plane</span>
            <div class="heatmap-toggle">
              <button
                class="toggle-btn"
                class:active={heatmapMode === 'eta'}
                onclick={() => heatmapMode = 'eta'}
              >η</button>
              <button
                class="toggle-btn"
                class:active={heatmapMode === 'eta_prime'}
                onclick={() => heatmapMode = 'eta_prime'}
              >η′</button>
            </div>
          </div>
          <FocalPlanePlot
            fwhm_x_nm={fwhm.x_m * 1e9}
            fwhm_y_nm={fwhm.y_m * 1e9}
            fluence_phcm2={etaResult.fluence_phcm2}
            sigma_photo={crossSections.sigma_photo}
            {etaPrimeRatio}
            mode={spatialMode.value}
            {heatmapMode}
          />
        </div>

        <div class="grid-cell">
          <div class="plot-header">
            <span class="section-label" style="margin-bottom:0; text-transform:none">σ vs photon energy</span>
          </div>
          <CrossSectionPlot data={energyScan} currentKeV={photonEnergy.eV / 1e3} />
        </div>

        <div class="grid-cell">
          <div class="element-section">
            <div class="section-label">Element</div>
            <div class="element-picker">
              {#each ELEMENTS as el}
                <button
                  class="element-chip"
                  class:active={element === el}
                  onclick={() => element = el}
                >
                  <span class="element-sym">{el}</span>
                  <span class="element-z">{elementZ(el)}</span>
                  {#if element === el}
                    <span class="element-bar"></span>
                  {/if}
                </button>
              {/each}
            </div>
          </div>

          <div class="lifetime-section">
            <div class="section-label">Hole lifetime override</div>
            <div class="lifetime-chips">
              {#each etaResult.shells as s}
                <button
                  class="lifetime-chip"
                  class:active-lifetime={tauOverride_fs === '' ? s.name === etaResult.eta_prime_shell : sigfigs(s.tau_hole_s * 1e15, 3) === tauOverride_fs}
                  onclick={() => tauOverride_fs = sigfigs(s.tau_hole_s * 1e15, 3)}
                >
                  <span class="lifetime-shell">{s.name}</span>
                  <span class="lifetime-tau">{tauDisplay(s.tau_hole_s)}</span>
                </button>
              {/each}
            </div>
            <div class="lifetime-input-row">
              <input
                type="number"
                class="lifetime-input"
                placeholder="auto"
                bind:value={tauOverride_fs}
                step="any"
                min="0"
              />
              <span class="output-unit">fs</span>
              {#if tauOverride_fs !== ''}
                <button class="lifetime-clear" onclick={() => tauOverride_fs = ''}>clear</button>
              {/if}
            </div>
          </div>
        </div>

        <div class="grid-cell">
          <div class="output-group">
            <div class="section-label">Derived</div>
            <div class="output-rows">
              <div class="output-row">
                <span class="output-label">σ (total)</span>
                <span class="output-value">{sigmaDisplay()} <select class="unit-select" bind:value={sigmaUnit}><option value="barn">barn</option><option value="cm²">cm²</option><option value="m²">m²</option></select></span>
              </div>
              <div class="output-row">
                <span class="output-label">η (photo)</span>
                <span class="output-value">{fmt(etaResult.eta_photo)} <span class="output-unit">ph/atom</span></span>
              </div>
              <div class="output-row">
                <span class="output-label">η (total)</span>
                <span class="output-value">{fmt(etaResult.eta_total)} <span class="output-unit">ph/atom</span></span>
              </div>
              <div class="output-row">
                <span class="output-label">η′</span>
                <span class="output-value">{fmt(etaResult.eta_prime_val)} <span class="output-unit">ph/atom</span></span>
              </div>
            </div>
          </div>

          <details class="shell-details" bind:open={shellTableOpen}>
            <summary class="section-label clickable">Shell-resolved breakdown</summary>
            {#if etaResult.shells.length > 0}
              <div class="shell-table-wrap">
                <table class="shell-table">
                  <thead>
                    <tr>
                      <th>Shell</th>
                      <th>σ [barn]</th>
                      <th>η</th>
                      <th>Γ [eV]</th>
                      <th>τ<sub>hole</sub></th>
                      <th>η′</th>
                    </tr>
                  </thead>
                  <tbody>
                    {#each etaResult.shells as s}
                      <tr>
                        <td>{s.name}</td>
                        <td>{sigfigs(s.sigma_cm2 * 1e24, 3)}</td>
                        <td>{sigfigs(s.eta_shell, 3)}</td>
                        <td>{sigfigs(s.width_eV, 3)}</td>
                        <td>{tauDisplay(s.tau_hole_s)}</td>
                        <td>{sigfigs(s.eta_prime, 3)}</td>
                      </tr>
                    {/each}
                  </tbody>
                </table>
              </div>
            {:else}
              <p class="no-shells">No accessible shells at this photon energy.</p>
            {/if}
          </details>
        </div>
      </div>
    </div>
  </div>
</div>

<style>
  .calculator {
    padding: 42px 50px 60px;
    max-width: 1100px;
  }

  .tool-header {
    border-bottom: 1px solid var(--color-rule);
    padding-bottom: 16px;
    margin-bottom: 0;
  }

  .tool-header-top {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    margin-bottom: 10px;
  }

  .tool-number {
    font-family: var(--font-mono);
    font-size: 10.5px;
    color: var(--color-text-faint);
  }

  .tool-category {
    font-family: var(--font-ui);
    font-weight: 500;
    font-size: 10px;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: var(--color-text-faint);
  }

  h1 {
    margin: 0 0 4px;
    font-family: var(--font-ui);
    font-weight: 600;
    font-size: 30px;
    line-height: 1.05;
    letter-spacing: -0.03em;
  }

  .tool-description {
    margin: 0;
    max-width: 500px;
    font-family: var(--font-ui);
    font-size: 12px;
    line-height: 1.55;
    color: var(--color-text-muted);
  }

  /* ── Main layout ──────────────────────────────────────────────── */

  .main-layout {
    display: flex;
    flex-wrap: wrap;
    gap: 1px;
    background: var(--color-rule);
    border: 1px solid var(--color-rule);
    border-top: 0;
  }

  .col-left {
    flex: 1 1 270px;
    max-width: 100%;
    background: var(--color-surface-card);
    padding: 22px 22px;
    display: grid;
    grid-template-columns: minmax(0, 1fr);
    gap: 18px;
    align-content: start;
  }

  .col-right {
    flex: 9 1 560px;
    min-width: 0;
    display: grid;
    grid-template-columns: minmax(0, 1fr);
    gap: 1px;
    background: var(--color-rule);
    align-content: start;
  }

  .section-label {
    font-family: var(--font-ui);
    font-weight: 500;
    font-size: 10px;
    letter-spacing: 0.11em;
    text-transform: uppercase;
    color: var(--color-text-faint);
    margin-bottom: 12px;
  }

  /* ── Element picker — mini periodic table ─────────────────────── */

  .element-section {
    display: grid;
    gap: 8px;
  }

  .element-section .section-label {
    margin-bottom: 0;
  }

  .element-picker {
    display: flex;
    flex-wrap: wrap;
    gap: 5px;
  }

  .element-chip {
    position: relative;
    padding: 5px 8px 6px;
    min-width: 36px;
    background: #F1EEE5;
    border: 1px solid var(--color-rule);
    cursor: pointer;
    text-align: center;
    transition: border-color 0.1s;
  }

  .element-chip:hover {
    border-color: var(--color-link);
  }

  .element-sym {
    display: block;
    font-family: var(--font-mono);
    font-size: 13px;
    line-height: 1;
    color: var(--color-text);
  }

  .element-z {
    display: block;
    font-family: var(--font-mono);
    font-size: 8px;
    line-height: 1;
    color: var(--color-text-faint);
    margin-top: 2px;
  }

  .element-bar {
    position: absolute;
    left: -1px;
    right: -1px;
    bottom: -1px;
    height: 3px;
    background: var(--color-accent);
  }

  /* ── Lifetime override ────────────────────────────────────────── */

  .lifetime-section {
    display: grid;
    gap: 8px;
  }

  .lifetime-section .section-label {
    margin-bottom: 0;
  }

  .lifetime-chips {
    display: flex;
    flex-wrap: wrap;
    gap: 4px;
  }

  .lifetime-chip {
    padding: 4px 8px;
    background: #F1EEE5;
    border: 1px solid var(--color-rule);
    cursor: pointer;
    text-align: center;
    transition: border-color 0.1s;
  }

  .lifetime-chip:hover {
    border-color: var(--color-link);
  }

  .lifetime-chip.active-lifetime {
    background: #EF6C1E;
    border-color: #EF6C1E;
  }

  .lifetime-chip.active-lifetime .lifetime-shell {
    color: #fff;
  }

  .lifetime-chip.active-lifetime .lifetime-tau {
    color: rgba(255, 255, 255, 0.7);
  }

  .lifetime-shell {
    display: block;
    font-family: var(--font-mono);
    font-size: 10px;
    line-height: 1;
    color: var(--color-text);
  }

  .lifetime-tau {
    display: block;
    font-family: var(--font-mono);
    font-size: 8px;
    line-height: 1;
    color: var(--color-text-faint);
    margin-top: 2px;
  }

  .lifetime-input-row {
    display: flex;
    align-items: center;
    gap: 6px;
  }

  .lifetime-input {
    width: 80px;
    padding: 4px 6px;
    font-family: var(--font-mono);
    font-size: 12px;
    border: 1px solid var(--color-rule);
    background: var(--color-surface);
    color: var(--color-text);
  }

  .lifetime-input::placeholder {
    color: var(--color-text-faint);
  }

  .lifetime-clear {
    padding: 2px 8px;
    font-family: var(--font-ui);
    font-size: 10px;
    border: 1px solid var(--color-rule);
    background: var(--color-surface);
    color: var(--color-text-muted);
    cursor: pointer;
  }

  .lifetime-clear:hover {
    border-color: var(--color-link);
  }

  /* ── Result band ──────────────────────────────────────────────── */

  .result-band {
    background: var(--color-surface-card);
    padding: 10px 24px;
    display: flex;
    flex-wrap: wrap;
    align-items: flex-end;
    gap: 8px 32px;
    transition: background 0.2s;
  }

  .result-band.nonlinear {
    background: #EF6C1E;
  }

  .result-block {
    flex: none;
  }

  .result-label {
    font-family: var(--font-ui);
    font-weight: 500;
    font-size: 9px;
    letter-spacing: 0.09em;
    color: var(--color-text-faint);
  }

  .nonlinear .result-label {
    color: rgba(255, 255, 255, 0.7);
  }

  .result-number {
    font-family: var(--font-mono);
    font-size: 28px;
    line-height: 1;
    letter-spacing: -0.02em;
    margin-top: 4px;
    color: var(--color-text);
  }

  .nonlinear .result-number {
    color: #fff;
  }

  .result-regime {
    margin-left: auto;
    text-align: right;
  }

  .regime-name {
    font-family: var(--font-ui);
    font-weight: 600;
    font-size: 16px;
    line-height: 1.1;
    letter-spacing: -0.025em;
    margin-top: 4px;
    color: var(--color-text);
  }

  .nonlinear .regime-name {
    color: #fff;
  }

  .regime-note {
    font-family: var(--font-mono);
    font-size: 10px;
    color: var(--color-text-faint);
    margin-top: 3px;
  }

  .nonlinear .regime-note {
    color: rgba(255, 255, 255, 0.6);
  }

  /* ── 2×2 grid: plots top, controls bottom ───────────────────── */

  .grid-2x2 {
    display: grid;
    grid-template-columns: 1fr 1fr;
    grid-template-rows: auto auto;
    gap: 1px;
    background: var(--color-rule);
  }

  .grid-cell {
    background: var(--color-surface-card);
    padding: 18px 22px;
    display: flex;
    flex-direction: column;
    gap: 18px;
    width: 100%;
    min-width: 0;
  }

  .plot-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 6px;
  }

  .heatmap-toggle {
    display: flex;
    border: 1px solid var(--color-rule);
  }

  .toggle-btn {
    padding: 4px 10px;
    font-family: var(--font-mono);
    font-weight: 400;
    font-size: 11px;
    border: 0;
    cursor: pointer;
    background: var(--color-surface);
    color: var(--color-text-muted);
    transition: background 0.1s, color 0.1s;
  }

  .toggle-btn:first-child {
    border-right: 1px solid var(--color-rule);
  }

  .toggle-btn.active {
    background: var(--color-sidebar);
    color: var(--color-sidebar-text);
  }

  .toggle-btn:not(.active):hover {
    background: var(--color-surface-card-hover);
  }

  /* ── Outputs ──────────────────────────────────────────────────── */

  .output-rows {
    display: flex;
    flex-direction: column;
  }

  .output-row {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    padding: 6px 0;
    border-bottom: 1px solid var(--color-rule-light);
  }

  .output-row:last-child {
    border-bottom: 0;
  }

  .output-label {
    font-family: var(--font-ui);
    font-size: 11.5px;
    color: var(--color-text-muted);
  }

  .output-value {
    font-family: var(--font-mono);
    font-size: 13px;
    font-weight: 500;
    font-variant-numeric: tabular-nums;
    text-align: right;
  }

  .output-unit {
    font-weight: 400;
    font-size: 11px;
    color: var(--color-text-faint);
    margin-left: 3px;
  }

  .unit-select {
    font-family: var(--font-mono);
    font-weight: 400;
    font-size: 11px;
    color: var(--color-text-faint);
    margin-left: 3px;
    padding: 0 2px;
    border: 0;
    border-bottom: 1px solid var(--color-rule);
    background: transparent;
    cursor: pointer;
    -webkit-appearance: none;
    appearance: none;
    outline: none;
  }

  .unit-select:hover {
    color: var(--color-text);
    border-bottom-color: var(--color-text);
  }

  /* ── Shell table ──────────────────────────────────────────────── */

  .shell-details {
    border-top: 1px solid var(--color-rule);
    padding-top: 12px;
  }

  .clickable {
    cursor: pointer;
    user-select: none;
  }

  .shell-table-wrap {
    overflow-x: auto;
    margin-top: 6px;
  }

  .shell-table {
    width: 100%;
    border-collapse: collapse;
    font-family: var(--font-mono);
    font-size: 10px;
    font-variant-numeric: tabular-nums;
  }

  .shell-table th {
    text-align: left;
    font-family: var(--font-ui);
    font-weight: 500;
    font-size: 9px;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    color: var(--color-text-faint);
    padding: 4px 6px 4px 0;
    border-bottom: 1px solid var(--color-rule);
    white-space: nowrap;
  }

  .shell-table td {
    padding: 4px 6px 4px 0;
    border-bottom: 1px solid var(--color-rule-light);
    white-space: nowrap;
  }

  .no-shells {
    font-family: var(--font-ui);
    font-size: 11px;
    color: var(--color-text-faint);
    margin: 6px 0 0;
  }

  @media (max-width: 1000px) {
    .grid-2x2 {
      grid-template-columns: 1fr;
    }
  }

  @media (max-width: 900px) {
    .main-layout {
      flex-direction: column;
    }

    .result-band {
      gap: 8px 24px;
    }

    .result-number {
      font-size: 24px;
    }

    .regime-name {
      font-size: 14px;
    }
  }
</style>
