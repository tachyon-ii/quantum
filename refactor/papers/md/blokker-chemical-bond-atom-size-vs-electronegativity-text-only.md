---
title: "The Chemical Bond: When Atom Size Instead of Electronegativity Difference Determines Trend in Bond Strength"
author: "Eva Blokker et al."
source_file: "blokker-et-al-chemical-bond-atom-size-vs-electronegativity.pdf"
pages: 7
---

# The Chemical Bond: When Atom Size Instead of Electronegativity Difference Determines Trend in Bond Strength

**Eva Blokker et al.**

> **Conversion note.** This is an editable Markdown transcription of the supplied PDF. Paragraphs, headings, captions, references, and machine-readable tables are retained where the PDF text layer allows. Displayed mathematics that cannot be reconstructed reliably from the text layer is preserved as a fixed-width extraction rather than silently altered. For exact checking of equations, figures, tables, typography, and reading order, use the complete Markdown package supplied alongside this file.

<!-- Source PDF page 1 -->

## The Chemical Bond: When Atom Size Instead of Electronegativity Difference Determines Trend in Bond Strength

### Eva Blokker,[a] Xiaobo Sun,[a, b] Jordi Poater,[b, c] J. Martijn van der Schuur,[d] Trevor A. Hamlin,[a]

### and F. Matthias Bickelhaupt*[a, e]

Abstract: We have quantum chemically analyzed element- element bonds of archetypal HnX- YHn molecules (X, Y=C, N, O, F, Si, P, S, Cl, Br, I), using density functional theory. One purpose is to obtain a set of consistent homolytic bond dissociation energies (BDE) for establishing accurate trends across the periodic table. The main objective is to elucidate the underlying physical factors behind these chemical bonding trends. On one hand, we confirm that, along a period (e.g., from C- C to C- F), bonds strengthen because the electronegativity difference across the bond increases. But, down a period, our findings constitute a paradigm shift. From C- F to C- I, for example, bonds do become weaker, however, not because of the decreasing electronegativity difference. Instead, we show that the effective atom size (via steric Pauli repulsion) is the causal factor behind bond weakening in this series, and behind the weakening in orbital interactions at the equilibrium distance. We discuss the actual bonding mechanism and the importance of analyzing this mechanism as a function of the bond distance.

The chemical bond is a key concept in chemistry.[1–4] Structure, stability and reactivity of molecules critically depend on the length and, especially, the stability of chemical bonds. A sound and minute understanding of trends in element- element bond strengths across the periodic table is, therefore, indispensable for chemical theory and rational design in the molecular sciences. A well-known example of such a trend is that a more polar bond X- Y often tends to be stronger than a related but less polar bond, as reflected by the bond dissociation enthalpy (BDE; see Equation (1)).[1–5]

X- Y ! X

. þ Y

### . DH ¼ BDE (1)

The accepted picture behind this trend is that the larger electronegativity difference across the X- Y bond leads to a greater stabilization of the bonding electron stemming from the more electropositive radical fragment. From a molecular orbital (MO) perspective, this is understood as the more stabilizing orbital interaction as the electron of the higherenergy singly-occupied molecular orbital (SOMO) drops deeper in energy into the bonding combination with the lower-energy SOMO in the case of a larger orbital-energy gap (vide infra).[3] A textbook example is the weakening of the carbon- halogen bond in H3C- Y along Y=F, Cl, Br and I.[4] Despite a number of bonding studies on first- and second-row elements,[6] and other studies into the chemical bond,[7] little quantitative knowledge of the actual bonding mechanism of polar bonds exists beyond the arguments based on electronegativity differences.[8–15]

