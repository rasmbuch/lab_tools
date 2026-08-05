export interface ShellInfo {
  edge_keV: number;
  width_eV: number;
}

export interface XrayElementData {
  element: string;
  Z: number;
  A_r: number;
  shells: Record<string, ShellInfo>;
  grid: {
    energy_keV: number[];
    sigma_photo: number[];
    sigma_rayleigh: number[];
    sigma_compton: number[];
    sigma_total: number[];
    sigma_shells: Record<string, number[]>;
  };
}

export interface XrayCrossSections {
  sigma_photo: number;
  sigma_rayleigh: number;
  sigma_compton: number;
  sigma_total: number;
  shells: Record<string, number>;
}
