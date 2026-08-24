import type { XrayElementData, XrayCrossSections } from './xray-types';

import dataH from './data/xray-H.json';
import dataC from './data/xray-C.json';
import dataO from './data/xray-O.json';
import dataNe from './data/xray-Ne.json';
import dataXe from './data/xray-Xe.json';
import dataFe from './data/xray-Fe.json';
import dataCu from './data/xray-Cu.json';
import dataAu from './data/xray-Au.json';
import dataPt from './data/xray-Pt.json';

export type ElementSymbol = 'H' | 'C' | 'O' | 'Ne' | 'Xe' | 'Fe' | 'Cu' | 'Au' | 'Pt';

export const ELEMENTS: readonly ElementSymbol[] = ['H', 'C', 'O', 'Ne', 'Fe', 'Cu', 'Xe', 'Pt', 'Au'];

const RAW: Record<ElementSymbol, XrayElementData> = {
  H: dataH as XrayElementData,
  C: dataC as XrayElementData,
  O: dataO as XrayElementData,
  Ne: dataNe as XrayElementData,
  Xe: dataXe as XrayElementData,
  Fe: dataFe as XrayElementData,
  Cu: dataCu as XrayElementData,
  Au: dataAu as XrayElementData,
  Pt: dataPt as XrayElementData,
};

interface PreparedGrid {
  logE: Float64Array;
  logSigmaPhoto: Float64Array;
  logSigmaRayleigh: Float64Array;
  logSigmaCompton: Float64Array;
  logSigmaTotal: Float64Array;
  logSigmaShells: Record<string, Float64Array>;
  edgeIndices: Map<string, number>;
}

const prepared = new Map<ElementSymbol, PreparedGrid>();

function safeLog(v: number): number {
  return v > 0 ? Math.log(v) : -Infinity;
}

function prepare(sym: ElementSymbol): PreparedGrid {
  const cached = prepared.get(sym);
  if (cached) return cached;

  const raw = RAW[sym];
  const g = raw.grid;
  const n = g.energy_keV.length;

  const logE = new Float64Array(n);
  const logSigmaPhoto = new Float64Array(n);
  const logSigmaRayleigh = new Float64Array(n);
  const logSigmaCompton = new Float64Array(n);
  const logSigmaTotal = new Float64Array(n);

  for (let i = 0; i < n; i++) {
    logE[i] = Math.log(g.energy_keV[i]);
    logSigmaPhoto[i] = safeLog(g.sigma_photo[i]);
    logSigmaRayleigh[i] = safeLog(g.sigma_rayleigh[i]);
    logSigmaCompton[i] = safeLog(g.sigma_compton[i]);
    logSigmaTotal[i] = safeLog(g.sigma_total[i]);
  }

  const logSigmaShells: Record<string, Float64Array> = {};
  for (const [name, arr] of Object.entries(g.sigma_shells)) {
    const logArr = new Float64Array(n);
    for (let i = 0; i < n; i++) {
      logArr[i] = safeLog(arr[i]);
    }
    logSigmaShells[name] = logArr;
  }

  // Pre-compute the grid index of each edge for edge-aware interpolation
  const edgeIndices = new Map<string, number>();
  for (const [name, info] of Object.entries(raw.shells)) {
    const logEdge = Math.log(info.edge_keV);
    let idx = binarySearch(logE, logEdge);
    edgeIndices.set(name, idx);
  }

  const result: PreparedGrid = {
    logE, logSigmaPhoto, logSigmaRayleigh, logSigmaCompton, logSigmaTotal,
    logSigmaShells, edgeIndices,
  };
  prepared.set(sym, result);
  return result;
}

function binarySearch(arr: Float64Array, target: number): number {
  let lo = 0;
  let hi = arr.length - 1;
  while (lo < hi) {
    const mid = (lo + hi) >>> 1;
    if (arr[mid] < target) lo = mid + 1;
    else hi = mid;
  }
  return lo;
}

function interpLogLog(logE: Float64Array, logSigma: Float64Array, logEq: number): number {
  const n = logE.length;
  if (logEq <= logE[0]) return Math.exp(logSigma[0]);
  if (logEq >= logE[n - 1]) return Math.exp(logSigma[n - 1]);

  let i = binarySearch(logE, logEq);
  if (i === 0) i = 1;

  const s0 = logSigma[i - 1];
  const s1 = logSigma[i];

  if (s0 === -Infinity && s1 === -Infinity) return 0;
  if (s0 === -Infinity) return Math.exp(s1);
  if (s1 === -Infinity) return Math.exp(s0);

  const t = (logEq - logE[i - 1]) / (logE[i] - logE[i - 1]);
  return Math.exp(s0 + t * (s1 - s0));
}

export function getCrossSections(element: ElementSymbol, energy_keV: number): XrayCrossSections {
  const raw = RAW[element];
  const grid = prepare(element);
  const logEq = Math.log(energy_keV);

  const shells: Record<string, number> = {};
  for (const [name, logArr] of Object.entries(grid.logSigmaShells)) {
    const edgeKeV = raw.shells[name]?.edge_keV ?? 0;
    if (energy_keV < edgeKeV) {
      shells[name] = 0;
    } else {
      shells[name] = interpLogLog(grid.logE, logArr, logEq);
    }
  }

  return {
    sigma_photo: interpLogLog(grid.logE, grid.logSigmaPhoto, logEq),
    sigma_rayleigh: interpLogLog(grid.logE, grid.logSigmaRayleigh, logEq),
    sigma_compton: interpLogLog(grid.logE, grid.logSigmaCompton, logEq),
    sigma_total: interpLogLog(grid.logE, grid.logSigmaTotal, logEq),
    shells,
  };
}

export function getElementInfo(element: ElementSymbol) {
  const raw = RAW[element];
  return {
    Z: raw.Z,
    A_r: raw.A_r,
    shells: raw.shells,
  };
}
