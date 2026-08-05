<script lang="ts">
  import { computeBeam, type SpatialMode } from './lib/beam';
  import { photonEnergy } from './lib/stores.svelte';
  import { sigfigs } from './lib/format';

  type Field = 'photonEnergy' | 'pulseEnergy' | 'fwhmX' | 'fwhmY' | 'pulseDuration';

  let mode: SpatialMode = $state('gaussian');

  // Input values in SI
  let pulseEnergy_J = $state(100e-6);
  let fwhm_x_m = $state(200e-9);
  let fwhm_y_m = $state(200e-9);
  let pulseDuration_s = $state(10e-15);

  // Unit selections
  let energyUnit: 'eV' | 'keV' = $state('keV');
  let pulseEnergyUnit: 'µJ' | 'mJ' = $state('µJ');
  let fwhmXUnit: 'nm' | 'µm' = $state('nm');
  let fwhmYUnit: 'nm' | 'µm' = $state('nm');
  let durationUnit: 'as' | 'fs' | 'ps' = $state('fs');

  // Focus tracking
  let activeField: Field | null = $state(null);
  let rawInput = $state('');

  // Unit conversion factors (display unit → SI)
  const energyFactors: Record<string, number> = { 'eV': 1, 'keV': 1e3 };
  const pulseEnergyFactors: Record<string, number> = { 'µJ': 1e-6, 'mJ': 1e-3 };
  const lengthFactors: Record<string, number> = { 'nm': 1e-9, 'µm': 1e-6 };
  const durationFactors: Record<string, number> = { 'as': 1e-18, 'fs': 1e-15, 'ps': 1e-12 };

  function fmt(v: number): string {
    if (!Number.isFinite(v) || v <= 0) return '—';
    return sigfigs(v, 4);
  }

  function siToDisplay(si: number, unit: string, factors: Record<string, number>): string {
    return fmt(si / factors[unit]);
  }

  // Display values (formatted when not focused, raw when focused)
  let photonEnergyDisplay = $derived(
    activeField === 'photonEnergy' ? rawInput : siToDisplay(photonEnergy.eV, energyUnit, energyFactors)
  );
  let pulseEnergyDisplay = $derived(
    activeField === 'pulseEnergy' ? rawInput : siToDisplay(pulseEnergy_J, pulseEnergyUnit, pulseEnergyFactors)
  );
  let fwhmXDisplay = $derived(
    activeField === 'fwhmX' ? rawInput : siToDisplay(fwhm_x_m, fwhmXUnit, lengthFactors)
  );
  let fwhmYDisplay = $derived(
    activeField === 'fwhmY' ? rawInput : siToDisplay(fwhm_y_m, fwhmYUnit, lengthFactors)
  );
  let pulseDurationDisplay = $derived(
    activeField === 'pulseDuration' ? rawInput : siToDisplay(pulseDuration_s, durationUnit, durationFactors)
  );

  function handleFocus(field: Field) {
    activeField = field;
    switch (field) {
      case 'photonEnergy':
        rawInput = fmt(photonEnergy.eV / energyFactors[energyUnit]); break;
      case 'pulseEnergy':
        rawInput = fmt(pulseEnergy_J / pulseEnergyFactors[pulseEnergyUnit]); break;
      case 'fwhmX':
        rawInput = fmt(fwhm_x_m / lengthFactors[fwhmXUnit]); break;
      case 'fwhmY':
        rawInput = fmt(fwhm_y_m / lengthFactors[fwhmYUnit]); break;
      case 'pulseDuration':
        rawInput = fmt(pulseDuration_s / durationFactors[durationUnit]); break;
    }
  }

  function handleInput(field: Field, value: string) {
    activeField = field;
    rawInput = value;
    const num = parseFloat(value);
    if (!Number.isFinite(num) || num <= 0) return;

    switch (field) {
      case 'photonEnergy':
        photonEnergy.eV = num * energyFactors[energyUnit]; break;
      case 'pulseEnergy':
        pulseEnergy_J = num * pulseEnergyFactors[pulseEnergyUnit]; break;
      case 'fwhmX':
        fwhm_x_m = num * lengthFactors[fwhmXUnit]; break;
      case 'fwhmY':
        fwhm_y_m = num * lengthFactors[fwhmYUnit]; break;
      case 'pulseDuration':
        pulseDuration_s = num * durationFactors[durationUnit]; break;
    }
  }

  function handleUnitChange(field: Field) {
    if (activeField === field && rawInput) {
      handleInput(field, rawInput);
    }
  }

  function handleBlur() {
    activeField = null;
    rawInput = '';
  }

  // Compute beam results
  let result = $derived(computeBeam({
    photonEnergy_eV: photonEnergy.eV,
    pulseEnergy_J,
    fwhm_x_m,
    fwhm_y_m,
    pulseDuration_s,
    mode,
  }));

  // Format outputs
  let outputs = $derived({
    nPhotons: fmt(result.nPhotons),
    peakPower_GW: fmt(result.peakPower_W / 1e9),
    peakIrradiance: sigfigs(result.peakIrradiance_Wcm2, 4),
    fluence: sigfigs(result.fluence_phcm2, 4),
    peakFlux: sigfigs(result.peakFlux_phcm2s, 4),
    effectiveArea_um2: fmt(result.effectiveArea_m2 * 1e12),
    beamWaist_x_nm: result.beamWaist_x_m != null ? fmt(result.beamWaist_x_m * 1e9) : null,
    beamWaist_y_nm: result.beamWaist_y_m != null ? fmt(result.beamWaist_y_m * 1e9) : null,
    rayleigh_x_um: result.rayleighLength_x_m != null ? fmt(result.rayleighLength_x_m * 1e6) : null,
    rayleigh_y_um: result.rayleighLength_y_m != null ? fmt(result.rayleighLength_y_m * 1e6) : null,
  });
