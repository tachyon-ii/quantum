---
title: "Magnetic Moments of Astrophysical Neutrinos"
author: "Joachim Kopp, Toby Opferkuch, and Edward Wang"
source_file: "kopp-et-al-magnetic-moments-astrophysical-neutrinos.pdf"
pages: 22
---

# Magnetic Moments of Astrophysical Neutrinos

**Joachim Kopp, Toby Opferkuch, and Edward Wang**

> **Conversion note.** This is an editable Markdown transcription of the supplied PDF. Paragraphs, headings, captions, references, and machine-readable tables are retained where the PDF text layer allows. Displayed mathematics that cannot be reconstructed reliably from the text layer is preserved as a fixed-width extraction rather than silently altered. For exact checking of equations, figures, tables, typography, and reading order, use the complete Markdown package supplied alongside this file.

<!-- Source PDF page 1 -->

### CERN-TH-2022-213, MITP-22-110, TUM-HEP-1448/22

### Magnetic Moments of Astrophysical Neutrinos

Joachim Kopp,1, 2, a Toby Opferkuch,3, 4, b and Edward Wang5, c

1Theoretical Physics Department, CERN, 1 Esplanade des Particules, 1211 Geneva 23, Switzerland 2PRISMA Cluster of Excellence & Mainz Institute for Theoretical Physics, Johannes Gutenberg University, Staudingerweg 7, 55099 Mainz, Germany 3Berkeley Center for Theoretical Physics, University of California, Berkeley, CA 94720 4Theoretical Physics Group, Lawrence Berkeley National Laboratory, Berkeley, CA 94720 5Physik Department T70, Technische Universit¨at M¨unchen, James-Franck-Straße, 85748 Garching, Germany

We study the impact of neutrino magnetic moments on astrophysical neutrinos, in particular supernova neutrinos and ultra-high energy neutrinos from extragalactic sources. We show that magnetic moment-induced conversion of Dirac neutrinos from left-handed states into unobservable righthanded singlet states can substantially change the flux and flavour composition of these neutrinos at Earth. Notably, neutrinos from a supernova’s neutronisation burst, whose flux can be predicted with O(10%) accuracy, offer a discovery reach to neutrino magnetic moments ∼few × 10−13 µB, up to one order of magnitude below current limits. For high-energy neutrinos from distant sources, for which no robust flux prediction exists, we show how the flavour composition at Earth can be used as a handle to establish the presence of non-negligible magnetic moments, potentially down to few × 10−17 µB if the measurement can be performed on neutrinos from a single source. In both cases, the sensitivity strongly depends on the galactic (intergalactic) magnetic field profiles along the line of sight. Therefore, while a discovery is possible down to very small values of the magnetic moment, the absence of a discovery does not imply an equally strong limit. We also comment on the dependence of our results on the right-handed neutrino mass, paying special attention to the transition from coherent deflection by a classical magnetic field to incoherent scattering on individual scattering targets. Finally, we show that a measurement of Standard Model Dirac neutrino magnetic moments, of order 10−19 µB, could be possible under rather optimistic, but not completely outrageous, assumptions using flavour ratios of high-energy astrophysical neutrinos.

## 1 INTRODUCTION

In 1970, Cisneros [1] first proposed the neutrino magnetic moment as an explanation for the solar neutrino problem. Since magnetic moments convert left-handed particles into right-handed ones in the presence of a magnetic field, and since right-handed neutrinos cannot be detected, such conversion leads to an apparent deficit in the measured neutrino flux. While it is now known that this deficit is due to neutrino mass mixing rather than neutrino magnetic moments, conversion between left-handed and right-handed neutrinos is still a powerful tool to constrain, or better yet, discover, neutrino magnetic moments. In the simplest extension of the Standard Model including right-handed neutrino fields, the neutrino magnetic moment, µν, is [2]

```text
µν = 3eGF mν
```

```text
8
√
```

```text
2π2
≈3 × 10−19µB
 mν
```

## 1 eV

```text

,
(1)
```

where mν is the neutrino mass, e is the electric charge unit, GF is the Fermi constant, and µB = e/(2me) is the Bohr magneton, with me the electron mass. So far, neutrino magnetic moments have proven too small to

a jkopp@cern.ch b tobyopferkuch@berkeley.edu

c edward.wang@tum.de

be detectable, but numerous constraints have been derived from neutrino experiments [3, 4] as well as from astrophysical [5–10] and cosmological arguments [11–17]. While these constraints still fall several orders of magnitude short of probing magnetic moments as small as in eq. (1), they are highly relevant to theories beyond the Standard Model, where µν can take values that saturate current constraints [15, 18–20]. More recently, large neutrino magnetic moments have been proposed in relation to experimental anomalies, notably the XENON1T electron excess [15, 21–23] which has since gone away [24], the muon g −2 anomaly [25], and various B physics anomalies [15]. In this paper, we will investigate the role magnetic moments play in the propagation of astrophysical neutrinos through galactic and intergalactic magnetic fields. We will consider the case of Dirac neutrinos, for which standard flavour oscillations and magnetic moment-induced spin precession can be decoupled. Majorana neutrinos, in contrast, for which only flavour off-diagonal magnetic moments are allowed, would experience coupled spin– flavour precession, and since interstellar and intergalactic magnetic fields as well as neutrino magnetic moments are small, only negligible corrections to standard flavour oscillations are expected in this case. For the case of O(10 MeV) neutrinos from a supernova explosion, we will show that the reduction in the detectable neutrino flux due to a magnetic moment-induced helicity flip can be large enough to be detectable for magnetic moments that are up to an order of magnitude below current limits. This is true in particular

*arXiv:2212.11287v3 [hep-ph] 25 Mar 2024*


<!-- Source PDF page 2 -->

for neutrinos from the neutronisation burst that happens early on in the explosion [26] because the corresponding flux can be robustly predicted with an uncertainty of only O(10%) [27–30]. In a recent paper [31], Jana et al. have studied future supernova constraints on neutrino magnetic moments as well. However, their interest was in transitions magnetic moments between active neutrino flavours, whereas we focus on magnetic moment-induced conversion between active (left-handed) and sterile (right-handed) neutrinos, relevant for instance in scenarios with Dirac neutrino mass terms. The authors of ref. [31] have considered neutrino flavour conversion in the source’s magnetic field, whereas will be mainly concerned with interstellar magnetic fields. We will explain in section 4.1 why source magnetic fields are unimportant for us, and why interstellar magnetic fields are unimportant in ref. [31]. In the second part of the paper, we will focus on O(TeV) neutrinos from cosmic ray accelerators, which may experience a similar helicity flip during propagation. However, as there is no robust prediction for their initial flux, the resulting flux reduction is undetectable. Nevertheless, if magnetic moments are flavour non-universal, the disappearance of only some neutrino flavours may be detectable in measurements of neutrino flavour ratios. The structure of this paper is as follows: in section 2 we introduce the notation and present approximate analytic results for the conversion probability from left-handed to right-handed neutrinos in a magnetic field. In section 3 we describe the properties of interstellar and intergalactic magnetic fields pertinent to our study. In section 4 we then discuss the neutrino flux from supernovae, in particular during the neutronisation phase, and apply the results from sections 2 and 3 to this flux. This allows us to estimate the discovery reach for neutrino magnetic moments in DUNE and Hyper-Kamiokande. We then move on in section 5 to ultra-high energy neutrinos detectable at neutrino telescopes, where in particular flavour nonuniversal magnetic moments can dramatically affect the observed flavour ratios. We finally broaden our discussion in section 6 to comment on the prospects of detecting neutrino magnetic moments as small as in the Standard Model, and to elaborate on how the mass of the righthanded neutrinos affects our results. In this context, we discuss the transition from coherent deflection by a classical magnetic field to hard scattering on individual electrons/nuclei in the interstellar medium. We conclude in section 7. All numerical codes used in this paper, as well as all plots, can be found on GitHub [32].

## 2 NEUTRINO MAGNETIC MOMENTS

Neutrino magnetic moments are described by the operator

```text
L ⊃ˆµαβ
ν
2 Fµν ¯να
LσµνN β
R + h.c.,
(2)
```

where να L is the left-handed neutrino field of flavour α, N β R are right-handed neutrino fields, and Fµν is the electromagnetic field strength tensor. In the case of Majorana neutrinos, NR can be the charge conjugate of a left-handed neutrino field, N β R = (νβ)c. In this case, the CPT-symmetry mandates that the magnetic moments of particles and antiparticles have opposite signs, meaning that the magnetic moment matrix ˆµ is antisymmetric and, in particular, that its diagonal components vanish. While the numerical results we present in sections 4 and 5 will be applicable only to Dirac neutrinos (as competitive limits arise only in this scenario), we will keep the discussion in this section general and include also the Majorana case. As usual, the neutrino flavour eigenstate fields να L are related to their mass eigenstate counterparts, νi, according to

```text
να = Uαiνi ,
(3)
```

where

```text
U =
```



 1 c23 s23 −s23 c23







 c13 s13eiδ

## 1 −s13eiδ c13







 c12 s12 −s12 c12 1





is the leptonic mixing matrix. It depends on the neutrino mixing angles θij through sij ≡sin θij, cij ≡cos θij, and on the CP-violating phase δ. The flavour evolution of a neutrino is governed by the Schr¨odinger equation

i d

```text
dtψ(t) = ˆHψ(t) ,
(4)
```

where ψ is a unit vector in flavour space whose components describe the admixture of each flavour to the neutrino state. Thus, for the case of three right-handed states, ψ = (νe, νµ, ντ, N e R, N µ R, N τ R). In this case, a pure νµ would be described by the vector ψ = (0, 1, 0, 0, 0, 0). If neutrinos travel along the z-axis through a magnetic field B, the Hamiltonian in the flavour basis can be written in block-diagonal form as1

```text
ˆH = 1
```

2p

 U U

```text
  ˆ
M 2
ν
ˆ
M 2
N
```

  U †

U †



+ 1

2

```text

0
B⊥eiϕˆµν
B⊥e−iϕˆµ†
ν
0
```

```text

,
(5)
```

with the neutrino momentum p, the diagonal mass matrices

```text
ˆ
Mν = diag(mν1, mν2, mν3) ,
(6)
ˆ
MN = diag(mN1, mN2, mN3) ,
(7)
```

1 This can be most easily seen by direct evaluation of eq. (2), choosing a particular representation for the spinors and γ matrices.


<!-- Source PDF page 3 -->

and the general magnetic moment matrix (with the individual entries in this matrix labelled using the notation defined in eq. (2))

```text
ˆµν =
```



```text

µee
ν
µeµ
ν
µeτ
ν
µµe
ν
µµµ
ν
µµτ
ν
µτe
ν
µτµ
ν
µττ
ν
```



```text
.
(8)
```

We have written the components of the magnetic field perpendicular to the neutrino’s direction of travel in terms of B⊥≡ q

```text
B2x + B2y and ϕ ≡arctan(Bx/By).2
```

If the magnetic field direction is constant along the line of sight, the phase ϕ is unphysical. For spatially varying magnetic fields, however, it is important as we will discuss below. As astrophysical neutrinos propagate as mass eigenstates,3 it is useful to rotate ˆH to the mass basis

```text
ˆH = 1
```

2p

```text
 ˆ
M 2
ν
ˆ
M 2
N
```

 + 1

2

```text

0
B⊥eiϕˆ˜µν
B⊥e−iϕˆ˜µ†
ν
0
```

```text

,
(9)
```

where ˆ˜µν ≡U †ˆµνU. While numerically solving eq. (4) is straightforward, deriving an approximate analytic solution provides additional insight. Utilising the two-flavour approximation—considering only one left-handed neutrino, νL, and one right-handed neutrino, NR, with a transition magnetic moment µν—and under the assumption of a uniform magnetic field, we ascertain the conversion probability to be

```text
PνL→NR(µν; t) =
4p2µ2
νB2
⊥
(∆m2
Nν)2 + 4p2µ2νB2
⊥
```

sin2 p

```text
(∆m2
Nν)2 + 4p2µ2νB2
⊥
4p
t

,
(10)
```

with ∆m2 Nν = m2 N−m2 ν. Before discussing the conditions under which the two-flavour approximation is useful, let us first interpret eq. (10). Both the oscillation amplitude and the oscillation phase are governed by the interplay of the frequency ∆m2 Nν/(2p) and the magnetic moment interaction, µνB⊥. In the case of mN = mν (Dirac neutrinos), the oscillation amplitude becomes maximal, and

2 The longitudinal component of B is unimportant here as can be seen from the transformation of the magnetic field to the neutrino’s rest frame. For ultra-relativistic neutrinos, B⊥in the rest frame is enhanced by a relativistic γ-factor, while the longitudinal component, B∥, is not. 3 This can be understood by considering that the oscillation lengths corresponding to standard flavour oscillations are much shorter than the typical distances that astrophysical neutrinos travel. Neighbouring oscillation maxima are therefore extremely close in energy and cannot be resolved by the detector. In the mass basis, the off-diagonal elements of the density matrix describing the observed neutrino flux therefore average to zero, implying an incoherent statistical mixture of mass eigenstates.

