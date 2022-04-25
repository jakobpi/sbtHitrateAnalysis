#!/bin/bash

#./createRunAnaList.sh > queue_list_ana.txt

inPath=/eos/experiment/ship/user/jpship/anutest/reco

outPath=/eos/experiment/ship/user/jpship/anutest/ana

for a in `ls $inPath`
	do
		new=`echo $a | sed 's/_rec.root/.sbt.root/'`
		newnew=`echo $new | sed 's/2937531.//'`
		#echo $newnew
		if [[ -f $outPath/$a ]]
		then
			:
		else
			echo $a
		fi
	done
