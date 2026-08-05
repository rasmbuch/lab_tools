<script lang="ts">
  import { sigfigs } from './lib/format';

  type Field = 'width' | 'height' | 'distance';

  // Input values in SI (metres)
  let width_m = $state(200e-3);
  let height_m = $state(200e-3);
  let distance_m = $state(120e-3);

  // Unit selections
  let widthUnit: 'mm' | 'cm' = $state('mm');
  let heightUnit: 'mm' | 'cm' = $state('mm');
  let distanceUnit: 'mm' | 'cm' | 'm' = $state('mm');

  // Focus tracking
  let activeField: Field | null = $state(null);
  let rawInput = $state('');

  // Unit conversion factors (display unit → SI metres)
  const lengthFactors: Record<string, number> = { 'mm': 1e-3, 'cm': 1e-2, 'm': 1 };

  function fmt(v: number): string {
    if (!Number.isFinite(v) || v <= 0) return '—';
    return sigfigs(v, 4);
  }

  function siToDisplay(si: number, unit: string): string {
    return fmt(si / lengthFactors[unit]);
  }

  // Display values
  let widthDisplay = $derived(
    activeField === 'width' ? rawInput : siToDisplay(width_m, widthUnit)
  );
  let heightDisplay = $derived(
    activeField === 'height' ? rawInput : siToDisplay(height_m, heightUnit)
  );
  let distanceDisplay = $derived(
    activeField === 'distance' ? rawInput : siToDisplay(distance_m, distanceUnit)
  );

  function handleFocus(field: Field) {
    activeField = field;
    switch (field) {
      case 'width':    rawInput = siToDisplay(width_m, widthUnit); break;
      case 'height':   rawInput = siToDisplay(height_m, heightUnit); break;
      case 'distance': rawInput = siToDisplay(distance_m, distanceUnit); break;
    }
  }

  function handleInput(field: Field, value: string) {
    activeField = field;
    rawInput = value;
    const num = parseFloat(value);
    if (!Number.isFinite(num) || num <= 0) return;

    switch (field) {
      case 'width':    width_m = num * lengthFactors[widthUnit]; break;
      case 'height':   height_m = num * lengthFactors[heightUnit]; break;
      case 'distance': distance_m = num * lengthFactors[distanceUnit]; break;
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

  // Exact solid angle for a rectangle centered on the normal axis:
  // Ω = 4 · arctan( a·b / (2d · √(a² + b² + 4d²)) )
  // where a, b = full width, height; d = distance
  let solidAngle_sr = $derived.by(() => {
    const a = width_m;
    const b = height_m;
    const d = distance_m;
    if (a <= 0 || b <= 0 || d <= 0) return 0;
    return 4 * Math.atan((a * b) / (2 * d * Math.sqrt(a * a + b * b + 4 * d * d)));
  });

  // Half-angle to corner: arctan( √((a/2)² + (b/2)²) / d )
  let halfAngle_deg = $derived.by(() => {
    const halfW = width_m / 2;
    const halfH = height_m / 2;
    const d = distance_m;
    if (d <= 0) return 0;
    return Math.atan(Math.sqrt(halfW * halfW + halfH * halfH) / d) * (180 / Math.PI);
  });

  let fractionOf4pi_pct = $derived(solidAngle_sr / (4 * Math.PI) * 100);

  // Auto-switch sr / msr
  let omegaDisplay = $derived(
    solidAngle_sr >= 0.01
      ? { value: fmt(solidAngle_sr), unit: 'sr' }
      : { value: fmt(solidAngle_sr * 1e3), unit: 'msr' }
  );
</script>

<div class="calculator">
  <div class="tool-header">
    <div class="tool-header-top">
      <span class="tool-number">04</span>
      <span class="tool-category">geometry</span>
    </div>
    <h1>Solid angle</h1>
    <p class="tool-description">
      Rectangular detector, centered on-axis. Exact integral — no small-angle approximation.
    </p>
  </div>

  <div class="fields">
    <div class="field-row">
      <label class="field-label" for="sa-width">Detector width</label>
      <div class="field-input-group">
        <input
          id="sa-width"
          type="text"
          inputmode="decimal"
          class="field-input"
          value={widthDisplay}
          onfocus={() => handleFocus('width')}
          oninput={(e) => handleInput('width', e.currentTarget.value)}
          onblur={handleBlur}
        />
        <select
          class="field-unit"
          bind:value={widthUnit}
          onchange={() => handleUnitChange('width')}
        >
          <option value="mm">mm</option>
          <option value="cm">cm</option>
        </select>
      </div>
    </div>

    <div class="field-row">
      <label class="field-label" for="sa-height">Detector height</label>
      <div class="field-input-group">
        <input
          id="sa-height"
          type="text"
          inputmode="decimal"
          class="field-input"
          value={heightDisplay}
          onfocus={() => handleFocus('height')}
          oninput={(e) => handleInput('height', e.currentTarget.value)}
          onblur={handleBlur}
        />
        <select
          class="field-unit"
          bind:value={heightUnit}
          onchange={() => handleUnitChange('height')}
        >
          <option value="mm">mm</option>
          <option value="cm">cm</option>
        </select>
      </div>
    </div>

    <div class="field-row">
      <label class="field-label" for="sa-distance">Sample–detector distance</label>
      <div class="field-input-group">
        <input
          id="sa-distance"
          type="text"
          inputmode="decimal"
          class="field-input"
          value={distanceDisplay}
          onfocus={() => handleFocus('distance')}
          oninput={(e) => handleInput('distance', e.currentTarget.value)}
          onblur={handleBlur}
        />
        <select
          class="field-unit"
          bind:value={distanceUnit}
          onchange={() => handleUnitChange('distance')}
        >
          <option value="mm">mm</option>
          <option value="cm">cm</option>
          <option value="m">m</option>
        </select>
      </div>
    </div>
  </div>

  <div class="output-section">
    <div class="section-label">Results</div>
    <div class="output-rows">
      <div class="output-row">
        <span class="output-label">Solid angle Ω</span>
        <span class="output-value">{omegaDisplay.value} <span class="output-unit">{omegaDisplay.unit}</span></span>
      </div>
      <div class="output-row">
        <span class="output-label">Ω / 4π</span>
        <span class="output-value">{fmt(fractionOf4pi_pct)} <span class="output-unit">%</span></span>
      </div>
      <div class="output-row">
        <span class="output-label">Half-angle to corner</span>
        <span class="output-value">{fmt(halfAngle_deg)} <span class="output-unit">°</span></span>
      </div>
    </div>
  </div>
</div>

<style>
  .calculator {
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

  /* ── Output section ──────────────────────────────────────────────── */

  .output-section {
    margin-top: 40px;
    border-top: 1px solid var(--color-rule);
    padding-top: 16px;
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
