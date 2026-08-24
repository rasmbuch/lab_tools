# XFEL Fluence and Eta Calculator: Validation References

Compiled 2026-08-24. Seven published references with beam parameters
suitable for validating the fluence/eta calculator formulas.

---

## Reference 1: Nass et al. 2020 (LCLS CXI, hard X-ray, Fe/Gd proteins)

**Citation:** Nass K, Gorel A, Abdullah MM, et al. "Structural dynamics in
proteins induced by and probed with X-ray free-electron laser pulses."
*Nature Communications* 11, 1814 (2020).
DOI: 10.1038/s41467-020-15610-4

| Field | Value |
|-------|-------|
| Facility / beamline | LCLS, Coherent X-ray Imaging (CXI) instrument |
| Photon energy | 7.112 keV (pump), ~7.032 keV (probe) |
| Pulse energy | ~1 mJ total (split ~0.5 mJ each), gas detector |
| Beamline transmission | ~45% |
| Focal spot FWHM | ~0.2 um (nominal, single value; beam profile via imprints) |
| Pulse duration | 15 fs FWHM |
| Beam profile | Gaussian (simulations); experimentally calibrated via imprint method |
| Target element | Fe (ferredoxin [4Fe-4S] clusters), Gd (gadoteridol-soaked lysozyme) |
| Reported fluence | 7.0 x 10^12 ph/um^2 (high); 4.4 x 10^12 ph/um^2 (medium); 8.8 x 10^11 ph/um^2 (low) |
| Reported irradiance | 2.7 x 10^19 W/cm^2 (average intensity in focus) |
| Reported dose | 7 GGy (thaumatin), 33 GGy (lysozyme+Gd) |
| Fluence determination | RADDOSE-3D (dose); beam imprints for profile; gas detector for pulse energy |
| Notes | X-ray pump / X-ray probe experiment. Two 15 fs pulses separated by ~80 eV, centered on Fe K-edge. Excellent validation target for Fe cross-sections. |

**Validation use:** Compare our calculated peak fluence (photons/um^2) from
E_pulse=0.225 mJ (0.5 mJ * 0.45), hv=7.112 keV, FWHM=0.2 um Gaussian,
against their reported 7.0 x 10^12 ph/um^2 (high fluence condition). Also
compute eta for Fe at 7.112 keV and compare with their reported 33 GGy dose
for Gd-soaked lysozyme.

---

## Reference 2: Rudek et al. 2018 (LCLS CXI, hard X-ray, Xe ionization)

**Citation:** Rudek B, Toyota K, Foucar L, et al. "Relativistic and
resonant effects in the ionization of heavy atoms by ultra-intense hard
X-rays." *Nature Communications* 9, 4200 (2018).
DOI: 10.1038/s41467-018-06745-6

| Field | Value |
|-------|-------|
| Facility / beamline | LCLS, CXI nano-focus instrument |
| Photon energy | 5.5, 6.5, 7.0, 7.5, 8.3 keV (five energies) |
| Pulse energy | 3.7-4.4 mJ (gas detector, upstream) |
| Beamline transmission | 19.8-35.9% (varies by photon energy; see Table 1 in paper) |
| Focal spot FWHM | 0.35 um x 0.30 um |
| Pulse duration | 30 fs (nominal) |
| Beam profile | Double Gaussian (two independent Gaussians with fitted ratio of peak fluences and widths) |
| Target element | Xe (xenon atoms) |
| Reported fluence | 2.21-5.12 mJ/um^2 (peak energy fluence) |
| Reported irradiance | ~10^19 W/cm^2 |
| Reported charge states | Xe^8+ through Xe^42+ |
| Fluence determination | XCALIB toolkit calibration using Ar reference charge state distributions; minimized squared difference between theory and experiment |
| Notes | Double-Gaussian beam model: ratio of peak fluences ~0.16, ratio of widths ~2.5. Beamline transmission Table 1 is critical for validation. Xe is a supported element in our calculator. |

