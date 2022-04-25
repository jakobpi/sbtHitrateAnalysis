import csv
import time
import os
import sys
maxInt = sys.maxsize

inputPath = "/eos/experiment/ship/user/jpship/anutest/ana"
outputPath = "./combined.csv"

while True:
    # decrease the maxInt value by factor 10
    # as long as the OverflowError occurs.
    try:
        csv.field_size_limit(maxInt)
        break
    except OverflowError:
        maxInt = int(maxInt/10)

def combine(csvdir, outdir):
    with open(outdir,"w") as summary:
        writer = csv.writer(summary)
        for num, sList in enumerate(os.listdir(csvdir)):
            with open(csvdir +"/"+sList) as f:
                reader = csv.reader(f)
                for row in reader:
                    writer.writerow(row)

def readHits(csvdir="/eos/experiment/ship/user/jpship/anutest/ana", Hits = []):
    max_E = 0
    weights_m = []
    for num, sList in enumerate(os.listdir(csvdir)):
        with open(csvdir + "/" + sList) as f:
            reader = csv.reader(f)
            for row in reader:
                Hit = [int(row[0]), list(map(float, row[1].strip("[]").split(","))), list(map(float,row[2].strip("[]").split(",")))]
                if 1.0 in Hit[2]:
                    diverse = False
                    for i in Hit[2]:
                        if i != 1.0:
                            diverse = True
                    if diverse == False:
                        if sum(Hit[1]) > max_E:
                            Hits.append(Hit)
                            max_E = sum(Hit[1])
                            weights_m = Hit[2]
                            print(sList)
                            print("new max_E: ", max_E)
                            print("in segment ", Hit[0], " with weights: ", weights_m)
                        #print(Hit[2], sum(Hit[1]))
    print(max_E)
    return(Hits)


start = time.time()
print("starting the combination ...")
combine(inputPath, outputPath)

#combine()
end = time.time()
print("elapsed time:", end-start)

quit()

with open("./muonsummaryList.csv") as f:
    reader = csv.reader(f)
    for row in reader:
        Hits.append([int(row[0]), list(map(float,row[1].strip("[]").split(","))), list(map(float,row[1].strip("[]").split(",")))])
        writer.writerow(row)
