# XFEL Nanofocus Intensity Calculations — Foundations

## Setup

Gaussian X-ray pulse focused by KB mirrors onto a gold sample. Measured inputs: pulse energy $E_\text{pulse}$, photon energy $E_\gamma$, focal spot FWHM (possibly elliptical: $\text{FWHM}_x$, $\text{FWHM}_y$), pulse duration $\tau$ (FWHM). Goal: derive peak intensities in useful units and the number of photon interactions per atom per pulse.

---

## 1. Photon count

$$N_\gamma = \frac{E_\text{pulse}}{E_\gamma}$$

with $E_\gamma$ in Joules ($= E_\text{keV} \times 1.602 \times 10^{-16}$ J).

---

## 2. Gaussian beam conventions

We use the standard optics convention throughout:

$$I(r) = I_0 \, \exp\!\left(-\frac{2r^2}{w_0^2}\right)$$

where $w_0$ is the **1/e² intensity radius** (beam waist). Relation to the experimentally measured FWHM:

$$w_0 = \frac{\text{FWHM}}{\sqrt{2 \ln 2}} \approx \frac{\text{FWHM}}{1.1774}$$

For an **elliptical** beam with independent $\text{FWHM}_x$, $\text{FWHM}_y$ the 2D profile is:

$$I(x,y) = I_0 \, \exp\!\left(-\frac{2x^2}{w_{0x}^2} - \frac{2y^2}{w_{0y}^2}\right)$$

---

## 3. Effective focal area

Integrating the normalised spatial profile over the transverse plane:

$$A_\text{eff} = \frac{\iint I(x,y)\,dx\,dy}{I_0} = \frac{\pi}{2}\,w_{0x}\,w_{0y}$$

Expressed in terms of FWHM:

$$\boxed{A_\text{eff} = \frac{\pi}{4\ln 2}\,\text{FWHM}_x \cdot \text{FWHM}_y \approx 1.1331 \; \text{FWHM}_x \cdot \text{FWHM}_y}$$

For a circular beam ($\text{FWHM}_x = \text{FWHM}_y \equiv d$): $A_\text{eff} = \pi\,d^2 / (4\ln 2)$.

---

## 4. Temporal profile and peak power

Gaussian temporal envelope with FWHM $\tau$:

$$P(t) = P_0 \, \exp\!\left(-4\ln 2 \;\frac{t^2}{\tau^2}\right)$$

The pulse energy is $E_\text{pulse} = \int P(t)\,dt = P_0 \cdot \tau \sqrt{\pi / (4\ln 2)}$, so:

$$\boxed{P_\text{peak} = E_\text{pulse} \cdot \frac{\sqrt{4\ln 2 / \pi}}{\tau} \approx \frac{0.9394 \; E_\text{pulse}}{\tau}}$$

---

## 5. Intensity / irradiance (W/cm²)

Peak on-axis, at pulse centre:

$$\boxed{I_\text{peak} = \frac{P_\text{peak}}{A_\text{eff}} = \frac{E_\text{pulse}}{A_\text{eff}\;\tau} \cdot \sqrt{\frac{4\ln 2}{\pi}}}$$

This is the "power density" in the conventional sense.

---

## 6. Photon fluence (photons/cm²)

The **fluence** is the time-integrated flux — the total photon surface density delivered by the pulse. At beam centre:

$$\boxed{\Phi_0 = \frac{N_\gamma}{A_\text{eff}} = \frac{N_\gamma \cdot 4\ln 2}{\pi \; \text{FWHM}_x \cdot \text{FWHM}_y}}$$

This is the central quantity: it connects directly to per-atom interaction probabilities and is independent of the temporal profile.

---

## 7. Photons per atom per pulse

For a single atom sitting at the beam centre, the expected number of photon interactions per pulse is:

$$\boxed{\eta = \sigma \cdot \Phi_0}$$

where $\sigma$ is the relevant atomic cross section (in the same area units as $\Phi_0$).

Which cross section to use depends on the question:

| quantity | xraylib call | what it counts |
|---|---|---|
| photoabsorption | `CS_Photo(Z, E_keV)` | photoelectric absorption only |
| total attenuation | `CS_Total(Z, E_keV)` | photo + coherent + incoherent scattering |
| specific shell | `CS_Photo_Partial(Z, shell, E_keV)` | e.g. K-shell only |

xraylib returns cross sections in **cm²/g**. Convert to **cm²/atom**:

$$\sigma_\text{atom} = \sigma_\text{cm²/g} \times \frac{A_r}{N_A}$$

where $A_r$ is the atomic weight (g/mol) and $N_A$ is Avogadro's number.

**Physical interpretation:** $\eta < 1$ means most atoms see zero or one photon (linear regime). $\eta \gtrsim 1$ means sequential multi-photon processes become probable — the nonlinear regime.

---

## 8. Summary of unit conversions

Starting from ($E_\text{pulse}$, $E_\gamma$, $\text{FWHM}_x$, $\text{FWHM}_y$, $\tau$):

| Quantity | Formula | Units |
|---|---|---|
| Photon count | $N_\gamma = E_\text{pulse}/E_\gamma$ | photons/pulse |
| Peak power | $P_0 = 0.9394 \; E_\text{pulse}/\tau$ | W |
| Effective area | $A_\text{eff} = \pi\,\text{FWHM}_x\,\text{FWHM}_y\,/\,(4\ln 2)$ | cm² |
| Peak irradiance | $I_0 = P_0 / A_\text{eff}$ | W/cm² |
| Peak fluence | $\Phi_0 = N_\gamma / A_\text{eff}$ | ph/cm²/pulse |
| Peak photon flux | $\dot\Phi_0 = \Phi_0 \times 0.9394/\tau$ | ph/cm²/s |
| Photons per atom | $\eta = \sigma \cdot \Phi_0$ | dimensionless |