**Validation use:** Xe is in our element list. At each photon energy, compute
E_at_sample = E_gas * T, then peak fluence for the narrow Gaussian component.
Compare against their reported 2.21-5.12 mJ/um^2 range. Note the
double-Gaussian complication: our calculator assumes a single Gaussian, so
the narrow component alone should be used. Also compute eta for Xe at each
energy using their calibrated fluence.

---

## Reference 3: Rudenko et al. 2017 (LCLS CXI, hard X-ray, CH3I/C6H5I)

**Citation:** Rudenko A, Inhester L, Hanasaki K, et al. "Femtosecond
response of polyatomic molecules to ultra-intense hard X-rays." *Nature*
546, 129-132 (2017). DOI: 10.1038/nature22373

| Field | Value |
|-------|-------|
| Facility / beamline | LCLS, CXI nano-focus instrument |
| Photon energy | 8.3 keV |
| Pulse energy | Not explicitly stated (similar setup to Rudek 2018; likely ~3.7 mJ gas detector) |
| Beamline transmission | 32% |
| Focal spot FWHM | 0.35 um x 0.30 um |
| Pulse duration | 30 fs |
| Beam profile | Double Gaussian (same as Rudek 2018 setup) |
| Target element | Iodine (in CH3I and C6H5I molecules) |
| Reported fluence | 4.13 x 10^12 photons/um^2 (peak) |
| Reported irradiance | >10^19 W/cm^2 |
| Fluence determination | Same XCALIB method as Rudek 2018 |
| Notes | "Molecular black hole" paper. Iodine absorbs so many photons it strips electrons from neighboring C and H atoms. Data accumulated over 287,400 LCLS shots. |

**Validation use:** At 8.3 keV, our calculator can verify the peak fluence
from E_pulse * 0.32 / (photon_energy) / A_eff. Iodine is not currently in
our element list but could be added. The fluence in photons/um^2 is directly
comparable to our output.

---

## Reference 4: Williams et al. 2025 (SwissFEL, hard X-ray, Fe-heme/disulfides)

**Citation:** Williams LJ, Thompson AJ, Dijkstal P, et al. "Damage before
destruction? X-ray-induced changes in single-pulse serial femtosecond
crystallography." *IUCrJ* 12(3), 358-371 (2025).
DOI: 10.1107/S2052252525002660

| Field | Value |
|-------|-------|
| Facility / beamline | SwissFEL ARAMIS, Cristallina experimental station |
| Photon energy | 12.03 keV |
| Pulse energy | 10, 50, 100 uJ (at sample, directly measured) |
| Beamline transmission | Not stated as a single factor; transmission calculated via XOP for each beamline element |
| Focal spot FWHM | 3.8 um (H) x 2.1 um (V) |
| Pulse duration | 7.9 +/- 1.4, 23.8 +/- 0.6, 41.3 +/- 0.7, 52.7 +/- 2.5 fs |
| Beam profile | Complex multi-peak temporal structure (non-simple Gaussian) |
| Target element | Fe (iron-heme peroxidase DtpAa), S (disulfide bonds in thaumatin) |
| Reported dose | 3-146 kGy (ADER from RADDOSE-XFEL) |
| Reported photon count | 5.3 x 10^10 photons/pulse at 100 uJ |
| Fluence determination | Direct detector measurement (JUNGFRAU 1.5M) with filter calibration curves; dose via RADDOSE-XFEL |
| Notes | First SFX experiment with directly measured pulse duration. Systematic matrix of 4 durations x 3 energies. Dose values are relatively low (kGy not GGy) due to moderate pulse energies. |

**Validation use:** Excellent for testing at 12 keV with well-characterized
at-sample pulse energies. Our calculator can reproduce their photon count
(100 uJ / (12030 eV * 1.602e-19 J/eV) = 5.2 x 10^10, matching their
5.3 x 10^10). Compute peak fluence for 3.8 x 2.1 um Gaussian and compare
with their dose estimates. Fe is a supported element.