Herein, we show based on detailed quantum chemical analyses how, and why, the electronegativity model for the strength of polar bonds breaks down for certain series (C- F to

[a] E. Blokker, Dr. X. Sun, Dr. T. A. Hamlin, Prof. Dr. F. M. Bickelhaupt Department of Theoretical Chemistry Amsterdam Institute of Molecular and Life Sciences (AIMMS) Amsterdam Center for Multiscale Modeling (ACMM) Vrije Universiteit Amsterdam De Boelelaan 1083, 1081 HV Amsterdam (The Netherlands) E-mail: f.m.bickelhaupt@vu.nl Homepage: https://www.theochem.nl

[b] Dr. X. Sun, Prof. Dr. J. Poater Departament de Química Inorgànica i Orgànica & IQTCUB Universitat de Barcelona Martí i Franquès 1–11, 08028 Barcelona (Spain)

[c] Prof. Dr. J. Poater ICREA Pg. Lluís Companys 23, 08010 Barcelona (Spain)

[d] Dr. Ir. J. M. van der Schuur Polymer Specialties, Nouryon Zutphenseweg 10, 7418 AJ Deventer (The Netherlands)

[e] Prof. Dr. F. M. Bickelhaupt Institute of Molecules and Materials Radboud University Heyendaalseweg 135, 6525 AJ Nijmegen (The Netherlands)

Supporting information for this article is available on the WWW under https://doi.org/10.1002/chem.202103544

© 2021 The Authors. Chemistry - A European Journal published by Wiley- VCH GmbH. This is an open access article under the terms of the Creative Commons Attribution License, which permits use, distribution and reproduction in any medium, provided the original work is properly cited.

*Table 1. Bond dissociation enthalpies ΔH (BDE) of the HnX- YHn systems.[a]*

YHn

*

HnX

* CH3

* NH2

* OH

* F

* SiH3

* PH2

* SH

* Cl

*

H3C

* 85.2 80.3 89.2 111.3 83.2 67.3 70.7 80.9 H2N

* 80.3 60.7 59.8 74.2 96.7 68.3 63.9 60.8 HO

* 89.2 59.8 52.9 55.9 118.1 86.5 69.5 57.8 F

* 111.3 74.2 55.9 48.0 148.6 112.0 86.2 66.8 H3Si

* 83.2 96.7 118.1 148.6 71.4 66.4 82.3 103.6 H2P

* 67.3 68.3 86.5 112.0 66.4 54.4 63.3 75.9 HS

* 70.7 63.9 69.5 86.2 82.3 63.3 61.7 63.8 Cl

* 80.9 60.8 57.8 66.8 103.6 75.9 63.8 59.2

```text
[a] Computed at BLYP-D3(BJ)/TZ2P at 298.15 K and 1 atm.
```

Chemistry—A European Journal

Communication doi.org/10.1002/chem.202103544

15616 Chem. Eur. J. 2021, 27, 15616–15622 © 2021 The Authors. Chemistry - A European Journal published by Wiley-VCH GmbH


<!-- Source PDF page 2 -->

C- I) whereas it holds for others (C- C to C- F). Interestingly, the series of carbon-halogen bonds, for which the electronegativity model breaks down, has hitherto served to illustrate this textbook model.[4,10,16–17]

Thus, we have explored and analyzed the length and strength (BDE) of single bonds X- Y derived from elements across the periodic table (X, Y=periods 2–3, groups 14–17, and Br, I) using dispersion-corrected density functional theory (DFT) and quantitative canonical MO theory in conjunction with a matching bond energy decomposition analysis (EDA) using ADF.[18–20] Not only do we provide accurate trends in BDEs for all possible X- Y electron pair bonds along model systems HnX- YHn, all consistently obtained at BLYP-D3(BJ)/TZ2P,[21] and for Br and I including ZORA;[22] we also reveal the physical factors at play behind the computed trends, as already alluded to above. Interestingly, our explorations highlight the importance of carrying out bonding analyses as a function of the X- Y bond distance if one wishes to go beyond correlations and uncover the actual causalities in the bonding mechanism. Table 1 provides all our computed HnX- YHn bond dissociation enthalpies ΔH (BDE),[23] using standard conditions (298.15 K

*Figure 1. Bond dissociation enthalpy (BDE, in kcalmol- 1) of the HnX- YHn systems as a function of the Pauling electronegativity of the main-group element [Pauling electronegativity χ from lowest to highest value: Si (1.90), P (2.19), C (2.55), S (2.58), N (3.04), Cl (3.16), O (3.44) and F (3.98)].[8] BDE computed at BLYP- D3(BJ)/TZ2P at 298.15 K and 1 atm.*

*Table 2. H3C- CH3, H3C- F and H3C- Cl bonding mechanisms at the equilibrium and at a consistent geometry (in Å, kcalmol- 1, eV) with the SOMO- SOMO gap Δɛ and overlap S.[a,b]*

dX- Y ΔE ΔEstrain ΔEint ΔVelstat ΔEPauli ΔEoi Δɛ S

Equilibrium geometry H3C- CH3 1.538 - 92.1 18.4 - 110.4 - 129.5 204.6 - 186.4 0.00 0.42 H3C- F 1.413 - 115.3 6.3 - 121.6 - 105.3 254.0 - 272.5 7.44 0.26 H3C- Cl 1.820 - 84.2 5.9 - 90.0 - 96.1 172.8 - 167.4 3.88 0.34 Consistent geometry H3C- CH3 1.400 - 85.5 23.0 - 108.4 - 169.8 289.6 - 229.1 0.00 0.42 H3C- F 1.400 - 115.2 6.6 - 121.8 - 108.9 264.9 - 280.1 7.42 0.26 H3C- Cl 1.400 - 13.3 17.5 - 30.8 - 248.8 567.6 - 350.3 3.16 0.35

[a] Computed at BLYP-D3(BJ)/TZ2P. [b] The dispersion energy ΔEdisp (around - 1.0 kcalmol- 1) and the spin polarization ΔEspinpol (around +2.5 kcalmol- 1) are not shown.

*Figure 2. Schematic orbital interaction diagrams: a) SOMO- SOMO interaction; b) SOMO- SOMO interaction in the presence of a lower-lying occupied orbital; c) X- Y bond with radical Y1 leading to a smaller ΔEoi stabilization; and d) radical Y1 leading to a larger ΔEoi stabilization.*

