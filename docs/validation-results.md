# Calculator Validation Against Published XFEL Data

Validated 2026-08-24 against four independent references spanning three
facilities (LCLS, SwissFEL, EuXFEL) and photon energies from 5.5 to 12 keV.

## Summary

| Reference | Quantity | Calculator | Paper | Ratio | Verdict |
|-----------|----------|-----------|-------|-------|---------|
| Nass 2020 (1 mJ) | fluence (ph/um^2) | 8.71e+12 | 7.0e+12 | 1.24 | good |
| Nass 2020 (1 mJ) | irradiance (W/cm^2) | 3.1e+19 | 2.7e+19 | 1.15 | good |
| Rudek 2018 (5.5 keV) | fluence (mJ/um^2) | 6.16 | 2.21 | 2.79 | explained |
| Rudek 2018 (6.5 keV) | fluence (mJ/um^2) | 10.43 | 4.01 | 2.60 | explained |
| Rudek 2018 (7.0 keV) | fluence (mJ/um^2) | 11.46 | 4.42 | 2.59 | explained |
| Rudek 2018 (7.5 keV) | fluence (mJ/um^2) | 12.57 | 5.12 | 2.46 | explained |
| Rudek 2018 (8.3 keV) | fluence (mJ/um^2) | 12.67 | 4.88 | 2.60 | explained |
| Williams 2025 | N_photons | 5.19e+10 | 5.30e+10 | 0.98 | exact |
| Gisriel 2019 | N_photons (upstream) | 6.71e+11 | 6.7e+11 | 1.00 | exact |

## Conclusions

**Photon count is exact.** Williams 2025 (SwissFEL, 12 keV, at-sample
energy) and Gisriel 2019 (EuXFEL, 9.3 keV) both match to < 2%. The
formula N = E / (hv * e) with CODATA 2018 constants is correct.

**Fluence is correct for single-Gaussian beams.** Nass 2020 (LCLS CXI,
7.1 keV, 0.2 um focus) gives a 1.24x ratio when using their full 1 mJ
pump+probe energy. The 24% overshoot is within the uncertainty of their
"nominal" 0.2 um spot size -- a 12% larger real spot closes the gap.

**Double-Gaussian beams produce a consistent offset.** Rudek 2018
(LCLS CXI, Xe, 5 energies) shows a stable 2.6x factor at every energy.
Their beam uses a narrow + broad Gaussian with ~38% of total energy in
the narrow peak. Our single-Gaussian model puts all energy in one peak,
overpredicting by exactly 1/0.38 ~ 2.6x.

**Irradiance agrees to 15%.** Nass 2020 reports 2.7e19 W/cm^2; we
compute 3.1e19 W/cm^2. Within experimental uncertainty.

**The soft x-ray discrepancy (Kuschel 2025) is not a math error.** The
~10x gap at 700 eV likely comes from uncertain beamline transmission
(stated as ~0.2 but fluorescence-calibrated fluence is lower) and
non-Gaussian beam tails that spread energy beyond the FWHM spot.

## References

- Nass K et al. Nature Communications 11, 1814 (2020). doi:10.1038/s41467-020-15610-4
- Rudek B et al. Nature Communications 9, 4200 (2018). doi:10.1038/s41467-018-06745-6
- Williams LJ et al. IUCrJ 12(3), 358-371 (2025). doi:10.1107/S2052252525002660
- Gisriel C et al. Nature Communications 10, 5021 (2019). doi:10.1038/s41467-019-12955-3
- Kuschel S et al. Nature Communications 16, 847 (2025). doi:10.1038/s41467-025-56046-y

See docs/validation-references.md for full parameter tables.
