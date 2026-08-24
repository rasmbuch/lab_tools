<script lang="ts">
  import katex from 'katex';
  import 'katex/dist/katex.min.css';

  function tex(expr: string): string {
    return katex.renderToString(expr, { displayMode: true, throwOnError: false });
  }

  function itex(expr: string): string {
    return katex.renderToString(expr, { displayMode: false, throwOnError: false });
  }
</script>

<div class="maths">
  <div class="tool-header">
    <div class="tool-header-top">
      <span class="tool-number">05</span>
      <span class="tool-category">reference</span>
    </div>
    <h1>Formulas</h1>
    <p class="tool-description">
      Every formula used in these calculators, with derivations and literature references.
      Validated against published XFEL data from LCLS, EuXFEL and SwissFEL.
    </p>
  </div>

  <div class="grid">
    <div class="card">
      <div class="card-header">
        <span class="card-number">1</span>
        <span class="card-category">beam</span>
      </div>
      <h2>Photon count</h2>
      <div class="formula">{@html tex(String.raw`N_\gamma = \frac{E_\text{pulse}}{E_\gamma}`)}</div>
      <p>
        where {@html itex(String.raw`E_\gamma = E_\text{keV} \times 1.602 \times 10^{-16}`)} J.
        CODATA 2018 exact constants <a href="#ref">[10]</a>.
      </p>
    </div>

    <div class="card">
      <div class="card-header">
        <span class="card-number">2</span>
        <span class="card-category">beam</span>
      </div>
      <h2>Gaussian beam waist</h2>
      <div class="formula">{@html tex(String.raw`w_0 = \frac{\text{FWHM}}{\sqrt{2\ln 2}}`)}</div>
      <p>
        Converts measured FWHM to {@html itex(String.raw`1/e^2`)} intensity radius.
        Profile: {@html itex(String.raw`I(r) = I_0 \exp(-2r^2/w_0^2)`)}.
      </p>
    </div>

    <div class="card">
      <div class="card-header">
        <span class="card-number">3</span>
        <span class="card-category">beam</span>
      </div>
      <h2>Effective focal area</h2>
      <div class="formula">{@html tex(String.raw`A_\text{eff} = \frac{\pi}{2}\, w_{0x}\, w_{0y}`)}</div>
      <p>
        Equivalent top-hat area.
        Flat-top: {@html itex(String.raw`A_\text{eff} = \tfrac{\pi}{4}\,\text{FWHM}_x \cdot \text{FWHM}_y`)}.
        XCALIB Eq. 8 <a href="#ref">[5]</a>.
      </p>
    </div>

    <div class="card">
      <div class="card-header">
        <span class="card-number">4</span>
        <span class="card-category">beam</span>
      </div>
      <h2>Peak power</h2>
      <div class="formula">{@html tex(String.raw`P_\text{peak} = \frac{E_\text{pulse}}{\tau}\sqrt{\frac{4\ln 2}{\pi}}`)}</div>
      <p>
        Gaussian temporal pulse with FWHM {@html itex(String.raw`\tau`)}.
        Numerically {@html itex(String.raw`\approx 0.9394 \cdot E_\text{pulse}/\tau`)}.
      </p>
    </div>

    <div class="card">
      <div class="card-header">
        <span class="card-number">5</span>
        <span class="card-category">beam</span>
      </div>
      <h2>Peak irradiance</h2>
      <div class="formula">{@html tex(String.raw`I_\text{peak} = \frac{P_\text{peak}}{A_\text{eff}}`)}</div>
      <p>On-axis power density at pulse centre, in W/cm<sup>2</sup>.</p>
    </div>

    <div class="card">
      <div class="card-header">
        <span class="card-number">6</span>
        <span class="card-category">beam</span>
      </div>
      <h2>Peak fluence</h2>
      <div class="formula">{@html tex(String.raw`\Phi_0 = \frac{N_\gamma}{A_\text{eff}}`)}</div>
      <p>
        Time-integrated photon surface density at beam centre.
        Neutze et al. Eq. 1 <a href="#ref">[2]</a>, Chapman et al. Supplementary <a href="#ref">[3]</a>.
      </p>
    </div>

    <div class="card">
      <div class="card-header">
        <span class="card-number">7</span>
        <span class="card-category">beam</span>
      </div>
      <h2>Rayleigh length</h2>
      <div class="formula">{@html tex(String.raw`z_R = \frac{\pi\, w_0^2}{\lambda}`)}</div>
      <p>
        Distance from waist where beam area doubles.
        XCALIB Eq. 6 <a href="#ref">[5]</a>; computed per-axis for elliptical beams.
      </p>
    </div>

    <div class="card">
      <div class="card-header">
        <span class="card-number">8</span>
        <span class="card-category">eta</span>
      </div>
      <h2>Photons per atom — {@html itex(String.raw`\eta`)}</h2>
      <div class="formula">{@html tex(String.raw`\eta = \sigma_\text{photo} \cdot \Phi_0`)}</div>
      <p>
        Expected photoabsorptions per atom per pulse.
        {@html itex(String.raw`\eta < 1`)} linear, {@html itex(String.raw`\eta \geq 1`)} nonlinear.
        Son et al. rate-equation formalism <a href="#ref">[1]</a>;
        Neutze et al. Eq. 1 damage threshold <a href="#ref">[2]</a>.
      </p>
    </div>

    <div class="card">
      <div class="card-header">
        <span class="card-number">9</span>
        <span class="card-category">eta</span>
      </div>
      <h2>Within core-hole lifetime — {@html itex(String.raw`\eta'`)}</h2>
      <div class="formula">{@html tex(String.raw`\eta' = \frac{\eta_\text{photo}}{2}\,\operatorname{erf}\!\left(\frac{2\sqrt{\ln 2}\;\tau_\text{hole}}{\tau_\text{FWHM}}\right)`)}</div>
      <p>
        Fraction of fluence arriving in {@html itex(String.raw`[0,\,\tau_\text{hole}]`)} from pulse peak.
        Closed-form Gaussian-pulse integral; constant-{@html itex(String.raw`\sigma`)} approximation
        to the Son et al. rate equations <a href="#ref">[1]</a>.
      </p>
    </div>

    <div class="card">
      <div class="card-header">
        <span class="card-number">10</span>
        <span class="card-category">eta</span>
      </div>
      <h2>Core-hole lifetime</h2>
      <div class="formula">{@html tex(String.raw`\tau_\text{hole} = \frac{\hbar}{\Gamma}`)}</div>
      <p>
        Natural linewidth {@html itex(String.raw`\Gamma`)} in eV.
        Widths from Campbell & Papp <a href="#ref">[9]</a>.
      </p>
    </div>
  </div>

  <div class="xraylib-box">
    <div class="xraylib-header">
      <h2>Cross sections from xraylib</h2>
    </div>
    <p>
      All atomic cross sections are pre-computed from
      <a href="https://github.com/tschoonj/xraylib">xraylib</a>
      (Elam/Kissel/EPDL97 databases) and shipped as static JSON.
      The generation script calls:
    </p>
    <table>
      <thead>
        <tr>
          <th>xraylib function</th>
          <th>returns</th>
          <th>units</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><code>CS_Photo(Z, E)</code></td>
          <td>photoabsorption cross section</td>
          <td>cm<sup>2</sup>/g</td>
        </tr>
        <tr>
          <td><code>CS_Rayl(Z, E)</code></td>
          <td>Rayleigh (coherent) scattering</td>
          <td>cm<sup>2</sup>/g</td>
        </tr>
        <tr>
          <td><code>CS_Compt(Z, E)</code></td>
          <td>Compton (incoherent) scattering</td>
          <td>cm<sup>2</sup>/g</td>
        </tr>
        <tr>
          <td><code>CS_Total(Z, E)</code></td>
          <td>total attenuation</td>
          <td>cm<sup>2</sup>/g</td>
        </tr>
        <tr>
          <td><code>CS_Photo_Partial(Z, shell, E)</code></td>
          <td>shell-resolved photoabsorption</td>
          <td>cm<sup>2</sup>/g</td>
        </tr>
        <tr>
          <td><code>EdgeEnergy(Z, shell)</code></td>
          <td>absorption edge energy</td>
          <td>keV</td>
        </tr>
        <tr>
          <td><code>AtomicLevelWidth(Z, shell)</code></td>
          <td>natural linewidth {@html itex(String.raw`\Gamma`)}</td>
          <td>keV</td>
        </tr>
      </tbody>
    </table>
    <p>
      All cm<sup>2</sup>/g values are converted to cm<sup>2</sup>/atom:
      {@html itex(String.raw`\sigma_\text{atom} = \sigma_{\text{cm}^2\text{/g}} \times A_r / N_A`)}.
      Energy grid: 0.1–200 keV with 2000 log-spaced points plus
      paired points bracketing each absorption edge.
    </p>
  </div>

  <div class="references" id="ref">
    <h2>References</h2>
    <ol>
      <li>Son, Young & Santra, Phys. Rev. A <b>83</b>, 033402 (2011). <a class="doi" href="https://doi.org/10.1103/PhysRevA.83.033402">10.1103/PhysRevA.83.033402</a></li>
      <li>Neutze et al., Nature <b>406</b>, 752 (2000). <a class="doi" href="https://doi.org/10.1038/35021099">10.1038/35021099</a></li>
      <li>Chapman et al., Nature <b>470</b>, 73 (2011). <a class="doi" href="https://doi.org/10.1038/nature09750">10.1038/nature09750</a></li>
      <li>Barty et al., Nature Photonics <b>6</b>, 35 (2012). <a class="doi" href="https://doi.org/10.1038/nphoton.2011.297">10.1038/nphoton.2011.297</a></li>
      <li>Toyota et al., J. Synchrotron Rad. <b>26</b>, 1017 (2019). <a class="doi" href="https://doi.org/10.1107/S1600577519003564">10.1107/S1600577519003564</a></li>
      <li>Nass et al., Nature Comms. <b>11</b>, 1814 (2020). <a class="doi" href="https://doi.org/10.1038/s41467-020-15610-4">10.1038/s41467-020-15610-4</a></li>
      <li>Williams et al., IUCrJ <b>12</b>, 358 (2025). <a class="doi" href="https://doi.org/10.1107/S2052252525002660">10.1107/S2052252525002660</a></li>
      <li>Kuschel et al., Nature Comms. <b>16</b>, 847 (2025). <a class="doi" href="https://doi.org/10.1038/s41467-025-56046-y">10.1038/s41467-025-56046-y</a></li>
      <li>Campbell & Papp, At. Data Nucl. Data Tables <b>77</b>, 1 (2001).</li>
      <li>Tiesinga et al., Rev. Mod. Phys. <b>93</b>, 025010 (2021). <a class="doi" href="https://doi.org/10.1103/RevModPhys.93.025010">10.1103/RevModPhys.93.025010</a></li>
    </ol>
  </div>
