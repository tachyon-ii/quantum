# FACTCHECK — SPEC v6 (bumps and locks) and the conversation claims that feed it

Checked 18 Nov 2026 by web search against the sources listed. Scope: statements of established fact or measurement only; POSIT / CONSTRUCT / COMPUTED items were not judged.

Method notes
- Values were confirmed from search-result extracts of the cited pages, not from full-text reads. Where an extract did not show the exact figure, the row says so.
- Could not be fetched (not retried): `https://nds.iaea.org/relnsd/v1/data?fields=ground_states&nuclides=59fe` (client error); the sandbox shell is blocked from the web (proxy 403), which is also why the NUBASE2020 file named in SPEC §6 could not be downloaded. Half-lives were therefore taken from Wikipedia isotope tables (NUBASE2020-derived), KAERI/NNDC-derived tables and periodictable.com rather than from NUBASE directly.
- "Correct" means correct at the precision stated (e.g. "~3 h" for 2.6 h passes).

Totals: 105 rows — correct 94, imprecise 6, wrong 1, could not verify 4.

## Table

| # | Claim | Stated value | Verified value | Verdict | Source URL |
|---|---|---|---|---|---|
| 1 | Fe-59 half-life | 44 d | 44.50 d | correct | https://en.wikipedia.org/wiki/Isotopes_of_iron |
| 2 | Fe-60 half-life | 2.6 My | 2.62(4) My (1.5 My before 2009) | correct | https://en.wikipedia.org/wiki/Isotopes_of_iron |
| 3 | Fe-61 half-life | 6 min | 5.98 min | correct | https://en.wikipedia.org/wiki/Isotopes_of_iron |
| 4 | Fe-62 half-life | 68 s | 68 s | correct | https://atom.kaeri.re.kr/cgi-bin/nuclide?nuc=Fe-62 |
| 5 | Fe-55 (radioactive; no value stated) | — | 2.756 y, electron capture | correct | https://en.wikipedia.org/wiki/Isotopes_of_iron |
| 6 | C-14 half-life | 5,730 y | 5,730 y (NUBASE2020: 5,700 ± 30 y) | correct | https://www.wikipedia.org/wiki/List_of_isotopes_by_half-life |
| 7 | C-15 half-life | ~2 s | 2.449 s | correct | https://www.wikipedia.org/wiki/List_of_isotopes_by_half-life |
| 8 | Si-31 half-life | ~3 h | 157.3 min (2.62 h) | correct | https://pripyat.mit.edu/KAERI/cgi-bin/nuclide?nuc=Si31 |
| 9 | Si-32 half-life | ~153 y | 153(19) y; some evaluations ~157 y | correct | https://www.nndc.bnl.gov/ensnds/32/Si/adopted.pdf |
| 10 | Si-33 half-life | ~6 s | 6.18 s | correct | https://ipfs.ssi.eecc.de/ipns/en.wikipedia-on-ipfs.org/wiki/Isotopes_of_silicon |
| 11 | Ca-41 half-life | ~100,000 y | ~1.0 × 10⁵ y (102,000 y) | correct | https://periodictable.com/Isotopes/020.41/index.html |
| 12 | Ca-45 half-life | 163 d | 162.6 d | correct | https://periodictable.com/Isotopes/020.45/index.html |
| 13 | Ca-47 half-life | ~5 d | 4.54 d | correct | https://periodictable.com/Isotopes/020.47/index.html |
| 14 | Ca-49 half-life | ~9 min | 8.72 min | correct | https://periodictable.com/Isotopes/020.49/index2.html |
| 15 | O-19 half-life | 27 s | 26.9 s | correct | https://periodictable.com/Isotopes/008.19/index.html |
| 16 | O-20 half-life | 14 s | 13.5 s | correct | https://wiki.riteme.site/wiki/Talk:Isotopes_of_oxygen/Archive_1 |
| 17 | O-21 half-life | ~3 s | 3.42 s | correct | https://periodictable.com/Isotopes/008.21/index2.html |
| 18 | O-22 half-life | ~2 s | 2.25 s | correct | https://periodictable.com/Isotopes/008.22/index2.html |
| 19 | He-6 half-life | 0.8 s | 0.807 s | correct | https://periodictable.com/Isotopes/002.8/index2.html |
| 20 | He-8 half-life | 0.1 s | 0.119 s | correct | https://periodictable.com/Isotopes/002.8/index2.html |
| 21 | Pb-209 half-life | 3 h | 3.235 h | correct | https://en.wikipedia.org/wiki/Isotopes_of_lead |
| 22 | Pb-210 half-life | 22 y | 22.2 y | correct | https://en.wikipedia.org/wiki/Isotopes_of_lead |
| 23 | Pb-211 half-life | 36 min | 36.16 min | correct | https://en.wikipedia.org/wiki/Isotopes_of_lead |
| 24 | Pb-212 half-life | 11 h | 10.63 h | correct | https://en.wikipedia.org/wiki/Isotopes_of_lead |
| 25 | Pb-213 half-life | 10 min | 10.2(3) min (single source) | correct | https://www.doc.surf/wiki/isotopes-of-lead |
| 26 | Pb-214 half-life | 27 min | 27.06 min (older tables 26.8 min) | correct | https://en.wikipedia.org/wiki/Isotopes_of_lead |
| 27 | Ni-56 half-life | ~6 d | 6.075 d | correct | https://arxiv.org/pdf/1611.08746 |
| 28 | Co-56 half-life | ~11 weeks | 77.24 d (11.0 weeks) | correct | https://arxiv.org/pdf/1611.08746 |
| 29 | Be-7 half-life | 53 d | 53.1–53.4 d across tables (NUBASE 53.22 d) | correct | https://www.wikipedia.org/wiki/List_of_isotopes_by_half-life |
| 30 | Tritium half-life | 12 y | 12.3 y | correct | https://saylordotorg.github.io/text_the-basics-of-general-organic-and-biological-chemistry/s14-02-half-life.html |
| 31 | Free neutron "half-life" | ~15 min | Mean life 878.4 ± 0.5 s (14.6 min); half-life = τ ln2 ≈ 609 s (10.1 min) | imprecise | https://pdglive.lbl.gov/Particle.action?node=S017 |
| 32 | Be-8 half-life | ~1e-16 s | 8.19(37) × 10⁻¹⁷ s | correct | https://en.wikipedia.org/wiki/Beryllium-8 |
| 33 | U-238 half-life | 4.5e9 y | 4.468 × 10⁹ y | correct | https://www.wikipedia.org/wiki/List_of_isotopes_by_half-life |
| 34 | Fe-57 first excited state | 14.4 keV | 14.41 keV | correct | https://www.physlab-wiki.com/phylabs/lab_courses/phys-334-wiki-home/mossbauer-spectroscopy-of-fe-57/start |
| 35 | Fe-57 14.4 keV state lifetime | ~1e-7 s | half-life 98 ns; mean life ~141 ns | correct | https://www.physics.wisc.edu/courses/home/spring2020/407/experiments/mossbauer/mossbauer.pdf |
| 36 | Fe-57 fractional linewidth | ~1 part in 1e12 | Γ = 4.7 × 10⁻⁹ eV; Γ/E ≈ 3 × 10⁻¹³ (1 part in ~3 × 10¹²) | imprecise | https://www.ocw.mit.edu/courses/8-13-14-experimental-physics-i-ii-junior-lab-fall-2016-spring-2017/48e831b658c4acd78c3e63ab31789ff2_MIT8_13-14F16-S17exp13.pdf |
| 37 | Fe-57 ground-state magnetic moment | < 0.1 μN | ≈ +0.090 μN (from μ₁ = −0.1547 μN and μ₁/μ₀ = −1.7145); tabulated value +0.0906 not shown in extract | correct | https://www.osti.gov/biblio/4837516 |
| 38 | Fe-57 natural abundance | ~2% | 2.119% | correct | https://webelements.co.uk/iron/isotopes.html |
| 39 | Fe-56 share of natural iron | ~92% | 91.754% | correct | https://webelements.co.uk/iron/isotopes.html |
| 40 | Fe-56 first excited state | 847 keV | 847 keV, 2⁺ (846.8 keV) | correct | https://ealga.mit.edu/KAERI/cgi-bin/nuclide?nuc=Fe56 |
| 41 | Highest binding energy per nucleon | Ni-62, then Fe-58, then Fe-56 | 8794.5, 8792.3, 8790.4 keV/A in that order | correct | https://ui.adsabs.harvard.edu/abs/1995AmJPh..63..653F/abstract ; https://arxiv.org/pdf/1709.01386 |
| 42 | Pound–Rebka 1960 | 22 m tower; shift ~2 parts in 1e15 | 22.5 m; predicted one-way gh/c² = 2.46 × 10⁻¹⁵; measured (2.57 ± 0.26) × 10⁻¹⁵ one-way (5.13 ± 0.51 two-way); PRL 4, 337 | correct | https://luth.obspm.fr/IHP06/lectures/mester-vinet/IHP-2GravRedshift.pdf |
| 43 | Neutron-interferometry gravity phase shift | 1975, Colella–Overhauser–Werner | PRL 34, 1472 (9 June 1975) | correct | https://faculty.cst.temple.edu/~tuf43817/PHYS5701/PhysRevLett.34.1472.pdf |
| 44 | Smallest source mass with measured gravity | ~90 mg, Westphal et al. 2021 | 90 mg gold sphere, ~1 mm radius; Nature 591, 225 (2021) | correct | https://arxiv.org/abs/2009.09546v1 |
| 45 | Newtonian gravity tested at short range | down to a few hundredths of a mm | 1/r² holds at separations 52 µm–3 mm; gravitational-strength Yukawa excluded for λ > 38.6 µm (Lee et al., PRL 124, 101101, 2020) | correct | https://arxiv.org/pdf/2002.11761 |
| 46 | Equivalence principle | ~1e-15, MICROSCOPE, Ti vs Pt | η(Ti,Pt) = [−1.5 ± 2.3 (stat) ± 1.5 (syst)] × 10⁻¹⁵; PRL 129, 121102 (2022) | correct | https://arxiv.org/pdf/2209.15487 |
| 47 | ALPHA-g 2023 | antihydrogen falls downward | Confirmed; a = (0.75 ± 0.13 ± 0.16) g; Nature, DOI 10.1038/s41586-023-06527-1 | correct | https://news.berkeley.edu/?p=119481 |
| 48 | Stable odd-odd nuclei | only four: H-2, Li-6, B-10, N-14 | Four in their ground states; the stable-nuclide list has a fifth odd-odd entry, the isomer Ta-180m (decay never observed) | imprecise | https://en.wikipedia.org/wiki/Stable_nuclide |
| 49 | Even-even ground states | all spin 0 | All known even-even nuclei have 0⁺ ground states, without exception | correct | https://arxiv.org/pdf/2607.22887 |
| 50 | Odd-Z elements | at most two stable isotopes | No odd-Z element has more than two stable isotopes (K has three primordial, but K-40 is radioactive) | correct | https://en.wikipedia.org/wiki/List_of_elements_by_stability_of_isotopes |
| 51 | Even-Z elements | up to ten (tin) | Tin has ten stable isotopes, the most of any element | correct | https://en.wikipedia.org/wiki/Stable_nuclide |
| 52 | Number of nuclides | ~250 stable; ~3,300 known | 251 stable; NUBASE2020 lists 3,340 ground states | correct | https://en.wikipedia.org/wiki/Stable_nuclide ; https://cpc.ihep.ac.cn/article/doi/10.1088/1674-1137/abddae |
| 53 | Magic numbers | 2, 8, 20, 28, 50, 82, 126 | Same | correct | https://en.wikipedia.org/wiki/Nuclear_shell_model |
| 54 | Harmonic-oscillator closures | 2, 8, 20, 40, 70, 112 = 2 × tetrahedral numbers | Closures confirmed; tetrahedral numbers are 1, 4, 10, 20, 35, 56, so the doubling is exact (arithmetic) | correct | https://en.wikipedia.org/wiki/Nuclear_shell_model |
| 55 | Real closures = oscillator closure + intruder of 8, 10, 12, 14 | 28, 50, 82, 126 | 20+8 (1f7/2), 40+10 (1g9/2), 70+12 (1h11/2), 112+14 (1i13/2); source confirms the f7/2 and g9/2 cases explicitly and the general rule for the rest | correct | https://en.wikipedia.org/wiki/Nuclear_shell_model |
| 56 | Superdeformed shell gaps at 2:1 | exists | Deformed-oscillator gaps at integer axis ratios; Dy-152 (Z = 66, N = 86) the first case, 1986. Real nuclei are nearer 1.6–1.8:1 | correct | https://arxiv.org/pdf/1710.01210 |
| 57 | Ca-43 quadrupole moment | slightly negative, ~ −0.04 b | −0.0408(8) b recommended; a later determination gives −0.0444(6) b | correct | https://www-nds.iaea.org/nuclearmoments/isotope_measurement_results.php?A=43&Z=20 |
| 58 | Li-7 quadrupole moment | slightly negative, ~ −0.04 b | Magnitude 0.0386–0.0406 b; negative (recent measurement −0.0386(5) b; standard tables −0.0400 b) | correct | https://arxiv.org/pdf/2504.18516 |
| 59 | Neutron mean-square charge radius | negative (positive inside, negative outside) | −0.1161 ± 0.0022 fm² (PDG); attributed to a slightly negative outer region | correct | https://pdg.web.cern.ch/2020/tables/rpp2020-tab-baryons-N.pdf ; https://archive.aps.org/dnp/2021/qj/2 |
| 60 | Proton lifetime limit | > 1e34 y | τ/B(p → e⁺π⁰) > 2.4 × 10³⁴ y, 90% CL (Super-K 2020); limit is per decay mode | correct | https://arxiv.org/pdf/2010.16098 |
| 61 | Neutron lifetime discrepancy | bottle ~878 s, beam ~888 s, ~9 s gap | Bottle/PDG 878.4 ± 0.5 s (UCNτ 877.75 s); beam ~888.0 ± 2.0 s; gap ~9–10 s, ~4σ | correct | https://pdglive.lbl.gov/Particle.action?node=S017 ; https://arxiv.org/pdf/2106.10375 ; https://arxiv.org/pdf/1801.01124 |
| 62 | Dark-decay proposal | Fornal & Grinstein 2018 | PRL 2018; ~1% branching into dark-sector particles | correct | https://arxiv.org/pdf/1801.01124 |
| 63 | Annual modulation of decay rates | claimed by Jenkins, Fischbach ~2009; later tests | Claim: arXiv 0808.3283 (publ. 2009). Not confirmed: Norman et al. 2009 found none; Cassini RTG data none; Pommé et al. 2016 (14 labs) bound annual amplitude to 0.0006–0.008% and attribute the effect to instruments | correct | https://ar5iv.labs.arxiv.org/html/0808.3283 ; https://publications.jrc.ec.europa.eu/repository/handle/JRC101875 |
| 64 | Photon-to-baryon ratio | over 1e9 | ~1.6 × 10⁹ (η ≈ 6.0–6.1 × 10⁻¹⁰) | correct | https://pdg.lbl.gov/2025/reviews/rpp2025-rev-bbang-nucleosynthesis.pdf |
| 65 | Relic neutrino density | ~300 per cm³ | ~336 per cm³ (112 per flavour, ν + ν̄) | correct | https://arxiv.org/pdf/1512.00817 |
| 66 | Solar neutrino flux at Earth | ~6e10 per cm² per s | 6.5 × 10¹⁰ cm⁻² s⁻¹ | correct | https://arxiv.org/pdf/hep-ex/0312045 |
| 67 | Neutrino decoupling | ~1 s | ~1 s, T ~ 1 MeV | correct | https://ipfs.ssi.eecc.de/ipns/en.wikipedia-on-ipfs.org/wiki/Chronology_of_the_universe |
| 68 | Nucleosynthesis | ~3 min | Starts at ~2–3 min, T ~ 0.1 MeV (10⁹ K) | correct | https://pdg.lbl.gov/2025/reviews/rpp2025-rev-bbang-nucleosynthesis.pdf |
| 69 | Recombination | ~380,000 y | 370,000–380,000 y (z ≈ 1100) | correct | https://ipfs.ssi.eecc.de/ipns/en.wikipedia-on-ipfs.org/wiki/Chronology_of_the_universe |
| 70 | Deuterium bottleneck (bath breaks the deuteron until it cools) | exists | Confirmed: nuclei form once photons above the 2.23 MeV threshold fall below one per baryon, T ≈ 0.1 MeV | correct | https://pdg.lbl.gov/2025/reviews/rpp2025-rev-bbang-nucleosynthesis.pdf |
| 71 | GZK cut-off | protons lose energy on CMB above ~5e19 eV | E ≈ 5 × 10¹⁹ eV, photo-pion production; source horizon ~50 Mpc | correct | https://arxiv.org/pdf/astro-ph/0506412 |
| 72 | Be and B made mainly by cosmic-ray spallation of C, N, O | yes | Li-6, Be-9, B-10 essentially all spallation; B-11 mostly (some supernova neutrino process) | correct | https://arxiv.org/pdf/2211.07838 |
| 73 | Lithium made mainly by cosmic-ray spallation (SPEC §4: "most of the lithium") | yes | No. Li-7 (~92% of lithium) is largely primordial plus stellar (novae, giants, supernovae); spallation is the main source only of Li-6 | wrong | https://arxiv.org/pdf/2211.07838 ; https://link.springer.com/article/10.1038/360439a0 |
| 74 | Limits on variation of α | atomic clocks, quasars, Oklo | Clocks: α̇/α = 1.0(1.1) × 10⁻¹⁸ /yr (Lange 2021). Oklo: abs(Δα/α) below ~1 × 10⁻⁷ (Damour–Dyson 1996), ~1 × 10⁻⁸ in a 2015 reappraisal, over ~2 Gy. Quasars: ppm-level claims (Webb), dipole not confirmed, likely systematics | correct | https://arxiv.org/abs/2010.06620v1 ; https://arxiv.org/abs/hep-ph/9606486 ; https://arxiv.org/pdf/1510.00856 |
| 75 | Varying-speed-of-light cosmologies | Moffat; Albrecht & Magueijo | Moffat, Int. J. Mod. Phys. D 2, 351 (1993); Albrecht & Magueijo, Phys. Rev. D 59, 043516 (1999) | correct | https://arxiv.org/pdf/gr-qc/9211020 ; https://arxiv.org/abs/astro-ph/9811018 |
| 76 | Fluctuation-theorem experiment | Wang et al. 2002, colloidal bead in optical trap, entropy-consuming trajectories over seconds | PRL 89, 050601 (2002); bead dragged through water in an optical trap; "seconds" not shown in the extract (paper reports up to ~2 s). Later comments note it confirms, not violates, the second law | correct | https://researchportalplus.anu.edu.au/en/publications/experimental-demonstration-of-violations-of-the-second-law-of-the/ |
| 77 | Large-scale structure | fractal-like up to some scale, homogeneous beyond; debated | Fractal dimension D ≈ 2 up to ~10–20 Mpc/h; homogeneity reached by ~70–80 Mpc/h (Hogg 2005; WiggleZ 2012: 70–81 Mpc/h, D₂ < 2.97 excluded beyond ~80 Mpc/h). Disputed by Sylos Labini et al., who find no homogeneity below 100 Mpc/h | correct | https://arxiv.org/pdf/1205.6812 ; https://arxiv.org/pdf/astro-ph/0501583 ; https://arxiv.org/abs/0805.1132v1 |
| 78 | Dose-rate effect / DDREF | same dose at high rate more damaging | ICRP DDREF = 2 (since ICRP 60, kept 2007); value contested (SSK argues 1); under ICRP review | correct | https://www.ssk.de/SharedDocs/Beratungsergebnisse/EN/2014/DDREF.pdf |
| 79 | FLASH radiotherapy | ultra-high dose rate spares normal tissue | Favaudon et al. 2014: ≥ 40 Gy/s spared lung tissue in mice with tumour control kept. Note this runs opposite to the classical dose-rate effect | correct | https://en.wikipedia.org/wiki/FLASH_radiotherapy |
| 80 | s- vs r-process timescales | slow vs rapid capture | s: ~decade per capture, thousands of years for the path, slower than β decay; r: captures much faster than β decay (a "milliseconds" figure was not found in the extracts) | correct | https://inpp.ohio.edu/~meisel/ASTR4201/file/QuickNotes_22_sprocess.pdf ; https://en.wikipedia.org/wiki/R-process |
| 81 | Twin abundance peaks | exist | Paired peaks near A ≈ 130/138 and 195/208 from N = 82, 126 (r below s) | correct | https://arxiv.org/pdf/astro-ph/0301422 |
| 82 | Skyrme 1961 | baryon = topological soliton, baryon number = winding number | Confirmed | correct | https://ar5iv.labs.arxiv.org/html/1604.04850 |
| 83 | Heisenberg 1932 exchange proposal (also SPEC §10) | exists | Confirmed; 1932 papers, exchange force between n and p | correct | https://arxiv.org/pdf/2402.00191 |
| 84 | np charge-exchange scattering | backward peak | Sharp peak near 180° (u ≈ 0), "np charge exchange" | correct | https://arxiv.org/pdf/0805.3133 |
| 85 | Lowest nuclear excited state | Th-229m, ~8 eV | ~8.4 eV (2020.409 THz; laser-excited 2024, PRL 132, 182501) | correct | https://physics.aps.org/featured-article-pdf/10.1103/PhysRevLett.132.182501 |
| 86 | Ta-180m | longest-lived natural isomer, > 1e15 y | Decay never observed; limit T½ > 0.29 × 10¹⁸ y (Majorana 2023, PRL 131, 152501); previous 4.5 × 10¹⁶ y | imprecise | https://pdf.arxiv.org/pdf/2306.01965 |
| 87 | Cosmic-ray hit probability per nucleus over the age of the universe | ~1e-7 (flux a few per cm² per s; σ ~40 mb) | For a proton target: ~4 cm⁻² s⁻¹ × ~3–4 × 10⁻²⁶ cm² × 4.35 × 10¹⁷ s ≈ 5–7 × 10⁻⁸, i.e. ~10⁻⁷. For a composite nucleus the inelastic cross-section is several hundred mb (C ~250, Fe ~700), giving ~10⁻⁶. Flux and pp cross-section figures only partly confirmed from extracts (PDG spectrum; σ_inel ~30 mb near 10 GeV) | imprecise | https://ccwww.kek.jp/pdg/2011/reviews/rpp2011-rev-cosmic-rays.pdf ; https://arxiv.org/pdf/astro-ph/0410617 |
| 88 | SPEC P19: binding of 2, 3, 4 bodies | 2.22, 8.48, 28.30 MeV | 2.2246, 8.4818, 28.2957 MeV | correct | https://sjsu.edu/faculty/watkins/BEsmallnuclides2.htm |
| 89 | SPEC §2.2: np with spins opposed just fails | −0.07 MeV | Singlet state unbound (virtual) by ~0.064–0.07 MeV | correct | https://arxiv.org/pdf/0801.0917 |
| 90 | SPEC §2.2: Be-8 unbound | by 0.09 MeV | 91.84 keV above 2α; width 5.57 eV | correct | https://www.nndc.bnl.gov/ensnds/8/Be/adopted.pdf |
| 91 | SPEC §2.2: He-5 takes no single extra | unbound | Unbound to n + He-4 by ~0.8–1 MeV | correct | https://arxiv.org/pdf/nucl-th/0601064 |
| 92 | SPEC §2.2: He-4 + 3n unbound; Li-7 stable | — | He-7 is a resonance ~0.4 MeV above n + He-6, width ~0.18 MeV; Li-7 stable | correct | https://ar5iv.arxiv.org/html/1210.1897 |
| 93 | SPEC §2.2: Fe-57 state "lasts ~1e14 turns" (turn ~1e-22 s, P14) | 1e14 | 1.4 × 10⁻⁷ s ÷ 10⁻²² s ≈ 1 × 10¹⁵ | imprecise | https://www.physics.wisc.edu/courses/home/spring2020/407/experiments/mossbauer/mossbauer.pdf |
| 94 | SPEC §2.2: Fe-61 outlives Fe-62; Ni-56 decays; tritium decays, He-3 stable; Ca-43 stable | — | Rows 3, 4, 27, 30; Ca-43 is a stable isotope | correct | (rows above) ; https://www-nds.iaea.org/nuclearmoments/isotope_measurement_results.php?A=43&Z=20 |
| 95 | SPEC P14: "stability is not depth" (deuteron vs Be-8 vs Ni-56) | — | Deuteron bound by 2.22 MeV total and stable; Be-8 unbound by 92 keV; doubly magic Ni-56 decays in 6 d | correct | (rows 27, 88, 90) |
| 96 | SPEC §4: CMB photon energy | ~1e-3 eV, ten orders below nuclear | Mean ~6 × 10⁻⁴ eV at 2.725 K; 9–10 orders below MeV | correct | https://arxiv.org/pdf/0806.3713 |
| 97 | SPEC §4: gamma de-excitation | typically within 1e-12 s | Typical excited-state lifetimes are picoseconds (range fs to ns and beyond; isomers excepted) | correct | https://mn.uio.no/fysikk/studier/master/masteroppgaver/Physics/nuclear-particle/nep/lifetime-measurements.html |
| 98 | SPEC P21: ordinary matter about a sixth of total matter | 1/6 | Planck 2018: Ω_b h² = 0.0224, Ω_c h² = 0.120 → 15.7% | correct | https://arxiv.org/pdf/1807.06209 |
| 99 | SPEC P18: collisions yield only whole hadrons, re-formed within ~1e-23 s | 1e-23 s | Free quarks never observed; hadron formation ~1 fm/c ≈ 3 × 10⁻²⁴ s in its rest frame (models 1–6 fm/c) | correct | https://arxiv.org/pdf/nucl-th/0306027 ; https://arxiv.org/pdf/hep-ph/9503349 |
| 100 | SPEC P24: small systems step backward | — | Row 76 | correct | (row 76) |
| 101 | SPEC §10: Reeves, Fowler, Hoyle 1970 (spallation origin of Li, Be, B) | — | Nature 1970, "Galactic cosmic ray origin of Li, Be and B in stars" | correct | https://arxiv.org/pdf/astro-ph/9911320 |
| 102 | SPEC §5: liquid drop, 1935, five constants, energies to ~1% | ~1% | Weizsäcker 1935, five terms confirmed; the ~1% accuracy figure not found | could not verify | https://en.wikipedia.org/wiki/Semi-empirical_mass_formula |
| 103 | SPEC P14: internal nuclear motion ~1e-22 s per turn | 1e-22 s | No source found | could not verify | — |
| 104 | SPEC §10 citations: Greisen, Zatsepin, Kuzmin 1966; Mayer and Jensen 1949; Reason 1990 | — | Names appear with the right topics; years not shown in any extract | could not verify | — |
| 105 | SPEC P26: bound systems do not stretch with space; uniform gravitating matter must clump | — | Not searched to a source | could not verify | — |

