### Primary Sources for Black Hole Radio Telescope Data

1. **Event Horizon Telescope (EHT) Data**
   - **Description**: EHT is the gold standard for BH imaging, using very-long-baseline interferometry (VLBI) at 1.3 mm (230 GHz) and 0.87 mm (345 GHz) to capture Sgr A* and M87* shadows. Data includes ring diameters (~40 μas for M87*), polarization (EVPA patterns), and multi-frequency constraints—key for our Φ-boundary chromaticity (T(ω,Φ) shifts) and birefringence predictions.
   - **Access**:
     - **Public Repository**: EHT Collaboration releases processed images, visibilities, and reconstructed datasets via their website (eventhorizontelescope.org/data) and GitHub (github.com/eventhorizontelescope). Raw visibilities (uv-fits format) and calibrated data available for 2017-2021 campaigns (M87* 2017, Sgr A* 2022).
     - **Data Archives**: ALMA Science Archive (almascience.nrao.edu/aq) hosts EHT data (ALMA as core array). Search for project codes like 2016.1.01114.V (M87*) or 2017.1.00841.V (Sgr A*). Formats: FITS, CASA tables.
     - **Zenodo**: EHT datasets and papers (e.g., M87* 2017: zenodo.org/records/3748311) include visibilities, scripts, and reconstructed images.
   - **Relevance to TOE**: Test ring size offsets (230 vs. 345 GHz, our T(ω) predicts ~5-10% shift vs. achromatic GR), EVPA twists (birefringence beyond GRMHD), and potential HFQPO-like modulations in time-series (p-mode leakage). Use Python tools (eht-imaging, THEMIS) for analysis.
   - **Steps**:
     1. Visit eventhorizontelescope.org/data or ALMA archive.
     2. Download uv-fits (e.g., M87* 2017 April 5-11) or calibrated visibilities.
     3. Use Python packages (eht-imaging: pip install ehtim) for imaging/reconstruction.
     4. Compare ring diameters across frequencies or analyze polarization maps.

2. **Atacama Large Millimeter/submillimeter Array (ALMA)**
   - **Description**: ALMA, a key EHT component, provides high-resolution mm/sub-mm data for Sgr A* and M87* (1.3 mm, 3 mm). Includes visibilities, continuum, and spectral line data, critical for our CMB medium tests (Φ-saturation, e^n/π relics).
   - **Access**:
     - **ALMA Science Archive**: almascience.nrao.edu/aq (or ESO/NAOJ mirrors). Search "Sgr A*" or "M87" with filters for Band 6 (1.3 mm, 230 GHz) or Band 3 (3 mm, 100 GHz).
     - **Formats**: FITS, CASA (requires CASA software for processing).
     - **Public Data**: EHT-related datasets (e.g., 2017.1.00841.V) public after proprietary period (~1 year). Check ALMA Cycle 5-9.
   - **Relevance to TOE**: Probe Φ-boundary chromaticity (ring size, T(ω)), test CMB as resonant medium (dispersionless propagation, e^n/π modes). Spectral data for potential instability-driven oscillations (p-modes, our HFQPO recipe: f_n = ω_n / 2π · g_GR).
   - **Steps**:
     1. Access ALMA archive, query "Sgr A*" or "M87" (e.g., project 2016.1.01114.V).
     2. Download CASA tables or FITS (continuum/polarization).
     3. Process with CASA or eht-imaging for ring fits or time-series analysis.

3. **Very Long Baseline Array (VLBA)**
   - **Description**: VLBA provides high-resolution radio data (cm to mm wavelengths) for BH jets and accretion (Sgr A*, M87*). Complements EHT with broader frequency range (e.g., 7 mm, 43 GHz), useful for our jet puncture predictions (anisotropic Φ leakage).
   - **Access**:
     - **NRAO Archive**: science.nrao.edu/facilities/vlba/data-archive. Search for Sgr A* or M87 (e.g., project codes BM272, BL229).
     - **Formats**: FITS, IDI-FITS (use AIPS or CASA for processing).
     - **Public Data**: Available post-proprietary (~1 year).
   - **Relevance to TOE**: Test jet asymmetry (anisotropic drag from Φ-boundary), complement EHT ring data for multi-scale Φ effects (λ_0 compression vs. longer λ_n in jets). Time-series for HFQPO-like variability.
   - **Steps**:
     1. Visit NRAO archive, query "Sgr A*" or "M87".
     2. Download FITS for 43 GHz or 86 GHz observations.
     3. Analyze with AIPS/CASA for jet structure or variability.

