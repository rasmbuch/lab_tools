<script lang="ts">
  const HC_KEV_ANGSTROM = 12.39842  // hc in keV·Å

  let wavelength_A = $state(1.5406)  // Cu Kα default

  let energy_keV = $derived(
    wavelength_A > 0 ? HC_KEV_ANGSTROM / wavelength_A : NaN
  )
</script>

<main>
  <h1>Lab Tools</h1>
  <p class="subtitle">Crystallography & scattering calculators</p>

  <div class="card">
    <label>
      Wavelength (Å)
      <input
        type="number"
        bind:value={wavelength_A}
        step="0.001"
        min="0.01"
      />
    </label>

    <div class="result">
      {#if Number.isFinite(energy_keV)}
        <span class="value">{energy_keV.toFixed(4)}</span>
        <span class="unit">keV</span>
      {:else}
        <span class="value">—</span>
      {/if}
    </div>
  </div>
</main>

<style>
  main {
    max-width: 480px;
    margin: 4rem auto;
    padding: 2rem;
    font-family: system-ui, -apple-system, sans-serif;
    color: #222;
  }

  h1 {
    margin: 0;
    font-size: 1.8rem;
  }

  .subtitle {
    color: #666;
    margin-top: 0.25rem;
  }

  .card {
    margin-top: 2rem;
    padding: 1.5rem;
    border: 1px solid #ddd;
    border-radius: 8px;
    background: #fafafa;
  }

  label {
    display: block;
    font-size: 0.9rem;
    color: #555;
  }

  input {
    display: block;
    margin-top: 0.5rem;
    padding: 0.5rem;
    font-size: 1.1rem;
    border: 1px solid #ccc;
    border-radius: 4px;
    width: 100%;
    box-sizing: border-box;
  }

  .result {
    margin-top: 1.5rem;
    text-align: center;
  }

  .value {
    font-size: 2rem;
    font-weight: 600;
    font-variant-numeric: tabular-nums;
  }

  .unit {
    font-size: 1.2rem;
    color: #666;
    margin-left: 0.5rem;
  }
</style>
