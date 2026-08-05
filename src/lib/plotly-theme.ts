import type { Layout, Config } from 'plotly.js';

// Hard-coded from CSS tokens in app.css (:root).
// Update these if the dashboard palette changes.
//   --color-surface:      #F4F1EA
//   --color-surface-card: #FBF9F4
//   --color-text:         #171512
//   --color-text-muted:   #5C554B
//   --color-sidebar:      #16225C  (ultramarine)
//   --font-ui:            'Archivo'
//   --font-mono:          'IBM Plex Mono'

export const labLayout: Partial<Layout> = {
  paper_bgcolor: 'transparent',
  plot_bgcolor: '#F4F1EA',
  font: {
    family: "'IBM Plex Mono', monospace",
    color: '#171512',
    size: 12,
  },
  xaxis: {
    gridcolor: 'rgba(22, 34, 92, 0.12)',
    linecolor: '#16225C',
    zerolinecolor: '#16225C',
    title: { font: { family: "'Archivo', sans-serif" } },
  },
  yaxis: {
    gridcolor: 'rgba(22, 34, 92, 0.12)',
    linecolor: '#16225C',
    zerolinecolor: '#16225C',
    title: { font: { family: "'Archivo', sans-serif" } },
  },
  margin: { l: 60, r: 20, t: 30, b: 50 },
};

export const labConfig: Partial<Config> = {
  displaylogo: false,
  modeBarButtonsToRemove: ['lasso2d', 'select2d'],
};

/**
 * Threshold colorscale: greyscale below `threshold`, Plasma above.
 * Returns a Plotly-compatible colorscale array.
 */
export function thresholdColorscale(
  zmin: number,
  zmax: number,
  threshold = 1.0,
): Array<[number, string]> {
  const frac = Math.max(0, Math.min(1, (threshold - zmin) / (zmax - zmin)));

  // Greyscale ramp below threshold (darker = lower)
  const grey: Array<[number, string]> = [
    [0, '#2a2a2a'],
    [frac * 0.5, '#666666'],
    [frac, '#999999'],
  ];

  // Plasma ramp above threshold
  const plasma: Array<[number, string]> = [
    [frac, '#0d0887'],
    [frac + (1 - frac) * 0.25, '#7e03a8'],
    [frac + (1 - frac) * 0.5, '#cc4778'],
    [frac + (1 - frac) * 0.75, '#f89540'],
    [1.0, '#f0f921'],
  ];

  return [...grey, ...plasma];
}