---

## Reference 5: Grunbein et al. 2018 (European XFEL, hard X-ray, lysozyme)

**Citation:** Grunbein ML, Bielecki J, Gorel A, et al. "Megahertz data
collection from protein microcrystals at an X-ray free-electron laser."
*Nature Communications* 9, 3487 (2018).
DOI: 10.1038/s41467-018-05953-4

| Field | Value |
|-------|-------|
| Facility / beamline | European XFEL, SPB/SFX instrument |
| Photon energy | 7.47 keV, 9.22 keV |
| Pulse energy | 0.9-1.5 mJ (at sample) |
| Beamline transmission | Not explicitly stated |
| Focal spot FWHM | ~15 um diameter (7.47 keV); ~28 um diameter (9.22 keV) |
| Pulse duration | ~50 fs FWHM (from electron beam diagnostics) |
| Beam profile | Not specified (assumed Gaussian) |
| Target element | Light atoms (lysozyme: C, N, O, S) |
| Reported fluence | Not explicitly reported |
| Reported dose | Not reported |
| Notes | First megahertz-rate SFX data collection at EuXFEL. 1.128 MHz intra-train repetition rate. Large focal spot means moderate fluence despite high pulse energy. |

**Validation use:** Calculator can predict fluence: E=1.5 mJ, hv=9.22 keV,
FWHM=28 um Gaussian gives N_photons = 1.02 x 10^12, A_eff = pi/2 *
(28/sqrt(2*ln2))^2 um^2 = 1410 um^2, peak fluence = 7.2 x 10^8 ph/um^2.
This is the moderate-fluence regime for SFX.

---

## Reference 6: Gisriel et al. 2019 (European XFEL, hard X-ray, photosystem I)

**Citation:** Gisriel C, Coe J, Letrun R, et al. "Membrane protein
megahertz crystallography at the European XFEL." *Nature Communications*
10, 5021 (2019). DOI: 10.1038/s41467-019-12955-3

| Field | Value |
|-------|-------|
| Facility / beamline | European XFEL, SPB/SFX instrument |
| Photon energy | 9.3 keV |
| Pulse energy | 0.7-1 mJ (upstream of hutch) |
| Beamline transmission | ~50% (estimated flux reduction to sample) |
| Focal spot FWHM | 16 +/- 4 um diameter |
| Pulse duration | ~50 fs (estimated from electron bunch length) |
| Beam profile | Not specified (Gaussian assumed) |
| Target element | Fe (in photosystem I Fe4S4 clusters), Mg, Mn |
| Reported photon count | 4.7-6.7 x 10^11 photons/pulse (upstream) |
| Reported fluence | Not reported |
| Reported dose | Not reported |
| Notes | Photosystem I is a ~1 MDa membrane protein complex with Fe4S4 clusters. 30-pulse trains at 1.128 MHz. |

**Validation use:** With T=0.5, E_at_sample = 0.5 mJ, hv=9.3 keV,
FWHM=16 um. Our calculator should give N_photons = 3.4 x 10^11 and
peak fluence = ~8.5 x 10^8 ph/um^2. Compare upstream photon count:
1 mJ / (9300 * 1.602e-19) = 6.7 x 10^11, matching their stated range.

---

## Reference 7: Kuschel et al. 2025 (LCLS TMO, soft X-ray, Xe nanoparticles)

**Citation:** Kuschel S, Ho PJ, Al Haddad A, et al. "Non-linear enhancement
of ultrafast X-ray diffraction through transient resonances." *Nature
Communications* 16, 847 (2025). DOI: 10.1038/s41467-025-56046-y

