# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Stack

Svelte 5 + Vite 8 + TypeScript 6 + Plotly.js. Static site (no backend). Decided during grilling session: user has prior Svelte exposure, TypeScript matches their typed-Python style, Plotly handles scientific plots natively.

## Users

5–10 scientists at an XFEL nanofocus beamline. Strong physics background, not coders. Use the tools during experiment planning (office, desktop) and occasionally at the beamline (tablet). They switch between unit systems, estimate whether pulse parameters reach the nonlinear regime, and calculate detector geometry — currently done on paper, in notebooks, or with ad-hoc Python scripts they can't easily share.

## Product Purpose

A browser-based dashboard of small, fast scientific calculators and plotters for a crystallography/scattering lab. Each tool takes measured inputs and returns derived quantities live as you type. The dashboard replaces scattered notebooks and back-of-envelope calculations with something shareable, correct, and pleasant to use. Success: coworkers bookmark it and reach for it instead of opening Python.

## Positioning

Not a general-purpose scientific computing platform. Not a notebook replacement. A curated, opinionated set of tools for this lab's specific workflows — built by someone who uses them, designed for people who don't code. The tools encode domain knowledge (correct cross-section databases, proper Gaussian beam conventions, shell-resolved atomic physics) that a generic unit converter cannot.

## Operating Context

- Experiments at XFEL/synchrotron beamlines: pulse energies (µJ–mJ), photon energies (keV), focal spots (nm), pulse durations (fs–as)
- Planning phase: estimating whether parameters reach nonlinear regime (η > 1)
- Data collection: quick geometry calculations (solid angle, detector coverage)
- Post-experiment: unit conversions for papers and presentations
- Tools are used independently — no workflow between them, no data persistence needed
- Scientists are familiar with the quantities and units; the tools don't need to teach physics

## Capabilities and Constraints

Four tools for v1:
1. **Energy/wavelength converter** — eV, keV, Å, nm, THz, cm⁻¹
2. **Intensity unit converter** — W/cm² ↔ photons/nm² at a given photon energy
3. **η/η′ calculator** — photons per atom per pulse from pulse parameters and element, with interactive plots (η vs energy, focal-plane maps)
4. **Solid angle calculator** — detector area + distance → steradians and fraction of 4π

Constraints:
- Must run locally without a server (static files)
- Must load instantly and update live as inputs change
- Cross sections from xraylib databases (ported to TypeScript for v1)
- No data file upload in v1 — manual input only
- Must not look auto-generated ("AI slop" is an explicit anti-goal)

## Brand Commitments

- Name: Lab Tools (working name, kept intentionally simple)
- Voice: precise but inviting — like good science communication, not a software product
- Design references declared binding by the user: Nolde Museum Seebüll, Seaborn documentation, Frans Hals Museum (see DESIGN.md for detailed analysis)
- Anti-references: Bootstrap/Material dashboards, Grafana, neon "data science" palettes, Streamlit defaults, Jupyter aesthetic, anything that looks templated

## Evidence on Hand

- `docs/xfel_calc.py` — working Python implementation of the η/η′ calculator with shell-resolved cross sections, verified against known-answer test cases
- `docs/xfel_intensity_foundations.md` — full derivation of all formulas with correct Gaussian beam conventions
- `docs/test_intensity_cases.ipynb` — notebook with publication-quality plots (η vs energy, focal-plane maps, cross-section curves)
- No user testimonials, no logo, no existing brand assets

## Product Principles

1. **Curated, not comprehensive.** Fewer tools done well. Each one earns its place by replacing a real workflow pain point.
2. **Live, not submitted.** Results update as you type or drag. No "calculate" buttons, no loading spinners for simple math.
3. **Correct by construction.** Formulas match the derivation document. Cross sections come from established databases. Units are labeled. Axes are named.
4. **Designed, not decorated.** Every visual choice is deliberate. The interface should feel like a well-designed instrument, not a themed template.
5. **Shareable by default.** A colleague can open the same URL and use it immediately. No setup, no accounts, no dependencies.
