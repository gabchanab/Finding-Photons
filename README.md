# The Ability of the *Powheg+Pythia8* Model to predict the production of Photons in the Drell-Yan process

## Photon and Dilepton System Analysis (ATLAS vs MC)

---

### Abstract

The performance of the *Powheg+Pythia8* model was tested against the 2015 ATLAS 13 TeV proton-proton collision dataset in order to see how well it understood the production of photons that radiate off leptons in Z boson decays. Events containing the production of two muons along with a photon were collected and their kinematic properties were displayed in the form of histograms and ratio plots. Ratio plots for the invariant mass and transverse momentum of the dilepton system showed that the simulation understood this system well. However, for the llγ system, these plots showed a lot more variance in predictive ability, with more overproduction of events for both momentum plots, and generally more underproduction of µµγ events in the invariant mass of the llγ system. Future changes that could give more insight into the model’s ability to generate µµγ events could include further study of the Drell-Yan process at low masses when the photon (γ^*) is more prominent. Comparison of these distributions with the ones made in this study would also provide information on how well the simulation understands the low mass Drell-Yan process.

---

## Overview

This project performs a comparative analysis of **measured and experimental data** and **simulated Monte Carlo data** related to **dilepton and photon systems** in high-energy particle collisions. The goal is to apply physics-inspired selection criteria and produce histograms for key kinematic observables — enabling direct comparisons between data and simulation.


The final output includes comparison plots (e.g. transverse momentum distributions), such as:

![Final Graph Output](output/finalGraph.pdf)

---

## Project Structure

|- input/ 
||- measuredFiles/ #ROOT files containing measured detector data
||- MonteCarloFiles/ # ROOT files containing simulated (MC) data
|- output/ 
||- simMeasHits.root # Output file of separate histograms of all observables for each system
||- finalGraph.pdf # Sample comparison plot (e.g. photon pT)
|- cuttingMain.py # Main Python script performing event selection --> creates simMeasHists.py
|- compaisonPlots.py # second Python script combining the measured and MC data of a particular observable in a specific system onto one graph ---> creates finalGraph.pdf
|- README.md # This file


---


## Input

- Already contained in the MC and measured data folders are three .root sample data files which can be used to show how the .py files work
- For further use with other data, simulated data files should be uploaded into MonteCarloFiles/ and measured data files should be uploaded into measuredFiles/


---


## Analysis Description

The script `cuttingMain.py` does the following:

1. **Loads Measured and MC Data:**
   - Uses ROOT's `TChain` to load multiple ROOT files for both data types.

2. **Applies Physics-Based Event Selection Cuts:**
   - Requires ≥2 tight muons (with \( p_T > 25 \) GeV for leading muon)
   - Opposite charge and same lepton type (muon pair)
   - Invariant mass of the dilepton system \( M_{\ell\ell} > 65 \) GeV
   - Optional tight photon with \( p_T > 20 \) GeV and angular separation \( \Delta R > 0.4 \)

3. **Fills Histograms:**
   - Kinematic variables: invariant mass, transverse momentum \(p_T\), pseudorapidity \(\eta\), and azimuthal angle \(\phi\)
   - Histograms are separated into four physics systems:
     - Inclusive dilepton
     - Exclusive dilepton (with isolated photon veto)
     - Photon-only system
     - Combined dilepton + photon system

4. **Writes Histograms to Output ROOT File**


The script `comparisonPlots.py` conatins a function `drawHists()` which draws a plot with both measured and MC data on one graph with their ratio below. This takes four arguments:

1. **v** str:
    - Chosen Observable takes values "Mass", "Pt", "Eta" or "Phi" representing Invariant Mass, Transverse Momentum, Pseudorapidity and Azimuthal Angle respectivley.

2. **IorE** str:
    - Choose between events that are inclusive or exclusive to photons takes values "Inc" or "Exc".
    
3. **isPhoton** *bool (default==False):
    - Does the system include photons. 

4. **printChiSqr** *bool (default==False): 
    - Option to calculate and print the chi^2 value to the legend. 

---


## Output

- Histograms are stored in `output/simMeasHists.root`
- Final plots (e.g. comparison of photon \(p_T\)) can be found in `output/finalGraph.pdf`

Sample plot shows:
- Data vs MC for photon \(p_T\)
- Ratio plot (Data / MC)
- Chi-squared value for shape agreement

---

## Requirements

- Python 3.x
- ROOT with PyROOT bindings
- NumPy

To install ROOT on macOS (if needed):
```bash
brew install root

## Notes 

- All histograms are generated with 75 bins over variable-specific ranges.
- All ROOT files are assumed to contain a tree named 'analysis' with expected branches for lepton and photon properties. 
- These can both be edited in 'cuttingMain.py'