| Field | Value |
|-------|-------|
| Facility / beamline | LCLS, TMO endstation (LAMP) |
| Photon energy | 650-740 eV (scanned near Xe 3d edge), 1500 eV |
| Pulse energy | 1.5 mJ (>100 fs), 0.1 mJ (5-10 fs), 0.02 mJ (~0.5 fs) |
| Beamline transmission | ~0.2 (stated in known reference context) |
| Focal spot FWHM | 1.5 um (near-Gaussian) |
| Pulse duration | >100 fs, 5-10 fs, ~0.5 fs (three regimes) |
| Beam profile | Near-Gaussian |
| Target element | Xe (nanoparticles, 60-150 nm diameter) |
| Reported fluence | Supplementary Table 1 (not fully reproduced in accessible text; values ~10x lower than calculator predicts per handoff doc) |
| Fluence determination | Cross-checked via M-shell fluorescence yield and gas detector pulse energy |
| Notes | KNOWN DISCREPANCY: Handoff document states their fluence is ~10x lower than our calculator predicts after applying T=0.2. They calibrated independently via fluorescence yield. This is the soft X-ray regime (<2 keV) where beamline transmission is more uncertain. Xe is a supported element. |

**Validation use:** This is the reference that originally motivated the
validation effort. At 700 eV, 1.5 mJ * 0.2 = 0.3 mJ at sample; with
1.5 um FWHM Gaussian, calculator gives a peak fluence that is reportedly
~10x higher than their fluorescence-calibrated value. Possible explanations:
(1) beamline transmission is lower than 0.2, (2) beam profile is not
Gaussian (broader pedestal), (3) fluorescence calibration includes
additional losses. This discrepancy should be investigated.

---

## Summary Table

| # | First author | Year | Facility | hv (keV) | E_pulse | T | FWHM (um) | tau (fs) | Profile | Element | Fluence reported? |
|---|-------------|------|----------|----------|---------|---|-----------|----------|---------|---------|-------------------|
| 1 | Nass | 2020 | LCLS CXI | 7.1 | 0.5 mJ (gas) | 0.45 | 0.2 | 15 | Gaussian | Fe, Gd | Yes: 7e12 ph/um^2 |
| 2 | Rudek | 2018 | LCLS CXI | 5.5-8.3 | 3.7-4.4 mJ (gas) | 0.20-0.36 | 0.35x0.30 | 30 | Double Gaussian | Xe | Yes: 2.2-5.1 mJ/um^2 |
| 3 | Rudenko | 2017 | LCLS CXI | 8.3 | ~3.7 mJ (gas) | 0.32 | 0.35x0.30 | 30 | Double Gaussian | I (CH3I) | Yes: 4.1e12 ph/um^2 |
| 4 | Williams | 2025 | SwissFEL | 12.0 | 10-100 uJ (sample) | measured | 3.8x2.1 | 7.9-52.7 | Complex | Fe | Yes: dose 3-146 kGy |
| 5 | Grunbein | 2018 | EuXFEL | 7.5-9.2 | 0.9-1.5 mJ | -- | 15-28 | 50 | Gaussian | C,N,O,S | No (computable) |
| 6 | Gisriel | 2019 | EuXFEL | 9.3 | 0.7-1 mJ (upstream) | 0.5 | 16 | 50 | Gaussian | Fe | No (computable) |
| 7 | Kuschel | 2025 | LCLS TMO | 0.65-1.5 | 0.02-1.5 mJ | 0.2 | 1.5 | 0.5-100+ | Gaussian | Xe | Yes (Supp. Table 1) |

---

## Recommended Validation Strategy

### Tier 1: Direct comparison (reported fluence to compare against)

1. **Nass 2020** - Best reference. Complete parameter set, explicitly reported
   fluence in ph/um^2, RADDOSE-3D dose, and irradiance. Fe is a supported
   element. Single Gaussian beam.

2. **Rudek 2018** - Excellent for Xe validation across five photon energies
   with calibrated fluence. CAVEAT: double-Gaussian beam profile requires
   careful treatment. Use narrow Gaussian component only.

