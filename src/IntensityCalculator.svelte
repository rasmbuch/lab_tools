<script lang="ts">
  import { computeBeam } from './lib/beam';
  import { photonEnergy, pulseEnergy, fwhm, pulseDuration, spatialMode } from './lib/stores.svelte';
  import { sigfigs } from './lib/format';
  import BeamInputs from './lib/BeamInputs.svelte';

  function fmt(v: number): string {
    if (!Number.isFinite(v) || v <= 0) return '—';
    return sigfigs(v, 4);
  }

  let result = $derived(computeBeam({
    photonEnergy_eV: photonEnergy.eV,
    pulseEnergy_J: pulseEnergy.J,
    fwhm_x_m: fwhm.x_m,
    fwhm_y_m: fwhm.y_m,
    pulseDuration_s: pulseDuration.s,
    mode: spatialMode.value,
  }));

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
      <BeamInputs />
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
          {#if spatialMode.value === 'gaussian'}
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