the conversion probability reduces to

```text
PνL→NR(µν; t)
∆m2
Nν→0
−−−−−−−→sin2 µνB⊥t
```

## 2 . (11)

In the opposite limit, ∆m2 Nν/(2p) ≫ µνB⊥, lefthanded and right-handed neutrinos oscillate into one another with a frequency determined by their masses, ∆m2 Nν/(4p). The oscillation amplitude, however, becomes very small in this limit. These observations already hint at one of the reasons why the two-flavour approximation is useful: in the case of Dirac neutrinos, conversion between the lefthanded and right-handed components of the same Dirac spinor have maximal amplitude, while transitions between states of different mass are strongly suppressed. If the magnetic moment matrix ˆ˜µ in eq. (9) is diagonal in the mass basis, standard flavour oscillations and magnetic moment-induced conversion between left-handed and right-handed states decouple completely. But even for non-zero flavour off-diagonal magnetic moments, the mixing between different Dirac neutrino mass eigenstates during propagation is negligible given the weakness of large-scale magnetic fields in the Universe and the strong constraints on neutrino magnetic moments. In other words, Dirac neutrinos that form an incoherent ensemble of mass eigenstates will predominantly experience mixing only between the two Weyl components of each mass eigenstate and mixing between different mass eigenstates is negligible. (We have explicitly verified this numerically.) The description in terms of an incoherent ensemble of mass eigenstates is always appropriate for astrophysical neutrinos. First because the size of the neutrino production region is typically similar in size to, or larger than, the oscillation length, and second because any coherence between mass eigenstates will quickly be lost during propagation as wave packets separate.4

The above discussion also illustrates in more detail why the methods discussed in this paper are suitable only for constraining magnetic moments of Dirac neutrino (and even for those only the diagonal components of the magnetic moment matrix in the mass basis), not those of Majorana neutrinos. For astrophysical Majorana neutrinos propagating as an incoherent ensemble of mass eigenstates, the small magnetic moment-induced changes in the mixing between these mass eigenstates will be negligible compared to standard three-flavour mixing.

4 Note that wave packet separation between the two components of a Dirac neutrino due to energy splitting in the magnetic field is not an issue. The velocity difference between two states of mass m and energies E and E + ∆E is ∆v = m2∆E/(E2√

E2 −m2), and the distance by which the energy eigenstate wave packets get separated after travelling a distance L is ∆x = L ∆v. This difference is much smaller than even the most conservative estimate for the neutrino wave packet size (σx ∼1 ˚A) for both supernova neutrinos (E ∼30 MeV, L ∼10 kpc) and ultra-high-energy neutrinos (E ≳1 TeV, L ∼Gpc).


<!-- Source PDF page 4 -->

The other approximation entering eq. (10), namely that of constant B-field, is typically not applicable to astrophysical environments (see section 3 below for a detailed discussion). It is still useful for obtaining orderof-magnitude estimates, though. To go beyond these, eq. (4) needs to be integrated numerically, which is what we will do in sections 4 and 5 using the Python packages QuTiP v4.7.0 [33, 34], SciPy 1.7.1 [35], and NumPy v1.19.5 [36]. (For propagation in turbulent magnetic fields, we also outline in appendix C a numerical shortcut based on the stochastic nature of the problem.) Analytical insights can still be gained in some special cases. One such useful case arises if only the magnitude of the transverse magnetic field changes, but not its direction The oscillation probability in the limit µνB⊥≫∆m2 Nν/(2p) is

```text
PνL→NR(µν; t)|ϕ=const ≃sin2
µν
```

2

Z L

## 0 dx B⊥(x)  , (12)

which can be understood as a generalisation of eq. (11). Of course, in reality, both the magnitude and the direction of the field are expected to vary. For further theoretical considerations and phenomenological implications of the neutrino magnetic moment, see refs. [37–41] and references therein.

## 3 INTERSTELLAR AND INTERGALACTIC MAGNETIC FIELDS

The neutrino magnetic moment will interact with the magnetic fields it encounters as it propagates. For supernova burst neutrinos, which are detectable in large numbers only from within the Milky Way, we need to model the galactic magnetic field, whereas for high-energy astrophysical neutrinos, which mostly come from outside our galaxy, extragalactic magnetic fields are more important due to their huge travel distance.

## 3.1 The Milky Way’s Magnetic Field

The Milky Way’s magnetic field has both a large-scale component that is coherent on length scales of order kpc, and a small-scale component that is turbulent [42–46]. The large-scale magnetic field tends to follow the spiral arms of our galaxy. To describe this, one defines the pitch

```text
p = arctan
 Br
```

Bϕ

```text

,
(13)
```

where Br is the radial component of the magnetic field in the galactic plane, and Bϕ is its azimuthal component. The shape of the Milky Way’s spiral arms is welldescribed by a logarithmic spiral, that is, by a parametric curve of the form r ∝ekϕ, where r and ϕ are polar coordinates in the galactic plane and k is a constant. Such a curve is characterised by a constant pitch p = arctan k.

```text
−15
−10
−5
0
5
10
15
x [kpc]
```

−15

−10

−5

0

5

10

15

```text
y [kpc]
```

L

```text
⃗B [µG]
```

−2

−1

0

1

2

*FIG. 1. The coherent component of the Milky Way’s magnetic field according to the model from ref. [47] which we adopt here. We indicate the log-spirals delineating the Milky Way’s spiral arms, with the shading indicating the magnetic field strength. Shades of blue indicate magnetic fields pointing in the counterclockwise direction, while shades of orange/red indicate fields pointing clockwise. The location of our solar system is indicated by the cyan ⊕symbol. Note that this figure is rotated by 90 degrees clockwise compared to fig. 4 of ref. [47].*

For the Milky Way, estimates for p vary between −5◦and −30◦, and the strength of the coherent magnetic field is 1.5–2 µG in the solar neighbourhood and increases towards the Galactic Centre [44]. As a “fiducial” model for the large-scale galactic magnetic fields, we will use the one from ref. [47] (see refs. [48– 50] for alternative models), which divides the Milky Way into seven regions delimited by eight logarithmic spiral curves, as shown in fig. 1. The starting point of each spiral is set at a galactic radius of 5 kpc. The central 3 kpc are assumed to be free of large-scale fields, and between galactic radii of 3 kpc and 5 kpc the field is proportional to 1/r and oriented azimuthally. In the seven spiral-shaped regions, the field strength follows a 1/r law as well, but with a different coefficient in each region. The field is oriented tangentially to the logarithmic spiral curves. To account for uncertainties in the large-scale galactic magnetic field, we will also consider scenarios in which the coefficient of the 1/r law in each domain of the model is chosen randomly according to a Gaussian of width 1 µG, centred at zero magnetic field. The turbulent component of the Milky Way’s magnetic field can be characterised by its spectral density function, P(k), which describes how the energy stored in the field is distributed across eddies at different scales k. It is defined implicitly in terms of the two-point correlation


<!-- Source PDF page 5 -->

function as

```text
⟨B(X + ∆X)B(X)⟩=
Z
d3k eikXP(k) .
(14)
```

Note that we assume here large-scale isotropy and homogeneity, so that P(k) depends only on k ≡|k|, but not on any angular variables. It is easy to see that P(k) = | ˜B(k)|2, where ˜B(k) is the three-dimensional Fourier transform of B(X). It is reasonable to assume that, similar to innumerable other turbulent phenomena in astrophysics and elsewhere, the turbulent magnetic fields in the Milky Way obey Kolmogorov’s theory of turbulence [51], which stipulates that the energy carried by eddies at scale k is proportional to k−5/3. This implies that P(k) scales as

```text
P(k) ∝k−11/3 .
(15)
```

The spectral density function follows this scaling at scales smaller than some cutoff, which is between a few parsec to 100 pc [44]. The magnitude of turbulent galactic magnetic fields is of order few µG [44]. For our fiducial model, we choose the cutoff of Kolmogorov scaling at 10 pc, and the magnitude of the field at 2 µG. We divide the frequency domain into 1000 equidistant bins and choose the power in each of them according to a Gaussian distribution with width given by eq. (15) and centred at zero. The phase in each bin is chosen randomly between zero and 2π. We then apply a Fast Fourier Transform to obtain the (discretised) magnetic field configuration along the line of sight. We normalise this field configuration such that the root-meansquare magnetic field strength is 2 µG. This field configuration is then added to the large-scale magnetic field whose modelling has been discussed above, and fed into the evolution equation, eq. (9). To account for uncertainties, we consider a large number of field configurations randomly generated with this method, and we also vary the cutoff between 1 pc and 100 pc, and the root-meansquare field strength according to a Gaussian distribution with a width of 5 µG. Much of our knowledge about galactic magnetic field is derived from measurements of Faraday rotation [52] of radio waves. When linearly polarised electromagnetic waves cross a magnetised medium, the polarisation angle changes proportional to λ2 R ds ne(s)B∥(s), where λ is the photon wavelength, ne(s) is the electron number density, B∥(s) is the magnetic field component parallel to the photon momentum, and the integral runs along the line of sight. The integral also defines the so-called “rotation measure” or RM (up to an O(1) constant). Suitable sources for RM studies include pulsars as well as extragalactic sources such as quasars or fast radio bursts. As the polarisation angle of the source is not known, the λ- dependence of Faraday rotation is used to extract the RM from observations of the photon polarisation at different wavelengths.

## 3.2 Extragalactic Magnetic Fields

Relatively little is known about magnetic fields in between galaxies [45, 52]. Inside galaxy clusters, observations of diffuse radio emission and of the polarised photons from radio sources seen through a cluster provide clues and point towards field strengths of order µG (with O(1) uncertainties) [52]. There are also more indirect ways of constraining intracluster fields using the (non)observation of x-rays from inverse Compton scattering induced by the high-energy electron population needed to explain the observed synchrotron emission [53]. The lower limits on |B| derived in this way are roughly consistent with the values derived from diffuse radio emission and from the radiation measure of radio sources seen through a cluster. Observations also indicate that intracluster fields should be irregular and feature abundant small-scale structures. Evidence for magnetic fields outside of galaxy clusters is scarce [52] and partly contradictory. On the one hand, synchrotron emission from a region in between galaxy clusters suggests a magnetic field of order 0.2– 0.6 µG [54–56], which would be only an order of magnitude lower than galactic magnetic fields. On the other hand, the dependence of sources’ rotation measures on redshift suggests intergalactic magnetic fields cannot be larger than O(nG) [57]. Weak lower limits on extragalactic magnetic fields of order |B| ≳10−16 G to 10−13 G can also be derived from gamma-ray observations of blazars, see ref. [52] and references therein. High-energy primary photons from such objects should undergo secondary interactions in the intergalactic medium, leading to electromagnetic cascades (elongated over astrophysical distance scales) and thus to secondary gamma-ray emission at lower energies. The non-observation of this lower-energy emission can be understood by arguing that secondary electrons and positrons are deflected away from the line of sight by magnetic fields. A possible game-changer in the study of extragalactic magnetic fields are fast radio bursts (FRBs) [58– 60]. They are observable out to very large redshifts, and a large sample has recently become available from the CHIME/FRB collaboration [61]. Individual FRBs have already been used to derive constraints on the order of |B| < few × 10 nG [62, 63]. We define our fiducial model of intergalactic magnetic fields in the same way as the one for turbulent galactic magnetic fields. However, we divide the line of sight into three regions, corresponding to propagation through the galaxy cluster in which the source is located, the intercluster space, and our local galaxy cluster. The travel distance within each cluster is taken to be 10 Mpc, while the total distance is varied between 0.1 and 5 Gpc. We set the outer cutoff of the Kolmogorov spectrum to 1 Mpc within galaxy clusters, and to 10 Mpc outside. The rootmean-square strength of the intracluster fields is drawn from a normal distribution with a width of 1 µG, while for the intercluster fields we use a width of 5 nG.


<!-- Source PDF page 6 -->

## 4 SUPERNOVA NEUTRINOS

## 4.1 General Considerations

