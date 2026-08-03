"""
XFEL nanofocus intensity calculator.

Given pulse energy, photon energy, focal spot FWHM, and pulse duration,
computes peak irradiance, photon fluence, and photons-per-atom for a
Gaussian beam and pulse profile.

Cross sections from xraylib (Elam/Kissel/EPDL databases).

Usage:
    from xfel_calc import PulseParams, compute_intensity

    p = PulseParams(E_pulse=100e-6, E_photon_keV=9.7, fwhm_x=200e-9, fwhm_y=200e-9, tau=10e-15)
    r = compute_intensity(p, element='Au')
    print(r)
"""

from dataclasses import dataclass, field
from typing import Optional
import numpy as np
from scipy.special import erf

try:
    import xraylib as xrl
    HAS_XRAYLIB = True
except ImportError:
    HAS_XRAYLIB = False

# ── Constants ────────────────────────────────────────────────────────────────

eV_J = 1.602176634e-19      # J per eV
N_A = 6.02214076e23         # Avogadro
LN2 = np.log(2)             # 0.6931...
GAUSS_TEMPORAL = np.sqrt(4 * LN2 / np.pi)  # ≈ 0.9394
HBAR_eV_s = 6.582119514e-16  # ℏ in eV·s


# ── Data classes ─────────────────────────────────────────────────────────────

@dataclass
class PulseParams:
    """XFEL pulse parameters (all SI)."""
    E_pulse: float        # pulse energy [J]
    E_photon_keV: float   # photon energy [keV]
    fwhm_x: float         # focal spot FWHM in x [m]
    fwhm_y: float         # focal spot FWHM in y [m]
    tau: float             # pulse duration FWHM [s]

    @property
    def E_photon_J(self):
        return self.E_photon_keV * 1e3 * eV_J

    @property
    def N_photons(self):
        return self.E_pulse / self.E_photon_J

    @property
    def fwhm_x_nm(self):
        return self.fwhm_x * 1e9

    @property
    def fwhm_y_nm(self):
        return self.fwhm_y * 1e9

    @property
    def tau_fs(self):
        return self.tau * 1e15

    def summary(self):
        return (f"E_pulse = {self.E_pulse*1e6:.1f} µJ,  "
                f"E_photon = {self.E_photon_keV:.2f} keV,  "
                f"FWHM = {self.fwhm_x_nm:.0f}×{self.fwhm_y_nm:.0f} nm²,  "
                f"τ = {self.tau_fs:.1f} fs")


@dataclass
class HoleInfo:
    """Core-hole properties for one shell."""
    sigma_cm2: float    # partial photoabsorption cross section [cm²/atom]
    edge_keV: float     # absorption edge energy [keV]
    width_eV: float     # natural level width Γ [eV]
    tau_hole_s: float   # hole lifetime ℏ/Γ [s]

    @property
    def tau_hole_fs(self):
        return self.tau_hole_s * 1e15

    @property
    def tau_hole_as(self):
        return self.tau_hole_s * 1e18


@dataclass
class CrossSections:
    """Atomic cross sections [cm²/atom]."""
    sigma_photo: float      # photoelectric absorption
    sigma_rayleigh: float   # coherent (Rayleigh) scattering
    sigma_compton: float    # incoherent (Compton) scattering
    sigma_total: float      # photo + Rayleigh + Compton
    # shell-resolved photoabsorption {shell_name: sigma_cm2}
    shells: dict = field(default_factory=dict)
    # shell-resolved hole info {shell_name: HoleInfo}
    hole_info: dict = field(default_factory=dict)


