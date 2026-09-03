# papers/ — the reference shelf

One index, one nomenclature. If a paper is not in this table it is not on the shelf.

## Nomenclature

    <lead-author(s)>-<short-title>.<ext>

- **lowercase, hyphenated, ASCII** (ö → oe, no underscores, no spaces).
- **≤2 authors:** all surnames (`schoeneberg-vacher-…`, `battey-pratt-racey-…`).
- **≥3 authors:** first surname + `et-al` (`kopp-et-al-…`). Disambiguate colliding surnames with a second token (`li-kaisheng-…` vs `li-sparveris-et-al-…`).
- **Collaboration papers:** the collaboration (`besiii-…`).
- **Short title:** the title's load-bearing words, articles dropped. Not the arXiv number, not the journal's file id.
- **The `.pdf` and `.md` share a basename.** `pdf/x.pdf` ↔ `md/x.md`. That is the whole conversion-tracking mechanism: `ls md/` answers "have I converted it."
- **Reading notes** are `md/<basename>-notes.md`. Scans that need OCR carry `-scan-<year>`.
- Datasets go in `data/`, named by their source (`ame2020-…`), never by what we happened to use them for.

## Index

| basename | authors | title · venue · year | pdf | md | notes |
|---|---|---|---|---|---|
| `battey-pratt-racey-geometric-model-for-fundamental-particles` | E. P. Battey-Pratt, T. J. Racey | Geometric Model for Fundamental Particles · Int. J. Theor. Phys. 19(6) · 1980 | ✅ | ✅ | `-notes.md` ✅ — the spine's BP&R anchor; also a 2008 Xerox **scan** (20 pp, image-only, no text layer) kept as `…-scan-2008.pdf` — superseded by the text PDF, OCR only if the scan has pages the text PDF lacks |
| `li-kaisheng-classical-spiral-orbit-model-h2` | Kaisheng Li | A Classical Spiral Orbit Model for Molecular Spectra and Electron Spin: Applications to H₂ · independent · Apr 2025 | ✅ | ✅ | cited in the Φ review as "Li (2025)" |
| `li-sparveris-et-al-measured-proton-electromagnetic-structure` | R. Li, N. Sparveris, et al. (JLab) | Measured proton electromagnetic structure deviates from theoretical predictions · arXiv:2210.11461 · 2022 | ✅ | ☐ | proton form-factor anomaly — relevant to the capsid charge-radius coupling (`capsid_audit` §2.3) |
| `besiii-oscillating-features-electromagnetic-structure-neutron` | BESIII Collaboration (Ablikim et al.) | Oscillating features in the electromagnetic structure of the neutron (arXiv title: *New Features…*) · arXiv:2103.12486 / Nat. Phys. · 2021 | ✅ | ☐ | neutron form-factor oscillations — the neutron's own "orbit" fingerprint |
| `kopp-et-al-magnetic-moments-astrophysical-neutrinos` | J. Kopp, T. Opferkuch, E. Wang | Magnetic Moments of Astrophysical Neutrinos · arXiv:2212.11287v3 · 2024 | ✅ | ☐ | n=1 neutrino as the sole primitive ⇒ its moment is a first-class prediction target |
| `schoeneberg-vacher-mass-effect-electron-mass-variations-cosmology` | N. Schöneberg, L. Vacher | The mass effect — variations of the electron mass and their impact on cosmology · JCAP03(2025)004 · 2025 | ✅ | ☐ | if m_e is medium-set (ℏ as stiffness), varying-m_e cosmology is a live constraint channel |
| `sen-of-mass-charge-and-spin` | D. Sen | Of Mass, Charge and Spin, the Basic Attributes of Matter — Their Physical Origin · Horizons in World Physics 275, ch. 9 · 2011 | ✅ | ☐ | the orthodox review of exactly the three things §17.2 says must be derived |
| `blokker-et-al-chemical-bond-atom-size-vs-electronegativity` | E. Blokker, …, F. M. Bickelhaupt | The Chemical Bond: When Atom Size Instead of Electronegativity Difference Determines Trend in Bond Strength · Chem. Eur. J. 27, 15616 · 2021 | ✅ | ☐ | size-over-electronegativity — geometry beating a dial, one floor up |
| `swart-soccer-ball-symmetry` | David Swart | Soccer Ball Symmetry · Bridges 2015 · 2015 | ✅ | ☐ | truncated-icosahedron / capsid geometry reference |
| `xu-et-al-11-teraflops-photonic-convolutional-accelerator` | X. Xu, …, D. J. Moss (Swinburne) | 11 TOPS photonic convolutional accelerator for optical neural networks · Nature 589 · 2021 | ✅ | ☐ | analogue compute-in-place, silicon-photonic — FUBIT-adjacent, not physics-spine |
| `schrodinger-what-is-life-mind-and-matter` | E. Schrödinger (fwd. R. Penrose) | What is Life? · Mind and Matter · Autobiographical Sketches · CUP | ✅ | ☐ | the estate's namesake shelf; Axiom I is a descendant of the aperiodic-crystal chapter |

**Conversion status: 2 of 11 converted.** ☐ = `pdf/` only. Convert in the order the spine needs them: Sen → Kopp → Li/Sparveris → BESIII → Schöneberg-Vacher; the rest as they come up.

## Cited but not on the shelf

- **"Helland et al. (2026)"** — named in the Φ review alongside BP&R and Li. No PDF here. Either fetch it or strike the citation; a review may not lean on a paper the shelf cannot produce.

## data/

| file | what | note |
|---|---|---|
| `ame2020-mass-table.txt` | AME2020 atomic mass adjustment, A = 0–295, with header (dated 3 Mar 2021) | the binding-energy ground truth for `capsid_audit` |
| `ame2020-mass-table-rows-only.txt` | same table, header stripped | convenience copy for parsers |

`_condemned/` holds two further byte-variant duplicates of the rows-only table (`…dup2`, `…dup3`); they differ only in whitespace. Deletion is James's — `rm` them when convenient.

## Not papers, left where found

`../docs/postulate-infinity-n.html` — untitled HTML, not a paper; not indexed here.