In this section we demonstrate how neutrinos from the neutronisation (or deleptonisation) burst phase of a galactic core-collapse supernova can be used to probe neutrino magnetic moments. The neutronisation burst proceeds, as the name suggests, largely through the process e−+p →νe +n. The neutrinos are initially trapped, but leak out of the supernova core in the first ∼20 ms after core bounce. During this phase, the luminosity reaches a spectacular 1053 erg/sec. In contrast to neutrinos from the subsequent accretion and cooling phases, the emission during the neutronisation burst is dominated completely by the production of νe-flavoured neutrinos [26, 28, 29]. The crucial point for us is that the νe flux emitted during the neutronisation burst can be fairly well predicted (at the 10% level) as the properties of a stellar core at the point where it reaches the Chandrasekhar threshold and collapses are similar in all core-collapse supernovae [30]. This means that a moderate deficit of neutrinos, caused by their conversion into invisible right-handed states due to a magnetic moment, could be observable. Whether the νL deficit is large enough to be detected depends on the interplay of the mass squared difference ∆m2 Nν and the magnetic potential µνB⊥, in combination with the neutrinos’ typical travel distance, L ∼10 kpc, and their O(10 MeV) energy. As stated in section 2 we will focus on the case of pure Dirac neutrinos where ∆m2 Nν = 0 for two main reasons: (i) This trivially satisfies the requirement that the amplitude of the magnetic moment induced oscillations are large ∆m2 Nν/(µ2 νB2 ⊥) ≲1, c.f. eq. (10). (ii) It removes the dependence of the oscillation frequency on the momentum of the neutrino, see eq. (11). Before turning to simulations we can estimate the range of µν where observable effects occur. Given the amplitude is maximised, we must simply study the oscillation length, which from eq. (11) is Lconv = 2π/(µνB⊥). This implies that only a certain range of µν can be probed for fixed values of L and B⊥. The lower limit arises from the requirement that the oscillation phase is not vanishingly small, while an upper limit occurs from requiring L ≲Lconv, yielding µν ∈[3, 70] × 10−14µB. This range assumes a constant magnetic field with B⊥= µG and L = 10 kpc. Note that, throughout our discussion, we neglect νL ↔ NR conversion inside the exploding star. At first, this might seem surprising, given that magnetic fields outside a supernova core can reach 1010 G, so according to eq. (11) we could expect sensitivity to µν ≲10−14 µB from conversion in the supernova core alone. However, the large matter density in and around the supernova core suppresses νL ↔NR oscillations via the Mikheyev– Smirnov–Wolfenstein (MSW) effect [64–66]. The MSW potential generated by coherent forward scattering of neutrinos on ambient nucleons and electrons, |VMSW| ∼

GF nn, where nn is the ambient neutron density, affects νL but not NR. It therefore produces a large contribution to the upper left block of the Hamiltonian in eqs. (5) and (9), thus suppressing the effective mixing angle between νL and NR. In this case resonant transitions are nevertheless possible [67–69], particularly if the MSW potential for electron neutrinos VMSW ∼GF (ne −nn/2) is small. However, in our simulations we do not find regions inside the SN where these resonant transitions are relevant.5 Note that this is different from the situation discussed for instance in refs. [67, 70–75], as well as the recent ref. [31], where magnetic moment-induced νL ↔NR conversions are a dominant effect. This is because the authors of [31] are interested in transition magnetic moment between different active Majorana neutrino flavours. The MSW potential is approximately the same for all active neutrino species, so its effect cancels out to high accuracy. Lastly, we also ignore any possible effects arising from the rotation of the magnetic field [76–78]. A recent paper [79] studies these effects for SN with extremely strong magnetic fields at the surface of the Iron core. Resonant conversion could occur, but requires 1012 G magnetic fields which are moreover strongly twisted, with order-one rotation of the field over kilometer distance scales. It is currently unclear whether such twists in the SN magnetic field exist at the time of core bounce. Nevertheless we emphasise that resonances from this effect can lead to additional time dependence in the observed events, beyond what is presented below.

## 4.2 Expected Change in Event Rates

We model the initial neutrino flux emitted from the supernova core according to the results of ref. [80], which correspond to an electron-capture supernova with a 8.8 M⊙progenitor star. As we consider Dirac neutrinos, for which we have seen in section 2 that the νL →NR conversion probability is independent of energy, the neutrino spectrum is not relevant to the following discussion – only the flux as a function of time matters. To account for neutrino flavour transitions on the way out of the supernova core, we assume simple adiabatic conversion [81, 82]. The flux of flavour νβ at Earth is then given by

```text
fνβ(Eν; α)=
X
```

```text
i
|Ufi|2f 0
νi(Eν; α)

1 −PνL→NR(µii)

, (16)
```

where f 0 νi(Eν; α) is the initial flux emitted from the neutrinosphere, µii is the diagonal magnetic moment for mass eigenstate νi, and PνL→NR is the conversion probability from νL to NR in the two-flavour approximation

5 Note however, that the MSW potential neutrinos encounter while propagating through the dilute interstellar medium is negligible, even compared to the neutrinos’ tiny magnetic interaction.


<!-- Source PDF page 7 -->

assuming equal masses. Remember that, at the huge matter density inside the supernova core, the mass and flavour bases are aligned: for the normal mass hierarchy we have f 0 νe = f 0 ν3 and f 0 νx = f 0 ν2 = f 0 ν3, such that fνe = cos2(θ13)f 0 νx + sin2(θ12)f 0 νe, where x = µ, τ.6 Note that, for simplicity, we neglect Earth matter effects, assuming that the supernova occurs in a sky location above the detector. For a general magnetic field configuration, PνL→NR is computed by solving eq. (9) numerically, using galactic magnetic field profiles generated according to the prescription from section 3.1. Equation (16) then yields the expected fluxes of neutronisation burst neutrinos at terrestrial detectors. The two detectors we consider are Hyper-Kamiokande [86, 87] and DUNE [88, 89]. For Hyper-Kamiokande, the total fiducial mass is 374 kt (two modules of 187 kt fiducial mass each), while for DUNE it will be 40 kt (four modules of 10 kt fiducial mass each). The most important detection channels in a water ˇCerenkov detector like Hyper-Kamiokande are inverse beta decay (see refs. [90, 91] and more recently ref. [92]),

```text
¯νe + p →e+ + n ,
(17)
```

and

```text
νe(¯νe) + 16O →e± + X .
(18)
```

In DUNE’s liquid argon time projection chambers, the reaction

```text
νe + 40Ar →e−+ 40K∗
(19)
```

dominates. Moreover, neutrino–electron scattering,

```text
νx + e−→νx + e−,
(20)
```

can occur in both detectors. It has smaller cross-sections than the nuclear reactions (17) to (19), but offers significantly better angular resolution. (The latter is important for triangulating the location of the supernova in the sky, but is less relevant for setting limits on neutrino magnetic moments.) The cross-sections for the above reactions can be found in [90, 91, 93, 94]. As the observable we are interested in is an overall reduction in the neutrino flux, we will combine all detection channels relevant in a given detector into a single event sample. We will also use only one bin in energy. We will, however, resolve the time-dependence of the signal using five equidistant bins covering the range from t = −5 ms to 20 ms, where t = 0 is the moment of core bounce. The magnetic momentinduced flux deficit is expected to be the same in all time

6 We neglect here the fact – only recently appreciated by the community – that µ and τ neutrinos/anti-neutrinos do not oscillate in exactly the same way [83, 84]. The reasons are the production of muons (but not τ leptons) in the supernova core [85], as well as the three-flavour vacuum oscillation term in the evolution equation.

bins, so this binning serves only to highlight the time evolution of the primary flux and the impact of the neutrino mass ordering on the count rates at Earth. We repeat the above procedure for 50 different galactic magnetic field profiles, distributed randomly within the uncertainties given in section 3.1. The spread among these 50 different realisations will allow us to gauge the impact of our poor understanding of the Milky Way’s magnetic field on the final sensitivity. A comparison of expected event rates at DUNE and Hyper-Kamiokande with and without magnetic moments is shown in fig. 2 for a galactic magnetic field profile corresponding to the nominal model from section 3.1. We show results for both the normal (blue) and inverted (red) mass ordering, where the difference between the two cases comes from differences in the adiabatic flavour conversions inside the supernova. Our first observation is that even for µν substantially below the current limit (1.2 × 10−12 µB, from the position of the tip of the redgiant branch [10] in the Hertzsprung–Russell diagram), a dramatic deficit of supernova neutrinos can occur. However, due to large magnetic field uncertainties, such a large deficit is not guaranteed. This problem is exacerbated by the fact that, according to eq. (10), the νL ↔NR conversion probability depends sensitively on the exact distance to the supernova. As PνL→NR is independent of the neutrino energy in the case of Dirac neutrinos, and since the νL ↔NR oscillation length is much larger than the size of the supernova core, no averaging over oscillations is expected. However, we could be unlucky and it may be located close to a minimum in PνL→NR. Therefore, as long as only a single supernova is observed and no neutrino deficit is found, it will be difficult to set robust constraints. In other words, the sensitivity of this method is not optimal, while the discovery potential is substantial. If systematic uncertainties in galactic magnetic fields can be reduced to well below our (relatively conservative) error estimates, the sensitivity would dramatically improve and become comparable to the discovery reach.

## 4.3 Discovery Reach

The discovery potential of DUNE and Hyper- Kamiokande is best illustrated in fig. 3, where we show the χ2 that would be obtained if neutrinos have a nonnegligible magnetic moment, but µν = 0 is assumed in the fit. More precisely, we define

```text
χ2 = min
a
```

X

i

```text

ni(ˆµν; B, l) −(1 + a) ni(0)
2
```

(1 + a) ni(0) + a2

```text
σ2a
, (21)
```

where ni(ˆµν; B, l) is the assumed observed number of events in the i-th time bin for magnetic moment matrix ˆµν, turbulent magnetic field scale B, and outer turbulence scale l. Similarly, ni(0) is the fitted number of events for zero magnetic moment (where the magnetic


<!-- Source PDF page 8 -->

*FIG. 2. Expected number of events at DUNE (left) and Hyper-Kamiokande (right) from the neutronisation burst of a supernova 10 kpc away, both in the standard case without neutrino magnetic moments (dotted histograms), and assuming a Dirac neutrino magnetic moment of 10−13µB, more than an order of magnitude below the best current limit (solid shaded histograms). We show results assuming both normal (blue) and inverted (red) mass ordering, which determines flavour conversion inside the supernova. Hatched bands indicate the 10% uncertainty in the initial neutrino flux as well as the uncertainty from our poor knowledge of Galactic magnetic fields. The orientation of the assumed line of sight in the galaxy is indicated by the inset on the right, where the ⊕sign marks our location.*

10−13 10−12

```text
neutrino magnetic moment µν [µB]
```

0

2

4

6

8

10

discovery potential [χ2]

### DUNE

## 8.8 M⊙SN at 10 kpc

```text
current 90% C.L. limit
(ﬂavor-universal µν)
```

L

normal ordering

```text
ﬂavor-universal µν
µν ̸= 0 for νµ only
inverted ordering
```

```text
ﬂavor-universal µν
µν ̸= 0 for νµ only
```

10−13 10−12

```text
neutrino magnetic moment µν [µB]
```

0

2

4

6

8

10

```text
discovery potential [χ2]
```

HyperK

## 8.8 M⊙SN at 10 kpc

```text
current 90% C.L. limit
(ﬂavor-universal µν)
```

L

normal ordering

```text
ﬂavor-universal µν
µν ̸= 0 for νµ only
inverted ordering
```

```text
ﬂavor-universal µν
µν ̸= 0 for νµ only
```

*FIG. 3. Predicted χ2 profiles for the analysis of supernova neutronisation burst data in DUNE (left) and Hyper-Kamiokande (right). The assumed true (Dirac) magnetic moment is indicated on the horizontal axis, while the vertical axis shows the level of tension between the simulated “data” with µν ̸= 0 and the model prediction for µν = 0. We show results for both the normal (blue) and inverted (red) mass ordering, and for flavour-universal magnetic moments (solid) as well as magnetic moments affecting only νµ (dotted). Lines correspond to the median discovery potential as the assumed true magnetic field model and the true primary flux normalisation are varied within uncertainties. The coloured blue band (shown only for the normal ordering, flavour-universal case for clarity) illustrates the 1σ variation. Dashed horizontal lines indicate χ2 thresholds for one degree of freedom. The region to the right of the vertical dotted line is disfavoured by red-giant cooling constraints [10]. The orientation of the assumed line of sight in the galaxy is indicated by the inset below the legend, with the ⊕sign marking the location of the Earth.*


<!-- Source PDF page 9 -->

field parameters are irrelevant). The nuisance parameter a parameterises the uncertainty in the primary neutrino flux, and the pull term a2/σ2 a penalises deviations from the nominal flux. Here we choose σa = 0.1.

We see from fig. 3 that flavour-universal magnetic moments of few × 10−13 µB should be detectable in both DUNE and Hyper-Kamiokande. In fact the two experiments have rather similar discovery reach. At somewhat larger magnetic moments, the discovery reach goes through several maxima and minima due to the oscillatory behaviour of PνL→NR as a function of µν. Figure 3 also illustrate the strong dependence of the discovery reach on the true magnetic field profile. Specifically, the coloured bands indicate the 1σ variation in the χ2

curves as the magnetic field and the normalisation of the primary neutrino flux are varied. We find very similar discovery reach for the normal (blue) and inverted (red) mass ordering. If only one neutrino flavour – here νµ – carries a sizeable magnetic moment, the discovery reach is worsened by an order of magnitude.