</div>

<style>
  .maths {
    padding: 42px 50px 60px;
    max-width: 1360px;
  }

  .tool-header {
    border-bottom: 1px solid var(--color-rule);
    padding-bottom: 26px;
    margin-bottom: 0;
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
    max-width: 500px;
    font-family: var(--font-ui);
    font-size: 13.5px;
    line-height: 1.6;
    color: var(--color-text-muted);
  }

  /* ── Grid ─────────────────────────────────────────────────────── */

  .grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(min(300px, 100%), 1fr));
    gap: 1px;
    background: var(--color-rule);
    border: 1px solid var(--color-rule);
    border-top: 0;
  }

  .card {
    background: var(--color-surface-card);
    padding: 22px 24px 20px;
  }

  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    margin-bottom: 10px;
  }

  .card-number {
    font-family: var(--font-mono);
    font-size: 10.5px;
    color: var(--color-text-faint);
  }

  .card-category {
    font-family: var(--font-ui);
    font-weight: 500;
    font-size: 10px;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: var(--color-text-faint);
  }

  h2 {
    margin: 0 0 10px;
    font-family: var(--font-ui);
    font-weight: 600;
    font-size: 16px;
    letter-spacing: -0.01em;
  }

  .formula {
    margin-bottom: 12px;
    overflow-x: auto;
  }

  .formula :global(.katex-display) {
    margin: 0;
    padding: 10px 16px;
    background: var(--color-surface);
    text-align: left;
  }

  p {
    margin: 0;
    font-family: var(--font-ui);
    font-size: 12.5px;
    line-height: 1.6;
    color: var(--color-text-muted);
  }

  p a {
    color: var(--color-text-faint);
    text-decoration: none;
  }

  p a:hover {
    color: var(--color-text);
  }

  /* ── xraylib box ─────────────────────────────────────────────── */

  .xraylib-box {
    border: 1px solid var(--color-rule);
    border-top: 0;
    background: var(--color-surface-card);
    padding: 22px 24px 24px;
  }

  .xraylib-header {
    margin-bottom: 10px;
  }

  .xraylib-box p {
    margin-bottom: 12px;
  }

  .xraylib-box p a {
    color: var(--color-link);
    text-decoration: none;
  }

  .xraylib-box p a:hover {
    text-decoration: underline;
  }

  table {
    width: 100%;
    border-collapse: collapse;
    font-size: 11px;
    margin-bottom: 14px;
  }

  th {
    text-align: left;
    font-family: var(--font-ui);
    font-weight: 500;
    font-size: 9px;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    color: var(--color-text-faint);
    padding: 6px 10px 6px 0;
    border-bottom: 1px solid var(--color-rule);
  }

  td {
    font-family: var(--font-ui);
    font-size: 12px;
    padding: 6px 10px 6px 0;
    border-bottom: 1px solid var(--color-rule-light);
    color: var(--color-text);
  }

  code {
    font-family: var(--font-mono);
    font-size: 11.5px;
  }

  /* ── References ───────────────────────────────────────────────── */

  .references {
    border: 1px solid var(--color-rule);
    border-top: 0;
    background: var(--color-surface-card);
    padding: 22px 24px 24px;
  }

  .references h2 {
    margin-bottom: 12px;
  }

  .references ol {
    margin: 0;
    padding: 0 0 0 24px;
    font-family: var(--font-ui);
    font-size: 12px;
    line-height: 1.65;
    color: var(--color-text);
  }

  .references li {
    margin-bottom: 6px;
  }

  .references li:last-child {
    margin-bottom: 0;
  }

  .doi {
    font-family: var(--font-mono);
    font-size: 10.5px;
    color: var(--color-text-faint);
    text-decoration: none;
  }

  .doi:hover {
    color: var(--color-link);
  }
</style>
