import type { SpatialMode } from './beam';

let _eV = $state(9.7e3);
let _pulseEnergy_J = $state(100e-6);
let _fwhm_x_m = $state(200e-9);
let _fwhm_y_m = $state(200e-9);
let _pulseDuration_s = $state(10e-15);
let _mode: SpatialMode = $state('gaussian');
let _transmission = $state(1.0);

export const photonEnergy = {
  get eV() { return _eV; },
  set eV(v: number) { _eV = v; },
};

export const pulseEnergy = {
  get J() { return _pulseEnergy_J; },
  set J(v: number) { _pulseEnergy_J = v; },
};

export const fwhm = {
  get x_m() { return _fwhm_x_m; },
  set x_m(v: number) { _fwhm_x_m = v; },
  get y_m() { return _fwhm_y_m; },
  set y_m(v: number) { _fwhm_y_m = v; },
};

export const pulseDuration = {
  get s() { return _pulseDuration_s; },
  set s(v: number) { _pulseDuration_s = v; },
};

export const spatialMode = {
  get value() { return _mode; },
  set value(v: SpatialMode) { _mode = v; },
};

export const transmission = {
  get value() { return _transmission; },
  set value(v: number) { _transmission = v; },
};