Chemistry—A European Journal

Communication doi.org/10.1002/chem.202103544

15617 Chem. Eur. J. 2021, 27, 15616–15622 www.chemeurj.org © 2021 The Authors. Chemistry - A European Journal published by Wiley-VCH GmbH


<!-- Source PDF page 3 -->

and 1 atm) and the ideal gas model for thermodynamic corrections. The spectrum of BDEs in our model systems reaches from 48.0 kcalmol- 1 for F- F till 148.6 kcalmol- 1 for the strongest polar bond, H3Si- F. Furthermore, the BDE increases from C- C to C- F (85.2 to 111.3 kcalmol- 1), and it decreases from C- F to C- Cl (111.3 to 80.9 kcalmol- 1). Clearly, bond strengths correlate with the electronegativity difference Δχ= jχX- χYj across the X- Y bond. This becomes even more obvious upon plotting BDEs as a function of the Pauling electronegativity χ of the main-group elements, X and Y, involved in the X- Y bonds,[8] in Figure 1. In some cases, such as, from C- C

to C- N (85.2 to 80.3 kcalmol- 1, see also Table 1), the simple trend of stronger BDE for larger Δχ is disturbed,[24] however, by and large it holds (vide infra). The question, now, is whether these correlations along periods and groups are causal, or not. Table S1 in the Supporting Information shows that the trends in ΔH are set by the electronic bond dissociation energies ΔE.[5,25] We analyze the bond energy ΔE associated with the bond formation process X

*+Y

*!X- Y using the activation strain model in which ΔE is decomposed into the strain energy ΔEstrain and the interaction energy ΔEint.[19a] The interaction energy ΔEint can be further decomposed using our

*Figure 3. a–b) Energy decomposition analysis, c–d) SOMO- SOMO overlap S SOMO SOMO j h i and energy gap Δɛ (in eV), and e–f) overlaps S between the highest occupied orbitals HOMO - 1 SOMO j h i and HOMO - 1 HOMO - 1 j h i in the A1 orbital interaction scheme (Figure S4), as a function of the bond distance of H3C- YHn (left) and H3Si- YHn (right) with YHn=F and Cl (equilibrium geometry indicated with a dot), computed at BLYP-D3(BJ)/TZ2P.*

15618 Chem. Eur. J. 2021, 27, 15616–15622 www.chemeurj.org © 2021 The Authors. Chemistry - A European Journal published by Wiley-VCH GmbH


<!-- Source PDF page 4 -->

EDA method (see Table 2 for H3C- CH3, H3C- F, and H3C- Cl), into the classical electrostatic interaction ΔVelstat, the Pauli repulsion ΔEPauli (the destabilizing interaction between occupied orbitals), the orbital interaction ΔEoi (accounts for electron-pair bonding by the SOMO- SOMO interaction, charge transfer, and polarization), the dispersion energy ΔEdisp, and the spin polarization ΔEspinpol.[19a] Full details for all HnX- YHn systems can be found in the Supporting Information, including an activation strain analysis, EDA, and a KS-MO analysis as function of the bond distance for the combinations of CH3

*, F

*, SiH3

* and Cl

*

