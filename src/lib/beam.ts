import { eV_J, hc_eV_m } from './constants';

export type SpatialMode = 'gaussian' | 'flat-top';

export interface BeamParams {
  photonEnergy_eV: number;
  pulseEnergy_J: number;
  fwhm_x_m: number;
  fwhm_y_m: number;
  pulseDuration_s: number;
  mode: SpatialMode;
}

export interface BeamResult {
  nPhotons: number;
  effectiveArea_m2: number;
  peakPower_W: number;
  peakIrradiance_Wcm2: number;
  fluence_phcm2: number;
  peakFlux_phcm2s: number;
  beamWaist_x_m: number | null;
  beamWaist_y_m: number | null;
  rayleighLength_x_m: number | null;
  rayleighLength_y_m: number | null;
}

const LN2 = Math.log(2);
const GAUSS_TEMPORAL = Math.sqrt(4 * LN2 / Math.PI);

export function computeBeam(params: BeamParams): BeamResult {
  const { photonEnergy_eV, pulseEnergy_J, fwhm_x_m, fwhm_y_m, pulseDuration_s, mode } = params;

  const nPhotons = pulseEnergy_J / (photonEnergy_eV * eV_J);
  const wavelength_m = hc_eV_m / photonEnergy_eV;

  let effectiveArea_m2: number;
  let beamWaist_x_m: number | null = null;
  let beamWaist_y_m: number | null = null;
  let rayleighLength_x_m: number | null = null;
  let rayleighLength_y_m: number | null = null;

  if (mode === 'gaussian') {
    const w0_x = fwhm_x_m / Math.sqrt(2 * LN2);
    const w0_y = fwhm_y_m / Math.sqrt(2 * LN2);
    effectiveArea_m2 = (Math.PI / 2) * w0_x * w0_y;
    beamWaist_x_m = w0_x;
    beamWaist_y_m = w0_y;
    rayleighLength_x_m = Math.PI * w0_x ** 2 / wavelength_m;
    rayleighLength_y_m = Math.PI * w0_y ** 2 / wavelength_m;
  } else {
    effectiveArea_m2 = (Math.PI / 4) * fwhm_x_m * fwhm_y_m;
  }

  const effectiveArea_cm2 = effectiveArea_m2 * 1e4;

  const peakPower_W = pulseEnergy_J * GAUSS_TEMPORAL / pulseDuration_s;
  const peakIrradiance_Wcm2 = peakPower_W / effectiveArea_cm2;
  const fluence_phcm2 = nPhotons / effectiveArea_cm2;
  const peakFlux_phcm2s = fluence_phcm2 * GAUSS_TEMPORAL / pulseDuration_s;

  return {
    nPhotons,
    effectiveArea_m2,
    peakPower_W,
    peakIrradiance_Wcm2,
    fluence_phcm2,
    peakFlux_phcm2s,
    beamWaist_x_m,
    beamWaist_y_m,
    rayleighLength_x_m,
    rayleighLength_y_m,
  };
}