@dataclass
class IntensityResult:
    """All derived intensity quantities."""
    # Inputs (for reference)
    params: PulseParams
    element: str

    # Photon count
    N_photons: float          # photons per pulse

    # Beam geometry
    A_eff_cm2: float          # effective focal area [cm²]
    w0_x_m: float             # 1/e² beam waist x [m]
    w0_y_m: float             # 1/e² beam waist y [m]

    # Peak quantities
    P_peak_W: float           # peak power [W]
    I_peak_Wcm2: float        # peak irradiance [W/cm²]
    fluence_ph_cm2: float     # peak fluence [ph/cm²/pulse]
    flux_peak_ph_cm2_s: float # peak flux [ph/cm²/s]

    # Cross sections
    cross_sections: CrossSections

    # Photons per atom (integrated over full pulse)
    eta_photo: float          # using photoabsorption σ
    eta_total: float          # using total σ

    # η' (sequential absorption parameter)
    # Uses the longest M-hole lifetime (typically M5) since shorter M-holes
    # Auger-decay into M4/M5 and thus effectively feed the same channel.
    # η' = η_photo × erf(2√ln2 × τ_hole / τ_pulse) / 2
    eta_prime_val: float = 0.0        # scalar — the physically relevant η'
    eta_prime_shell: str = ''         # which shell was used (e.g. 'M5')
    eta_prime_tau_as: float = 0.0     # lifetime of that shell [as]
    # Per-shell dict kept for reference / detailed tables
    eta_prime: dict = field(default_factory=dict)

    def __repr__(self):
        lines = [
            f"═══ XFEL Intensity: {self.element} at {self.params.E_photon_keV:.2f} keV ═══",
            f"  {self.params.summary()}",
            f"",
            f"  N_photons        = {self.N_photons:.3e}",
            f"  A_eff            = {self.A_eff_cm2:.3e} cm²",
            f"  P_peak           = {self.P_peak_W:.3e} W  ({self.P_peak_W/1e9:.2f} GW)",
            f"  I_peak           = {self.I_peak_Wcm2:.3e} W/cm²",
            f"  Φ₀ (fluence)     = {self.fluence_ph_cm2:.3e} ph/cm²",
            f"  Φ̇₀ (peak flux)   = {self.flux_peak_ph_cm2_s:.3e} ph/cm²/s",
            f"",
            f"  σ_photo          = {self.cross_sections.sigma_photo:.3e} cm²/atom"
            f"  ({self.cross_sections.sigma_photo*1e24:.0f} barn)",
            f"  σ_total          = {self.cross_sections.sigma_total:.3e} cm²/atom",
            f"",
            f"  η (photo)        = {self.eta_photo:.3f} ph/atom/pulse",
            f"  η (total)        = {self.eta_total:.3f} ph/atom/pulse",
            f"  η′ ({self.eta_prime_shell}, τ={self.eta_prime_tau_as:.0f} as)"
            f"  = {self.eta_prime_val:.4f}",
        ]
        if self.cross_sections.hole_info:
            lines.append(f"")
            lines.append(f"  Shell-resolved (with hole lifetimes):")
            lines.append(f"  {'shell':>5s}  {'σ (barn)':>10s}  {'η':>8s}  "
                         f"{'Γ (eV)':>8s}  {'τ_hole (as)':>12s}  {'η′':>10s}  {'τ_hole/τ':>10s}")
            tau_pulse = self.params.tau
            for shell in sorted(self.cross_sections.hole_info.keys()):
                hi = self.cross_sections.hole_info[shell]
                eta_shell = hi.sigma_cm2 * self.fluence_ph_cm2
                ep = self.eta_prime.get(shell, 0)
                ratio = hi.tau_hole_s / tau_pulse
                lines.append(
                    f"    {shell:>3s}  {hi.sigma_cm2*1e24:10.0f}  {eta_shell:8.4f}  "
                    f"{hi.width_eV:8.1f}  {hi.tau_hole_as:12.1f}  {ep:10.6f}  {ratio:10.2e}"
                )
        elif self.cross_sections.shells:
            lines.append(f"")
            lines.append(f"  Shell-resolved photoabsorption:")
            for shell, sigma in sorted(self.cross_sections.shells.items()):
                eta_shell = sigma * self.fluence_ph_cm2
                lines.append(f"    {shell:>3s}: σ = {sigma:.3e} cm²  →  η = {eta_shell:.4f}")
        return "\n".join(lines)


