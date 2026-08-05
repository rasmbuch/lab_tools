import { hc_eV_m, h_eV_s } from './constants';

// Energy unit multipliers to eV
const energyToEv: Record<string, number> = {
  'eV':  1,
  'keV': 1e3,
  'MeV': 1e6,
};

// Wavelength unit multipliers to metres
const wavelengthToM: Record<string, number> = {
  'Å':  1e-10,
  'nm': 1e-9,
  'µm': 1e-6,
};

// Frequency unit multipliers to Hz
const frequencyToHz: Record<string, number> = {
  'THz': 1e12,
  'EHz': 1e18,
};

export type EnergyUnit = keyof typeof energyToEv;
export type WavelengthUnit = keyof typeof wavelengthToM;
export type FrequencyUnit = keyof typeof frequencyToHz;

export const energyUnits: EnergyUnit[] = ['eV', 'keV', 'MeV'];
export const wavelengthUnits: WavelengthUnit[] = ['Å', 'nm', 'µm'];
export const frequencyUnits: FrequencyUnit[] = ['THz', 'EHz'];

export function energyToEV(value: number, unit: EnergyUnit): number {
  return value * energyToEv[unit];
}

export function evToEnergy(eV: number, unit: EnergyUnit): number {
  return eV / energyToEv[unit];
}

export function wavelengthToEV(value: number, unit: WavelengthUnit): number {
  const metres = value * wavelengthToM[unit];
  return hc_eV_m / metres;
}

export function evToWavelength(eV: number, unit: WavelengthUnit): number {
  const metres = hc_eV_m / eV;
  return metres / wavelengthToM[unit];
}

export function frequencyToEV(value: number, unit: FrequencyUnit): number {
  const hz = value * frequencyToHz[unit];
  return h_eV_s * hz;
}

export function evToFrequency(eV: number, unit: FrequencyUnit): number {
  const hz = eV / h_eV_s;
  return hz / frequencyToHz[unit];
}
