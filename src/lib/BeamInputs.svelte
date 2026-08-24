<script lang="ts">
  import type { SpatialMode } from './beam';
  import { photonEnergy, pulseEnergy, fwhm, pulseDuration, spatialMode, transmission } from './stores.svelte';
  import { sigfigs } from './format';

  type Field = 'photonEnergy' | 'pulseEnergy' | 'fwhmX' | 'fwhmY' | 'pulseDuration' | 'transmission';

  let energyUnit: 'eV' | 'keV' = $state('keV');
  let pulseEnergyUnit: 'µJ' | 'mJ' = $state('µJ');
  let fwhmXUnit: 'nm' | 'µm' = $state('nm');
  let fwhmYUnit: 'nm' | 'µm' = $state('nm');
  let durationUnit: 'as' | 'fs' | 'ps' = $state('fs');
  let transmissionUnit = $state<'x1' | '%'>('x1');

  let activeField: Field | null = $state(null);
  let rawInput = $state('');

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

  let photonEnergyDisplay = $derived(
    activeField === 'photonEnergy' ? rawInput : siToDisplay(photonEnergy.eV, energyUnit, energyFactors)
  );
  let pulseEnergyDisplay = $derived(
    activeField === 'pulseEnergy' ? rawInput : siToDisplay(pulseEnergy.J, pulseEnergyUnit, pulseEnergyFactors)
  );
  let fwhmXDisplay = $derived(
    activeField === 'fwhmX' ? rawInput : siToDisplay(fwhm.x_m, fwhmXUnit, lengthFactors)
  );
  let fwhmYDisplay = $derived(
    activeField === 'fwhmY' ? rawInput : siToDisplay(fwhm.y_m, fwhmYUnit, lengthFactors)
  );
  let pulseDurationDisplay = $derived(
    activeField === 'pulseDuration' ? rawInput : siToDisplay(pulseDuration.s, durationUnit, durationFactors)
  );
  let transmissionDisplay = $derived(
    activeField === 'transmission' ? rawInput : (
      (transmissionUnit as string) === '%'
        ? fmt(transmission.value * 100)
        : String(transmission.value)
    )
  );

  function handleFocus(field: Field) {
    activeField = field;
    switch (field) {
      case 'photonEnergy':
        rawInput = fmt(photonEnergy.eV / energyFactors[energyUnit]); break;
      case 'pulseEnergy':
        rawInput = fmt(pulseEnergy.J / pulseEnergyFactors[pulseEnergyUnit]); break;
      case 'fwhmX':
        rawInput = fmt(fwhm.x_m / lengthFactors[fwhmXUnit]); break;
      case 'fwhmY':
        rawInput = fmt(fwhm.y_m / lengthFactors[fwhmYUnit]); break;
      case 'pulseDuration':
        rawInput = fmt(pulseDuration.s / durationFactors[durationUnit]); break;
      case 'transmission':
        rawInput = (transmissionUnit as string) === '%'
          ? fmt(transmission.value * 100)
          : String(transmission.value); break;
    }
  }

  function handleInput(field: Field, value: string) {
    activeField = field;
    rawInput = value;
    const num = parseFloat(value);
    if (!Number.isFinite(num)) return;
    if (field !== 'transmission' && num <= 0) return;

    switch (field) {
      case 'photonEnergy':
        photonEnergy.eV = num * energyFactors[energyUnit]; break;
      case 'pulseEnergy':
        pulseEnergy.J = num * pulseEnergyFactors[pulseEnergyUnit]; break;
      case 'fwhmX':
        fwhm.x_m = num * lengthFactors[fwhmXUnit]; break;
      case 'fwhmY':
        fwhm.y_m = num * lengthFactors[fwhmYUnit]; break;
      case 'pulseDuration':
        pulseDuration.s = num * durationFactors[durationUnit]; break;
      case 'transmission': {
        const val = (transmissionUnit as string) === '%' ? num / 100 : num;
        if (val >= 0 && val <= 1) transmission.value = val;
        break;
      }
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

  function setMode(m: SpatialMode) {
    spatialMode.value = m;
  }
</script>

<div class="mode-toggle">
  <button
    class="mode-btn"
    class:active={spatialMode.value === 'gaussian'}
    onclick={() => setMode('gaussian')}
  >Gaussian</button>
  <button
    class="mode-btn"
    class:active={spatialMode.value === 'flat-top'}
    onclick={() => setMode('flat-top')}
  >Flat-top</button>
</div>

<div class="fields">
  <div class="field-row">
    <label class="field-label" for="beam-photon-energy">Photon energy</label>
    <div class="field-input-group">
      <input
        id="beam-photon-energy"
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
    <label class="field-label" for="beam-pulse-energy">Pulse energy</label>
    <div class="field-input-group">
      <input
        id="beam-pulse-energy"
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
    <label class="field-label" for="beam-fwhm-x">FWHM x</label>
    <div class="field-input-group">
      <input
        id="beam-fwhm-x"
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
    <label class="field-label" for="beam-fwhm-y">FWHM y</label>
    <div class="field-input-group">
      <input
        id="beam-fwhm-y"
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
    <label class="field-label" for="beam-duration">Pulse duration</label>
    <div class="field-input-group">
      <input
        id="beam-duration"
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

  <div class="field-row">
    <label class="field-label" for="beam-transmission">Beamline transmission</label>
    <div class="field-input-group">
      <input
        id="beam-transmission"
        type="text"
        inputmode="decimal"
        class="field-input"
        value={transmissionDisplay}
        onfocus={() => handleFocus('transmission')}
        oninput={(e) => handleInput('transmission', e.currentTarget.value)}
        onblur={handleBlur}
      />
      <select
        class="field-unit"
        bind:value={transmissionUnit}
        onchange={() => handleUnitChange('transmission')}
      >
        <option value="x1">×1</option>
        <option value="%">%</option>
      </select>
    </div>
  </div>
</div>

<style>
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
</style>