(Figures S1–S3). The answer to our question, as revealed by our bonding analyses, is: No, along certain series of X- Y bonds, such as the carbon- halogen bonds (C- F to C- Cl), the correlation between BDE and Δχ is not causal but instead a side product of a different underlying mechanism. Along other series, such as the carbon-second-period-element bonds (C- C to C- F), the correlation is in fact confirmed to be causal. In the following, we guide the reader through our analyses to see how and why the electronegativity model breaks down in certain cases, strikingly, in those cases that are generally used to illustrate its validity, the carbon- halogen bonds.[4]

First, we examine the carbon- halogen bonds by comparing C- F and C- Cl in Table 2. The strain energy ΔEstrain, which results from the pyramidalization of the methyl fragment,[26] is small (6.3 and 5.9 kcalmol- 1), and, therefore, the bond weakening ΔE from - 115.3 to - 84.2 kcalmol- 1 is determined by ΔEint that becomes less stable from - 121.6 to - 90.0 kcalmol- 1. The orbital interaction ΔEoi that destabilizes from - 272.5 to - 167.4 kcalmol- 1 seems the causal factor, following the decrease in SOMO- SOMO gap Δɛ (7.44 to 3.88 eV), i.e., the decrease in electronegativity difference. Figures 2a and 2b show schematic representations of a SOMO- SOMO interaction. For H3C- F, the low-lying 2pσ SOMO on the halogen engages in a 2-center 3-electron interaction with the filled σC- H orbitals, which pushes up the σ-bonding orbital but effectively this does

not alter the trends (Figure 2b). Therefore, we could distill the orbital interaction scheme from C- F to C- Cl to Figure 2c, where the magnitude of the energy gap Δɛ determines ΔEoi, and thus the bond strength. Intriguingly, however, the bond weakening is not caused by ΔEoi, since, at any given bond distance, the latter is more stabilizing for C- Cl than for C- F (blue versus green striped lines in Figure 3a). The reason for this unexpected order in stabilization is a substantially better overlap S (Figure 3c, solid lines) of the comparatively diffuse CH3 SOMO with the valence npσ orbital of the heavier, and also more diffuse halogen Cl (Figure 4). The larger, more favorable SOMO- SOMO overlap for the C- Cl bond thus overrules the unfavorable decrease in energy gap (Figure 3c, dashed lines). We depict this schematically in Figure 2d, where the interaction with the smaller energy gap has now the largest ΔEoi stabilization (the X- Y1 bond) due to a larger bond overlap Sbond. Our analysis as a function of the bond distance reveals that the electronegativity model cannot be the reason for the stronger bond for C- F than for C- Cl as suggested in authoritative textbooks, for example, by Anslyn.[4]

But why does ΔEint, and thus the BDE, become weaker from C- F to C- Cl? The reason appears to be the increase in effective atom size of the halogen and, thus, the increase in Pauli repulsion ΔEPauli (Figure 3a) if one goes from F to Cl. The latter has spatially more extended occupied valence AOs which leads to an increase in the occupied- occupied overlap S (Figure 3e). Also, the heavier halogen has more subvalence shells which further raise the number of Pauli repulsive occupied- occupied orbital interactions. For example, at a consistent bond distance of 1.400 Å (Table 2), ΔEPauli increases from 264.9 to 567.6 kcalmol- 1 along C- F to C- Cl. This does not only make the carbon- halogen bond weaker but of course also pushes it to a longer equilibrium distance, from 1.413 Å for C- F to 1.820 Å for C- Cl (Figure 3a). Eventually, at this longer equilibrium distance, all energy terms are weaker. Interestingly, this leads to ΔEoi becoming less stabilizing at the respective equilibrium bond distances if we go from C- F to C- Cl (- 272.5 to - 167.4 kcalmol- 1, Table 2). Note that this trend ΔEoi at the equilibrium bond distances does not originate from the decrease in SOMO- SOMO gap Δɛ, and occurs despite an increase in bond overlap. It is a side effect of the increased ΔEPauli, and the resulting longer C- X bond, for the larger halogen. This trend, as well as the underlying mechanism, continues along the whole series of carbon-halogen bonds, with BDEs decreasing from 111.3 to 80.9 to 71.2 to 61.0 kcalmol- 1 along C- F, C- Cl, C- Br, and C- I (see Figures S5 and S6).[27,28]

