<script lang="ts">
  import {
    energyUnits, wavelengthUnits, frequencyUnits,
    energyToEV, evToEnergy,
    wavelengthToEV, evToWavelength,
    frequencyToEV, evToFrequency,
    type EnergyUnit, type WavelengthUnit, type FrequencyUnit,
  } from './lib/convert';
  import { sigfigs } from './lib/format';
  import { photonEnergy } from './lib/stores.svelte';

  type Field = 'energy' | 'wavelength' | 'frequency';

  let activeField: Field | null = $state(null);
  let rawInput = $state('');

  let energyUnit: EnergyUnit = $state('keV');
  let wavelengthUnit: WavelengthUnit = $state('Å');
  let frequencyUnit: FrequencyUnit = $state('THz');

  let energyDisplay = $derived(
    activeField === 'energy' ? rawInput : formatValue(evToEnergy(photonEnergy.eV, energyUnit))
  );
  let wavelengthDisplay = $derived(
    activeField === 'wavelength' ? rawInput : formatValue(evToWavelength(photonEnergy.eV, wavelengthUnit))
  );
  let frequencyDisplay = $derived(
    activeField === 'frequency' ? rawInput : formatValue(evToFrequency(photonEnergy.eV, frequencyUnit))
  );

  function formatValue(v: number): string {
    if (!Number.isFinite(v) || v <= 0) return '—';
    return sigfigs(v, 4);
  }

  function handleInput(field: Field, value: string) {
    activeField = field;
    rawInput = value;
    const num = parseFloat(value);
    if (!Number.isFinite(num) || num <= 0) return;

    if (field === 'energy')     photonEnergy.eV = energyToEV(num, energyUnit);
    if (field === 'wavelength') photonEnergy.eV = wavelengthToEV(num, wavelengthUnit);
    if (field === 'frequency')  photonEnergy.eV = frequencyToEV(num, frequencyUnit);
  }

  function handleUnitChange(field: Field) {
    if (activeField === field && rawInput) {
      const num = parseFloat(rawInput);
      if (!Number.isFinite(num) || num <= 0) return;
      if (field === 'energy')     photonEnergy.eV = energyToEV(num, energyUnit);
      if (field === 'wavelength') photonEnergy.eV = wavelengthToEV(num, wavelengthUnit);
      if (field === 'frequency')  photonEnergy.eV = frequencyToEV(num, frequencyUnit);
    }
  }

  function handleBlur() {
    activeField = null;
    rawInput = '';
  }
</script>

<div class="converter">
  <div class="tool-header">
    <div class="tool-header-top">
      <span class="tool-number">01</span>
      <span class="tool-category">converter</span>
    </div>
    <h1>Energy & wavelength</h1>
    <p class="tool-description">
      Type in any field. The others update live.
    </p>
  </div>

  <div class="fields">
    <div class="field-row">
      <label class="field-label" for="field-energy">Energy</label>
      <div class="field-input-group">
        <input
          id="field-energy"
          type="text"
          inputmode="decimal"
          class="field-input"
          value={energyDisplay}
          onfocus={() => { activeField = 'energy'; rawInput = formatValue(evToEnergy(photonEnergy.eV, energyUnit)); }}
          oninput={(e) => handleInput('energy', e.currentTarget.value)}
          onblur={handleBlur}
        />
        <select
          class="field-unit"
          bind:value={energyUnit}
          onchange={() => handleUnitChange('energy')}
        >
          {#each energyUnits as u}
            <option value={u}>{u}</option>
          {/each}
        </select>
      </div>
    </div>

    <div class="field-row">
      <label class="field-label" for="field-wavelength">Wavelength</label>
      <div class="field-input-group">
        <input
          id="field-wavelength"
          type="text"
          inputmode="decimal"
          class="field-input"
          value={wavelengthDisplay}
          onfocus={() => { activeField = 'wavelength'; rawInput = formatValue(evToWavelength(photonEnergy.eV, wavelengthUnit)); }}
          oninput={(e) => handleInput('wavelength', e.currentTarget.value)}
          onblur={handleBlur}
        />
        <select
          class="field-unit"
          bind:value={wavelengthUnit}
          onchange={() => handleUnitChange('wavelength')}
        >
          {#each wavelengthUnits as u}
            <option value={u}>{u}</option>
          {/each}
        </select>
      </div>
    </div>

    <div class="field-row">
      <label class="field-label" for="field-frequency">Frequency</label>
      <div class="field-input-group">
        <input
          id="field-frequency"
          type="text"
          inputmode="decimal"
          class="field-input"
          value={frequencyDisplay}
          onfocus={() => { activeField = 'frequency'; rawInput = formatValue(evToFrequency(photonEnergy.eV, frequencyUnit)); }}
          oninput={(e) => handleInput('frequency', e.currentTarget.value)}
          onblur={handleBlur}
        />
        <select
          class="field-unit"
          bind:value={frequencyUnit}
          onchange={() => handleUnitChange('frequency')}
        >
          {#each frequencyUnits as u}
            <option value={u}>{u}</option>
          {/each}
        </select>
      </div>
    </div>
  </div>
</div>

<style>
  .converter {
    padding: 60px 64px 80px;
    max-width: 720px;
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

  .fields {
    display: flex;
    flex-direction: column;
    gap: 24px;
  }

  .field-row {
    display: flex;
    flex-direction: column;
    gap: 6px;
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
    padding: 12px 16px;
    font-family: var(--font-mono);
    font-size: 22px;
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
    padding: 12px 16px;
    font-family: var(--font-mono);
    font-size: 14px;
    font-weight: 500;
    border: 0;
    border-left: 1px solid var(--color-rule);
    background: var(--color-surface);
    cursor: pointer;
    color: var(--color-text);
    outline: none;
    -webkit-appearance: none;
    appearance: none;
    min-width: 70px;
    text-align: center;
  }

  .field-unit:hover {
    background: var(--color-surface-card-hover);
  }
</style>
