from __future__ import print_function
from __future__ import division
# example for accessing smeared hits and fitted tracks
import ROOT,os,sys,getopt
import ctypes
import rootUtils as ut
import shipunit as u
from ShipGeoConfig import ConfigRegistry
from rootpyPickler import Unpickler
from decorators import *
import shipRoot_conf
from argparse import ArgumentParser
import time


start = time.time()
print("hello")


shipRoot_conf.configure()
PDG = ROOT.TDatabasePDG.Instance()

chi2CutOff  = 4.
fiducialCut = False
measCutFK = 25
measCutPR = 22
docaCut = 2.

parser = ArgumentParser()

parser.add_argument("-f", "--inputFile", dest="inputFile", help="Input file", required=True)
parser.add_argument("-n", "--nEvents",   dest="nEvents",   help="Number of events to analyze", required=False,  default=999999,type=int)
parser.add_argument("-g", "--geoFile",   dest="geoFile",   help="ROOT geofile", required=True)
parser.add_argument("--Debug",           dest="Debug", help="Switch on debugging", required=False, action="store_true")
options = parser.parse_args()

eosship = ROOT.gSystem.Getenv("EOSSHIP")
if not options.inputFile.find(',')<0 :
  sTree = ROOT.TChain("cbmsim")
  for x in options.inputFile.split(','):
   if x[0:4] == "/eos":
    sTree.AddFile(eosship+x)
   else: sTree.AddFile(x)
elif options.inputFile[0:4] == "/eos":
  eospath = eosship+options.inputFile
  f = ROOT.TFile.Open(eospath)
  sTree = f.cbmsim
else:
  f = ROOT.TFile(options.inputFile)
  sTree = f.cbmsim

# try to figure out which ecal geo to load
if not options.geoFile:
 options.geoFile = options.inputFile.replace('ship.','geofile_full.').replace('_rec.','.')
if options.geoFile[0:4] == "/eos":
  eospath = eosship+options.geoFile
  fgeo = ROOT.TFile.Open(eospath)
else:
  fgeo = ROOT.TFile(options.geoFile)

# new geofile, load Shipgeo dictionary written by run_simScript.py
upkl    = Unpickler(fgeo)
ShipGeo = upkl.load('ShipGeo')
ecalGeoFile = ShipGeo.ecal.File
dy = ShipGeo.Yheight/u.m

# -----Create geometry----------------------------------------------
import shipDet_conf
run = ROOT.FairRunSim()
run.SetName("TGeant4")  # Transport engine
run.SetOutputFile(ROOT.TMemFile('output', 'recreate'))  # Output file
run.SetUserConfig("g4Config_basic.C") # geant4 transport not used, only needed for the mag field
rtdb = run.GetRuntimeDb()


#################################################################
# Read out hits with energy and weights                   #######
#################################################################

import numpy as np
import pickle
from statistics import mean
import csv

hitLists = {}
Hits = []
thresholdsMeV = range(0,110,5) # MeV
thresholdsGeV = [i*0.001 for i in thresholdsMeV]
for tG in thresholdsGeV:
    hitLists[tG]=[]

#for debugging find particles weights that switch from !=1 to 1 (which shouldnt exist):
#bugweights = {}

# loop over all events in files and filter out vetopoints
nrOfEvents = sTree.GetEntries()
print("Number of events: ", nrOfEvents)
print("events printed:")
for eventNr in range(nrOfEvents):
    rc = sTree.GetEvent(eventNr)
    ElossPerDetId    = {}
    listOfVetoPoints = {}
    Weights = {}
    pdgCodes = {}
    positions = {}

    key = -1

    #Loop over all particle-SBT interaction within event eventNr
    for vPoint in sTree.vetoPoint:
        key += 1
        print(key)
        detID = vPoint.GetDetectorID()
        Eloss = vPoint.GetEnergyLoss()
        Weight = sTree.MCTrack[vPoint.GetTrackID()].GetWeight()
        pdgCode = sTree.MCTrack[vPoint.GetTrackID()].GetPdgCode()
        if detID not in ElossPerDetId:
            ElossPerDetId[detID]= 0
            listOfVetoPoints[detID]=[]
            Weights[detID]=[]
            # only save first pdgcode
            pdgCodes[detID] = pdgCode
            positions[detID] = [vPoint.GetX(), vPoint.GetY(), vPoint.GetZ()]

        ElossPerDetId[detID]+=Eloss
        listOfVetoPoints[detID].append(key)
        Weights[detID].append(Weight)

    # save extracted information into Hits list
    for n, seg in enumerate(ElossPerDetId):
        energy = ElossPerDetId[seg]
        weight = Weights[seg][0]
        hit = [seg, energy, weight, pdgCodes[seg]] + positions[seg] # combine lists
        Hits.append(hit)

#quit()
#print(Hits)

#save Hitlist into csv file
myFile = open('DigiHits.csv', 'a')
with myFile:
    #myFields = ['seg', 'Energy depostion of cell', 'mean Weight of cell', 'x', 'y', 'z']
    writer = csv.writer(myFile)
    #writer.writerow(myFields)
    writer.writerows(Hits)
for i in Hits:
    if (13 == i[3]) or (-13 == i[3]):
        print(i[:-3])

end = time.time()
print("elapsed time:", end - start)
