import { computeBeam, type BeamParams } from './beam';
import { getCrossSections, getElementInfo, type ElementSymbol } from './xray';

const LN2 = Math.log(2);
const HBAR_eV_s = 6.582119569e-16;

// Abramowitz & Stegun 7.1.26 — max error ~1.5e-7
export function erf(x: number): number {
  const sign = x < 0 ? -1 : 1;
  const a = Math.abs(x);
  const t = 1 / (1 + 0.3275911 * a);
  const poly = t * (0.254829592 + t * (-0.284496736 + t * (1.421413741 + t * (-1.453152027 + t * 1.061405429))));
  return sign * (1 - poly * Math.exp(-a * a));
}

export interface ShellEtaPrime {
  name: string;
  sigma_cm2: number;
  edge_keV: number;
  width_eV: number;
  tau_hole_s: number;
  eta_shell: number;
  eta_prime: number;
}

export interface EtaResult {
  eta_photo: number;
  eta_total: number;
  eta_prime_val: number;
  eta_prime_shell: string;
  eta_prime_tau_s: number;
  fluence_phcm2: number;
  shells: ShellEtaPrime[];
}

export function computeEta(params: BeamParams, element: ElementSymbol, tau_override_s?: number): EtaResult {
  const beam = computeBeam(params);
  const energy_keV = params.photonEnergy_eV / 1e3;
  const cs = getCrossSections(element, energy_keV);
  const info = getElementInfo(element);

  const fluence = beam.fluence_phcm2;
  const eta_photo = cs.sigma_photo * fluence;
  const eta_total = cs.sigma_total * fluence;

  const shells: ShellEtaPrime[] = [];
  for (const [name, sigma] of Object.entries(cs.shells)) {
    if (sigma <= 0) continue;
    const shellInfo = info.shells[name];
    if (!shellInfo) continue;

    const width_eV = shellInfo.width_eV;
    const tau_hole_s = width_eV > 0 ? HBAR_eV_s / width_eV : Infinity;
    const eta_shell = sigma * fluence;
    const x = 2 * Math.sqrt(LN2) * tau_hole_s / params.pulseDuration_s;
    const eta_prime = eta_photo * erf(x) / 2;

    shells.push({
      name,
      sigma_cm2: sigma,
      edge_keV: shellInfo.edge_keV,
      width_eV,
      tau_hole_s,
      eta_shell,
      eta_prime,
    });
  }

  let eta_prime_val = 0;
  let eta_prime_shell = '';
  let eta_prime_tau_s = 0;

  if (tau_override_s != null && tau_override_s > 0) {
    const x = 2 * Math.sqrt(LN2) * tau_override_s / params.pulseDuration_s;
    eta_prime_val = eta_photo * erf(x) / 2;
    eta_prime_shell = 'custom';
    eta_prime_tau_s = tau_override_s;
  } else if (shells.length > 0) {
    const dominant = shells.reduce((best, s) => {
      if (s.sigma_cm2 > best.sigma_cm2) return s;
      if (s.sigma_cm2 === best.sigma_cm2 && s.tau_hole_s > best.tau_hole_s) return s;
      return best;
    });
    eta_prime_val = dominant.eta_prime;
    eta_prime_shell = dominant.name;
    eta_prime_tau_s = dominant.tau_hole_s;
  }

  return {
    eta_photo,
    eta_total,
    eta_prime_val,
    eta_prime_shell,
    eta_prime_tau_s,
    fluence_phcm2: fluence,
    shells,
  };
}

export interface HeatmapData {
  x_nm: number[];
  y_nm: number[];
  eta_2d: number[][];
  eta_prime_2d: number[][];
  zmax_eta: number;
  zmax_eta_prime: number;
}

export function computeHeatmap(params: BeamParams, element: ElementSymbol, tau_override_s?: number, nPts = 201): HeatmapData {
  const etaResult = computeEta(params, element, tau_override_s);
  const cs = getCrossSections(element, params.photonEnergy_eV / 1e3);

  const fwhm_x_nm = params.fwhm_x_m * 1e9;
  const fwhm_y_nm = params.fwhm_y_m * 1e9;
  const extent_x = 2 * fwhm_x_nm;
  const extent_y = 2 * fwhm_y_nm;

  const x_nm: number[] = new Array(nPts);
  const y_nm: number[] = new Array(nPts);
  for (let i = 0; i < nPts; i++) {
    x_nm[i] = -extent_x + (2 * extent_x * i) / (nPts - 1);
    y_nm[i] = -extent_y + (2 * extent_y * i) / (nPts - 1);
  }

  const eta_2d: number[][] = new Array(nPts);
  const eta_prime_2d: number[][] = new Array(nPts);
  let zmax_eta = 0;
  let zmax_eta_prime = 0;

  const etaPrimeRatio = etaResult.eta_photo > 0
    ? etaResult.eta_prime_val / etaResult.eta_photo
    : 0;

  const isGaussian = params.mode === 'gaussian';

  for (let j = 0; j < nPts; j++) {
    eta_2d[j] = new Array(nPts);
    eta_prime_2d[j] = new Array(nPts);
    for (let i = 0; i < nPts; i++) {
      let envelope: number;
      if (isGaussian) {
        envelope = Math.exp(
          -4 * LN2 * (x_nm[i] ** 2 / fwhm_x_nm ** 2 + y_nm[j] ** 2 / fwhm_y_nm ** 2)
        );
      } else {
        // Flat-top elliptical: uniform inside the FWHM ellipse, zero outside
        const rx = fwhm_x_nm / 2;
        const ry = fwhm_y_nm / 2;
        envelope = (x_nm[i] ** 2 / rx ** 2 + y_nm[j] ** 2 / ry ** 2) <= 1 ? 1 : 0;
      }
      const fluence_local = etaResult.fluence_phcm2 * envelope;
      const eta = cs.sigma_photo * fluence_local;
      const etap = eta * etaPrimeRatio;

      eta_2d[j][i] = eta;
      eta_prime_2d[j][i] = etap;

      if (eta > zmax_eta) zmax_eta = eta;
      if (etap > zmax_eta_prime) zmax_eta_prime = etap;
    }
  }

  return { x_nm, y_nm, eta_2d, eta_prime_2d, zmax_eta, zmax_eta_prime };
}

export interface EnergyScanPoint {
  energy_keV: number;
  eta: number;
  eta_prime: number;
  sigma_barn: number;
}

export function computeEnergyScan(
  params: BeamParams,
  element: ElementSymbol,
  nPts = 300,
): EnergyScanPoint[] {
  const logMin = Math.log(0.1);
  const logMax = Math.log(100);
  const points: EnergyScanPoint[] = [];

  for (let i = 0; i < nPts; i++) {
    const logE = logMin + (logMax - logMin) * i / (nPts - 1);
    const energy_keV = Math.exp(logE);
    const scanParams = { ...params, photonEnergy_eV: energy_keV * 1e3 };
    const result = computeEta(scanParams, element);
    const cs = getCrossSections(element, energy_keV);
    points.push({
      energy_keV,
      eta: result.eta_photo,
      eta_prime: result.eta_prime_val,
      sigma_barn: cs.sigma_photo * 1e24,
    });
  }

  return points;
}