# ── Cross section retrieval ──────────────────────────────────────────────────

# Shell constants for xraylib
_SHELLS = [
    ('K',  'K_SHELL'),
    ('L1', 'L1_SHELL'), ('L2', 'L2_SHELL'), ('L3', 'L3_SHELL'),
    ('M1', 'M1_SHELL'), ('M2', 'M2_SHELL'), ('M3', 'M3_SHELL'),
    ('M4', 'M4_SHELL'), ('M5', 'M5_SHELL'),
    ('N1', 'N1_SHELL'), ('N2', 'N2_SHELL'), ('N3', 'N3_SHELL'),
    ('N4', 'N4_SHELL'), ('N5', 'N5_SHELL'),
]


def get_cross_sections(element: str, E_keV: float) -> CrossSections:
    """
    Retrieve atomic cross sections from xraylib.

    Parameters
    ----------
    element : str
        Element symbol, e.g. 'Au', 'Fe', 'Cu'.
    E_keV : float
        Photon energy in keV.

    Returns
    -------
    CrossSections with values in cm²/atom.
    """
    if not HAS_XRAYLIB:
        raise ImportError(
            "xraylib is required for cross sections. "
            "Install with: pip install xraylib"
        )

    Z = xrl.SymbolToAtomicNumber(element)
    A_r = xrl.AtomicWeight(Z)
    to_atom = A_r / N_A  # cm²/g → cm²/atom

    sigma_photo = xrl.CS_Photo(Z, E_keV) * to_atom
    sigma_rayl = xrl.CS_Rayl(Z, E_keV) * to_atom
    sigma_compt = xrl.CS_Compt(Z, E_keV) * to_atom
    sigma_total = xrl.CS_Total(Z, E_keV) * to_atom

    # Shell-resolved with hole lifetimes
    shells = {}
    hole_info = {}
    for name, attr in _SHELLS:
        shell_const = getattr(xrl, attr)
        try:
            edge_E = xrl.EdgeEnergy(Z, shell_const)
            if E_keV >= edge_E:
                cs = xrl.CS_Photo_Partial(Z, shell_const, E_keV) * to_atom
                if cs > 0:
                    shells[name] = cs
                    # Level width → hole lifetime
                    # NOTE: xraylib returns width in keV, convert to eV
                    try:
                        width_keV = xrl.AtomicLevelWidth(Z, shell_const)
                        width_eV = width_keV * 1e3
                        tau_hole = HBAR_eV_s / width_eV if width_eV > 0 else np.inf
                    except (ValueError, RuntimeError):
                        width_eV = 0.0
                        tau_hole = np.inf
                    hole_info[name] = HoleInfo(
                        sigma_cm2=cs,
                        edge_keV=edge_E,
                        width_eV=width_eV,
                        tau_hole_s=tau_hole,
                    )
        except (ValueError, RuntimeError):
            continue

    return CrossSections(
        sigma_photo=sigma_photo,
        sigma_rayleigh=sigma_rayl,
        sigma_compton=sigma_compt,
        sigma_total=sigma_total,
        shells=shells,
        hole_info=hole_info,
    )


# ── Main calculation ─────────────────────────────────────────────────────────

