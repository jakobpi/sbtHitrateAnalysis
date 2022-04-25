#!/bin/bash
ClusterId=$1
ProcId=$2
inFile=$3


OUTPUTDIR=/eos/experiment/ship/user/jpship/anutest/reco

source /cvmfs/ship.cern.ch/SHiP-2021/latest/setUp.sh
export ALIBUILD_WORK_DIR=/afs/cern.ch/work/j/jpship/anubuild/sw


source /afs/cern.ch/work/j/jpship/anubuild/config-new.sh

INPUTDIR=/eos/experiment/ship/user/jpship/anutest/sim

python $FAIRSHIP/macro/ShipReco.py -f $INPUTDIR/$inFile -g /afs/cern.ch/work/j/jpship/anubuild/HTCondor/geofile_full.conical.MuonBack-TGeant4.root

new=$(echo $inFile | sed 's/.root/_rec.root/')
mv $new $OUTPUTDIR/
