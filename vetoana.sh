#!/bin/bash
ClusterId=$1
ProcId=$2
inFile=$3

OUTPUTDIR=/eos/experiment/ship/user/jpship/anutest/ana

source /cvmfs/ship.cern.ch/SHiP-2021/latest/setUp.sh
export ALIBUILD_WORK_DIR=/afs/cern.ch/work/j/jpship/anubuild/sw
source /afs/cern.ch/work/j/jpship/anubuild/config-new.sh

INPUTDIR=/eos/experiment/ship/user/jpship/anutest/reco

python /afs/cern.ch/work/j/jpship/anubuild/FairShip/runSBT/vetoana.py -f $INPUTDIR/$inFile -g /afs/cern.ch/work/j/jpship/anubuild/HTCondor/geofile_full.conical.MuonBack-TGeant4.root

mv DigiHits.csv $OUTPUTDIR/$inFile