## Corrections needed

1. **Lithium (row 73, SPEC §4).** Wrong as written. Cosmic-ray spallation makes essentially all Li-6, Be-9 and B-10 and most B-11, but not most lithium: Li-7, about 92% of lithium, is mainly primordial (Big Bang) plus stellar (novae, giant stars, supernovae). Corrected: "collectively they make almost all the beryllium and boron and the Li-6 that exists; most lithium (Li-7) comes from the Big Bang and from stars."
2. **Free neutron (row 31).** "~15 min" is the mean life (878.4 s = 14.6 min). The half-life, the quantity every other entry in that list uses, is ~609 s ≈ 10.1 min.
3. **Fe-57 linewidth (row 36).** Γ/E ≈ 3 × 10⁻¹³, about 1 part in 3 × 10¹², not 1 in 10¹².
4. **Fe-57 "~10¹⁴ turns" (row 93, SPEC §2.2).** With the document's own unit (10⁻²² s) and the 141 ns mean life (98 ns half-life), the count is ~10¹⁵.
5. **Stable odd-odd nuclei (row 48, SPEC §2.2 and rung 1 gate).** Four in their ground states (H-2, Li-6, B-10, N-14). Ta-180m, an isomer, is a fifth observationally stable odd-odd nuclide and should be named as the exception rather than omitted, particularly as the document treats nuclei that hold an excitation as keys (P23).
6. **Ta-180m (row 86).** "> 10¹⁵ y" understates the current limit: T½ > 2.9 × 10¹⁷ y (Majorana Demonstrator 2023); the earlier limit was 4.5 × 10¹⁶ y.
7. **Cosmic-ray hit probability (row 87, SPEC §4).** ~10⁻⁷ over the age of the universe holds for a single proton (σ ≈ 30–40 mb). For a composite nucleus the inelastic cross-section is roughly 250 mb (carbon) to 700 mb (iron), so the chance is nearer 10⁻⁶. Corrected: "of order one chance in a million to ten million".