</script>

<div class="calculator">
  <div class="tool-header">
    <div class="tool-header-top">
      <span class="tool-number">02</span>
      <span class="tool-category">calculator</span>
    </div>
    <h1>Intensity & fluence</h1>
    <p class="tool-description">
      Beam parameters in, peak quantities out. Everything updates live.
    </p>
  </div>

  <div class="columns">
    <div class="col-inputs">
      <div class="section-label">Inputs</div>

      <div class="mode-toggle">
        <button
          class="mode-btn"
          class:active={mode === 'gaussian'}
          onclick={() => mode = 'gaussian'}
        >Gaussian</button>
        <button
          class="mode-btn"
          class:active={mode === 'flat-top'}
          onclick={() => mode = 'flat-top'}
        >Flat-top</button>
      </div>

      <div class="fields">
        <div class="field-row">
          <label class="field-label" for="calc-photon-energy">Photon energy</label>
          <div class="field-input-group">
            <input
              id="calc-photon-energy"
              type="text"
              inputmode="decimal"
              class="field-input"
              value={photonEnergyDisplay}
              onfocus={() => handleFocus('photonEnergy')}
              oninput={(e) => handleInput('photonEnergy', e.currentTarget.value)}
              onblur={handleBlur}
            />
            <select
              class="field-unit"
              bind:value={energyUnit}
              onchange={() => handleUnitChange('photonEnergy')}
            >
              <option value="eV">eV</option>
              <option value="keV">keV</option>
            </select>
          </div>
        </div>

        <div class="field-row">
          <label class="field-label" for="calc-pulse-energy">Pulse energy</label>
          <div class="field-input-group">
            <input
              id="calc-pulse-energy"
              type="text"
              inputmode="decimal"
              class="field-input"
              value={pulseEnergyDisplay}
              onfocus={() => handleFocus('pulseEnergy')}
              oninput={(e) => handleInput('pulseEnergy', e.currentTarget.value)}
              onblur={handleBlur}
            />
            <select
              class="field-unit"
              bind:value={pulseEnergyUnit}
              onchange={() => handleUnitChange('pulseEnergy')}
            >
              <option value="µJ">µJ</option>
              <option value="mJ">mJ</option>
            </select>
          </div>
        </div>

        <div class="field-row">
          <label class="field-label" for="calc-fwhm-x">FWHM x</label>
          <div class="field-input-group">
            <input
              id="calc-fwhm-x"
              type="text"
              inputmode="decimal"
              class="field-input"
              value={fwhmXDisplay}
              onfocus={() => handleFocus('fwhmX')}
              oninput={(e) => handleInput('fwhmX', e.currentTarget.value)}
              onblur={handleBlur}
            />
            <select
              class="field-unit"
              bind:value={fwhmXUnit}
              onchange={() => handleUnitChange('fwhmX')}
            >
              <option value="nm">nm</option>
              <option value="µm">µm</option>
            </select>
          </div>
        </div>

        <div class="field-row">
          <label class="field-label" for="calc-fwhm-y">FWHM y</label>
          <div class="field-input-group">
            <input
              id="calc-fwhm-y"
              type="text"
              inputmode="decimal"
              class="field-input"
              value={fwhmYDisplay}
              onfocus={() => handleFocus('fwhmY')}
              oninput={(e) => handleInput('fwhmY', e.currentTarget.value)}
              onblur={handleBlur}
            />
            <select
              class="field-unit"
              bind:value={fwhmYUnit}
              onchange={() => handleUnitChange('fwhmY')}
            >
              <option value="nm">nm</option>
              <option value="µm">µm</option>
            </select>
          </div>
        </div>

        <div class="field-row">
          <label class="field-label" for="calc-duration">Pulse duration</label>
          <div class="field-input-group">
            <input
              id="calc-duration"
              type="text"
              inputmode="decimal"
              class="field-input"
              value={pulseDurationDisplay}
              onfocus={() => handleFocus('pulseDuration')}
              oninput={(e) => handleInput('pulseDuration', e.currentTarget.value)}
              onblur={handleBlur}
            />
            <select
              class="field-unit"
              bind:value={durationUnit}
              onchange={() => handleUnitChange('pulseDuration')}
            >
              <option value="as">as</option>
              <option value="fs">fs</option>
              <option value="ps">ps</option>
            </select>
          </div>
        </div>
      </div>
    </div>

    <div class="col-outputs">
      <div class="output-group">
        <div class="section-label">Pulse & intensity</div>
        <div class="output-rows">
          <div class="output-row">
            <span class="output-label">N photons</span>
            <span class="output-value">{outputs.nPhotons}</span>
          </div>
          <div class="output-row">
            <span class="output-label">Peak power</span>
            <span class="output-value">{outputs.peakPower_GW} <span class="output-unit">GW</span></span>
          </div>
          <div class="output-row">
            <span class="output-label">Peak irradiance</span>
            <span class="output-value">{outputs.peakIrradiance} <span class="output-unit">W/cm²</span></span>
          </div>
          <div class="output-row">
            <span class="output-label">Fluence</span>
            <span class="output-value">{outputs.fluence} <span class="output-unit">ph/cm²</span></span>
          </div>
          <div class="output-row">
            <span class="output-label">Peak flux</span>
            <span class="output-value">{outputs.peakFlux} <span class="output-unit">ph/cm²/s</span></span>
          </div>
        </div>
      </div>

      <div class="output-group">
        <div class="section-label">Beam geometry</div>
        <div class="output-rows">
          <div class="output-row">
            <span class="output-label">Effective area</span>
            <span class="output-value">{outputs.effectiveArea_um2} <span class="output-unit">µm²</span></span>
          </div>
          {#if mode === 'gaussian'}
            <div class="output-row">
              <span class="output-label">Waist w₀ x</span>
              <span class="output-value">{outputs.beamWaist_x_nm} <span class="output-unit">nm</span></span>
            </div>
            <div class="output-row">
              <span class="output-label">Waist w₀ y</span>
              <span class="output-value">{outputs.beamWaist_y_nm} <span class="output-unit">nm</span></span>
            </div>
            <div class="output-row">
              <span class="output-label">Rayleigh z<sub>R</sub> x</span>
              <span class="output-value">{outputs.rayleigh_x_um} <span class="output-unit">µm</span></span>
            </div>
            <div class="output-row">
              <span class="output-label">Rayleigh z<sub>R</sub> y</span>
              <span class="output-value">{outputs.rayleigh_y_um} <span class="output-unit">µm</span></span>
            </div>
          {/if}
        </div>
      </div>
    </div>
  </div>
</div>

<style>
  .calculator {
    padding: 60px 64px 80px;
    max-width: 960px;
  }

  .tool-header {
    border-bottom: 1px solid var(--color-rule);
    padding-bottom: 26px;
    margin-bottom: 40px;
  }

  .tool-header-top {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    margin-bottom: 14px;
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
    margin: 0 0 6px;
    font-family: var(--font-ui);
    font-weight: 600;
    font-size: 38px;
    line-height: 1.1;
    letter-spacing: -0.03em;
  }

  .tool-description {
    margin: 0;
    font-family: var(--font-ui);
    font-size: 13.5px;
    line-height: 1.6;
    color: var(--color-text-muted);
  }

  /* ── Two-column layout ──────────────────────────────────────────── */

  .columns {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 48px;
    align-items: start;
  }

  @media (max-width: 760px) {
    .columns {
      grid-template-columns: 1fr;
      gap: 40px;
    }
  }

  .section-label {
    font-family: var(--font-ui);
    font-weight: 500;
    font-size: 10px;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: var(--color-text-faint);
    margin-bottom: 16px;
  }

  /* ── Mode toggle (segmented control) ────────────────────────────── */

  .mode-toggle {
    display: flex;
    border: 1px solid var(--color-rule);
    margin-bottom: 24px;
  }

  .mode-btn {
    flex: 1;
    padding: 9px 16px;
    font-family: var(--font-ui);
    font-weight: 500;
    font-size: 12px;
    letter-spacing: 0.02em;
    border: 0;
    cursor: pointer;
    background: var(--color-surface);
    color: var(--color-text-muted);
    transition: background 0.1s, color 0.1s;
  }

  .mode-btn:first-child {
    border-right: 1px solid var(--color-rule);
  }

  .mode-btn.active {
    background: var(--color-sidebar);
    color: var(--color-sidebar-text);
  }

  .mode-btn:not(.active):hover {
    background: var(--color-surface-card-hover);
  }

  /* ── Input fields ───────────────────────────────────────────────── */

  .fields {
    display: flex;
    flex-direction: column;
    gap: 16px;
  }

  .field-row {
    display: flex;
    flex-direction: column;
    gap: 5px;
  }

  .field-label {
    font-family: var(--font-ui);
    font-weight: 500;
    font-size: 11px;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: var(--color-text-faint);
  }

  .field-input-group {
    display: flex;
    gap: 0;
    border: 1px solid var(--color-rule);
    background: white;
  }

  .field-input {
    flex: 1;
    padding: 10px 14px;
    font-family: var(--font-mono);
    font-size: 18px;
    font-weight: 400;
    font-variant-numeric: tabular-nums;
    border: 0;
    background: transparent;
    outline: none;
    min-width: 0;
  }

  .field-input:focus {
    box-shadow: inset 0 0 0 2px var(--color-link);
  }

  .field-unit {
    flex: none;
    padding: 10px 14px;
    font-family: var(--font-mono);
    font-size: 13px;
    font-weight: 500;
    border: 0;
    border-left: 1px solid var(--color-rule);
    background: var(--color-surface);
    cursor: pointer;
    color: var(--color-text);
    outline: none;
    -webkit-appearance: none;
    appearance: none;
    min-width: 58px;
    text-align: center;
  }

  .field-unit:hover {
    background: var(--color-surface-card-hover);
  }

  /* ── Output rows ────────────────────────────────────────────────── */

  .col-outputs {
    display: flex;
    flex-direction: column;
    gap: 32px;
  }

  .output-group {
    border-top: 1px solid var(--color-rule);
    padding-top: 16px;
  }

  .output-rows {
    display: flex;
    flex-direction: column;
    gap: 0;
  }

  .output-row {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    padding: 8px 0;
    border-bottom: 1px solid var(--color-rule-light);
  }

  .output-row:last-child {
    border-bottom: 0;
  }

  .output-label {
    font-family: var(--font-ui);
    font-size: 13px;
    color: var(--color-text-muted);
  }

  .output-value {
    font-family: var(--font-mono);
    font-size: 15px;
    font-weight: 500;
    font-variant-numeric: tabular-nums;
    text-align: right;
  }

  .output-unit {
    font-weight: 400;
    font-size: 12px;
    color: var(--color-text-faint);
    margin-left: 4px;
  }
</style>