def compute_intensity(params: PulseParams, element: str = 'Au') -> IntensityResult:
    """
    Compute peak intensity quantities and photons-per-atom for a
    Gaussian XFEL nanofocus pulse.

    All formulas assume a 2D Gaussian spatial profile and 1D Gaussian
    temporal profile. See xfel_intensity_foundations.md for derivations.

    Parameters
    ----------
    params : PulseParams
        Pulse energy, photon energy, focal FWHMs, pulse duration.
    element : str
        Element symbol for cross-section lookup.

    Returns
    -------
    IntensityResult with all derived quantities.
    """
    p = params

    # Photon count
    N_ph = p.N_photons

    # Beam waists (1/e² radius)
    w0_x = p.fwhm_x / np.sqrt(2 * LN2)
    w0_y = p.fwhm_y / np.sqrt(2 * LN2)

    # Effective area: A_eff = (π/2) * w0x * w0y = π * FWHMx * FWHMy / (4 ln2)
    A_eff_m2 = (np.pi / 2) * w0_x * w0_y
    A_eff_cm2 = A_eff_m2 * 1e4  # m² → cm²

    # Peak power: P_peak = E_pulse * sqrt(4 ln2 / π) / τ
    P_peak = p.E_pulse * GAUSS_TEMPORAL / p.tau

    # Peak irradiance
    I_peak = P_peak / A_eff_cm2  # W/cm²

    # Peak fluence (photons/cm² integrated over pulse)
    fluence = N_ph / A_eff_cm2

    # Peak instantaneous flux (photons/cm²/s at t=0)
    flux_peak = fluence * GAUSS_TEMPORAL / p.tau

    # Cross sections
    cs = get_cross_sections(element, p.E_photon_keV)

    # Photons per atom (integrated over full pulse)
    eta_photo = cs.sigma_photo * fluence
    eta_total = cs.sigma_total * fluence

    # η' per shell (for reference)
    # η'_i = η_photo × erf(2√ln2 × τ_hole_i / τ) / 2
    # Integrates σ_photo × Φ̇(t) from t=0 over hole lifetime assuming
    # hole created at pulse peak. Caps at η/2.
    eta_prime = {}
    for name, hi in cs.hole_info.items():
        x = 2 * np.sqrt(LN2) * hi.tau_hole_s / p.tau
        eta_prime[name] = eta_photo * erf(x) / 2

    # Scalar η': use the longest M-hole (physically dominant — shorter
    # M-holes Auger-decay into M4/M5, feeding the same channel).
    m_holes = {n: hi for n, hi in cs.hole_info.items() if n.startswith('M')}
    if m_holes:
        dom_name = max(m_holes, key=lambda n: m_holes[n].tau_hole_s)
        dom_hi = m_holes[dom_name]
        eta_prime_val = eta_prime[dom_name]
        eta_prime_shell = dom_name
        eta_prime_tau_as = dom_hi.tau_hole_as
    else:
        # Fallback: longest hole of any shell
        dom_name = max(cs.hole_info, key=lambda n: cs.hole_info[n].tau_hole_s,
                       default='')
        eta_prime_val = eta_prime.get(dom_name, 0.0)
        eta_prime_shell = dom_name
        eta_prime_tau_as = (cs.hole_info[dom_name].tau_hole_as
                           if dom_name else 0.0)

    return IntensityResult(
        params=p,
        element=element,
        N_photons=N_ph,
        A_eff_cm2=A_eff_cm2,
        w0_x_m=w0_x,
        w0_y_m=w0_y,
        P_peak_W=P_peak,
        I_peak_Wcm2=I_peak,
        fluence_ph_cm2=fluence,
        flux_peak_ph_cm2_s=flux_peak,
        cross_sections=cs,
        eta_photo=eta_photo,
        eta_total=eta_total,
        eta_prime_val=eta_prime_val,
        eta_prime_shell=eta_prime_shell,
        eta_prime_tau_as=eta_prime_tau_as,
        eta_prime=eta_prime,
    )


# ── Convenience ──────────────────────────────────────────────────────────────