The same mechanism is found for the silicon- halogen bonds. From Si- F to Si- Cl, the ΔEint becomes less stable from - 151.1 to - 105.6 kcalmol- 1, and the bond lengthens from 1.625 to 2.082 Å, respectively. Down the halogens, the ΔEoi in the Si- X bond (Figure 3b) becomes more stable due to the increase SOMO- SOMO overlap S, and despite the decrease in energy gap Δɛ (Figure 3d). Again, the increase in ΔEPauli from Si- F to Si- Cl (Figure 3b) is what determines the trend in bond strength (and length) because of the increase in occupied- occupied overlap S (Figure 3f) as well as the larger number of

*Figure 4. Contour plots of CH3*

*, F

*, SiH3

*, and Cl

* SOMOs (10 contour lines between 0.05, 1.0; scan values are evenly spaced; color represents phase), computed at BLYP-D3(BJ)/TZ2P.

15619 Chem. Eur. J. 2021, 27, 15616–15622 www.chemeurj.org © 2021 The Authors. Chemistry - A European Journal published by Wiley-VCH GmbH


<!-- Source PDF page 5 -->

subvalence shells in the case of the heavier halogen. Likewise, the series Cl- F to Cl- Cl and H- F to H- Cl (which augments work in Ref. [29]) reveal the same trends and mechanism (Figures S2, S3, and S7). The popular electronegativity model, however, does not break down in all cases. In particular, the trend in X- Y bond strength as one of the atoms runs along a period (instead of down a group) does indeed depend in a causal way on the trend in electronegativity (Figure 2c), but also on Pauli repulsive closed-shell interactions. For example, from C- C to C- F, the bond energy ΔE strengthens from - 92.1 to - 115.3 kcalmol- 1

(see Table 2) because of a corresponding trend in ΔEint

(strengthening from - 110.4 to - 121.6 kcalmol- 1), modulated by the strain energy ΔEstrain associated with pyramidalizing one or two methyl groups.[24,26] The strengthening in ΔEint from C- C to C- F is determined by both ΔEPauli and ΔEoi and somewhat counteracted by ΔVelstat (Figure 5a). The ΔEPauli becomes less repulsive along this series due to the smaller occupied valence atomic orbitals for fluorine, which decreases the occupied- occupied overlap S (Figure 5e). The ΔEoi becomes more stabilizing (Figure 5a), and is, especially at the C- F equilibrium, essential to overcome the destabilization in ΔVelstat. The stabilization in ΔEoi is caused by the larger, more favorable SOMO- SOMO gap Δɛ for the C- F bond (Figures 2c and 5c), and despite the reduction

*Figure 5. a–b) Energy decomposition analysis, c–d) SOMO- SOMO overlap S SOMO SOMO j h i and energy gap Δɛ (in eV), and e–f) overlaps S between the highest occupied orbitals HOMO - 1 SOMO j h i and HOMO - 1 HOMO - 1 j h i in the A1 orbital interaction scheme (Figure S4), as a function of the bond distance of H3C- YHn (left) and H3Si- YHn (right) with YHn=CH3 and F (equilibrium geometry indicated with a dot), computed at BLYP-D3(BJ)/TZ2P.*

15620 Chem. Eur. J. 2021, 27, 15616–15622 www.chemeurj.org © 2021 The Authors. Chemistry - A European Journal published by Wiley-VCH GmbH


<!-- Source PDF page 6 -->

in bond overlap that emerges from the aggravating mismatch in spatial extension between the SOMOs from C- C to C- F (Figure 4). Likewise, we find that the same trends and underlying bonding mechanism are active for the analogous series along a period, for example, along Si- C to Si- F bonds (Figure 5b, d, f), as well as for Si- Si to Si- Cl (Figures S2 and S3). We already mentioned that the simple trend of stronger BDE for larger Δχ is in some cases disturbed, notably from C- C to C- N, along which ΔE weakens, instead of strengthens, from - 92.1 to - 87.3 kcalmol- 1 (see Figure 1 for the irregularity). This anomaly is caused by the pyramidalization of either two or one methyl group(s) (C- C versus C- N).[24] The C- C bond experiences a stabilizing effect, since the cost of ΔEstrain upon pyramidalizing two methyl groups goes with an even larger relief of steric (Pauli) repulsion, as the C- H bonds of one methyl fragment bend away from the other fragment, and vice versa, causing the C- C bond to be stronger than the C- N bond. However, pyramidalization is a special case for methyl groups, and does not, or to a lesser extent, occur for other fragments that are already pyramidal, such as SiH3,[26] or that have lone-pair orbitals at the central atom that do not contain substituents to bend away, for instance for NH2, OH, or F.[24]

