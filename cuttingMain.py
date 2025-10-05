import ROOT
import numpy as np
import os

# set up files: Add measured data to measured data TChain and 
# add simulated data to MC data TChain:


measFiles = ROOT.TChain("analysis")
simFiles = ROOT.TChain("analysis")

# read data files for MC and measured separately
inPath = ["input/measuredFiles","input/MonteCarloFiles"]
measData = os.listdir("./"+inPath[0])
simData = os.listdir("./"+inPath[1])

# add data files to TChain objects
for f in measData:
    measFiles.Add(inPath[0]+"/"+f)
for g in simData:
    simFiles.Add(inPath[1]+"/"+g)


dataFiles = [measFiles, simFiles]

print(measData)

# create output file:
outFilePath = "./output/simMeasHists.root"
outFile = ROOT.TFile(outFilePath,"recreate")

ROOT.gStyle.SetOptStat(0)

# set observables and histogram labels
vars = ["Mass" , "Pt" , "Eta" , "Phi"]
varLabels = {
    "Mass" : "Invariant Mass; Mass [GeV]; Events",
    "Pt" : "Transverse Momentum; p_{T} [GeV]; Events",
    "Eta" : "Rapidity; #eta; Events",
    "Phi" : "Azimuthal Angle; #phi [rad]; Events"
}




# create arrays to store histograms for each system
diLepIncHists = []
diLepExcHists = []
photonHists = []
diLepPhotonHists = []
allHistograms = [diLepIncHists , diLepExcHists , photonHists , diLepPhotonHists]

# create Histogram objects for each system for MC and meas separately:
NoBins = 75
histoRange = [[NoBins,0,200],[NoBins,0,500],[NoBins,-4,4],[NoBins,0,4]]
systemLabels = [["dilepInc" , " Inclusive Dilepton "] , 
                ["dilepExc" , " Exclusive Dilepton "] , 
                ["photon" , " Photon "] , 
                ["dilepPho" , " Dilepton + Photon "]
                ]
for h in range(len(allHistograms)):
    for v in range(len(vars)):
        histLabel = systemLabels[h][0]+vars[v]
        histTitle = systemLabels[h][1]+varLabels[vars[v]]
        measHist = ROOT.TH1F(histLabel , histTitle , histoRange[v][0] , histoRange[v][1] , histoRange[v][2])
        MCHist = ROOT.TH1F("MC "+histLabel , "MC "+histTitle , histoRange[v][0] , histoRange[v][1] , histoRange[v][2])
        allHistograms[h].append(measHist)
        allHistograms[h].append(MCHist)
        # add histograms to output file
        outFile.Add(measHist)
        outFile.Add(MCHist)




# method to fill histogram with specific variable
def plotVar(graph, fourVec, v):
    if v=="Pt":
        graph.Fill(fourVec.Pt())
    if v=="Eta":
        graph.Fill(fourVec.Eta())
    if v=="Phi":
        graph.Fill(fourVec.Phi())
    if v=="Mass":
        graph.Fill(fourVec.M())

# method to calculate the angular separation between two objects
def findAngle(photon, particle):
    dETA = (np.abs(photon.Eta()-particle.Eta()))**2
    dPHI = (min(np.abs(photon.Phi()-particle.Phi()),2*np.pi-np.abs(photon.Phi()-particle.Phi())))**2
    dR = np.sqrt(dETA+dPHI)
    return dR


# create particle objects:
leadLepton = ROOT.TLorentzVector()
trailLepton = ROOT.TLorentzVector()
extraPhoton = ROOT.TLorentzVector()



#EVENT SELECTION#

#alternate between measured and MC files:
for f in range(len(dataFiles)):
    # get data
    tree = dataFiles[f]
    Nevents = tree.GetEntries()
    frac = 0.0
    ev = 0
    print("Total number of entries: ",Nevents)

    for event in tree:
        # print percentage of processed events 
        ev+=1
        tempFrac = 100*(ev/Nevents)
        if tempFrac-frac>5:
            frac=tempFrac
            print("Processing event", ev, "Percentage Complete =", int(frac),"%")

        # build a list of tight_photons
        tight_photons=[]
        if tree.photon_n >= 1:
            for iph in range(tree.photon_n):
                if tree.photon_isTightID[iph] and tree.photon_pt[iph]>20:      
                    aphoton=ROOT.TLorentzVector()
                    aphoton.SetPtEtaPhiE(tree.photon_pt[iph], tree.photon_eta[iph], tree.photon_phi[iph], tree.photon_e[iph])
                    tight_photons.append(aphoton)

        # Cut #1: At least 2 leptons
        tight_leptons = []
        tight_leptons_charge = []
        if tree.lep_n >= 2:
            for ilep in range(tree.lep_n): #check tight photons ***
                if tree.lep_isTightID[ilep]:             
                    alepton = ROOT.TLorentzVector()
                    alepton.SetPtEtaPhiE(tree.lep_pt[ilep], tree.lep_eta[ilep], tree.lep_phi[ilep], tree.lep_e[ilep])
                    
                    # Cut 1a: Remove low Pt leptons
                    if alepton.Pt()>10:
                        tight_leptons.append(alepton)
                        tight_leptons_charge.append(tree.lep_charge[ilep])
            
            # Cut 1b: Remove low Pt leptons
            if len(tight_leptons) >=2 and tight_leptons[0].Pt()>25:

                # Cut #2: Leptons with opposite charge
                if (tree.lep_charge[0] != tree.lep_charge[1]):
                
                    # Cut #3: Leptons of the same family (check muons only)
                    if (tree.lep_type[0] == 13 and tree.lep_type[1] == 13):

                        leadLepton = tight_leptons[0]
                        trailLepton = tight_leptons[1]
                        dilepton = leadLepton+trailLepton

                        # Cut #4: Check mass of dilepton system is high enough
                        if dilepton.M()>65:
                            for x in range(int(np.floor(len(vars)))):
                                plotVar(diLepIncHists[2*x+f], dilepton, vars[x])

                            # Cut #5: Check angular separation between photon and muon
                            if len(tight_photons)>0:
                                
                                extraPhoton = tight_photons[0]
                                dR = findAngle(tight_photons[0], leadLepton)
                                
                                if dR > 0.4:
                                    dilepPhoton = dilepton+extraPhoton

                                    for x in range(int(np.floor(len(vars)))):
                                        plotVar(diLepExcHists[2*x+f], dilepton, vars[x])
                                        plotVar(diLepPhotonHists[2*x+f], dilepPhoton, vars[x])
                                        plotVar(photonHists[2*x+f], extraPhoton, vars[x])


# write all histograms to output file
outFile.Write()
