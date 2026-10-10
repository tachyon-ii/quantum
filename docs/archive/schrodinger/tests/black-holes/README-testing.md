For testing your Critical Boundary Layer (CBL) black hole model, here are the most relevant observational datasets currently available:

## Event Horizon Telescope (EHT) Data

**Public releases available:**
- **M87*** (2019, 2021): Full visibility data and calibrated images at 230 GHz
- **Sgr A*** (2022): First image data and analysis products
- Dataset access: [EHT Data Portal](https://eventhorizontelescope.org/for-astronomers/data)
- Includes: Visibility amplitudes, closure phases, calibrated FITS images

**What to look for:**
- Ring thickness measurements (your model predicts ~0.25% edge sharpness)
- Brightness asymmetries around the ring
- Comparison of 2017 vs 2018 observations for variability

## GRAVITY Interferometer Data

**ESO VLT/GRAVITY observations:**
- Near-IR interferometry of Sgr A* flares
- Astrometric positions of hot spots orbiting at ~3-5 r_g
- Public data via [ESO Archive](http://archive.eso.org/eso/eso_archive_main.html)
- Key papers: GRAVITY Collaboration 2018-2023

**Relevant for CBL:**
- Orbital dynamics very close to your predicted boundary layer
- Could show deviations from Keplerian orbits if CBL affects dynamics

## X-ray Timing Data

**RXTE Archive (completed mission):**
- High-frequency QPOs from stellar-mass black holes
- Available at [HEASARC](https://heasarc.gsfc.nasa.gov/docs/rxte/data_archive.html)
- Systems: GRS 1915+105, XTE J1550-564, GRO J1655-40

**NICER (ongoing):**
- Current X-ray timing of black hole binaries
- Public data releases via HEASARC
- Better timing resolution than RXTE

**Your model predictions to test:**
- HFQPO frequency ratios (you predict 3:2 or other rational ratios)
- Phase lags between different QPO modes
- Mass scaling: f_n ∝ M^(-1)

## Gravitational Wave Data

**LIGO/Virgo/KAGRA:**
- Merger ringdown signals
- Data at [Gravitational Wave Open Science Center](https://www.gw-openscience.org)
- Look for: Echo signals 2-20 ms after merger (for stellar mass BHs)

**What CBL predicts:**
- Delayed echoes from the finite-redshift cavity
- Modified ringdown frequencies
- Deviations in quasi-normal mode spectrum

## Radio Monitoring Data

**VLBA Monitoring:**
- Long-term monitoring of Sgr A* and M87
- Data available through [NRAO Archive](https://data.nrao.edu)
- Multi-frequency observations (good for separating plasma vs metric effects)

**MeerKAT/ALMA:**
- Some public data releases
- Higher frequency = less plasma scattering, cleaner view of shadow

## Practical Analysis Approach

Start with the EHT M87* data:
1. Download the calibrated visibility data
2. Fit ring models with variable edge sharpness
3. Compare standard GR (sharp but not infinitely sharp) vs CBL (enhanced sharpness)
4. Look for thickness variations around the ring

For the QPO analysis:
1. Get RXTE archival data for GRS 1915+105 (well-studied, lots of QPOs)
2. Compute power spectra
3. Look for your predicted frequency ratios and phase relationships
4. Test mass scaling using multiple sources

## Critical Tests

Your CBL model makes specific predictions that differ from GR:
- **Edge sharpness**: CBL predicts sharper transition than pure GR
- **Ring thickness**: Should vary with observing frequency if plasma present
- **QPO harmonics**: Specific frequency ratios from cavity modes
- **Time delays**: Echo signals in both GW and EM observations

The EHT collaboration has been conservative about releasing raw data, but what's available should be sufficient to test whether the ring edge sharpness matches your CBL predictions versus standard GR. The combination of improved EHT resolution (adding more telescopes) and multi-wavelength observations will be particularly powerful for separating plasma effects from genuine metric modifications.