# papers/ — the reference shelf

One index, one nomenclature. If a paper is not in this table it is not on the shelf.

## Nomenclature

    <lead-author(s)>-<short-title>.<ext>

- **lowercase, hyphenated, ASCII** (ö → oe, no underscores, no spaces).
- **≤2 authors:** all surnames (`schoeneberg-vacher-…`, `battey-pratt-racey-…`).
- **≥3 authors:** first surname + `et-al` (`kopp-et-al-…`). Disambiguate colliding surnames with a second token (`li-kaisheng-…` vs `li-sparveris-et-al-…`).
- **Collaboration papers:** the collaboration (`besiii-…`).
- **Short title:** the title's load-bearing words, articles dropped. Not the arXiv number, not the journal's file id.
- **Conversion tracking is a move, not a flag:** a PDF that has been converted lives in `pdf/converted-to-md/`; one still awaiting conversion sits in `pdf/`. `ls pdf/` is the to-do list. (James's convention, 2026-09-03.)
- **`.md` suffixes:** `<basename>-text-only.md` is the verbatim conversion; `<basename>-READING-NOTES.md` is commentary. Same basename as the PDF.
- Datasets live in `../data/` (estate level, not under papers/), named by their source (`ame2020-…`), never by what we happened to use them for.

## Index

| basename | authors | title · venue · year | pdf | md | notes |
|---|---|---|---|---|---|
| `battey-pratt-racey-geometric-model-for-fundamental-particles` | E. P. Battey-Pratt, T. J. Racey | Geometric Model for Fundamental Particles · Int. J. Theor. Phys. 19(6) · 1980 | `converted-to-md/` | `-text-only` ✅ `-READING-NOTES` ✅ | the spine's BP&R anchor. (A 2008 image-only Xerox scan of the same paper was deleted by James in chunk 0 — the text PDF supersedes it.) |
| `li-kaisheng-classical-spiral-orbit-model-h2` | Kaisheng Li | A Classical Spiral Orbit Model for Molecular Spectra and Electron Spin: Applications to H₂ · independent · Apr 2025 | `converted-to-md/` | ✅ | cited in the Φ review as "Li (2025)" |
| `li-sparveris-et-al-measured-proton-electromagnetic-structure` | R. Li, N. Sparveris, et al. (JLab) | Measured proton electromagnetic structure deviates from theoretical predictions · arXiv:2210.11461 · 2022 | ✅ | ☐ | proton form-factor anomaly — relevant to the capsid charge-radius coupling (`capsid_audit` §2.3) |
| `besiii-oscillating-features-electromagnetic-structure-neutron` | BESIII Collaboration (Ablikim et al.) | Oscillating features in the electromagnetic structure of the neutron (arXiv title: *New Features…*) · arXiv:2103.12486 / Nat. Phys. · 2021 | ✅ | ☐ | neutron form-factor oscillations — the neutron's own "orbit" fingerprint |
| `kopp-et-al-magnetic-moments-astrophysical-neutrinos` | J. Kopp, T. Opferkuch, E. Wang | Magnetic Moments of Astrophysical Neutrinos · arXiv:2212.11287v3 · 2024 | ✅ | ☐ | n=1 neutrino as the sole primitive ⇒ its moment is a first-class prediction target |
| `schoeneberg-vacher-mass-effect-electron-mass-variations-cosmology` | N. Schöneberg, L. Vacher | The mass effect — variations of the electron mass and their impact on cosmology · JCAP03(2025)004 · 2025 | `converted-to-md/` | ✅ | if m_e is medium-set (ℏ as stiffness), varying-m_e cosmology is a live constraint channel |
| `sen-of-mass-charge-and-spin` | D. Sen | Of Mass, Charge and Spin, the Basic Attributes of Matter — Their Physical Origin · Horizons in World Physics 275, ch. 9 · 2011 | ✅ | ☐ | the orthodox review of exactly the three things §17.2 says must be derived |
| `blokker-et-al-chemical-bond-atom-size-vs-electronegativity` | E. Blokker, …, F. M. Bickelhaupt | The Chemical Bond: When Atom Size Instead of Electronegativity Difference Determines Trend in Bond Strength · Chem. Eur. J. 27, 15616 · 2021 | ✅ | ☐ | size-over-electronegativity — geometry beating a dial, one floor up |
| `swart-soccer-ball-symmetry` | David Swart | Soccer Ball Symmetry · Bridges 2015 · 2015 | ✅ | ☐ | truncated-icosahedron / capsid geometry reference |
| `xu-et-al-11-teraflops-photonic-convolutional-accelerator` | X. Xu, …, D. J. Moss (Swinburne) | 11 TOPS photonic convolutional accelerator for optical neural networks · Nature 589 · 2021 | ✅ | ☐ | analogue compute-in-place, silicon-photonic — FUBIT-adjacent, not physics-spine |
| `schrodinger-what-is-life-mind-and-matter` | E. Schrödinger (fwd. R. Penrose) | What is Life? · Mind and Matter · Autobiographical Sketches · CUP | ✅ | ☐ | the estate's namesake shelf; Axiom I is a descendant of the aperiodic-crystal chapter |

**Conversion status: 3 of 11 converted** (`ls pdf/converted-to-md/`). ☐ = still in `pdf/`. Convert on demand — when a `what next?` question pulls the paper, not before (chunk-2 rule: nothing crosses by default). If forced to guess the order: Sen → Kopp → Li/Sparveris → BESIII.

## Cited but not on the shelf

- **"Helland et al. (2026)"** — named in the Φ review alongside BP&R and Li. No PDF here. Either fetch it or strike the citation; a review may not lean on a paper the shelf cannot produce.

## ../data/ (estate level)

| file | what | note |
|---|---|---|
| `ame2020-mass-table.txt` | AME2020 atomic mass adjustment, A = 0–295, with header (dated 3 Mar 2021) | the binding-energy ground truth for the capsid work |
| `ame2020-mass-table-rows-only.txt` | same table, header stripped | convenience copy for parsers |
| `binding-energy/binding-energy{,1,2,3}.txt` | the same table under its original names (one with header, three whitespace-variant rows-only copies) | carried across as-is by James; redundant with the two files above — one `rm -r` when convenient |

`papers/_condemned/` still holds two of the whitespace-variant duplicates from the first pass; also `rm` fodder.

## Not carried across (still in `schrodinger/` history, commit f85d38d)

`docs/reference/Spec-for-Suman.md` and `docs/reference/truncated-tetrahedrons.pdf` did not make the move. Pull on demand if a question asks for them.

## Not papers, left where found

`../docs/postulate-infinity-n.html` — untitled HTML, not a paper; not indexed here.