---

## 9. Quick sanity check

Parameters: $E_\text{pulse} = 100\;\mu\text{J}$, $E_\gamma = 10\;\text{keV}$, FWHM $= 200\;\text{nm}$ (circular), $\tau = 10\;\text{fs}$.

| Quantity | Value |
|---|---|
| $N_\gamma$ | $6.24 \times 10^{10}$ |
| $A_\text{eff}$ | $4.53 \times 10^{-10}\;\text{cm}^2$ |
| $P_\text{peak}$ | $9.4\;\text{GW}$ |
| $I_\text{peak}$ | $2.1 \times 10^{19}\;\text{W/cm}^2$ |
| $\Phi_0$ | $1.38 \times 10^{20}\;\text{ph/cm}^2$ |
| $\eta$ (Au, $\sigma_\text{photo} \approx 3.8 \times 10^{-20}\;\text{cm}^2$) | $\approx 5.2$ |

Five photons per atom per pulse at 100 µJ — firmly in the nonlinear regime.

---

## 10. Implementation plan

### What to build (Step 1 — this ticket)

A single Python module (or notebook) with a clean function interface:

```
pulse_params = PulseParams(
    E_pulse=100e-6,      # J
    E_photon_keV=10.0,
    fwhm_x=200e-9,       # m
    fwhm_y=200e-9,       # m
    tau=10e-15,           # s
)

result = compute_intensity(pulse_params, element='Au')
# result.N_photons, result.A_eff, result.P_peak,
# result.I_peak_Wcm2, result.fluence_ph_cm2,
# result.eta_photo, result.eta_total, ...
```

**Dependencies:** `numpy`, `scipy.constants`, `xraylib`. Nothing exotic.

**xraylib for cross sections** is the right call — it wraps the Elam/Kissel/EPDL databases and gives you photoabsorption, scattering, and shell-resolved cross sections with one function call. It also handles edge energies, fluorescence yields, and Coster-Kronig coefficients, all of which matter for Step 2.

**Avoid the 3D volumetric approach** from the existing notebooks. For photons-per-atom you only need the 2D fluence. The z-dependence (Rayleigh length, beam divergence) matters if you want to model intensity variation through a thick sample, but that's a separate concern and shouldn't be mixed into the base calculation.

### Possible extras for Step 1

- Plotting: $\eta$ vs $E_\text{pulse}$ for a given focus, showing the linear/nonlinear threshold.
- Tabulate $\eta$ broken down by shell (K, L1, L2, L3, M...) using `CS_Photo_Partial`.
- Show how $I_\text{peak}$ scales across the parameter space (contour plot of focus size vs pulse energy).

### What comes next (Step 2 — nonlinear / conditional probabilities)

Once $\eta > 1$, sequential processes matter. The key questions:

1. **Sequential two-photon absorption.** Given the first photon created a K-hole, what is the modified cross section for the second photon? The atom now has a different electronic configuration — one fewer core electron, shifted edge energy, modified screening. xraylib doesn't cover excited-state cross sections directly, but Hartree-Fock/Dirac calculations or tabulated hollow-atom data can fill in.

2. **Competition with Auger decay.** The K-hole lifetime in Au is ~0.6 fs (width ~1 eV). If $\tau \lesssim 1$ fs, the second photon can arrive before the hole is filled. The relevant figure of merit is $\Gamma_\text{Auger} \cdot \tau$ vs $\eta$. This is where attosecond pulses become essential.

3. **Rate equation / master equation model.** Track populations of ground state, single-hole, double-hole, etc. as a function of time during the pulse. Inputs: ground-state cross sections (xraylib), excited-state cross sections (theory/literature), Auger rates (xraylib `AugerRate` + `FluorYield`), pulse temporal profile.

4. **Bayesian inference on the nonlinear signal.** You already have `nonlinear_bayes.ipynb` doing power-law fits with PyMC. The natural extension: instead of fitting a phenomenological $I^\alpha$, fit the physical rate-equation model to the data and extract the excited-state cross section as a posterior.

### Why Python + xraylib and not Mathematica

- xraylib has a Python API (`import xraylib`), so everything stays in one ecosystem with numpy/scipy/matplotlib.
- The Mathematica notebook `xrl_session_gold.nb` you have works, but Python is more portable, version-controllable, and plays better with Bayesian fitting (PyMC, emcee).
- A clean Python module can be imported from both scripts and Jupyter notebooks without duplication.
- If you need symbolic derivations, sympy handles that within Python (you're already using it).

---

## Notes on what's wrong with the current notebooks

The existing `intensity.ipynb` and `intensity_xrl.ipynb` have two issues worth fixing:

1. **Volumetric flux normalization.** The flux is defined as photons/m³/s with a Rayleigh-length factor in the denominator. This is a 3D photon density, not a fluence. For the photons-per-atom question you want the 2D fluence (photons/cm², integrated over time). The 3D approach would be correct for computing energy deposition in a volume, but it conflates the beam propagation direction with the transverse profile and makes the normalization depend on an assumed $z_R$ even when all you care about is the on-axis intensity.

2. **Using geometric atomic radius.** `calculate_photons_for_atom` multiplies the volumetric flux by $\pi r_\text{Au}^2 \times 1\;\text{Å}$ as an "effective volume." This doesn't correspond to any physical interaction cross section. The correct quantity is $\sigma_\text{photo}$ (or $\sigma_\text{total}$) from xraylib, which already accounts for the quantum-mechanical interaction probability and is typically orders of magnitude different from the geometric area.