In fig. 4, we compare the expected discovery reach of DUNE and Hyper-Kamiokande to existing limits on neutrino magnetic moments. For each magnetic field profile, we define the 90% CL discovery reach as the value of µν for which χ2 first crosses the threshold of 2.71. We see that even for unfavourable magnetic field configurations, it is likely that the next Galactic supernova should be sensitive to magnetic moments below the best current limit (the one based on the location of the tip of the red giant branch in the Hertzsprung–Russell diagram, which would be modified if νL →NR conversions entail extra energy loss from stars). Under favourable circumstances, even an order of magnitude improvement is possible. The discovery reach is roughly the same for DUNE and Hyper-Kamiokande, and it is moreover largely independent of the neutrino mass ordering. Note that fig. 4 is for flavour-universal magnetic moments; if only some neutrino flavours experience a large magnetic moment, limits will be correspondingly weaker.

These results show that, thanks to robust predictions of the primary neutrino flux, the neutronisation burst of a Galactic supernova can be a powerful tool to search for physics beyond the Standard Model. They also show that a better understanding of Galactic magnetic fields would greatly aid in this endeavour (besides, of course, being a very interesting goal in itself due to its impact on Galactic astrophysics and radio astronomy).

## 5 ULTRA-HIGH ENERGY NEUTRINOS

The discovery of an ultra-high energy astrophysical neutrino flux at IceCube [98, 99] provides us with a new opportunity of probing neutrino properties and observing the high-energy Universe. The neutrino flux can be

10−13

10−12

10−11

10−10

```text
neutrino magnetic moment µν [µB]
```

white dwarfs

red giants

BorexinoGemma

XENONnT

PandaX-II

```text
Planck+BAO
TRH = 100 GeV
```

```text
Planck+BAO
TRH = 100 MeV
```

### NO IO

NO

IO

90% CL discovery reach

DUNE HyperK

8.8M⊙SN at 10 kpc

```text
ﬂavour-universal µν
```

L

*FIG. 4. 90% confidence level limits on the Dirac neutrino magnetic moment. The left part of the plot summarises (in black) existing limits from the white dwarf luminosity function [6], the tip of the red giant branch [10], solar neutrino observations in Borexino [95], reactor neutrino measurements in GEMMA [96], solar neutrinos in XENONnT [24] and PandaX [97], as well as cosmological Neff constraints from the combination of Planck and baryon acoustic oscillation (BAO) data [16, 17]. The coloured lines and bands on the right indicate the anticipated discovery reach in DUNE and Hyper- Kamiokande, determined from the χ2 curves in fig. 3. Bands correspond to 1σ variations of the magnetic field parameters in our model and 1σ variations of the initial neutrino flux prediction. We have assumed an 8.8M⊙supernova at a distance of 10 kpc, with the line of sight indicated by the small inset on the top right. The ⊕sign in that inset marks the location of the Earth in the Milky Way. The magnetic moments are taken to be flavour-universal.*

approximated by a power law

```text
Φ(E) = ϕ0 ×

E
100 TeV
```

```text
−γ
.
(22)
```

```text
For 25 TeV < E < 2.8 PeV, the best-fit parameters are
[100]
```

```text
ϕ0 = (6.37+1.46
−1.62) × 10−18 GeV−1 s−1 sr−1 cm−2,
(23)
```

and

```text
γ = 2.87+0.20
−0.19 .
(24)
```