3. **Rudenko 2017** - Good cross-check at 8.3 keV with peak fluence in
   ph/um^2. Same double-Gaussian caveat.

4. **Williams 2025** - Good for 12 keV validation with at-sample pulse
   energy (no transmission uncertainty). Dose rather than fluence reported,
   so comparison requires RADDOSE-XFEL or converting our fluence to dose.

### Tier 2: Compute fluence from parameters and cross-check

5. **Grunbein 2018** - Verify photon count at 9.22 keV. Large focal spot
   gives moderate fluence.

6. **Gisriel 2019** - Verify photon count at 9.3 keV with T=0.5.
   Cross-check against their upstream photon count.

### Tier 3: Investigate discrepancy

7. **Kuschel 2025** - Known ~10x discrepancy in soft X-ray regime. May
   reveal systematic issue with beam profile assumption or transmission
   at low photon energies. Lower priority since soft X-ray (<2 keV) is
   not the primary use case.

---

## Additional Papers of Interest (incomplete parameter sets)

These papers are relevant background but lack a complete parameter set
for direct validation:

- **Boutet et al. 2012** - Science 337, 362-364. First high-resolution SFX
  (lysozyme at 1.9 A). LCLS CXI, 9.4 keV, 40 fs, dose 33 MGy. Focal spot
  and pulse energy not fully reported in accessible text.

- **Chapman et al. 2014** - Phil. Trans. R. Soc. B 369, 20130313. Review
  "Diffraction before destruction." Reports 4 x 10^11 ph/um^2 at 6 keV
  and intensities >10^17 W/cm^2 but as a review, aggregates multiple
  experiments.

- **Murphy et al. 2014** - Nature Communications 5, 4281. C60 explosion at
  LCLS. 485 eV, 345 uJ, 30 fs, 1.4 um focus. Soft X-ray; C is a supported
  element. Could be added as soft X-ray validation point.

- **Sugahara et al. 2015** - Nature Methods 12, 61-63. SACLA BL3, 7 keV,
  200 uJ, 1.5 x 1.5 um, 10 fs. Complete parameters but dose/fluence not
  reported.

- **RADDOSE-XFEL (Dickerson et al. 2020)** - J. Appl. Cryst. 53, 549-560.
  Contains dose calculation formulas for independent cross-validation of
  our dose-related outputs.

---

## Key Conversion Notes for Validation

For converting between units reported in these papers:

- 1 mJ/um^2 = 10^5 J/cm^2 = 10^9 J/m^2
- 1 ph/um^2 = 10^8 ph/cm^2
- Photon energy to wavelength: lambda(A) = 12398.42 / E(eV)
- N_photons = E_pulse(J) / (hv(eV) * 1.602e-19)
- A_eff(Gaussian) = (pi/2) * w0_x * w0_y where w0 = FWHM / sqrt(2*ln2)
- Peak fluence = N_photons / A_eff

---

## Sources

- Nass et al. 2020: https://doi.org/10.1038/s41467-020-15610-4
- Rudek et al. 2018: https://doi.org/10.1038/s41467-018-06745-6
- Rudenko et al. 2017: https://doi.org/10.1038/nature22373
- Williams et al. 2025: https://doi.org/10.1107/S2052252525002660
- Grunbein et al. 2018: https://doi.org/10.1038/s41467-018-05953-4
- Gisriel et al. 2019: https://doi.org/10.1038/s41467-019-12955-3
- Kuschel et al. 2025: https://doi.org/10.1038/s41467-025-56046-y
- Boutet et al. 2012: https://doi.org/10.1126/science.1217737
- Chapman et al. 2014: https://doi.org/10.1098/rstb.2013.0313
- Murphy et al. 2014: https://doi.org/10.1038/ncomms5281
- Sugahara et al. 2015: https://doi.org/10.1038/nmeth.3172
- Dickerson et al. 2020: https://doi.org/10.1107/S1600576720000643
