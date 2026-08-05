// CODATA 2018 exact values (SI redefinition)
export const h_J_s = 6.62607015e-34;        // Planck constant [J·s]
export const c_m_s = 299792458;              // speed of light [m/s]
export const eV_J = 1.602176634e-19;         // electron-volt [J]

// Derived constants in convenient unit combinations
export const h_eV_s = h_J_s / eV_J;         // h in [eV·s]
export const hc_eV_m = h_eV_s * c_m_s;      // hc in [eV·m]
export const hc_eV_A = hc_eV_m * 1e10;      // hc in [eV·Å]  ≈ 12398.42
export const hc_keV_A = hc_eV_A / 1e3;      // hc in [keV·Å]  ≈ 12.39842
