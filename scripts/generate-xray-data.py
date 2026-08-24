#!/usr/bin/env python3
"""
Generate static JSON cross-section data for the lab-tools dashboard.

Requires: xraylib, numpy

Outputs one JSON file per element to src/lib/data/xray-{symbol}.json.
The energy grid is adaptive: log-spaced baseline with extra points
around each absorption edge.
"""

import json
import math
import os
import sys

import numpy as np
import xraylib as xrl

ELEMENTS = ["H", "C", "O", "Ne", "Xe", "Fe", "Cu", "Au", "Pt"]

E_MIN_KEV = 0.1
E_MAX_KEV = 100.0
N_COARSE = 500
N_EDGE_POINTS = 50
EDGE_WINDOW_FRAC = 0.02  # ± 2% around each edge

N_A = 6.02214076e23

SHELLS = [
    ("K",  xrl.K_SHELL),
    ("L1", xrl.L1_SHELL), ("L2", xrl.L2_SHELL), ("L3", xrl.L3_SHELL),
    ("M1", xrl.M1_SHELL), ("M2", xrl.M2_SHELL), ("M3", xrl.M3_SHELL),
    ("M4", xrl.M4_SHELL), ("M5", xrl.M5_SHELL),
    ("N1", xrl.N1_SHELL), ("N2", xrl.N2_SHELL), ("N3", xrl.N3_SHELL),
    ("N4", xrl.N4_SHELL), ("N5", xrl.N5_SHELL),
]

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "src", "lib", "data")


def build_energy_grid(Z: int) -> np.ndarray:
    coarse = np.geomspace(E_MIN_KEV, E_MAX_KEV, N_COARSE)
    extra = []
    for _, shell_const in SHELLS:
        try:
            edge = xrl.EdgeEnergy(Z, shell_const)
        except (ValueError, RuntimeError):
            continue
        if edge < E_MIN_KEV or edge > E_MAX_KEV:
            continue
        lo = edge * (1 - EDGE_WINDOW_FRAC)
        hi = edge * (1 + EDGE_WINDOW_FRAC)
        lo = max(lo, E_MIN_KEV)
        hi = min(hi, E_MAX_KEV)
        extra.append(np.linspace(lo, hi, N_EDGE_POINTS))

    if extra:
        grid = np.concatenate([coarse] + extra)
    else:
        grid = coarse

    grid = np.unique(grid)
    grid.sort()
    return grid


def get_shell_info(Z: int) -> dict:
    shells = {}
    for name, shell_const in SHELLS:
        try:
            edge = xrl.EdgeEnergy(Z, shell_const)
        except (ValueError, RuntimeError):
            continue
        if edge <= 0:
            continue
        try:
            width_keV = xrl.AtomicLevelWidth(Z, shell_const)
            width_eV = width_keV * 1e3
        except (ValueError, RuntimeError):
            width_eV = 0.0
        shells[name] = {
            "edge_keV": round(edge, 6),
            "width_eV": round(width_eV, 4),
        }
    return shells


def generate_element(symbol: str) -> dict:
    Z = xrl.SymbolToAtomicNumber(symbol)
    A_r = xrl.AtomicWeight(Z)
    to_atom = A_r / N_A

    grid = build_energy_grid(Z)
    shell_info = get_shell_info(Z)

    sigma_photo = np.zeros(len(grid))
    sigma_rayleigh = np.zeros(len(grid))
    sigma_compton = np.zeros(len(grid))
    sigma_total = np.zeros(len(grid))

    shell_arrays: dict[str, np.ndarray] = {}
    for name in shell_info:
        shell_arrays[name] = np.zeros(len(grid))

    for i, E in enumerate(grid):
        try:
            sigma_photo[i] = xrl.CS_Photo(Z, float(E)) * to_atom
        except (ValueError, RuntimeError):
            pass
        try:
            sigma_rayleigh[i] = xrl.CS_Rayl(Z, float(E)) * to_atom
        except (ValueError, RuntimeError):
            pass
        try:
            sigma_compton[i] = xrl.CS_Compt(Z, float(E)) * to_atom
        except (ValueError, RuntimeError):
            pass
        try:
            sigma_total[i] = xrl.CS_Total(Z, float(E)) * to_atom
        except (ValueError, RuntimeError):
            pass

        for name, shell_const in SHELLS:
            if name not in shell_info:
                continue
            edge = shell_info[name]["edge_keV"]
            if float(E) < edge:
                continue
            try:
                cs = xrl.CS_Photo_Partial(Z, shell_const, float(E)) * to_atom
                if cs > 0:
                    shell_arrays[name][i] = cs
            except (ValueError, RuntimeError):
                pass

    def to_list(arr: np.ndarray) -> list:
        return [float(f"{v:.6e}") for v in arr]

    sigma_shells_out = {}
    for name, arr in shell_arrays.items():
        if np.any(arr > 0):
            sigma_shells_out[name] = to_list(arr)

    return {
        "element": symbol,
        "Z": Z,
        "A_r": round(A_r, 4),
        "shells": shell_info,
        "grid": {
            "energy_keV": to_list(grid),
            "sigma_photo": to_list(sigma_photo),
            "sigma_rayleigh": to_list(sigma_rayleigh),
            "sigma_compton": to_list(sigma_compton),
            "sigma_total": to_list(sigma_total),
            "sigma_shells": sigma_shells_out,
        },
    }


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    for symbol in ELEMENTS:
        print(f"Generating {symbol}...", end=" ", flush=True)
        data = generate_element(symbol)
        n_points = len(data["grid"]["energy_keV"])
        n_shells = len(data["grid"]["sigma_shells"])

        path = os.path.join(OUTPUT_DIR, f"xray-{symbol}.json")
        with open(path, "w") as f:
            json.dump(data, f, separators=(",", ":"))

        size_kb = os.path.getsize(path) / 1024
        print(f"{n_points} points, {n_shells} shells, {size_kb:.0f} KB")

    print("\nDone.")


if __name__ == "__main__":
    main()