4. **Chandra X-ray Observatory and NuSTAR**
   - **Description**: Chandra (0.5-7 keV) and NuSTAR (8-24 keV) provide X-ray data for BH accretion and jets, not horizon-scale (obscured by gas). Relevant for our TOE's accretion physics (Φ-modulated emission, T(ω) leakage as blackbody-like spectrum, high-freq peak). NuSTAR's COSMOS field data shows AGN populations, not rainbow horizons.
   - **Access**:
     - **Chandra Data Archive**: cxc.cfa.harvard.edu/cda (search "Sgr A*" or "M87", e.g., ObsID 3392, 242 for Sgr A*).
     - **NuSTAR Archive**: heasarc.gsfc.nasa.gov/docs/nustar/nustar_archive.html (COSMOS field, ObsID 60002023002).
     - **Formats**: FITS (event lists, spectra, images).
     - **Public Data**: Available post-proprietary (~1 year).
   - **Relevance to TOE**: Test non-horizon Φ effects (accretion emissivity, δI/I ∝ ∂ln T/∂Φ · ∂Φ/∂r · ξ_r(t)), HFQPO hard-band enhancement (p-modes, f_2/f_1 ~ 3:2). Clarify: X-ray "flavors" from gas, not rainbow Φ (our mm prediction).
   - **Steps**:
     1. Access Chandra/NuSTAR archives, query BH targets.
     2. Download FITS event lists/spectra.
     3. Use XSPEC or Sherpa for spectral fits, timing analysis for QPOs.

5. **General Astronomy Archives**
   - **HEASARC (NASA)**: heasarc.gsfc.nasa.gov hosts multi-wavelength data (Chandra, NuSTAR, XMM-Newton). Search "Sgr A*" or "M87" for X-ray/radio datasets.
   - **CDS VizieR**: vizier.u-strasbg.fr offers catalog data (e.g., BH masses, distances) to cross-correlate with EHT/VLBA.
   - **Relevance**: Combine radio (EHT/VLBA) with X-ray for multi-scale Φ tests (jets vs. rings), constrain M, a*, i for HFQPO fits (f_n = ω_n / 2π · g_GR).
   - **Steps**:
     1. Query HEASARC/VizieR for BH datasets.
     2. Cross-match EHT radio with X-ray timing (e.g., Sgr A* flares).

### Practical Steps to Access and Use Data
1. **Start with EHT**:
   - Go to eventhorizontelescope.org/data or Zenodo (e.g., doi:10.5281/zenodo.3748311).
   - Download M87* 2017 or Sgr A* 2022 uv-fits.
   - Install eht-imaging (pip install ehtim) or THEMIS for Python analysis.
   - Fit ring diameters (230 vs. 345 GHz) to test our chromaticity (T(ω,Φ) predicts ~5% offset).
2. **Supplement with ALMA/VLBA**:
   - ALMA archive for raw visibilities (CASA processing).
   - VLBA for jet data (AIPS for cm/mm imaging).
   - Analyze time-series for HFQPO-like variability (f_1 ~ 190 Hz, f_2 ~ 285 Hz for 10 M_⊙).
3. **X-ray for Context**:
   - Chandra/NuSTAR for accretion (HEASARC, XSPEC for spectra).
   - Test hard-band QPO enhancement (our T(ω) predicts overtone dominance).
4. **Tools**:
   - Python: eht-imaging, Astropy (FITS handling), NumPy/SciPy (spectral fits).
   - CASA/AIPS for radio data reduction.
   - XSPEC/Sherpa for X-ray timing.

### Relevance to Our Resonance TOE
Our black-holes.md predicts:
- **Chromatic Rings**: EHT data (230-345 GHz) to test T(ω,Φ) offset vs. achromatic GR (plasma-marginalized, ~5-10% shift expected).
- **HFQPOs**: Time-series for p-modes (f_2/f_1 ~ 3:2, jitter Δf ∝ -ΔL/L, hard-band enhancement), tied to λ_0 interior oscillations.
- **Polarization Twists**: EVPA patterns for birefringence (Φ-boundary vs. GRMHD).
- **DM Context**: Capsid unassembled parts as halo mass (test via lensing maps, 511 keV not halo-wide).
