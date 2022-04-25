#!/bin/bash

#./createRunRecoList.sh > queue_list_reco.txt

inPath=/eos/experiment/ship/user/jpship/anutest/sim

#inPath=/eos/experiment/ship/user/jpship/sbt/*root
for a in `ls $inPath`
	do
		echo $a
	done

#while read LINE
#        do
#	  #echo $LINE
#	  words=( $LINE )
#	  fileName=${words[0]}
#	  nevents=${words[1]}
#	  startEvent=0
#	  #echo $fileName $nevents
#          eventsPerRun=$eventsPerRunMax
#	  while [  $nevents -gt $eventsPerRunMax ]; do
#             echo $fileName $startEvent $eventsPerRun
#             let startEvent=startEvent+$eventsPerRun
#             let nevents=nevents-eventsPerRunMax
#             if [ $nevents -lt $eventsPerRunMax ]; then
#		let eventsPerRun=nevents-1
#             fi
#          done
#          echo $fileName $startEvent $eventsPerRun
#done < getEntriesForAllFiles.out
