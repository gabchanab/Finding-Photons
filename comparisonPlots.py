import ROOT
from ROOT import gPad as gp
import numpy as np
import array

# open file with MC and measured data graphs
f = ROOT.TFile.Open("./output/simMeasHists.root")

# set up canvas
ROOT.gStyle.SetOptStat(0)

compCanvas = ROOT.TCanvas("compCanvas","c",800,600)
gp.SetTickx(1)
gp.SetTicky(1)


# create graphing variables and ranges
NoBins = 75
histoRange = [[NoBins,5,250],[NoBins,0,350],[NoBins,-4,4],[NoBins,-4,4]]
vars = ["Mass", "Pt" , "Eta" , "Phi"] 

fitRanges = {
    "Mass" : [50,250],
    "Pt" : [20,500],
    "Eta" : [-4,4],
    "Phi" : [-4,4]
}

variables = {
    "Mass" : ["Invariant Mass" , "M" , " [GeV]"],
    "Pt" : ["Transverse Momentum" , "P_{t}" , " [GeV]"],
    "Eta" : ["Rapidity" , "#eta" , " "],
    "Phi" : ["Azimuthal Angle" , "#phi" , " [rad]"]
}

incOrExc = {
    "Inc" : "Inclusive: ",
    "Exc" : "Exclusive: "
}

systemType = ["_{ll}" , "_{ll#gamma}"]
titleNames = ["Dilepton" , "Dilepton+#gamma"]
graphedSystem = [ "twoLep" , ["Inc" , "Exc"]]

# function that puts simulated and measured data onto one graph

def drawHists(v, IorE, isPhoton=False, printChiSqr=False):
    # label variables
    fileName = "dilep" + IorE + v
    xAxisLabel = variables[v][1] + systemType[isPhoton] + variables[v][2]
    titleLabel = incOrExc[IorE] + variables[v][0] + " of " + titleNames[isPhoton] + " System"

    # account for if system includes photons
    if isPhoton:
        if IorE == "Exc":
            fileName = "dilepPho" + v
        else:
            fileName = "photon" + v
            xAxisLabel = variables[v][1] + "_{#gamma}" + variables[v][2]
            titleLabel = variables[v][0] + " of Photons"

    mcFiles = f.Get("MC " + fileName)
    dataFiles = f.Get(fileName)
    hists = [dataFiles, mcFiles]

    # rebin momentum histograms
    if "Pt" in fileName:
        binEdges = array.array('d', [0, 20, 40, 60, 80, 100, 140, 200, 300, 500])
        hists[0] = hists[0].Rebin(len(binEdges)-1, "data rebinned", binEdges)
        hists[1] = hists[1].Rebin(len(binEdges)-1, "mc rebinned", binEdges)

    # set up two graph spaces, one for the data and another for their ratio
    compCanvas.cd()
    pad1 = ROOT.TPad("pad1", "Top pad", 0, 0.3, 1, 1.0)
    pad1.SetBottomMargin(0.02)
    pad1.SetLogy("Pt" in fileName)
    pad1.SetTickx(1)
    pad1.SetTicky(1)
    pad1.Draw()

    pad2 = ROOT.TPad("pad2", "Bottom pad", 0, 0.05, 1, 0.3)
    pad2.SetTopMargin(0.05)
    pad2.SetBottomMargin(0.35)
    pad2.SetGridy()
    pad2.SetTickx(1)
    pad2.SetTicky(1)
    pad2.Draw()

    # scale MC to measured data
    if hists[1].Integral() != 0:
        hists[1].Scale(hists[0].Integral() / hists[1].Integral())

    # set limits of plots
    hists[0].SetMarkerStyle(8)
    hists[0].SetMarkerColor(ROOT.kBlack)
    hists[0].SetAxisRange(*fitRanges[v], "X")
    hists[0].SetStats(0)

    maxY = 2 * max(hists[0].GetMaximum(), hists[1].GetMaximum()) if "Pt" in fileName else 1.05 * max(hists[0].GetMaximum(), hists[1].GetMaximum())
    hists[0].SetMaximum(maxY)
    # hists[0].SetMinimum(28000)

    # draw histograms
    pad1.cd()
    if "Pt" in fileName:
        hists[0].Scale(1.0, "width")
        hists[1].Scale(1.0, "width")
    hists[0].Draw("e1")
    hists[1].SetFillColor(ROOT.kYellow)
    hists[1].SetLineWidth(2)
    hists[1].Draw("samehist")
    hists[0].Draw("samee1")

    # add legend
    legend = ROOT.TLegend(0.65, 0.65, 0.80, 0.80)
    legend.SetTextFont(132)
    legend.AddEntry(hists[0], "Data ", "P")
    legend.AddEntry(hists[1], "MC ")
    legend.SetBorderSize(0)
    legend.Draw("same")

    hists[0].SetTitle(titleLabel)
    hists[0].GetYaxis().SetTitle("Events")
    hists[0].GetXaxis().SetLabelSize(0)
    # hists[0].SetMaximum(350)

    ROOT.gStyle.SetErrorX(0.00)

    # calculate and print Chi Squared to legend
    if printChiSqr:
        Vals = []
        for b in range(NoBins):
            n = [hists[0].GetBinContent(b), hists[1].GetBinContent(b), hists[0].GetBinError(b)]
            Vals.append(n)
        X = []
        for i in range(NoBins):
            if Vals[i][2] != 0:
                var = np.power(Vals[i][2], 2)
                y = ((Vals[i][0] - Vals[i][1]) ** 2) / var
                X.append(y)
        Z = np.sum(X) / NoBins
        chiSq = round(Z, 3)
        print(fileName, "Chi Squared =", chiSq)

        XSqurd = ROOT.TLatex()
        XSqurd.SetTextSize(0.05)
        XSqurd.SetNDC()
        XSqurd.SetTextFont(132)
        XSqurd.DrawLatex(0.65, 0.60, f"#chi^{{2}}_{{DOF}} = {chiSq:.2f}")

    # put ratio plot onto other canvas
    pad2.cd()
    ratio = hists[0].Clone("ratio")
    ratio.SetStats(0)
    ratio.Sumw2()
    ratio.Divide(hists[1])
    ratio.SetMinimum(0.0)
    ratio.SetMaximum(4.0)
    ratio.SetMarkerStyle(8)
    ratio.SetLineColor(ROOT.kBlack)


    ratio.SetTitle("")
    ratio.GetYaxis().SetTitle("Data / MC")
    ratio.GetYaxis().SetNdivisions(505)
    ratio.GetYaxis().SetTitleSize(0.12)
    ratio.GetYaxis().SetLabelSize(0.10)
    ratio.GetYaxis().SetTitleOffset(0.2)

    ratio.GetXaxis().SetTitle(xAxisLabel)
    ratio.GetXaxis().SetTitleSize(0.16)
    ratio.GetXaxis().SetLabelSize(0.12)
    ratio.GetXaxis().SetTitleOffset(1.0)

    ratio.Draw("e1")
    ROOT.gPad.RedrawAxis()
    pad2.Update()

    # output graph as pdf
    compCanvas.cd()
    compCanvas.Update()
    compCanvas.Print("output/finalGraph.pdf")


a = input("What variable would you like to plot? Mass, Pt, Eta or Phi: ")
b = input("Inclusive or Exclusive to Photon Events? Inc or Exc: ")
c = bool(input("Do you events include Photons? True or False: "))



drawHists(a , b , isPhoton=c, printChiSqr=True)