def quick(E_pulse_uJ: float, E_keV: float = 9.7,
          fwhm_nm: float = 200.0, tau_fs: float = 10.0,
          element: str = 'Au',
          fwhm_y_nm: Optional[float] = None) -> IntensityResult:
    """
    Shorthand with practical units.

    Parameters
    ----------
    E_pulse_uJ : float   Pulse energy in µJ.
    E_keV : float         Photon energy in keV.
    fwhm_nm : float       Focal FWHM in nm (used for x, and y if fwhm_y_nm is None).
    tau_fs : float         Pulse duration FWHM in fs.
    element : str          Element symbol.
    fwhm_y_nm : float     If given, use elliptical beam with this y-FWHM in nm.
    """
    fy = fwhm_y_nm if fwhm_y_nm is not None else fwhm_nm
    p = PulseParams(
        E_pulse=E_pulse_uJ * 1e-6,
        E_photon_keV=E_keV,
        fwhm_x=fwhm_nm * 1e-9,
        fwhm_y=fy * 1e-9,
        tau=tau_fs * 1e-15,
    )
    return compute_intensity(p, element)


# ── Spatial profile helpers ──────────────────────────────────────────────────

def fluence_map(params: PulseParams, element: str = 'Au',
                extent_nm: float = 500, n_pts: int = 201):
    """
    Return 2D arrays of fluence, eta, and eta_prime over the focal plane.

    Returns
    -------
    x_nm, y_nm : 1D arrays [nm]
    fluence_2d : 2D array [ph/cm²]
    eta_2d : 2D array [ph/atom]
    eta_prime_2d : 2D array [ph/atom within dominant M-hole lifetime]
    """
    r = compute_intensity(params, element)
    x_nm = np.linspace(-extent_nm, extent_nm, n_pts)
    y_nm = np.linspace(-extent_nm, extent_nm, n_pts)
    X, Y = np.meshgrid(x_nm, y_nm)

    # Gaussian envelope: exp(-4 ln2 (x²/FWHMx² + y²/FWHMy²))
    fx = params.fwhm_x * 1e9  # nm
    fy = params.fwhm_y * 1e9
    envelope = np.exp(-4 * LN2 * (X**2 / fx**2 + Y**2 / fy**2))

    fluence_2d = r.fluence_ph_cm2 * envelope
    eta_2d = r.cross_sections.sigma_photo * fluence_2d
    # η' scales same as η (same spatial profile, just different peak value)
    eta_prime_2d = (r.eta_prime_val / r.eta_photo) * eta_2d if r.eta_photo > 0 else eta_2d * 0

    return x_nm, y_nm, fluence_2d, eta_2d, eta_prime_2d


# ── Threshold colormap ──────────────────────────────────────────────────────

def threshold_cmap(vmin, vmax, threshold=1.0, base='viridis', n=256):
    """
    Colormap that desaturates to grey below `threshold`.

    Below the threshold the colours are replaced by their luminance
    (grayscale), so the spatial structure is preserved but the
    nonlinear regime (≥ threshold) visually "lights up" in colour.

    Parameters
    ----------
    base : str or Colormap
        Base colormap name (default 'viridis').

    Returns (cmap, norm) ready for pcolormesh / imshow.
    """
    import matplotlib.pyplot as plt
    import matplotlib.colors as mcolors

    norm = mcolors.Normalize(vmin=vmin, vmax=vmax)
    if isinstance(base, str):
        base = plt.colormaps[base]
    raw = base(np.linspace(0, 1, n))  # (n, 4) RGBA

    # Fraction of the map that falls below threshold
    frac = np.clip((threshold - vmin) / (vmax - vmin), 0, 1)
    cut = int(frac * n)

    # Desaturate the lower portion: ITU-R BT.601 luminance
    for i in range(cut):
        lum = 0.299 * raw[i, 0] + 0.587 * raw[i, 1] + 0.114 * raw[i, 2]
        raw[i, :3] = lum

    return mcolors.ListedColormap(raw), norm


# Keep old name as alias for backwards compat
threshold_coolwarm = threshold_cmap


# ── Publication plot style ──────────────────────────────────────────────────

# Petroff (2021) 10-color cycle — optimised for colour-vision deficiency
PETROFF10 = [
    '#3f90da', '#ffa90e', '#bd1f01', '#94a4a2', '#832db6',
    '#a96b59', '#e76300', '#b9ac70', '#717581', '#92dadd',
]