Minor, no change to the argument: C-14 is 5,700 ± 30 y in NUBASE2020 (5,730 y is the conventional figure); Pb-212 is 10.6 h; Si-31 is 2.6 h; Ca-47 is 4.5 d; the Ca-43 quadrupole moment has a competing value of −0.0444 b; the proton-lifetime limit is mode-specific; Oklo bounds range 10⁻⁸–10⁻⁷ depending on the analysis; FLASH sparing is the reverse of the classical dose-rate effect, which matters if both are cited under P22 as the same rule.

## Could not verify

- Liquid-drop accuracy "~1% across the chart" (row 102). The date and five-term form are confirmed.
- Nuclear internal period ~10⁻²² s (row 103).
- Publication years for Greisen/Zatsepin–Kuzmin (1966), Mayer and Jensen (1949), Reason (1990) (row 104).
- "Bound systems do not stretch with space" and gravitational clumping of a uniform distribution (row 105).
- Partial: integrated interstellar cosmic-ray flux ("a few per cm² per s") and nucleus–nucleus inelastic cross-sections used in row 87 were not found as explicit figures; "milliseconds" for r-process captures (row 80); "over seconds" for Wang et al. (row 76); the tabulated Fe-57 moment +0.0906 μN (row 37, derived value 0.090 only); the sign of the Li-7 quadrupole moment in the standard table (row 58, one recent measurement confirms negative).
- Source not reachable: IAEA LiveChart API and the NUBASE2020 text file; half-lives rest on secondary tables.