In conclusion, we have shown that the correlation between the electron-pair bond strength and the electronegativity difference across the bond is not always causal. One of the striking exceptions is the series of carbon- halogen bonds which, ironically, is a popular, but erroneous as we show, example in textbooks for illustrating the aforementioned electronegativity model. Instead, we show that the carbon- halogen bond weakens from C- F to C- I because of an increasing steric (Pauli) repulsion with the effectively larger atom size and electron-richer heavier halogen atoms. This bond weakening from C- F to C- I occurs despite an orbital interaction which, at any given bond distance, becomes stronger, not weaker, because of an increasing bond overlap between the relatively diffuse methyl SOMO and the increasingly diffuse halogen np SOMO. Interestingly, it is the buildup of Pauli repulsion that, for heavier halogens, pushes the C- X bond to a longer equilibrium bond distance at which the orbital interaction becomes weaker, thus, establishing the non-causal correlation with the decreasing electronegativity difference. Finally, our work also shows that, for a full understanding of the causalities in a bonding mechanism, it is crucial to carry out the bonding analyses as a function of the bond formation process.

## Acknowledgements

We thank the Advanced Research Center Chemical Building Blocks Consortium (ARC CBBC; grant 2018.019.B), the Netherlands Organization for Scientific Research (NWO) and the Spanish MINECO (PID2019-106830GB-I00 and MDM-2017-0767) for financial support.

## Conflict of Interest

The authors declare no conflict of interest.

Keywords: Bond energy · Bond theory · Density functional calculations · Main group elements · Thermochemistry

[1] M. B. Smith, March’s Advanced Organic Chemistry: Reactions, Mechanisms, and Structure, 8th ed., Wiley, New York 2019. [2] J. Clayden, N. Greeves, S. Warren, Organic Chemistry, 2nd ed., Oxford University Press, Oxford 2012. [3] T. A. Albright, J. K. Burdett, M.-H. Whangbo, Orbital Interactions in Chemistry, 2nd ed., Wiley, New York 2013. [4] E. V. Anslyn, D. A. Dougherty, Modern Physical Organic Chemistry, University Science Books, Sausalito 2006. [5] P. W. Atkins, J. de Paula, Physical Chemistry, 9th ed., W. H. Freeman, New York 2010. [6] a) O. Mó, M. Yáñez, M. Eckert-Maksić, Z. B. Maksić, I. Alkorta, J. Elguero, J. Phys. Chem. A 2005, 109, 4359; b) B. Chan, L. Radom, J. Phys. Chem. A 2012, 116, 4975. [7] a) E. Kraka, D. Setiawan, D. Cremer, J. Comput. Chem. 2016, 37, 130; b) M. Kaupp, B. Metz, H. Stoll, Angew. Chem. Int. Ed. 2000, 39, 4607; c) C. Esterhuysen, G. Frenking, Theor. Chem. Acc. 2004, 111, 381. [8] a) L. Pauling, The Nature of the Chemical Bond, 3rd ed., Cornell University Press, New York 1960; b) A. L. Allred, J. Inorg. Nucl. Chem. 1961, 17, 215. [9] K. B. Wiberg, P. R. Rablen, J. Am. Chem. Soc. 1993, 115, 9234. [10] L. Deng, V. Branchadell, T. Ziegler, J. Am. Chem. Soc. 1994, 116, 10645. [11] J. W. Ochterski, G. A. Petersson, K. B. Wiberg, J. Am. Chem. Soc. 1995, 117, 11299. [12] N. Matsunaga, D. W. Rogers, A. A. Zavitsas, J. Org. Chem. 2003, 68, 3158. [13] M. L. Coote, A. Pross, L. Radom, Org. Lett. 2003, 5, 4689. [14] A. Hou, X. Zhou, T. Wang, F. Wang, J. Phys. Chem. A 2018, 122, 5050. [15] a) C. Tantardini, A. R. Organov, Nat. Commun. 2021, 12, 2087; b) C. Tantardini, A. R. Organov, Nat. Commun. 2021, 12, 3300. [16] A. Rauk, Orbital Interaction Theory of Organic Chemistry, 2nd ed., Wiley, New York 2001. [17] R. Kalescky, W. Zou, E. Kraka, D. Cremer, J. Phys. Chem. A 2014, 118, 1948. [18] a) G. te Velde, F. M. Bickelhaupt, E. J. Baerends, C. Fonseca Guerra, S. J. A. van Gisbergen, J. G. Snijders, T. Ziegler, J. Comput. Chem. 2001, 22, 931; b) C. Fonseca Guerra, J. G. Snijders, G. te Velde, E. J. Baerends, Theor. Chem. Acc. 1998, 99, 391; c) ADF2017, SCM, Theoretical Chemistry, Vrije Universiteit Amsterdam (The Netherlands), http:// www.scm.com. [19] a) F. M. Bickelhaupt, E. J. Baerends, in Reviews in Computational Chemistry, (Eds.: K. B. Lipkowitz, D. B. Boyd), Wiley-VCH, Hoboken 2000, pp 1–86; b) T. A. Hamlin, P. Vermeeren, C. Fonseca Guerra, F. M. Bickelhaupt, in Complementary Bonding Analysis (Ed: S. Grabowsky), De Gruyter, Berlin 2021, pp 199–212; c) T. Ziegler, A. Rauk, Theor. Chim. Acta 1977, 46, 1; d) T. Ziegler, A. Rauk, Inorg. Chem. 1979, 18, 1755. [20] a) W.-J. van Zeist, C. Fonseca Guerra, F. M. Bickelhaupt, J. Comput. Chem. 2008, 29, 312; b) X. Sun, T. M. Soini, J. Poater, T. A. Hamlin, F. M. Bickelhaupt, J. Comput. Chem. 2019, 40, 2227. [21] a) A. D. Becke, Phys. Rev. A. 1988, 38, 3098; b) C. T. Lee, W. T. Yang, R. G. Parr, Phys. Rev. B. 1988, 37, 785; c) S. Grimme, J. Antony, S. Ehrlich, H. Krieg, J. Chem. Phys. 2010, 132, 154104; d) S. Grimme, S. Ehrlich, L. Goerigk, J. Comput. Chem. 2011, 32, 1456; e) E. van Lenthe, E. J. Baerends, J. Comput. Chem. 2003, 24, 1142. [22] a) E. van Lenthe, E. J. Baerends, J. G. Snijders, J. Chem. Phys. 1993, 99, 4597; b) E. van Lenthe, E. J. Baerends, J. G. Snijders, J. Chem. Phys. 1994, 101, 9783. [23] OH

