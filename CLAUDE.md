# CLAUDE.md — Lab Tools

## Project Overview

A browser-based dashboard of small, fast scientific calculators and plotting
tools for a crystallography/scattering lab. Built as a learning project in
web development. Target audience: 5-10 scientists who are not coders.

## Tech Stack

- **Svelte 5** — UI framework (components, reactivity)
- **Vite 8** — dev server and build tool
- **TypeScript 6** — typed JavaScript
- **Plotly.js** — interactive scientific plots (to be added)
- Static site — no backend, runs locally from `dist/` or via dev server

## Principles

- Every tool should load instantly and give results as you type/drag
- Prefer fewer tools done well over many half-baked ones
- Design for scientists: label axes, show units, use proper notation
- Code should be readable and well-commented — this is a learning project

## Commands

- `npm run dev` — start dev server (localhost:5173, hot-reload)
- `npm run build` — production build to `dist/`
- `npm run preview` — preview production build locally
- `npm run check` — run Svelte + TypeScript type checking

## Working with This Codebase

- This is a wayfinder-managed project. See docs/.wayfinder/ for the decision map.
- Don't skip ahead — resolve wayfinder tickets in order.
- When in doubt, `/grill-me` before building.

## Agent skills

### Issue tracker

GitHub Issues on rasmbuch/lab_tools. See `docs/agents/issue-tracker.md`.

### Triage labels

Default five-label vocabulary. See `docs/agents/triage-labels.md`.

### Domain docs

Single-context: `CONTEXT.md` at repo root, ADRs in `docs/adr/`. See `docs/agents/domain.md`.