# Global save flag — set to True in a notebook to write PNGs
SAVE = False

# A4 text width ≈ 160 mm ≈ 6.3 in (25 mm margins each side)
FIG_SINGLE = (6.3, 3.9)    # single panel
FIG_DOUBLE = (6.3, 7.0)    # two-row panel
FIG_WIDE   = (6.3, 3.2)    # wide / shallow

# Font sizes (pt) — readable at A4 print size
FS_TITLE  = 11
FS_LABEL  = 10
FS_TICK   = 9
FS_LEGEND = 9
FS_ANNOT  = 8


def set_plot_style():
    """Apply publication-ready matplotlib defaults (call once per notebook)."""
    import matplotlib.pyplot as plt
    from cycler import cycler

    # Retina / HiDPI rendering in Jupyter / PyCharm notebooks
    try:
        from matplotlib_inline.backend_inline import set_matplotlib_formats
        set_matplotlib_formats('retina')
    except ImportError:
        try:
            from IPython.display import set_matplotlib_formats
            set_matplotlib_formats('retina')
        except (ImportError, NameError):
            pass

    plt.style.use('petroff10')
    plt.rcParams.update({
        # colour cycle (explicit, in case style sheet is absent)
        'axes.prop_cycle': cycler('color', PETROFF10),
        # figure — force white background regardless of IDE dark mode
        'figure.figsize': FIG_SINGLE,
        'figure.dpi': 150,
        'figure.facecolor': 'white',
        'figure.edgecolor': 'white',
        'savefig.dpi': 300,
        'savefig.bbox': 'tight',
        'savefig.pad_inches': 0.05,
        'savefig.facecolor': 'white',
        # fonts
        'font.size': FS_TICK,
        'axes.titlesize': FS_TITLE,
        'axes.labelsize': FS_LABEL,
        'xtick.labelsize': FS_TICK,
        'ytick.labelsize': FS_TICK,
        'legend.fontsize': FS_LEGEND,
        # axes — light background, dark edges
        'axes.facecolor': '#f8f8f8',
        'axes.edgecolor': '#333333',
        'axes.labelcolor': '#222222',
        'axes.linewidth': 0.8,
        'axes.grid': False,
        #'grid.alpha': 0.30,
        #'grid.linewidth': 0.5,
        # tick colours (force dark for dark-mode IDE)
        'xtick.color': '#333333',
        'ytick.color': '#333333',
        'xtick.direction': 'in',
        'ytick.direction': 'in',
        'xtick.major.size': 4,
        'ytick.major.size': 4,
        'xtick.minor.size': 2,
        'ytick.minor.size': 2,
        'xtick.top': True,
        'ytick.right': True,
        # text colour
        'text.color': '#222222',
        # lines
        'lines.linewidth': 1.5,
        'lines.markersize': 5,
        # legend
        'legend.framealpha': 0.9,
        'legend.edgecolor': '#cccccc',
        'legend.facecolor': 'white',
    })


IMG_DIR = 'images'

def savefig(fig, name, **kwargs):
    """Save figure to IMG_DIR/ if SAVE is True.  `name` without extension → .png."""
    import sys
    # Read SAVE from the live module object so `xfel_calc.SAVE = True` works
    _mod = sys.modules[__name__]
    if not getattr(_mod, 'SAVE', False):
        return
    import os
    img_dir = getattr(_mod, 'IMG_DIR', 'images')
    os.makedirs(img_dir, exist_ok=True)
    if not os.path.splitext(name)[1]:
        name += '.png'
    path = os.path.join(img_dir, name)
    fig.savefig(path, **kwargs)
    print(f'Saved: {path}')


if __name__ == '__main__':
    # Quick demo
    r = quick(100, E_keV=9.7, fwhm_nm=200, tau_fs=10)
    print(r)
