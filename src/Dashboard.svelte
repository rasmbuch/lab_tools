<script lang="ts">
  import ToolCard from './ToolCard.svelte';
  import { sigfigs } from './lib/format';
  import { hc_keV_A } from './lib/constants';

  const defaultKeV = 9.7;
  const defaultA = hc_keV_A / defaultKeV;
</script>

<div class="dashboard">
  <div class="hero">
    <div>
      <h1>Four instruments for<br>the beamline</h1>
    </div>
    <p class="hero-description">
      Everything updates as you type. Nothing is submitted, nothing is stored.
      Open the URL on the beamline tablet and it works the same.
    </p>
  </div>

  <div class="grid">
    <ToolCard
      route="energy"
      number="01"
      category="converter"
      title="Energy & wavelength"
      description="eV · keV · Å · nm · THz · EHz, all live at once."
      preview="{sigfigs(defaultKeV)} keV  ↔  {sigfigs(defaultA)} Å"
    />
    <ToolCard
      route="intensity"
      number="02"
      category="equivalents"
      title="Intensity & fluence"
      description="W/cm² ↔ ph/nm² at a photon energy and pulse length."
      preview="I = Ṅ · ℏω / A"
    />
    <ToolCard
      route="eta"
      number="03"
      category="focal map"
      title="η / η′ per atom"
      description="Photons absorbed per atom per pulse from beam parameters."
      preview="η = σ · Φ₀"
    />
    <ToolCard
      route="omega"
      number="04"
      category="geometry"
      title="Solid angle"
      description="Detector area and distance to solid angle in steradians."
      preview="Ω = A / r²"
    />
  </div>
</div>

<style>
  .dashboard {
    padding: 60px 64px 80px;
    max-width: 1360px;
  }

  .hero {
    display: flex;
    align-items: flex-end;
    justify-content: space-between;
    gap: 40px;
    border-bottom: 1px solid var(--color-rule);
    padding-bottom: 26px;
  }

  h1 {
    margin: 0;
    font-family: var(--font-ui);
    font-weight: 600;
    font-size: 50px;
    line-height: 1.0;
    letter-spacing: -0.035em;
  }

  .hero-description {
    margin: 0;
    max-width: 340px;
    font-family: var(--font-ui);
    font-size: 13.5px;
    line-height: 1.6;
    color: var(--color-text-muted);
    text-wrap: pretty;
  }

  .grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(min(320px, 100%), 1fr));
    gap: 1px;
    background: var(--color-rule);
    border: 1px solid var(--color-rule);
    border-top: 0;
    margin-top: 0;
  }
</style>
