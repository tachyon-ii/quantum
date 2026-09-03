# EMC Effect Periodic Structure Analysis

## Overview
Analysis of Jefferson Lab E03-103 experiment data (https://hallcweb.jlab.org/experiments/E03103/) to search for periodic structures in nuclear EMC ratios that might indicate geometric substructure in nucleons.

Main repository (https://hallcweb.jlab.org/experiments/)

```
Index of /experiments
[ICO] Name  Last modified Size  Description
[PARENTDIR] Parent Directory    -  
[DIR] A1n/  2020-12-23 13:02  -  
[DIR] E02019/ 2012-11-27 13:27  -  
[DIR] E03103/ 2024-02-07 14:42  -  
[DIR] E12-15-001/ 2018-11-27 15:17  -  
[DIR] EMC_SRC/  2012-02-21 14:41  -  
[DIR] ERR/  2017-01-20 09:48  -  
[DIR] ERR_3exps/  2017-06-21 16:15  -  
[DIR] GEp-III/  2018-05-22 11:50  -  
[DIR] HALLC_SIDIS/  2025-06-06 15:09  -  
[DIR] PAC40/  2020-08-07 04:07  -  
[DIR] PolHe3-2019/  2022-05-13 11:12  -  
[DIR] fpi/  2010-04-22 09:49  -  
[DIR] gen01/  2009-12-16 14:12  -  
[DIR] hks/  2005-09-23 16:25  -  
[DIR] jpsi-007/ 2018-12-07 16:06  -  
[DIR] rcs/  2008-01-26 16:27  -  
[DIR] rosen07/  2006-08-31 11:42  -  
[DIR] rss/  2011-10-03 11:17  -  
[DIR] sane/ 2020-07-10 16:27  -  
```

## Data Source
- **Experiment**: JLab E03-103 (XEM) plus CLAS and historical SLAC data
- **File**: EMC_Supplemental_Updated.xlsx
- **Content**: EMC ratios (nucleus/deuteron) for various nuclei
- **Nuclei**: He-3, He-4, Be-9, C-12, Al-27, Fe-56, Cu-64, Au-197, Pb-208
- **Total points**: ~370 measurements across x = 0.09 to 0.95

## Key Findings

### 1. Periodic Structure Discovery
When combining all nuclei data and phase-folding at period 0.167 (1/6), we consistently observe:
- **7 peaks** in the phase-folded data (not the expected 6)
- **Mean inter-peak spacing**: 0.024 in Bjorken-x units
- **Actual periodicity**: ~0.143 (approximately 1/7)

### 2. Dataset Dependence
- **SLAC data alone**: Weak/no periodic structure (older, coarser resolution)
- **CLAS data**: Clear 7-peak pattern, moderate regularity
- **XEM data**: Clear 7-peak pattern, good regularity
- **Combined JLab**: Robust 7-peak structure

### 3. Nuclear Mass Dependence
- **He-3 alone**: 6 peaks, period ~0.166 (nearly exact 1/6)
- **Light nuclei**: Transition to 7 peaks
- **All heavier nuclei**: Consistent 7-peak pattern
- Pattern persists even when removing light elements

### 4. Structure at Rational Fractions
All nuclei show consistent structure at:
- **x ≈ 1/3**: Enhanced ratios (~1.00)
- **x ≈ 2/3**: Suppressed ratios (~0.87-0.93)
- Effect strengthens with atomic number Z

## Analysis Methods

### Tools Developed
1. **Individual nucleus analyzer**: Spectral analysis per nucleus
2. **Meta-analyzer**: Combines normalized data from multiple nuclei
3. **Phase-folding**: Tests for periodicity at specific frequencies
4. **Binning strategies**: Irrational bin widths to avoid aliasing

### Key Techniques
- Polynomial detrending to remove broad EMC effect
- Lomb-Scargle periodogram for uneven sampling
- Weighted spline interpolation for smooth curves
- Peak detection with inter-peak distance analysis

## Physical Interpretation

The observed ~0.143 periodicity (7-fold structure) differs from the predicted 1/6 (hexagonal) but suggests:

1. **Intrinsic nucleon structure**: Periodicity appears even in He-3 (3 nucleons)
2. **Not emergent nuclear effect**: Too simple systems show it
3. **Compression-dependent**: Transition from 6 to 7 peaks with nuclear size
4. **Universal feature**: Same peak positions across all nuclei

## Theoretical Context

The analysis was motivated by a geometric model proposing:
- Nucleons adopt truncated octahedral (TO) geometry under compression
- TO has 14 faces (8 hexagonal, 6 square)
- Expected 1/6 periodicity from hexagonal faces
- Observed 1/7 might indicate modified geometry or edge effects

## Conclusions

1. **Robust periodic structure exists** in JLab EMC data with ~0.024 x-unit spacing
2. **Not instrumental artifact**: Persists across experiments, binning schemes
3. **Nuclear geometry signature**: Possibly indicates internal nucleon structure
4. **Requires further investigation**: The 7-fold vs 6-fold pattern needs explanation

## Code Repository

Main analysis scripts:
- `meta_analyzer.py`: Combined multi-nucleus analysis
- `simple_analyzer.py`: Direct periodicity testing
- `emc_cli.py`: Command-line interface for analysis

## Data Files
- `data.xlsx`: Reformatted EMC_Supplemental_Updated.xlsx
- Various output CSVs with analysis results