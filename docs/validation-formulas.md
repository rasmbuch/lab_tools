# Formula Validation: XFEL Beam Calculators

Validation of the physics formulas in `src/lib/beam.ts` and `src/lib/eta.ts`
against primary-source publications and standard physics references.

---

## 1. Gaussian Beam Model (beam.ts)

### 1.1 FWHM to beam waist: `w0 = FWHM / sqrt(2 ln 2)`

**Status: CORRECT**

The standard Gaussian beam intensity profile is
`I(r) = I0 exp(-2r^2/w0^2)`, where `w0` is the 1/e^2 radius.
Setting `I(FWHM/2) = I0/2` and solving:

    1/2 = exp(-2(FWHM/2)^2 / w0^2)
    ln 2 = FWHM^2 / (2 w0^2)
    w0 = FWHM / sqrt(2 ln 2)

This is the universally accepted conversion factor (sqrt(2 ln 2) ~ 1.1774).

**References:**
- Newport, "Gaussian Beam Optics" (https://www.newport.com/n/gaussian-beam-optics/)
- Ansys Optics, "How to convert FWHM measurements to 1/e^2 halfwidths"
  (https://optics.ansys.com/hc/en-us/articles/42661666396947)
- RP Photonics, "Beam Radius" (https://www.rp-photonics.com/beam_radius.html)

### 1.2 Effective area (Gaussian): `A_eff = (pi/2) w0_x w0_y`

**Status: CORRECT**

For a 2D elliptical Gaussian `I(x,y) = I0 exp(-2x^2/w0x^2 - 2y^2/w0y^2)`,
the total power (or total photon count) is obtained by integration:

    integral I(x,y) dx dy = I0 * (pi/2) * w0x * w0y

The effective area is defined as A_eff = P_total / I_peak, giving:

    A_eff = (pi/2) * w0x * w0y

This is confirmed in standard optics references as the "equivalent top-hat area"
for a Gaussian beam, sometimes written A_eff = pi w0^2 / 2 for a round beam.

**References:**
- FiberOptics4Sale, "Physical Properties of Gaussian Beams", Eq. 7:
  A_TH = pi w^2 / 2 (https://www.fiberoptics4sale.com/blogs/wave-optics/physical-properties-of-gaussian-beams)
- RP Photonics, "Effective Mode Area"
  (https://www.rp-photonics.com/effective_mode_area.html)
- XCALIB paper (Toyota et al., 2019), Eq. 8: n = F0 Delta^2 / a where
  a = 4 ln 2 / pi, giving the same relationship between peak fluence,
  total photons, and beam area.

### 1.3 Effective area (flat-top ellipse): `A_eff = (pi/4) FWHM_x FWHM_y`

**Status: CORRECT**

For a uniform elliptical beam with semi-axes a = FWHM_x/2 and b = FWHM_y/2,
the geometric area is pi * a * b = (pi/4) FWHM_x FWHM_y. For a flat-top
profile, effective area equals geometric area.

### 1.4 Temporal Gaussian factor: `f = sqrt(4 ln 2 / pi)` (~0.9394)

**Status: CORRECT**

For a Gaussian temporal pulse P(t) = P0 exp(-4 ln 2 t^2 / tau^2) where tau
is the FWHM, integrating over all time gives the pulse energy:

    E = P0 * tau * sqrt(pi / (4 ln 2))

Inverting: P0 = E * sqrt(4 ln 2 / pi) / tau ~ 0.9394 * E / tau

This factor is confirmed by Newport ("Laser Pulse Characterization") which gives
P_peak = E / (tau_HW1e * sqrt(pi)), and the conversion tau_FWHM = 2 sqrt(ln 2) *
tau_HW1e yields the same result. The numerical value 0.9394 is widely quoted in
ultrafast laser literature.

**References:**
- Newport, "Laser Pulse Characterization"
  (https://www.newport.com/n/laser-pulse-characterization/)
- RP Photonics, "Gaussian Pulses"
  (https://www.rp-photonics.com/gaussian_pulses.html)
- Light Conversion "Optics Toolbox"
  (https://toolbox.lightcon.com/tools/pulseintensity)

### 1.5 Rayleigh length: `z_R = pi w0^2 / lambda`

**Status: CORRECT**

This is the standard Rayleigh length for a Gaussian beam in vacuum.
Note that the XCALIB paper (Eq. 6) uses a slightly different convention:
z_R1 = (1/(2 ln 2)) pi Delta^2 / lambda, where Delta is the FWHM, which
after substituting w0 = Delta / sqrt(2 ln 2) gives z_R = pi w0^2 / lambda.

**References:**
- Standard Gaussian optics (Saleh & Teich, "Fundamentals of Photonics")
- XCALIB paper (Toyota et al., 2019), Eq. 6
  (arXiv:1808.06066, DOI:10.1107/S1600577519003564)

### 1.6 Peak fluence and photon number

**Status: CORRECT**

The code computes:
- `nPhotons = E_pulse / (photonEnergy_eV * eV_J)` -- correct energy-to-photon conversion
- `fluence_phcm2 = nPhotons / effectiveArea_cm2` -- peak photon fluence at beam center

This gives Phi_0 in photons/cm^2, which is the standard peak fluence for a
Gaussian beam (the fluence at the center, not the average fluence). This
convention matches the XCALIB paper (Eq. 7-8) and is standard in the XFEL
literature.

---

## 2. Eta and Eta-Prime (eta.ts)

### 2.1 eta = sigma_photo * Phi_0

**Status: CORRECT -- standard definition**

The quantity eta = sigma * Phi_0 (photoabsorption cross section times photon
fluence) gives the expected number of photoabsorption events per atom. This is
dimensionally [cm^2] * [photons/cm^2] = [photons absorbed / atom] and is the
fundamental definition used throughout the XFEL radiation damage literature.

Son, Young & Santra (2011) use this relationship implicitly in their rate
equations, where the ionization rate for a given shell is proportional to the
cross section times the instantaneous flux (time-dependent version of the same
relation). The time-integrated version gives eta = sigma * Phi_0.

Neutze et al. (2000) established the key threshold: the conventional damage
barrier corresponds to about 200 photons per Angstrom^2 at 12 keV, which at
a carbon photoabsorption cross section of ~1500 barn gives eta ~ 0.003 photons
per atom -- small enough that diffraction outpaces damage.

**References:**
- Son, Young & Santra, Phys. Rev. A 83, 033402 (2011)
  (DOI:10.1103/PhysRevA.83.033402, arXiv:1101.4932)
- Neutze, Wouts, van der Spoel, Weckert & Hajdu, Nature 406, 752-757 (2000)
  (DOI:10.1038/35021099)
- XCALIB paper (Toyota et al., 2019) -- fluence definition consistent
- Barty et al., Nature Photonics 6, 35-40 (2012) -- uses fluence/dose
  in the same convention (DOI:10.1038/nphoton.2011.297)

### 2.2 eta' = eta_photo * erf(2 sqrt(ln 2) * tau_hole / tau_FWHM) / 2

**Status: CORRECT -- derivable from first principles**

The quantity eta-prime represents the expected number of photoabsorption events
per atom occurring within one core-hole lifetime after a photoionization event
at the pulse peak. This is the worst-case (maximum) value for hollow-atom
formation probability.

**Derivation:**

Consider a Gaussian pulse with instantaneous photon flux:

    j(t) = j_0 exp(-4 ln 2 t^2 / tau^2)

where tau is the FWHM pulse duration. A photoabsorption event at t=0 (pulse
peak) creates a core hole that survives for time tau_hole. The number of
additional photoabsorptions per atom within this window is:

    eta' = sigma_photo * integral_0^{tau_hole} j(t) dt

To evaluate, substitute u = t * 2 sqrt(ln 2) / tau:

    eta' = sigma_photo * j_0 * (tau / (2 sqrt(ln 2))) * integral_0^{x} exp(-u^2) du

where x = 2 sqrt(ln 2) * tau_hole / tau.

Using erf(x) = (2/sqrt(pi)) integral_0^x exp(-u^2) du:

    eta' = sigma_photo * j_0 * (tau / (2 sqrt(ln 2))) * (sqrt(pi)/2) * erf(x)

Since the total fluence is:

    Phi_0 = integral_{-inf}^{inf} j(t) dt = j_0 * tau * sqrt(pi / (4 ln 2))

we get:

    eta' = sigma_photo * Phi_0 * erf(x) / 2 = eta_photo * erf(x) / 2

with x = 2 sqrt(ln 2) * tau_hole / tau_FWHM. **QED.**

**Physical interpretation:** The factor erf(x)/2 is the fraction of the total
pulse fluence delivered in the time window [0, tau_hole] from the peak. As
tau_hole -> infinity, erf -> 1 and eta' -> eta/2 (half the pulse arrives after
the peak). As tau_hole -> 0, eta' -> 0.

**Note on literature:** This exact erf formula does not appear to be published
as a named equation in the primary references (Son et al. 2011, Neutze et al.
2000, Chapman et al. 2011). Those works use full numerical rate-equation
approaches (XATOM toolkit) rather than this closed-form approximation. However,
the formula is a mathematically exact result for the stated assumptions
(constant cross section, Gaussian temporal profile, single-event picture) and
represents the correct analytical limit of the more detailed numerical models.
The approximation breaks down at very high fluence where sequential ionization
changes the cross section (the hollow-atom regime that Son et al. specifically
address), but it is a valid first-order estimate.

### 2.3 Hole lifetime: tau_hole = hbar / Gamma

**Status: CORRECT -- standard Heisenberg relation**

The core-hole lifetime is related to the natural width Gamma (in eV) by the
energy-time uncertainty relation: tau = hbar / Gamma. This is the standard
formula used throughout x-ray spectroscopy and atomic physics.

**References:**
- Campbell & Papp, At. Data Nucl. Data Tables 77, 1-56 (2001) --
  systematic compilation of K and L shell widths
- Krause & Oliver, J. Phys. Chem. Ref. Data 8, 329 (1979) --
  natural widths of atomic K and L levels

### 2.4 Gaussian 2D envelope: `exp(-4 ln 2 (x^2/FWHM_x^2 + y^2/FWHM_y^2))`

**Status: CORRECT**

This is the standard 2D Gaussian expressed in terms of FWHM. Starting from
I(x,y) = I0 exp(-2x^2/w0x^2 - 2y^2/w0y^2) and substituting
w0 = FWHM / sqrt(2 ln 2), we get 2/w0^2 = 4 ln 2 / FWHM^2, confirming
the formula. At (x,y) = (FWHM_x/2, 0) the envelope gives exp(-ln 2) = 0.5,
as required.

### 2.5 Dominant shell selection (largest sigma, ties broken by longest tau_hole)

**Status: PHYSICALLY REASONABLE but simplified**

The shell with the largest photoabsorption cross section is the dominant
ionization channel -- it produces the most core holes per pulse. This is the
standard heuristic for identifying which shell drives radiation damage. Below
an absorption edge, the next-lower shell dominates.

Son, Young & Santra (2011) show that the full picture requires tracking
ionization dynamics across all shells simultaneously, including Auger cascade
effects. The dominant-shell simplification is adequate for a first-order
estimate but may underestimate damage in cases where a shell with smaller
cross section but much longer hole lifetime (lower-Z elements, deeper shells)
accumulates more hollow-atom character.

The code also correctly uses eta_photo (total photoabsorption) rather than
eta_shell for the eta-prime calculation, which is physically appropriate: a
core hole in any shell changes the electronic structure, and the relevant
quantity is the total number of ionization events during the hole lifetime.

---

## 3. Constants

### 3.1 CODATA 2018 exact values

**Status: h, c, eV are CORRECT and exact**

The code uses:
- `h = 6.62607015e-34 J s` -- exact (SI redefinition, 20 May 2019)
- `c = 299792458 m/s` -- exact (since 1983)
- `eV = 1.602176634e-19 J` -- exact (SI redefinition, 20 May 2019)

These match the CODATA 2018 values that became exact with the 2019 SI
redefinition.

**Reference:**
- Tiesinga et al., Rev. Mod. Phys. 93, 025010 (2021)
  (DOI:10.1103/RevModPhys.93.025010)
- NIST CODATA 2018 (https://physics.nist.gov/cuu/pdf/all_2018.pdf)

### 3.2 Reduced Planck constant for hole lifetimes

**Status: MINOR DISCREPANCY (negligible in practice)**

The code uses `HBAR_eV_s = 6.582119514e-16` eV*s.

This is the CODATA **2014** recommended value. The CODATA 2018 exact value,
derived from the now-exact h and eV, is:

    hbar = h / (2 pi) = 6.62607015e-34 / (2 pi) J s
    hbar / eV = 1.054571817e-34 / 1.602176634e-19 = 6.582119569...e-16 eV s

The difference (514 vs 569 in the last three digits) amounts to a relative
error of ~8e-9, which is completely negligible for any practical hole-lifetime
calculation (cross sections and natural widths themselves have uncertainties
of 1-10%).

**Recommendation:** Update to `6.582119569e-16` for internal consistency with
the other CODATA 2018 exact constants, though the physics is unaffected.

---

## 4. Beam Profile Models Used in the XFEL Literature

### 4.1 Gaussian vs. other profiles

The Gaussian beam model is a standard first approximation in the XFEL
literature but is known to be simplified:

- **XCALIB** (Toyota et al., 2019) uses both a Single Gaussian Spatial Profile
  (SGSP) and a Double Gaussian Spatial Profile (DGSP) to model focused XFEL
  beams. The DGSP adds a broader pedestal component to capture the halo/tail
  structure of real focused beams.

- **Ptychographic measurements** of focused XFEL beams show complex wavefront
  structure with speckle-like features, especially at the European XFEL's
  SPB/SFX instrument. A simple Gaussian underestimates the intensity
  fluctuations across the focal plane.

- **Partial coherence** of SASE-FEL beams (transverse coherence ~0.85 at
  European XFEL) means the beam profile fluctuates shot-to-shot.

For a calculator tool, the Gaussian model is appropriate as a baseline
estimate. The code's flat-top option provides an alternative for beams shaped
by apertures or KB mirror systems that produce more uniform profiles.

**References:**
- Toyota et al., J. Synchrotron Rad. 26, 1017-1030 (2019)
  (arXiv:1808.06066) -- SGSP and DGSP models
- Coherence properties from speckle contrast analysis at the European XFEL
  (https://www.researchgate.net/publication/366550562)
- Single-pulse characterization of focal spot via CDI, J. Synchrotron Rad.
  30 (2023) (DOI not retrieved)

### 4.2 Gorkhover and collaborators' beam modeling

Gorkhover's single-particle imaging experiments at LCLS used focused XFEL
beams with parameters:
- Photon energy: 0.5-2 keV (soft X-ray, near Xe M-edge resonances)
- Focal spot: ~1-3 um FWHM (KB mirror focus)
- Pulse energy: ~1-5 mJ
- Pulse duration: 10-100 fs

In Gorkhover et al., Phys. Rev. Lett. 108, 245005 (2012) and Nature Photonics
10, 93-97 (2016), the beam profile is characterized primarily through its
integrated fluence (photons/um^2) rather than an assumed analytic form.

### 4.3 Kuschel's research area

Based on publication searches, Stephan Kuschel's primary research is in
laser-plasma acceleration, proton acceleration from relativistic laser
interactions, and high-field physics (TU Darmstadt / Helmholtz Institute Jena).
His publication record does not appear to include XFEL beam characterization
or single-particle imaging papers. He may be relevant to this project in a
different capacity (e.g., advisor, colleague, or contributor to related laser
optics work).

---

## 5. Typical XFEL Beam Parameters

### 5.1 LCLS (SLAC, USA)

- Photon energy: 0.25-25 keV (hard and soft X-ray)
- Pulse energy: 0.1-4 mJ (energy-dependent)
- Pulse duration: 10-250 fs (typical ~30-50 fs FWHM)
- Focus size: 0.1-10 um FWHM (depending on optics)
- Repetition rate: 120 Hz
- Single-spike attosecond mode: ~200-400 as

Source: LCLS Parameters Run 25-27 (2024-2026),
https://lcls.slac.stanford.edu/

### 5.2 European XFEL (Hamburg, Germany)

- Photon energy: 3-25 keV (SASE1/SASE2)
- Pulse energy: up to 4 mJ
- Pulse duration: ~25 fs FWHM (nominal)
- Focus size: 0.1-1 um (SPB/SFX instrument: 100 nm and 1 um foci)
- Repetition rate: up to 4.5 MHz intratrain, 10 Hz train rate
- Photons per pulse: 10^12-10^13

Source: European XFEL SPB/SFX instrument parameters,
https://www.xfel.eu/facility/instruments/spb_sfx/

### 5.3 Calculator parameter range assessment

The calculator's parameters should comfortably cover:
- Photon energy: 0.1-25 keV
- Pulse energy: 0.001-10 mJ (1 uJ to 10 mJ)
- Pulse duration: 1-300 fs
- Focus size: 50 nm - 50 um FWHM

These ranges encompass the operating space of LCLS, European XFEL, SACLA,
SwissFEL, and PAL-XFEL.

---

## 6. Summary Table

| Formula | Code | Matches literature? | Notes |
|---------|------|-------------------|-------|
| FWHM -> w0 | `FWHM / sqrt(2 ln 2)` | YES | Standard optics |
| Gaussian A_eff | `(pi/2) w0x w0y` | YES | Standard effective area |
| Flat-top A_eff | `(pi/4) FWHMx FWHMy` | YES | Geometric ellipse area |
| Temporal factor | `sqrt(4 ln 2 / pi)` | YES | ~0.9394, confirmed |
| Peak power | `E * f / tau` | YES | Standard Gaussian pulse |
| Peak fluence | `N_photons / A_eff` | YES | Standard convention |
| Rayleigh length | `pi w0^2 / lambda` | YES | Standard Gaussian optics |
| eta | `sigma * Phi_0` | YES | Universal definition |
| eta' (erf form) | `eta * erf(x)/2` | YES | Correct derivation (see 2.2) |
| tau_hole | `hbar / Gamma` | YES | Standard relation |
| 2D envelope | `exp(-4 ln2 ...)` | YES | Consistent with FWHM def |
| h, c, eV | CODATA 2018 exact | YES | Exact post-2019 SI |
| hbar (eta.ts) | `6.582119514e-16` | MINOR | CODATA 2014 value; 2018 = ...569 |

---

## 7. Discrepancies Found

### 7.1 hbar value (cosmetic, not physics-affecting)

`src/lib/eta.ts` line 5 uses `HBAR_eV_s = 6.582119514e-16`, the CODATA 2014
value. The CODATA 2018 exact value is `6.582119569e-16`. Relative difference
~8e-9, negligible for all practical purposes. Recommend updating for
consistency with the CODATA 2018 constants in `constants.ts`.

### 7.2 No other physics discrepancies found

All formulas are either standard textbook results (beam optics, cross section
definitions) or derivable from first principles (the eta-prime erf formula).
The physical assumptions (Gaussian beam, constant cross section during pulse)
are clearly stated limitations that are appropriate for a first-order
calculator tool.

---

## 8. Key References

1. **Son, Young & Santra** (2011), "Impact of hollow-atom formation on
   coherent x-ray scattering at high intensity," Phys. Rev. A 83, 033402.
   DOI:10.1103/PhysRevA.83.033402, arXiv:1101.4932

2. **Neutze, Wouts, van der Spoel, Weckert & Hajdu** (2000), "Potential for
   biomolecular imaging with femtosecond X-ray pulses," Nature 406, 752-757.
   DOI:10.1038/35021099

3. **Chapman et al.** (2011), "Femtosecond X-ray protein nanocrystallography,"
   Nature 470, 73-77. DOI:10.1038/nature09750

4. **Barty et al.** (2012), "Self-terminating diffraction gates femtosecond
   X-ray nanocrystallography measurements," Nature Photonics 6, 35-40.
   DOI:10.1038/nphoton.2011.297

5. **Toyota, Jurek, Son et al.** (2019), "XCALIB: a focal spot calibrator for
   intense X-ray free-electron laser pulses based on the charge state
   distributions of light atoms," J. Synchrotron Rad. 26, 1017-1030.
   DOI:10.1107/S1600577519003564, arXiv:1808.06066

6. **Gorkhover et al.** (2012), "Nanoplasma dynamics of single large xenon
   clusters," Phys. Rev. Lett. 108, 245005.
   DOI:10.1103/PhysRevLett.108.245005

7. **Gorkhover et al.** (2016), "Femtosecond and nanometre visualization of
   structural dynamics in superheated nanoparticles," Nature Photonics 10,
   93-97. DOI:10.1038/nphoton.2015.264

8. **Caleman et al.** (2011), "On the Feasibility of Nanocrystal Imaging Using
   Intense and Ultrashort X-ray Pulses," ACS Nano 5(1), 139-146.
   DOI:10.1021/nn1020693

9. **Tiesinga, Mohr, Newell & Taylor** (2021), "CODATA recommended values of
   the fundamental physical constants: 2018," Rev. Mod. Phys. 93, 025010.
   DOI:10.1103/RevModPhys.93.025010

10. **Hau-Riege et al.** (2007), "Theoretical study of electronic damage in
    single particle imaging experiments at XFELs for pulse durations 0.1-10
    fs," arXiv:1504.07376
