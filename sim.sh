#!/bin/bash
ClusterId=$1
ProcId=$2
inFile=$3
startEvent=$4
nEvents=$5

OUTPUTDIR=/eos/experiment/ship/user/jpship/anutest/sim

source /cvmfs/ship.cern.ch/SHiP-2021/latest/setUp.sh
export ALIBUILD_WORK_DIR=/afs/cern.ch/work/j/jpship/anubuild/sw

source /afs/cern.ch/work/j/jpship/anubuild/config-new.sh

python $FAIRSHIP/macro/run_simScript.py --nEvents $nEvents --firstEvent $startEvent -f $inFile --MuonBack

cp ship.conical.MuonBack-TGeant4.root $OUTPUTDIR/$ClusterId.$ProcId.root