Note, however, that there is some tension between different measurements of ϕ0 and γ. For instance, the spectral index quoted here based on IceCube’s High Energy Starting Event (HESE) sample, 2.87+0.20 −0.19 [100], is higher than the values extracted from upward-going muons (2.37 ± 0.09 [101]), from cascade-like events (2.53 ± 0.07 [102]), and from a study of the inelasticity of high-energy neutrino interactions (2.62 ± 0.07 [103]. As the parameters in eqs. (23) and (24) are extracted from data and attempts to predict them from first principles are fraught with large uncertainties, they cannot be used directly to


<!-- Source PDF page 10 -->

constrain new physics. In particular, using a flux deficit to probe disappearance of left-handed Dirac neutrinos into invisible right-handed states through the magnetic moment operator, as proposed in section 4 for Galactic supernova neutrinos, is not an option here. However, if magnetic moments are flavour non-universal, their effect may be observable because the νL →NR conversion probability will then be different for different νL flavours. This implies that the flavour composition of the neutrino flux arriving at Earth will be different compared to the Standard Model. Indeed, neutrino telescopes like Ice- Cube and KM3NeT have at least some flavour sensitivity. Magnetic moment-induced flavour conversions of ultrahigh energy astrophysical neutrinos have been studied previously in refs. [104–107] in the context of spin–flavour precession, but not for νL →NR conversions. A simple back-of-the-envelope estimate leads us to expect excellent sensitivity in neutrino telescopes. Namely, for a source at O(Gpc) distance and intergalactic magnetic fields of order nG, the oscillation phase in eq. (11) approaches unity already for µν ∼10−16µB. Taking into account conversion also in the intracluster medium, where magnetic fields are stronger according to the discussion in section 3.2, leads to an even more promising estimate. And indeed, this optimism appears to be justified as illustrated by the “flavour triangles” in fig. 5. Each of the three axes in these plots corresponds to the fractional admixture of one neutrino flavour to the observed flux. The triangular boundaries visualise the requirement that the νe, νµ, and ντ fractions must add up to 1. We compare the flavour composition at Earth expected for two astrophysically motivated flavour combinations: (i) a neutrino flux produced in the decay of high-energy pions in a lowdensity environment, which would give an initial flavour ratio (Φνe : Φνµ : Φντ ) = (1 : 2 : 0), see the left panel in fig. 5; and (ii) a flux from a source where pions decay in a dense environment, so that the resulting muons lose a considerable amount of energy before decaying. In this case, secondary muon decays do not contribute to the neutrino flux at high energies, and the initial flavour ratio is (0 : 1 : 0) (right panel in fig. 5). After propagation, these initial fluxes have evolved to the flavour ratios shown as green/blue dots, and the uncertainties in the final flavour ratios due to mixing angle uncertainties are indicated by the orange contours, with angles and uncertainties taken from the NuFit 5.1 fit [108]. As is well known, IceCube’s current constraints (large grey elliptical lines from ref. [109], see also ref. [110]) are not sufficient to resolve these mixing angle uncertainties, while future constraints (grey dashed ellipses, from ref. [111]) will get close. Further improvements are expected with the Gen-2 upgrade of the detector. IceCube could, however, already now detect non-zero neutrino magnetic moments if they violate lepton flavour universality. This is illustrated by the scattered coloured points in fig. 5. We assume here that only νµ have a non-

vanishing magnetic moment, with each point in the scatter plot corresponding to a random value of the magnetic moment, as indicated by its colour, as well as a random choice of mixing parameters, each of them drawn from a normal distribution with central value and error bar from NuFit 5.1 [108]. Results for a magnetic moment with a different flavour structure, namely a scenario where only the ν2 mass eigenstate has non-zero µν, are shown in appendix B. In a similar way as we did for supernova neutrinos, we again consider incoherent propagation and independent conversions between left-handed and righthanded neutrinos for each mass state, solving eq. (4) numerically in the two-flavour approximation and neglecting the vacuum oscillation term in the Hamiltonian.7 For each of the coloured points in fig. 5, we have chosen one of 50 extragalactic magnetic field profiles, each of them randomly drawn from the distributions described in section 3.2. Moreover, the distance of the neutrino source for each field profile has been chosen randomly between 100 Mpc and 5 Gpc. Each point thus describes a possible outcome of a measurement on a sample of neutrinos from a single source. (We comment below and in appendix B on the implications of these assumptions.) We do not account for possible additional νL ↔NR conversion inside the source due to our complete ignorance of the source magnetic field. Doing so is conservative because additional conversion would likely increase the deviation from the Standard Model point in the flavour triangle and thus increase the experimental sensitivity to neutrino magnetic moments. Figure 5 shows that, if the magnetic field configuration along the line of sight is favourable, even tiny lepton flavour universality-violating magnetic moments of order few × 10−17µB, well below the current limits of few × 10−12µB, can lead to flavour ratios that deviate significantly from those expected in the Standard Model. Typically, we will have very little information on the magnetic fields neutrinos encounter during propagation, therefore, the limit that can be set in absence of a discovery will be much weaker than 10−17µB. A possible gamechanger could be detailed measurements of Faraday rotation in radio emission from an identified neutrino source. Such a study could significantly constrain the magnetic field profile along the line of sight, thereby reducing the main systematic uncertainty limiting the sensitivity to neutrino magnetic moments. Our conclusions would remain unchanged if the magnetic moment matrix had several non-zero entries, as long as these entries all differ by O(1) factors. Only for close to flavour-universal magnetic moments, deviations from Standard Model expectations would become

7 The latter assumption is always justified for Dirac or pseudo- Dirac neutrinos. But even for large splitting between ˆ Mν and ˆ MN it is justified in the high-energy limit where Bµ ≫ ∆m2 N1/(2p). In this limit, our results also become independent of energy.


<!-- Source PDF page 11 -->

0.0

0.2

0.4

0.6

0.8

1.0

1.0

0.8

0.6

0.4

0.2

0.0

## 0.0 0.2 0.4 0.6 0.8 1.0

68% IC diﬀuse 90%

IC 15-yr 68% (proj.)

## 2000 points

```text
Initial composition
(νe:νµ:ντ) = (1:2:0)
```

```text
only νµ
has µν ̸= 0
```

single source

```text
νe
```

```text
νµ
```

```text
ντ
```

```text
SM 3σ
```

0

2

4

6

8

```text
Neutrino magnetic moment [µB]
```

×10−17

0.0

0.2

0.4

0.6

0.8

1.0

1.0

0.8

0.6

0.4

0.2

0.0

## 0.0 0.2 0.4 0.6 0.8 1.0

68% IC diﬀuse 90%

IC 15-yr 68% (proj.)

## 2000 points

```text
Initial composition
(νe:νµ:ντ) = (0:1:0)
```

```text
only νµ
has µν ̸= 0
```

single source

```text
νe
```

```text
νµ
```

```text
ντ
```

```text
SM 3σ
```

0

2

4

6

8

```text
Neutrino magnetic moment [µB]
```

×10−17

*FIG. 5. Predicted flavour ratios of astrophysical Dirac neutrinos in the Standard Model (small regions delineated in orange) and in presence of flavour non-universal neutrino magnetic moments (scattered points, with colour code indicating the magnitude of the magnetic moment). For the SM, the uncertainties in the neutrino mixing angles are taken into account, while for non-negligible magnetic moments, also the uncertainty in the extragalactic magnetic fields is included following the procedure outlined in section 3.2. The source is assumed to be between 0.1 and 5 Gpc away. We have used a different random magnetic field profile for each point, thus reflecting the range of possible outcomes if only events from a single source are considered. Expected results for a diffuse flux, and for magnetic moments with a different flavour structure, are shown in appendix B. We compare results for a pion decay source (initial flavour ratios (1 : 2 : 0), left panel) and for a muon-damped source (initial flavour ratios (0 : 1 : 0), right panel). Finally, current constraints (grey solid ellipses) [109] and future sensitivities (grey dashed ellipses) [111] for IceCube measurements on the diffuse flux are shown as well.*

weaker. Note that, similar to what we observed in fig. 3, the conversion probability for neutrino magnetic moments well above the sensitivity limit goes through a series of maxima and minima. We refer the reader to appendix B for a brief discussion of alternative magnetic moment matrices. Let us emphasise again that the large deviations from Standard Model expectations we predict here are unique to analyses using only neutrinos from a single source (that is, a single line of sight and magnetic field profile). To predict the flavour ratios of a diffuse flux, we would need to average over many lines of sight, which would lead to wash-out: each mass eigenstate experiences on average about 50% disappearance, leaving the flavour ratios unchanged. Results for a diffuse neutrino flux are shown in figs. 7 and 8 in appendix B. We should of course keep in mind that obtaining flavour information on neutrinos from a point source is very challenging. Only muon neutrinos can be observed with sufficient angular resolution to associate them with a particular source based on the sky location they are coming from. For νe and ντ, such an association is only possible based on timing. In other words, the source must be transient. To date, IceCube has identified two point sources of high-energy neutrinos, the blazar TXS 0506+056 with ∼15 detected neutrinos [112, 113] and the active nucleus of the NGC 1068 galaxy with about 80 neutrinos [114]. Both analyses are based on muon tracks only, so the detailed flavour structure of the neutrino flux from these sources is as yet unknown. Moreover, NGC 1068 is relatively close (14.4 Mpc), so its

neutrinos will experience much less νL ↔NR conversion than those from a source at O(Gpc), as we have assumed in fig. 5. Therefore, NGC 1068 is not optimal for constraining neutrino magnetic moments. TXS 0506+056, on the other hand, is 1.75 Gpc away from Earth, and is transient. Radio emission has been observed from both sources, but to the best of our knowledge has never been used to constrain the intermittent extragalactic magnetic fields.

## 6 DISCUSSION

In the following, we discuss several generalisations and extensions of the results obtained in the previous sections.

## 6.1 Neutrino Magnetic Moments in the Standard Model

We have found in section 5 that flavour ratios of highenergy astrophysical neutrinos may offer superior discovery reach to flavour non-universal neutrino magnetic moments down to few × 10−17 µB. This raises the question if, under favourable circumstances, even the neutrino magnetic moments predicted in the Standard Model (see eq. (1)) could be within reach. Note that, because of their neutrino mass dependence, these magnetic moments are flavour non-universal, fulfilling a first necessary condition for being detectable using flavour ratios of ultra-


<!-- Source PDF page 12 -->

high energy neutrinos. Second, according to the sensitivity projections shown in fig. 5 above, future IceCube (and even more so IceCube-Gen2) analyses should be able to detect O(10%) changes in the flavour ratios of highenergy cosmic neutrinos, especially once the uncertainties in the standard oscillation parameters will have been further reduced by the next generation of long-baseline experiments. This means that oscillation probabilities PνL→NR ∼O(10%) are required to make a detection. For magnetic moments of order few × 10−20 µB, this would require Z L

## 0 dx B⊥(x) ≃10 Gpc µG (25)

according to eq. (12). This estimate is valid in case the orientation of the magnetic field does not change along the line of sight. We expect any change in the magnetic field direction to reduce the νL ↔NR oscillation probability. As we have discussed in section 3.2, most observations indicate that extragalactic magnetic fields are ≲10 nG, while a few point towards larger fields of order 0.2–0.6 µG [54–56]. This would be enough to satisfy eq. (25) for a source more than 10 Gpc away from Earth. (For comparison, recall TXS 0506+056 is at a distance of 1.75 Gpc.) Alternatively, one could imagine a line of sight that passes through many galaxy clusters (with intracluster fields of order µG), such that the integrated distance neutrinos travel inside clusters is several Gpc. In any case, the magnetic fields the neutrinos encounter on their way to Earth would need to be oriented in the same direction to avoid cancellations in the integral on the left-hand side of eq. (25). For the same reason, neutrinos should also come from a single point source, corresponding to a single line of sight. To summarise, neutrino magnetic moments as small as in the Standard Model might be detectable in IceCube if

1. a sizeable sample of neutrinos from a single point source at ∼10 Gpc distance is available to enable detection of O(10%) deviations in the flavour ratios;

2. magnetic fields between galaxy clusters are as large as suggested in refs. [54–56] (in conflict with other constraints), or if an O(1) fraction of the line of sight passes through galaxy clusters;

3. magnetic fields along the line of sight are oriented in similar directions to avoid cancellation.

## 6.2 Heavier Right-Handed Neutrinos and Decoherence

In sections 4 and 5, we have assumed magnetic moment transitions between the left-handed and right-handed partners of a Dirac pair, that is, we have taken ∆m2 Nν = 0. As discussed in section 2, this is justified as long as µνB⊥≫∆m2 Nν/(2p). For larger right-handed neutrino

masses, the oscillation amplitude becomes very small according to eq. (10), so this case is phenomenologically less relevant. In particular, the expected discovery reach for magnetic moment-induced transitions to heavier righthanded neutrinos using the methods discussed in this paper is significantly worse than the one for ∆m2 N1 ≃0. Constraints on heavier NR can still be obtained, but these are typically based on inelastic νL →NR transitions [115], followed by NR decay [15]. This raises an interesting theoretical question. Namely, when can νL ↔NR transitions be described as an interference phenomenon similar to conventional neutrino oscillation (as we have done in this paper so far), and when is a description as a hard scattering process more appropriate? The key to answering this question is the Heisenberg principle. If the νL and NR masses are sufficiently similar so that the small changes in energy and momentum incurred during a νL ↔NR transition fall below the quantum mechanical energy and momentum uncertainties, neutrino interactions with the magnetic field are coherent and oscillations can occur. This is no longer the case if the NR are significantly heavier than the active neutrinos. Then it is at least in principle possible based on kinematics to determine where along the neutrino trajectory the conversion has happened. In this regime, the transition probability is most easily obtained by evaluating the Feynman diagram describing the inelastic scattering of a neutrino on one of the particles that source the magnetic field. We will denote the two scenarios the “coherent” and “incoherent” scattering regimes, respectively. The natural question to ask in this context is how and where the transition between these two very different theoretical descriptions occurs. We will here focus on the “where” – that is, the threshold value of mN that separates the two regimes. The “how” – that is, the detailed dynamics of the transition, is discussed in appendix D. Here we proceed with a simple derivation of the mN threshold. Consider inelastic scattering νL →NR on a hypothetical massive target at rest, such that no energy transfer occurs. We compare the momentum transferred to the target, ∆p, in this hypothetical process to the Heisenberg momentum uncertainty, σp, of the electrons in the interstellar medium (ISM) which source interstellar magnetic fields. If ∆p > σp, the process νL +e →NR +e leads to an appreciable change in the electron’s quantum state, so the scattering will be incoherent. In contrast, if ∆p < σp, the electron wave function remains largely unaffected, and the νL →NR flavour conversion is welldescribed as a coherent oscillation process using the formalism from section 2. If we denote the initial and final neutrino momenta by kν and pN, respectively, we have

```text
∆p = |pN −kν|=
```

r

```text
2E2ν −m2
N + 2Eν
q
```

```text
E2ν + m2
N. (26)
```

Here, we have used that the νL and NR energies are identical in our hypothetical scattering process on a very mas-


<!-- Source PDF page 13 -->

sive target, and we have considered the scattering angle to be 180◦, corresponding to the kinematic configuration with the maximal momentum transfer. From eq. (26), we can immediately derive that the coherence condition, ∆p < σp, corresponds to the requirement

```text
mN < 2
q
```

```text
σp(Eν −σp) ≃2
p
```

```text
σpEν
```

```text
= 6.3 keV ×
1 cm
```

```text
σx
```

```text
 Eν
```

## 1 TeV

```text

.
(27)
```

In the last step, we have defined the spatial localisation of the ISM electrons σx = 1/(2σp). The benchmark value σx ≃1 cm has been chosen based on typical ISM densities. (Keep in mind, though, that the latter can vary by several orders of magnitude.) Equation (27) shows that the coherent formalism employed in this paper is mostly relevant for fairly light NR. Only then, νL →NR scattering occurs coherently on all electrons along the neutrino trajectory. The constraint is fairly tight for supernova neutrinos (Eν ∼10 MeV). But even for the highest-energy cosmic neutrinos with Eν ∼PeV, coherent flavour conversion is relevant only for NR masses well below 1 MeV.

## 7 CONCLUSIONS

In summary, we have examined the role neutrino magnetic moments play in the propagation of astrophysical neutrinos through both Galactic and extragalactic magnetic fields. The key take-home messages are as follows:

• (Extra-)Galactic magnetic fields are a powerful discovery tool for neutrino magnetic moments inducing transitions from left-handed active to right-handed neutrinos, νL →NR. However, this conversion probability is only sizeable for small mass-splitting, namely for the case where the active neutrinos are Dirac or pseudo- Dirac in nature, see eq. (10).

• For supernova neutrinos the precise prediction of the flux from the neutronisation burst affords the ability to construct sensitive observables based on the depletion of the observed neutrino flux through νL →NR conversions in our Galactic magnetic field, see fig. 2. However, due to large uncertainties on both the largescale coherent and small-scale turbulent components of this field (see section 3.1) it is challenging to place robust constraints. Nevertheless, under conservative assumptions on these uncertainties this method affords a discovery reach an order of magnitude superior to current constraints (see fig. 4) depending also on the lineof-sight to the supernova. Interestingly these results are largely independent of the details of the supernova magnetic field as the initial neutrino flux before propagation depends only on the ordering of the neutrino mass hierarchy.

• An alternative approach that yields potentially far greater sensitivities utilises high-energy astrophysical neutrinos observed in neutrino telescopes. As the sources of these neutrinos are not well understood the sensitivity here arises from deviations in the flavour composition. This method is exceptionally powerful if there is a large hierarchy in the neutrino magnetic moments of various neutrino flavours, and if a sample of neutrinos from a single point source is considered. In this case, probing magnetic moments as small as 10−17 µB seems feasible, see fig. 5. Measuring the flavour composition of neutrinos from a point source would most likely require this source to be transient due to the limited angular resolution of νe and ντ reconstruction. But even for diffuse astrophysical neutrino fluxes, the discovery reach is still several orders of magnitude beyond current limits.

• Under very favourable circumstances neutrino magnetic moments arising purely from Standard Model contributions may be detectable in IceCube, see section 6.1. This however will require an extremely distant point source, with not only favourable orientation of the magnetic field (to avoid cancellations) but also an O(1) fraction of the line-of-sight passing through galaxy clusters or other structures with enhanced magnetic fields.

• Lastly, we have discussed for which values of the νL–NR mass-splittings our formalism which describes νL ↔ NR transitions as coherent oscillations is valid. In particular, it is required that the magnetic field act coherently on the propagating neutrinos. In section 6.2 we sketched an argument showing that for ultra-highenergy neutrinos this requires sub-MeV NR masses, while in appendix D a detailed calculation of this decoherence criterion is presented.

To conclude, we have established several new and highly promising avenues towards discovering tiny neutrino magnetic moments in theories beyond the Standard Model – or even in the Standard Model itself. So far, these methods are limited by our poor understanding of Galactic and intergalactic magnetic fields, but we note that there is significant room for improvement in this field, for instance through observations of Faraday rotation in fast radio bursts and through large-scale radio surveys. Even modest advances in our knowledge about the magnitude and structure of magnetic fields will allow for tremendous improvements in the sensitivity and discovery reach for neutrino magnetic moments.

## ACKNOWLEDGEMENTS

It is a pleasure to thank Vedran Brdar and Admir Greljo for inspiring and useful discussions in the early stages of this work. We also thank Evgeny Akhmedov for correcting a statement regarding resonant spin-flavour


<!-- Source PDF page 14 -->

oscillations in the Dirac case. EW’s work is supported by the Collaborative Research Center SFB 1258 of the German Research Foundation. The plots in this paper have been created using Matplotlib (v3.5.2) [116] as well as the Python ternary package (v1.0.8) [117].

```text
A
LINE-OF-SIGHT DEPENDENCE OF
GALACTIC νL →NR CONVERSION
```

In section 4 we have illustrated that a substantial fraction of active neutrinos emitted by a supernova can be converted to invisible NR if non-negligible magnetic moments allow for transitions between the two states in the Galactic magnetic fields. We have illustrated this point in fig. 2 for one particular line of sight. As the coherent component of the Galactic magnetic field strongly depends on the line of sight, we show in fig. 6 sample spectra for several other lines of sight. We confirm that, indeed, there is a strong dependence on the direction from which neutrinos arrive.

### B FLAVOUR RATIOS OF ULTRA-HIGH ENERGY NEUTRINOS: ALTERNATIVE SCENARIOS

To complement the discussion in section 5, we show in fig. 7 the predicted flavour ratios of ultra-high energy astrophysical neutrinos for a diffuse neutrino flux. As in fig. 5, we focus first on the case where only νµ carry a non-zero magnetic moment. As anticipated in section 5, deviations from the Standard Model are smaller in this case because a measurement on the diffuse flux averages over many different lines of sight with randomly varying magnetic field profiles and therefore randomly varying νL →NR conversion probabilities. Note the different scaling of the colour bar here compared to fig. 5. In fig. 8, we repeat our analysis for a different magnetic moment flavour structure, namely one where only the ν1 mass eigenstate carries non-zero µν. Once again, deviations from the Standard Model flavour ratios are larger in the single-source case, but also for a diffuse flux, magnetic moments well below current limits can lead to deviations that should be observable in future IceCube analyses. This can be understood from the fact that the flavour composition of ν1 in the normal hierarchy case is about 50% νe. Removing ν1 from the neutrino flux via oscillations to NR thus disproportionately depletes the νe component at Earth, even after averaging over many magnetic field configurations. Plots for other flavour structures of the magnetic moment matrix can be found on the GitHub repository accompanying this paper [32].

C MAGNETIC MOMENT-INDUCED νL ↔NR OSCILLATIONS IN TURBULENT MAGNETIC FIELDS

In the main part of this paper, we have evaluated the probability for νL ↔NR transitions in galactic and intergalactic magnetic fields by numerically solving the Schr¨odinger equation (4). This is, however, rather time-consuming, especially for large µν, where it requires tracking potentially many oscillation maxima and minima. Also generating and storing the turbulent magnetic field configurations comes with a non-negligible overhead. For this reason, we have also investigated an approximate method for determining these probabilities, especially for the case of propagation through turbulent magnetic fields while using the two-flavour approximation. Taking into account the stochastic nature of these fields, the idea is to describe the oscillation probability as a sin2-function with a randomly chosen phase, φ(t). Specifically, we draw φ(L) from a Gaussian distribution with a width that is fitted to the numerically calculated distribution. This is motivated by the observation that, for small µν (such that µν ⟨B⊥⟩L ≪1), neutrinos will not have time to complete a single oscillation, even in the most favourable case that B⊥(x) does not change direction along the line of sight. This extreme scenario, which maximises φ(L), is statistically unlikely, while cancellations between regions with different field orientations are more likely. This behaviour is correctly modelled by the Gaussian distribution, as illustrated in the left and middle panels of fig. 9. In the opposite limit, µν ⟨B⊥⟩L ≫1, the Gaussian approximation is less suitable. Here, even small changes in B⊥(t) lead to large changes in the oscillation phase. so one might speculate that the phase should be uniformly distributed. This would indeed be the case if the direction of B⊥did not change, so that the oscillation probability follows precisely a sin2 law, as in eq. (12). For realistic field profiles, however, the behaviour of PνL→NR is more involved, and in fact fig. 9 (right) shows that in this case a uniform distribution in the probability provides the most accurate description.

### D DETAILED DERIVATION OF THE DECOHERENCE CONDITION

In section 6.2, we have heuristically argued that νL → NR transitions can occur coherently only if mN satisfies eq. (27). We will now corroborate the arguments given there by employing the wave packet formalism. Our strategy is to compute the probability for νL →NR scattering on a background electron, assuming the initial and final state electron wave packets are identical. This corresponds to the regime of coherent conversion. For large mN, the cross-section will be strongly suppressed, indicating the transition to the incoherent regime. We are interested in the value of mN at which this transition


<!-- Source PDF page 15 -->

*FIG. 6. Similar to fig. 2, we show the expected number of events at DUNE (left) and Hyper-Kamiokande (right) from the neutronisation burst of a supernova with and without magnetic moment-induced νL ↔NR conversion. Compared to fig. 2, we here vary the assumed location of the supernova in the Milky Way, as indicated by the inset on the right.*

happens.

We write the initial and final state wave packets in the form

```text
|ψ⟩=
Z
d3p
(2π)3p
```

```text
2Ep
f(p)|p⟩,
(D1)
```

where |p⟩is a momentum eigenstate, and Ep is the corresponding energy. The momentum eigenstates are normalised according to

```text
⟨k|p⟩= 2E(k) (2π)3δ(3)(p −k) ,
(D2)
```

and the normalisation of the wave packet shape factor,

```text
f(p) is
Z
d3p
(2π)3 |f(p)|2 = 1 .
(D3)
```

For the electrons, we choose a Gaussian wave packet with standard deviation σp centred around 0:

```text
fe(p) =
2π
```

```text
σ2p
```

3/4 exp  −p 2

```text
4σ2p
```

 . (D4)

We take the neutrino to be initially in a momentum eigenstate:

```text
fν(p) =
1
√
```

```text
V
(2π)3δ(3)(p −kν) ,
(D5)
```

where the prefactor is chosen to satisfy the normalisation condition, eq. (D3).8 For the neutrino in the final state, we use an analogous function. The transition probability is then given by


<!-- Source PDF page 16 -->

0.0

0.2

0.4

0.6

0.8

1.0

1.0

0.8

0.6

0.4

0.2

0.0

## 0.0 0.2 0.4 0.6 0.8 1.0

68% IC diﬀuse 90%

IC 15-yr 68% (proj.)

## 200 points

```text
Initial composition
(νe:νµ:ντ) = (1:2:0)
```

```text
only νµ
has µν ̸= 0
```

multiple sources

```text
νe
```

```text
νµ
```

```text
ντ
```

```text
SM 3σ
```

0.0

0.2

0.4

0.6

0.8

1.0

```text
Neutrino magnetic moment [µB]
```

×10−15

0.0

0.2

0.4

0.6

0.8

1.0

1.0

0.8

0.6

0.4

0.2

0.0

## 0.0 0.2 0.4 0.6 0.8 1.0

68% IC diﬀuse 90%

IC 15-yr 68% (proj.)

## 200 points

```text
Initial composition
(νe:νµ:ντ) = (0:1:0)
```

```text
only νµ
has µν ̸= 0
```

multiple sources

```text
νe
```

```text
νµ
```

```text
ντ
```

```text
SM 3σ
```

0.0

0.2

0.4

0.6

0.8

1.0

```text
Neutrino magnetic moment [µB]
```

×10−15

*FIG. 7. In analogy to fig. 5, we show here the predicted flavour ratios of astrophysical neutrinos in the presence of a non-zero neutrino magnetic moment affecting only the νµ flavour. In contrast to fig. 5, we here assume a diffuse neutrino flux (as opposed to a single point source) and hence average the oscillation probabilities over 50 randomly generated magnetic field profiles. We compare results for a pion decay source (initial flavour ratios (1 : 2 : 0), left panel) and for a muon-damped source (initial flavour ratios (0 : 1 : 0), right panel). The orange regions correspond to Standard Model predictions, taking into account uncertainties in the neutrino mixing angles. Current and future IceCube constraints for the diffuse neutrino flux [109, 111] are shown in grey. Note the different scaling of the colour bar compared to fig. 5.*

0.0

0.2

0.4

0.6

0.8

1.0

1.0

0.8

0.6

0.4

0.2

0.0

## 0.0 0.2 0.4 0.6 0.8 1.0

68% IC diﬀuse 90%

IC 15-yr 68% (proj.)

## 2000 points

```text
Initial composition
(νe:νµ:ντ) = (1:2:0)
```

```text
only ν1
has µν ̸= 0
```

single source

```text
νe
```

```text
νµ
```

```text
ντ
```

```text
SM 3σ
```

0

2

4

6

8

10

```text
Neutrino magnetic moment [µB]
```

×10−17

0.0

0.2

0.4

0.6

0.8

1.0

1.0

0.8

0.6

0.4

0.2

0.0

## 0.0 0.2 0.4 0.6 0.8 1.0

68% IC diﬀuse 90%

IC 15-yr 68% (proj.)

## 2000 points

```text
Initial composition
(νe:νµ:ντ) = (0:1:0)
```

```text
only ν1
has µν ̸= 0
```

single source

```text
νe
```

```text
νµ
```

```text
ντ
```

```text
SM 3σ
```

0

2

4

6

8

10

```text
Neutrino magnetic moment [µB]
```

×10−17

0.0

0.2

0.4

0.6

0.8

1.0

1.0

0.8

0.6

0.4

0.2

0.0

## 0.0 0.2 0.4 0.6 0.8 1.0

68% IC diﬀuse 90%

IC 15-yr 68% (proj.)

## 200 points

```text
Initial composition
(νe:νµ:ντ) = (1:2:0)
```

```text
only ν1
has µν ̸= 0
```

multiple sources

```text
νe
```

```text
νµ
```

```text
ντ
```

```text
SM 3σ
```

0.0

0.2

0.4

0.6

0.8

1.0

```text
Neutrino magnetic moment [µB]
```

×10−15

0.0

0.2

0.4

0.6

0.8

1.0

1.0

0.8

0.6

0.4

0.2

0.0

## 0.0 0.2 0.4 0.6 0.8 1.0

68% IC diﬀuse 90%

IC 15-yr 68% (proj.)

## 200 points

```text
Initial composition
(νe:νµ:ντ) = (0:1:0)
```

```text
only ν1
has µν ̸= 0
```

multiple sources

```text
νe
```

```text
νµ
```

```text
ντ
```

```text
SM 3σ
```

0.0

0.2

0.4

0.6

0.8

1.0

```text
Neutrino magnetic moment [µB]
```

×10−15

*FIG. 8. Same as figs. 5 and 7, but for a scenario where only the ν1 mass eigenstate carries non-zero magnetic moment.*


<!-- Source PDF page 17 -->

## 0.0 0.2 0.4 0.6 0.8 1.0 Conversion Probability

0

20

40

60

80

Counts

```text
L = 1 Gpc
```

```text
Numerical, µν = 1 × 10−17µB
Gaussian distribution, σ = 0.19
```

## 0.0 0.2 0.4 0.6 0.8 1.0 Conversion Probability

0

5

10

15

20

25

Counts

```text
L = 1 Gpc
```

```text
Numerical, µν = 1 × 10−16µB
Gaussian distribution, σ = 0.88
```

## 0.0 0.2 0.4 0.6 0.8 1.0 Conversion Probability

0

5

10

15

20

25

Counts

```text
L = 1 Gpc
```

```text
Numerical, µν = 1 × 10−15µB
Gaussian distribution, σ = 20.00
```

*FIG. 9. Comparison of the exact numerical results for the two-flavour νL →NR oscillation probability in a turbulent magnetic field to the approximate results discussed in appendix C. The blue-shaded histogram shows the distribution of numerically calculated PνL→NR(L = 1 Gpc) values for 100 different extragalactic magnetic field profiles generated according to the procedure outlined in section 3.2. Unshaded red dashed histograms correspond to approximations based on drawing the oscillation phase φ(L) from a Gaussian distribution with a width fitted to the numerical result. The three panels correspond to three different values of the neutrino magnetic moment, µν.*

```text
P =
Z d3pN
```

```text
(2π)3 V

1
p
```

```text
2EkνV
1
p
```

2EpN V

Z d3ke

```text
(2π)3
fe(ke)
p
```

2Eke

```text
d3pe
(2π)3
f ∗
e (pe)
p
```

```text
2Epe
A(kν, ke, pN, pe)
```

## 2 , (D8)

where the subscripts ν, N, e, refer to the active neutrino νL, sterile neutrino NR, and electron, respectively. We use the letter k for initial state momenta and p for final state momenta, and we already impose that the initial and final state electron wave packets should have the same shape, fe. The quantity A(kν, ke, pN, pe) is the scattering amplitude for momentum eigenstates, which we can obtain from the Feynman rules of the theory. As done in ref. [118], it is convenient to express A in coordinate space:

```text
A(kν, ke, pN, pe) =
Z
d4x Me(ke, pe)e−i(pe−ke)·x
Z
d4y Mν(kν, pN)e−i(pN−kν)·y G(y −x) ,
(D9)
```

where Me and Mν are the electron and the neutrino interaction amplitudes respectively, and the propagator, G(y−x), is:

```text
G(y −x) =
Z
d4p
(2π)4 e−ip·(y−x)
i
p2 + iϵ .
(D10)
```

We first carry out the integrals over ke and pe. We use the fact that Me varies much more slowly as a function of ke and pe than both fe and the oscillating exponentials, hence it is justified to pull Me out of the momentum integrals and replace it by its value at ke = pe = 0. Moreover, as the electron is non-relativistic, we can replace its energy by its mass. We thus arrive at two simple Gaussian integrals, each of which has the form Z d3p (2π)3 fe(p) p

```text
2Epe
e−ip·x =
2σ2
p
π
```

```text
3/4
1
√2me
e−σ2
px 2−imet .
(D11)
```

Next is the integral over x: Z d4x eip·x 2σ2 p π

```text
3/2
1
2me
e−2σ2
px2 = 2π δ(p0)
1
2me
e
−p2
```

```text
8σ2p .
(D12)
```

8 The philosophy here is that we imagine for the moment that the process takes place in a box of finite volume V and is restricted to a finite time interval, T. δ-functions should then be thought of as strongly peaked functions defined on these intervals, for instance δ(p0) = R T/2 −T/2(dt/2π) eip0t = sin(p0T/2)/(πp0). To check that eq. (D5) indeed satisfies the normalisation condition, eq. (D3),

```text
one can use the identities
h
(2π)3δ(3)(p −q)
i2
= V (2π)3δ(3)(p −q),
(D6)
h
(2π)δ(p0 −q0)
i2
= T(2π)δ(p0 −q0).
(D7)
```


<!-- Source PDF page 18 -->

The integral over y yields just a delta function, Z d4y e−i(p+pN−kν)y = (2π)4δ(4)(p + pN −kν) , (D13)

which we can use to evaluate also the integral over p. For the transition probability, we are thus left with

```text
P =
1
2Ekν
```

## 1 (2me)2 M2 e M2 ν

```text
2σ2
p
π
```

3 Z d3pN

```text
(2π)3
1
2EpN
e
−(pN −kν )2
```

```text
4σ2p
2πδ(p0
N −k0
ν)
1
(pN −kν)2
```

## 2 . (D14)

It would be straightforward to evaluate the remaining integral in spherical coordinates, using eq. (D7) to rewrite the squared delta function in terms of a single delta function. However, we can already read off the relevant physical conclusions from eq. (D14). The delta function requires the νL and NR energies to be identical, and with this constraint, the exponential takes the form

```text
e
−(pN −kν )2
```

```text
4σ2p
= exp

−2E2
ν −m2
N −2Eν
p
```

```text
E2ν −m2
N cos θ
4σ2p
```

 . (D15)

Here, Eν ≡|kν| = p

|pN|2 + m2 N is the common energy of νL and NR, and θ is the angle between kν and pN. The exponential is most strongly suppressed at cos θ = −1, and requiring no suppression corresponds to the condition that the exponent be larger than ∼−1. This trans-

lates into the condition

```text
mN < 2
q
```

```text
σp(Eν −σp) ,
(D16)
```

which is precisely eq. (27).

[1] A. Cisneros, Effect of neutrino magnetic moment on solar neutrino observations, Astrophys. Space Sci. 10 (1971) 87–92. [2] K. Fujikawa and R. Shrock, The Magnetic Moment of a Massive Neutrino and Neutrino Spin Rotation, Phys. Rev. Lett. 45 (1980) 963. [3] G. Magill, R. Plestid, M. Pospelov, and Y.-D. Tsai, Dipole Portal to Heavy Neutral Leptons, Phys. Rev. D 98 (2018), no. 11 115015, [1803.03262]. [4] P. Coloma, P. A. N. Machado, I. Martinez-Soler, and I. M. Shoemaker, Double-Cascade Events from New Physics in Icecube, Phys. Rev. Lett. 119 (2017), no. 20 201804, [1707.08573]. [5] A. H. C´orsico, L. G. Althaus, M. M. Miller Bertolami, S. O. Kepler, and E. Garc´ıa-Berro, Constraining the neutrino magnetic dipole moment from white dwarf pulsations, JCAP 08 (2014) 054, [1406.6034]. [6] M. M. Miller Bertolami, Limits on the neutrino magnetic dipole moment from the luminosity function of hot white dwarfs, Astron. Astrophys. 562 (2014) A123, [1407.1404]. [7] S. Arceo-D´ıaz, K. P. Schr¨oder, K. Zuber, and D. Jack, Constraint on the magnetic dipole moment of neutrinos by the tip-RGB luminosity in ω -Centauri, Astropart. Phys. 70 (2015) 1–11. [8] G. G. Raffelt, Limits on neutrino electromagnetic properties: An update, Phys. Rept. 320 (1999) 319–327. [9] S. A. D´ıaz, K.-P. Schr¨oder, K. Zuber, D. Jack, and E. E. B. Barrios, Constraint on the axion-electron coupling constant and the neutrino magnetic dipole moment by using the tip-RGB luminosity of fifty

globular clusters, 1910.10568. [10] F. Capozzi and G. Raffelt, Axion and neutrino bounds improved with new calibrations of the tip of the red-giant branch using geometric distance determinations, Phys. Rev. D 102 (2020), no. 8 083007, [2007.03694]. [11] J. A. Morgan, Cosmological Upper Limit to Neutrino Magnetic Moments, Phys. Lett. B 102 (1981) 247–250. [12] M. Fukugita and S. Yazaki, Reexamination of Astrophysical and Cosmological Constraints on the Magnetic Moment of Neutrinos, Phys. Rev. D 36 (1987) 3817. [13] P. Elmfors, K. Enqvist, G. Raffelt, and G. Sigl, Neutrinos with magnetic moment: Depolarization rate in plasma, Nucl. Phys. B 503 (1997) 3–23, [hep-ph/9703214]. [14] A. Ayala, J. C. D’Olivo, and M. Torres, Right-handed neutrino production in dense and hot plasmas, Nucl. Phys. B 564 (2000) 204–222, [hep-ph/9907398]. [15] V. Brdar, A. Greljo, J. Kopp, and T. Opferkuch, The Neutrino Magnetic Moment Portal: Cosmology, Astrophysics, and Direct Detection, JCAP 01 (2021) 039, [2007.15563]. [16] P. Carenza, G. Lucente, M. Gerbino, M. Giannotti, and M. Lattanzi, Strong cosmological constraints on the neutrino magnetic moment, 2211.10432. [17] S.-P. Li and X.-J. Xu, Neutrino magnetic moments meet precision Neff measurements, JHEP 02 (2023) 085, [2211.04669]. [18] C. Giunti and A. Studenikin, Neutrino electromagnetic interactions: a window to new physics, Rev. Mod. Phys. 87 (2015) 531, [1403.6344].


<!-- Source PDF page 19 -->

[19] M. Lindner, B. Radovˇci´c, and J. Welter, Revisiting Large Neutrino Magnetic Moments, JHEP 07 (2017) 139, [1706.02555]. [20] X.-J. Xu, Tensor and scalar interactions of neutrinos may lead to observable neutrino magnetic moments, Phys. Rev. D 99 (2019), no. 7 075003, [1901.00482]. [21] K. S. Babu, S. Jana, and M. Lindner, Large Neutrino Magnetic Moments in the Light of Recent Experiments, JHEP 10 (2020) 040, [2007.04291]. [22] O. G. Miranda, D. K. Papoulias, M. T´ortola, and J. W. F. Valle, XENON1T signal from transition neutrino magnetic moments, Phys. Lett. B 808 (2020) 135685, [2007.01765]. [23] I. M. Shoemaker, Y.-D. Tsai, and J. Wyenberg, An Active-to-Sterile Neutrino Transition Dipole Moment and the XENON1T Excess, 2007.05513. [24] (XENON Collaboration)††, XENON Collaboration, E. Aprile et al., Search for New Physics in Electronic Recoil Data from XENONnT, Phys. Rev. Lett. 129 (2022), no. 16 161805, [2207.11330]. [25] K. S. Babu, S. Jana, M. Lindner, and V. P. K, Muon g −2 Anomaly and Neutrino Magnetic Moments, 2104.03291. [26] H.-T. Janka, K. Langanke, A. Marek, G. Martinez-Pinedo, and B. Mueller, Theory of Core-Collapse Supernovae, Phys. Rept. 442 (2007) 38–74, [astro-ph/0612072]. [27] P. D. Serpico, S. Chakraborty, T. Fischer, L. Hudepohl, H.-T. Janka, and A. Mirizzi, Probing the neutrino mass hierarchy with the rise time of a supernova burst, Phys. Rev. D 85 (2012) 085031, [1111.4483]. [28] J. Wallace, A. Burrows, and J. C. Dolence, Detecting the Supernova Breakout Burst in Terrestrial Neutrino Detectors, Astrophys. J. 817 (2016), no. 2 182, [1510.01338]. [29] E. O’Connor et al., Global Comparison of Core-Collapse Supernova Simulations in Spherical Symmetry, J. Phys. G 45 (2018), no. 10 104001, [1806.04175]. [30] M. Kachelriess, R. Tomas, R. Buras, H.-T. Janka, A. Marek, and M. Rampp, Exploiting the neutronization burst of a galactic supernova, Phys. Rev. D 71 (2005) 063003, [astro-ph/0412082]. [31] S. Jana, Y. P. Porto-Silva, and M. Sen, Exploiting a future galactic supernova to probe neutrino magnetic moments, 2203.01950. [32] J. Kopp, T. Opferkuch, and E. Wang, 2022. GitHub repository accompanying this paper: https://github.com/koppj/mm-astro-nu/. [33] J. R. Johansson, P. D. Nation, and F. Nori, QuTiP: An open-source Python framework for the dynamics of open quantum systems, Computer Physics Communications 183 (Aug., 2012) 1760–1772, [1110.0573]. [34] J. R. Johansson, P. D. Nation, and F. Nori, QuTiP 2: A Python framework for the dynamics of open quantum systems, Computer Physics Communications 184 (Apr., 2013) 1234–1240, [1211.6518]. [35] P. Virtanen, R. Gommers, T. E. Oliphant, M. Haberland, T. Reddy, D. Cournapeau, E. Burovski, P. Peterson, W. Weckesser, J. Bright, S. J. van der Walt, M. Brett, J. Wilson, K. J. Millman, N. Mayorov,

A. R. J. Nelson, E. Jones, R. Kern, E. Larson, C. J. Carey, ˙I. Polat, Y. Feng, E. W. Moore, J. VanderPlas, D. Laxalde, J. Perktold, R. Cimrman, I. Henriksen, E. A. Quintero, C. R. Harris, A. M. Archibald, A. H. Ribeiro, F. Pedregosa, P. van Mulbregt, and SciPy 1.0 Contributors, SciPy 1.0: Fundamental Algorithms for Scientific Computing in Python, Nature Methods 17 (2020) 261–272. [36] C. R. Harris, K. J. Millman, S. J. van der Walt, R. Gommers, P. Virtanen, D. Cournapeau, E. Wieser, J. Taylor, S. Berg, N. J. Smith, R. Kern, M. Picus, S. Hoyer, M. H. van Kerkwijk, M. Brett, A. Haldane, J. F. del R´ıo, M. Wiebe, P. Peterson, P. G´erard-Marchant, K. Sheppard, T. Reddy, W. Weckesser, H. Abbasi, C. Gohlke, and T. E. Oliphant, Array programming with NumPy, Nature 585 (Sept., 2020) 357–362. [37] E. K. Akhmedov, S. Petcov, and A. Smirnov, Neutrinos with mixing in twisting magnetic fields, Phys. Rev. D 48 (1993) 2167–2181, [hep-ph/9301211]. [38] E. K. Akhmedov, The Neutrino magnetic moment and time variations of the solar neutrino flux, in 4th International Solar Neutrino Conference, 5, 1997. hep-ph/9705451. [39] C. Broggini, C. Giunti, and A. Studenikin, Electromagnetic Properties of Neutrinos, Adv. High Energy Phys. 2012 (2012) 459526, [1207.3980]. [40] P. Kurashvili, L. Chotorlishvili, K. Kouzakov, and A. Studenikin, Coherence and mixedness of neutrino oscillations in a magnetic field, 2008.04727. [41] A. Popov and A. Studenikin, Neutrino eigenstates and flavour, spin and spin-flavour oscillations in a constant magnetic field, Eur. Phys. J. C 79 (2019), no. 2 144, [1902.08195]. [42] R. Beck, Galactic magnetic fields, Scholarpedia 2 (2007), no. 8 2411. revision #193987, available at https://scholarpedia.org/article/Galactic_ magnetic_fields. [43] R. Beck, Galactic and Extragalactic Magnetic Fields, AIP Conf. Proc. 1085 (2009), no. 1 83–96, [0810.2923]. [44] M. Haverkorn, Magnetic Fields in the Milky Way, in Magnetic Fields in Diffuse Media (A. Lazarian, E. M. de Gouveia Dal Pino, and C. Melioli, eds.), vol. 407 of Astrophysics and Space Science Library, p. 483, Jan., 2015. 1406.0283. [45] U. Klein, Galactic and Intergalactic Magnetic Fields / Ulrich Klein, Andrew Fletcher. Springer, Cham, 2015. [46] K. Ferri`ere, Interstellar magnetic fields: from galactic scales to the edge of the heliosphere, Journal of Physics: Conference Series 577 (jan, 2015) 012008. [47] J. C. Brown, M. Haverkorn, B. M. Gaensler, A. R. Taylor, N. S. Bizunok, N. M. McClure-Griffiths, J. M. Dickey, and A. J. Green, Rotation Measures of Extragalactic Sources Behind the Southern Galactic Plane: New Insights into the Large-Scale Magnetic Field of the Inner Milky Way, Astrophys. J. 663 (2007) 258–266, [0704.0458]. [48] X. Sun, W. Reich, A. Waelkens, and T. Enslin, Radio observational constraints on Galactic 3D-emission models, Astron. Astrophys. 477 (2008) 573, [0711.1572]. [49] C. Van Eck et al., Modeling the Magnetic Field in the Galactic Disk using New Rotation Measure


<!-- Source PDF page 20 -->

Observations from the Very Large Array, Astrophys. J. 728 (2011) 97, [1012.2938]. [50] T. Akahori et al., Cosmic Magnetism in Centimeter and Meter Wavelength Radio Astronomy, Publ. Astron. Soc. Jap. 70 (2018), no. 1 R2, [1709.02072]. [51] A. Kolmogorov, The Local Structure of Turbulence in Incompressible Viscous Fluid for Very Large Reynolds’ Numbers, Akademiia Nauk SSSR Doklady 30 (Jan., 1941) 301–305. [52] J. Han, Observing interstellar and intergalactic magnetic fields, Annual Review of Astronomy and Astrophysics 55 (2017), no. 1 111–157, [https://doi.org/10.1146/annurev-astro-091916-055221]. [53] R. Bartels, F. Zandanel, and S. Ando, Inverse-Compton Emission from Clusters of Galaxies: Predictions for ASTRO-H, Astron. Astrophys. 582 (2015) A20, [1501.06940]. [54] K. T. Kim, P. P. Kronberg, G. Giovannini, and T. Venturi, Discovery of intergalactic radio emission in the Coma-A1367 supercluster, Nature 341 (Oct., 1989) 720–723. [55] S. Brown and L. Rudnick, Diffuse radio emission in/around the Coma cluster: beyond simple accretion, MNRAS 412 (Mar., 2011) 2–12, [1009.4258]. [56] P. P. Kronberg, R. Kothes, C. J. Salter, and P. Perillat, Discovery of new faint radio emission on 8 ◦to 3 ′ scales in the Coma field, and some Galactic and extragalactic implications, Astrophys. J. 659 (2007) 267–274, [0704.3288]. [57] M. S. Pshirkov, P. G. Tinyakov, and F. R. Urban, New limits on extragalactic magnetic fields from rotation measures, Phys. Rev. Lett. 116 (2016), no. 19 191302, [1504.06546]. [58] T. Akahori, D. Ryu, and B. M. Gaensler, Fast Radio Bursts as Probes of Magnetic Fields in the Intergalactic Medium, Astrophys. J. 824 (2016), no. 2 105, [1602.03235]. [59] F. Vazza, M. Br¨uggen, P. M. Hinz, D. Wittor, N. Locatelli, and C. Gheller, Probing the origin of extragalactic magnetic fields with Fast Radio Bursts, Mon. Not. Roy. Astron. Soc. 480 (2018), no. 3 3907–3915, [1805.11113]. [60] S. Bhandari and C. Flynn, Probing the Universe with Fast Radio Bursts, Universe 7 (Apr., 2021) 85. [61] CHIME/FRB Collaboration, M. Amiri et al., The First CHIME/FRB Fast Radio Burst Catalog, Astrophys. J. Supp. 257 (2021), no. 2 59, [2106.04352]. [62] V. Ravi et al., The magnetic field and turbulence of the cosmic web measured using a brilliant fast radio burst, Science 354 (2016) 1249, [1611.05758]. [63] K. W. Bannister et al., A single fast radio burst localized to a massive galaxy at cosmological distance, 1906.11476. [64] L. Wolfenstein, Neutrino Oscillations in Matter, Phys.Rev. D17 (1978) 2369–2374. [65] S. P. Mikheyev and A. Y. Smirnov, Resonance enhancement of oscillations in matter and solar neutrino spectroscopy, Sov. J. Nucl. Phys. 42 (1985) 913–917. [66] S. P. Mikheyev and A. Y. Smirnov, Resonant amplification of neutrino oscillations in matter and solar neutrino spectroscopy, Nuovo Cim. C9 (1986) 17–26. [67] C.-S. Lim and W. J. Marciano, Resonant Spin - Flavor

Precession of Solar and Supernova Neutrinos, Phys. Rev. D 37 (1988) 1368–1373. [68] E. K. Akhmedov, Resonance enhancement of the neutrino spin precession in matter and the solar neutrino problem, Sov. J. Nucl. Phys. 48 (1988) 382–383. [69] E. K. Akhmedov, Resonant Amplification of Neutrino Spin Rotation in Matter and the Solar Neutrino Problem, Phys. Lett. B 213 (1988) 64–68. [70] E. K. Akhmedov, A. Lanza, S. T. Petcov, and D. W. Sciama, Resonant neutrino spin flavor precession and supernova shock revival, Phys. Rev. D 55 (1997) 515–522, [hep-ph/9603443]. [71] T. Totani and K. Sato, Resonant spin flavor conversion of supernova neutrinos and deformation of the anti-electron-neutrino spectrum, Phys. Rev. D 54 (1996) 5975–5992, [astro-ph/9609035]. [72] H. Nunokawa, Y. Z. Qian, and G. M. Fuller, Resonant neutrino spin flavor precession and supernova nucleosynthesis and dynamics, Phys. Rev. D 55 (1997) 3265–3275, [astro-ph/9610209]. [73] S. Ando and K. Sato, Resonant spin flavor conversion of supernova neutrinos: Dependence on presupernova models and future prospects, Phys. Rev. D 68 (2003) 023003, [hep-ph/0305052]. [74] E. K. Akhmedov and T. Fukuyama, Supernova prompt neutronization neutrinos and neutrino magnetic moments, JCAP 12 (2003) 007, [hep-ph/0310119]. [75] T. Yoshida, A. Takamura, K. Kimura, H. Yokomakura, S. Kawagoe, and T. Kajino, Resonant Spin-Flavor Conversion of Supernova Neutrinos: Dependence on Electron Mole Fraction, Phys. Rev. D 80 (2009) 125032, [0912.2851]. [76] J. Vidal and J. Wudka, Nondynamical contributions to left-right transitions in the solar neutrino problem, Phys. Lett. B 249 (1990) 473–477. [77] A. Y. Smirnov, The Geometrical phase in neutrino spin precession and the solar neutrino problem, Phys. Lett. B 260 (1991) 161–164. [78] E. K. Akhmedov, A. Y. Smirnov, and P. I. Krastev, Resonant neutrino spin flip transitions in twisting magnetic fields, Z. Phys. C 52 (1991) 701–709. [79] S. Jana and Y. Porto, New Resonances of Supernova Neutrinos in Twisting Magnetic Fields, 2303.13572. [80] L. Hudepohl, B. Muller, H. T. Janka, A. Marek, and G. G. Raffelt, Neutrino Signal of Electron-Capture Supernovae from Core Collapse to Cooling, Phys. Rev. Lett. 104 (2010) 251101, [0912.0260]. [Erratum: Phys.Rev.Lett. 105, 249901 (2010)]. [81] A. S. Dighe and A. Y. Smirnov, Identifying the neutrino mass spectrum from the neutrino burst from a supernova, Phys. Rev. D 62 (2000) 033007, [hep-ph/9907423]. [82] K. Scholberg, Supernova Signatures of Neutrino Mass Ordering, J. Phys. G 45 (2018), no. 1 014002, [1707.06384]. [83] F. Capozzi, M. Chakraborty, S. Chakraborty, and M. Sen, Fast flavor conversions in supernovae: the rise of mu-tau neutrinos, Phys. Rev. Lett. 125 (2020) 251801, [2005.14204]. [84] S. Shalgar and I. Tamborra, Three flavor revolution in fast pairwise neutrino conversion, Phys. Rev. D 104 (2021), no. 2 023011, [2103.12743]. [85] R. Bollig, H. T. Janka, A. Lohs, G. Martinez-Pinedo,


<!-- Source PDF page 21 -->

C. J. Horowitz, and T. Melson, Muon Creation in Supernova Matter Facilitates Neutrino-driven Explosions, Phys. Rev. Lett. 119 (2017), no. 24 242702, [1706.04630]. [86] Hyper-Kamiokande Collaboration, K. Abe et al., Hyper-Kamiokande Design Report, 1805.04163. [87] J. Lagoda, The Hyper-Kamiokande Project, PoS FPCP2017 (2017) 024. slides available from https://indico.cern.ch/event/586719/ contributions/2531379/. [88] DUNE Collaboration, B. Abi et al., Deep Underground Neutrino Experiment (DUNE), Far Detector Technical Design Report, Volume II DUNE Physics, 2002.03005. [89] DUNE Collaboration, B. Abi et al., Supernova Neutrino Burst Detection with the Deep Underground Neutrino Experiment, 2008.06647. [90] I. Gil Botella and A. Rubbia, Oscillation effects on supernova neutrino rates and spectra and detection of the shock breakout in a liquid argon TPC, JCAP 10 (2003) 009, [hep-ph/0307244]. [91] A. Strumia and F. Vissani, Precise quasielastic neutrino/nucleon cross-section, Phys. Lett. B 564 (2003) 42–54, [astro-ph/0302055]. [92] G. Ricciardi, N. Vignaroli, and F. Vissani, An accurate evaluation of electron (anti-)neutrino scattering on nucleons, JHEP 08 (2022) 212, [2206.05567]. [93] K. Nakazato, T. Suzuki, and M. Sakuda, Charged-current scattering off 16O nucleus as a detection channel for supernova neutrinos, PTEP 2018 (2018), no. 12 123E02, [1809.08398]. [94] J. N. Bahcall, M. Kamionkowski, and A. Sirlin, Solar neutrinos: Radiative corrections in neutrino - electron scattering experiments, Phys. Rev. D 51 (1995) 6146–6158, [astro-ph/9502003]. [95] Borexino Collaboration, M. Agostini et al., Limiting neutrino magnetic moments with Borexino Phase-II solar neutrino data, Phys. Rev. D 96 (2017), no. 9 091103, [1707.09355]. [96] A. G. Beda, V. B. Brudanin, V. G. Egorov, D. V. Medvedev, V. S. Pogosov, E. A. Shevchik, M. V. Shirchenko, A. S. Starostin, and I. V. Zhitnikov, Gemma experiment: The results of neutrino magnetic moment search, Phys. Part. Nucl. Lett. 10 (2013) 139–143. [97] PandaX-II Collaboration, X. Zhou et al., A Search for Solar Axions and Anomalous Neutrino Magnetic Moment with the Complete PandaX-II Data, Chin. Phys. Lett. 38 (2021), no. 1 011301, [2008.06485]. [Erratum: Chin.Phys.Lett. 38, 109902 (2021)]. [98] IceCube Collaboration, M. G. Aartsen et al., Evidence for High-Energy Extraterrestrial Neutrinos at the IceCube Detector, Science 342 (2013) 1242856, [1311.5238]. [99] IceCube Collaboration, M. G. Aartsen et al., Observation of High-Energy Astrophysical Neutrinos in Three Years of IceCube Data, Phys. Rev. Lett. 113 (2014) 101101, [1405.5303]. [100] IceCube Collaboration, R. Abbasi et al., The IceCube high-energy starting event sample: Description and flux characterization with 7.5 years of data, Phys. Rev. D 104 (2021) 022002, [2011.03545]. [101] IceCube Collaboration, R. Abbasi et al., Improved Characterization of the Astrophysical Muon–neutrino

Flux with 9.5 Years of IceCube Data, Astrophys. J. 928 (2022), no. 1 50, [2111.10299]. [102] IceCube Collaboration, M. G. Aartsen et al., Characteristics of the diffuse astrophysical electron and tau neutrino flux with six years of IceCube high energy cascade data, Phys. Rev. Lett. 125 (2020), no. 12 121104, [2001.09520]. [103] IceCube Collaboration, M. G. Aartsen et al., Measurements using the inelasticity distribution of multi-TeV neutrino interactions in IceCube, Phys. Rev. D 99 (2019), no. 3 032004, [1808.07629]. [104] P. Kurashvili, K. A. Kouzakov, L. Chotorlishvili, and A. I. Studenikin, Spin-flavor oscillations of ultrahigh-energy cosmic neutrinos in interstellar space: The role of neutrino magnetic moments, Phys. Rev. D 96 (2017), no. 10 103017, [1711.04303]. [105] A. K. Alok, N. R. S. Chundawat, and A. Mandal, Cosmic neutrino flux and spin flavor oscillations in intergalactic medium, 2207.13034. [106] A. Lichkunov, A. Popov, and A. Studenikin, Three-flavour neutrino oscillations in a magnetic field, 2207.12285. [107] N. R. Singh Chundawat, A. Mandal, and T. Sarkar, UHE neutrinos encountering decaying and non-decaying magnetic fields of compact stars, 2208.06644. [108] I. Esteban, M. C. Gonzalez-Garcia, M. Maltoni, T. Schwetz, and A. Zhou, The fate of hints: updated global analysis of three-flavor neutrino oscillations, JHEP 09 (2020) 178, [2007.14792]. see http://www.nu-fit.org; we use numbers from the NuFit 5.1 fit. [109] IceCube Collaboration, M. G. Aartsen et al., A combined maximum-likelihood analysis of the high-energy astrophysical neutrino flux measured with IceCube, Astrophys. J. 809 (2015), no. 1 98, [1507.03991]. [110] M. Bustamante and M. Ahlers, Inferring the flavor of high-energy astrophysical neutrinos at their sources, Phys. Rev. Lett. 122 (2019), no. 24 241101, [1901.10087]. [111] IceCube-Gen2 Collaboration, M. G. Aartsen et al., IceCube-Gen2: the window to the extreme Universe, J. Phys. G 48 (2021), no. 6 060501, [2008.04323]. [112] IceCube, Fermi-LAT, MAGIC, AGILE, ASAS-SN, HAWC, H.E.S.S., INTEGRAL, Kanata, Kiso, Kapteyn, Liverpool Telescope, Subaru, Swift NuSTAR, VERITAS, VLA/17B-403 Collaboration, M. G. Aartsen et al., Multimessenger observations of a flaring blazar coincident with high-energy neutrino IceCube-170922A, Science 361 (2018), no. 6398 eaat1378, [1807.08816]. [113] IceCube Collaboration, M. G. Aartsen et al., Neutrino emission from the direction of the blazar TXS 0506+056 prior to the IceCube-170922A alert, Science 361 (2018), no. 6398 147–151, [1807.08794]. [114] IceCube Collaboration, R. Abbasi et al., Evidence for neutrino emission from the nearby active galaxy NGC 1068, Science 378 (2022), no. 6619 538–543. [115] P. Vogel and J. Engel, Neutrino Electromagnetic Form-Factors, Phys. Rev. D 39 (1989) 3378. [116] J. D. Hunter, Matplotlib: A 2d graphics environment, Computing in Science & Engineering 9 (2007), no. 3 90–95.


<!-- Source PDF page 22 -->

[117] M. H. et al, python-ternary: Ternary plots in python, Zenodo 10.5281/zenodo.594435 (2015). [118] M. Beuthe, Oscillations of neutrinos and mesons in

```text
quantum field theory, Phys. Rept. 375 (2003) 105–218,
[hep-ph/0109119].
```