*, SH

*, F

* and Cl

* were computed in their correct valence state involving one singly occupied molecular orbital and otherwise closed shells, for example, fluorine (1s)2(2s)2(2px)2(2py)2(2pz)1. [24] For a detailed discussion on the anomaly in the trend in bond strength from C- C to C- N, see: W.-J. van Zeist, F. M. Bickelhaupt, Phys. Chem. Chem. Phys. 2009, 11, 10317. [25] F. Jensen, Introduction to Computational Chemistry, Wiley, New York 2007. [26] F. M. Bickelhaupt, T. Ziegler, P. v. R. Schleyer, Organometallics 1996, 15, 1477.

15621 Chem. Eur. J. 2021, 27, 15616–15622 www.chemeurj.org © 2021 The Authors. Chemistry - A European Journal published by Wiley-VCH GmbH


<!-- Source PDF page 7 -->

[27] Computed at BLYP-D3(BJ)/TZ2P for H3C- F and H3C- Cl and ZORA-BLYP- D3(BJ)/TZ2P for H3C- Br and H3C- I. [28] Augments work provided in: a) G. Frenking, F. M. Bickelhaupt, in The Chemical Bond: Fundamental Aspects of Chemical Bonding (Eds: G. Frenking, S. Shaik), Wiley-VCH, Hoboken 2014, pp. 121–157; b) F. M. Bickelhaupt, H. L. Hermann, G. Boche, Angew. Chem. Int. Ed. 2006, 45, 823.

[29] D. Devarajan, S. J. Gustafson, F. M. Bickelhaupt, D. H. Ess, J. Chem. Educ. 2015, 92, 286.

Manuscript received: September 30, 2021 Accepted manuscript online: October 5, 2021 Version of record online: October 19, 2021

15622 Chem. Eur. J. 2021, 27, 15616–15622 www.chemeurj.org © 2021 The Authors. Chemistry - A European Journal published by Wiley-VCH GmbH

