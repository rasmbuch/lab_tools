let _eV = $state(9.7e3);

export const photonEnergy = {
  get eV() { return _eV; },
  set eV(v: number) { _eV = v; },
};
