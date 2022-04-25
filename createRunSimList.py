import os

complete_list = []
mutual_list = []

for file in os.listdir("/eos/experiment/ship/user/jpship/sbt/reco-s"):
    complete_list.append(file.split("_"))
for file in os.listdir("/eos/experiment/ship/user/jpship/sbt/ana-s"):
    mutual_list.append(file.split("_"))


with open("/afs/cern.ch/work/j/jpship/runSBT/queue_list.txt", "w") as ql:
    for file in complete_list:
        if not(file in mutual_list):
            line = "/eos/experiment/ship/data/Mbias/background-prod-2018/pythia8_Geant4_10.0_withCharmandBeauty%s_mu.root %s %s\n"%(file[0],file[1],file[2])
            ql.write(line)
