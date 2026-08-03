# DESIGN.md — Lab Tools Visual Identity

> This file captures the design direction for the lab-tools dashboard.
> Created from PR's reference sites. Feed this to `/impeccable init` and
> `/impeccable polish` in Claude Code CLI.

## References

1. **Nolde Museum Seebüll** (https://nolde-museum.de/)
2. **Seaborn documentation** (https://seaborn.pydata.org/)
3. **Frans Hals Museum** (https://franshalsmuseum.nl/en)

## What I Like About Each

### Nolde Museum
- Full-bleed hero images that command attention
- Warm, expressive color palette (amber, teal, deep reds from the paintings)
- Generous white space — content breathes
- Elegant serif + sans-serif type pairing
- Structured grid that feels organic, not corporate
- Bilingual nav handled cleanly (DE/DA/EN toggle)
- The site feels like the art it houses — not a generic CMS template

### Seaborn
- Gallery of thumbnails that preview what the tool does — show, don't tell
- Clean white background, content is the star
- Minimal navigation — not overwhelming for a tool/reference site
- Professional but approachable — science that doesn't feel cold
- Good example of how to present data visualization tools

### Frans Hals Museum
- Bold, modern museum identity — large sans-serif logo/wordmark
- Horizontal scrolling collection gallery — elegant for browsing items
- Muted colors with strong black accents
- Hero image with overlaid text — confident, not busy
- Cards with hover states for collection items
- Responsive layout that still feels intentional on mobile

## Design Principles for Lab Tools

Derived from the references:

1. **Gallery, not grid.** Show what each tool does with a visual preview,
   like Seaborn's thumbnail gallery — a mini-plot or calculation result,
   not just a title and description.

2. **Museum-quality spacing.** Generous margins and padding. White space is
   not wasted space — it's what makes the tools feel curated rather than
   crammed.

3. **Warm scientific.** Not cold corporate blue. Not neon dashboard. Think
   Nolde's palette: warm amber, teal, earthy tones. The tools handle
   hard science, but the interface should feel inviting.

4. **Typography that reads.** A clean sans-serif for UI elements, optionally
   a serif for headings or hero text (the Nolde/Frans Hals museum approach).
   Proper typographic scale — not everything the same size.

5. **Show the output.** Each tool's card on the dashboard should preview its
   result — an interactive mini-plot, a formula rendering, a sample output.
   Like the museum showing a painting thumbnail, not just the title.

6. **Confident simplicity.** Frans Hals Museum's black-and-white confidence.
   Don't overdesign. Let the science speak. One clear action per screen.

## Anti-References (What We DON'T Want)

- Generic Bootstrap/Material UI dashboards
- Grafana-style data-dense panels with tiny text
- Bright neon "data science" color schemes
- Cookie-cutter SaaS landing pages
- Jupyter notebook aesthetic in the browser
- "Made with Streamlit" default styling
- Anything that looks auto-generated

## Color Direction

| Role | Feeling | Reference |
|------|---------|-----------|
| Background | Warm white / off-white | Nolde Museum's clean backdrop |
| Primary | Deep teal or petrol blue | Nolde's painting backgrounds |
| Accent | Warm amber / golden | Nolde's sunflower palette |
| Text | Near-black, not pure #000 | Frans Hals Museum typography |
| Muted | Warm grey | Seaborn's understated palette |
| Error/warning | Burnt sienna | Expressionist warmth, not harsh red |

## Typography Direction

- **Headings**: Something with character — a serif or a distinctive sans-serif.
  Not generic system fonts.
- **Body/UI**: Clean, readable sans-serif. Good at small sizes for axis labels
  and data.
- **Monospace**: For displaying calculated values — something that looks
  intentional, not default Courier.

## Layout Direction

- Dashboard: card grid with tool previews (2-3 columns on desktop)
- Tool view: full-width, inputs on left/top, output (plot/result) dominant
- Navigation: minimal — sidebar or top bar, not both
- Mobile: stacked cards, tools still usable on tablet at the beamline

## Notes for Impeccable

When running `/impeccable init` in Claude Code, feed it:
- Audience: scientists, non-coders, 5-10 people
- Brand lane: "museum for scientific tools" — curated, warm, confident
- Anti-references: see list above
- Voice: precise but inviting, like good science communication
