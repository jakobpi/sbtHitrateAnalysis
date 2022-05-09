import csv
import pickle
import os
from mpl_toolkits.mplot3d import Axes3D
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter

import sys
import numpy as np
import time

import sys
maxInt = sys.maxsize

start = time.time()

while True:
    # decrease the maxInt value by factor 10
    # as long as the OverflowError occurs.

    try:
        csv.field_size_limit(maxInt)
        break
    except OverflowError:
        maxInt = int(maxInt/10)


inputdir = "/afs/cern.ch/work/j/jpship/analysis/test.csv"
file = open(inputdir)
print(file)
MeV = 0.001 # give unit MeV in units of GeV

def plotHistogram(E, W, weighted = True, binp = [0,1000,0.0005]):
    bins = [i for i in np.arange(binp[0],binp[1],binp[2]).tolist()]
    ax = plt.figure().add_subplot(111)
    #data, edges, bars = plt.hist(E, bins = bins, weights = W, color="b", log = True, histtype = 'step')
    data, edges, bars = plt.hist(E, bins = bins, weights = W, cumulative = -1, color="b", log = True, histtype = 'step')
    #ax.yaxis.tick_right()
    #ax.yaxis.set_label_position("right")
    ax.annotate('0 MeV: %1.2e' % data[int(0.00/binp[2])], (0.006, data[int(0.00/binp[2])]), textcoords='data')
    ax.annotate('45 MeV: %1.2e' % data[int(0.045/binp[2])], (0.045, 1.02* data[int(0.045/binp[2])]), textcoords='data')
    plt.xlabel("$E_{th}$ [GeV]")
    plt.ylabel("#DigiHits")
    plt.title("DigiHits above energy threshold $E_{th}")
    #plt.title("Muon DigiHits with ennergy above E_{th}")
    plt.xlim(0,0.07)
    plt.ylim(1e6,2e8)
    #plt.ylim(2e5,5e5)
    print(data[int(0.045/binp[2])])
    plt.show()

def plotDetIDHits(IDs, E, W, threshold = 45):
    hitlist = {}
    for n, id in enumerate(IDs):
        if id not in hitlist:
            hitlist[id] = 0
        if E[n] >= threshold * MeV:
            hitlist[id] += W[n]
    keys = hitlist.keys()
    values = hitlist.values()
    sum = np.sum(np.array(list(values)))
    maxY, maxX = max(values), list(keys)[list(values).index(max(values))]
    plt.annotate('max: %.2f' %(maxY), (maxX, maxY), textcoords='data')
    plt.xlabel("Detector ID")
    plt.ylabel("N Digi Hits/ Spill")
    # plt.ticklabel_format(style='sci', axis='x', scilimits=(0,0))
    plt.title("DigiHits per cell E_th > %d MeV"%threshold)
    plt.bar(keys, values, width=1000, log = True)
    plt.rcParams["figure.figsize"] = (50,30)
    #plt.xlim(400000,460000)
    plt.plot([], [], ' ', label="total: %.2f"%sum)
    plt.legend()
    plt.show()
    return(None)
    hitlist = {}
    count = 0
    for n, id in enumerate(IDs):
        if id not in hitlist:
            hitlist[id] = 0
        if E[n] >= threshold * MeV:
            hitlist[id] += W[n]
            count += 1
        if hitlist[id] == 0:
            del hitlist[id]
    print(count)
    keys = hitlist.keys()
    values = hitlist.values()
    sum = np.sum(np.array(list(values)))
    maxY, maxX = max(values), list(keys)[list(values).index(max(values))]
    print("determined maxX and maxY")
    print(len(keys),keys)
    print(len(values))
    #plt.bar(keys, values, width=10, log = True)

    plt.bar(keys, values, width=10, log = True)
    plt.xticks(range(0,700000,1000))
    # Set the ticks to be at the edges of the bins.
    #ax.set_xticks(range(0,700000,10000))
    # Set the xaxis's tick labels to be formatted with 1 decimal place...
    #ax.xaxis.set_major_formatter(FormatStrFormatter('%0.1f'))

    #plt.hist(list(keys),weights=list(values),log=True,rwidth=0.01)
    #plt.plot(keys, values, 'r.', label="total: %.2f"%sum)
    #plt.ticklabel_format(style='sci', axis='x', scilimits=(0,0))
    #plt.locator_params(axis='x', nbins=10)

    """plt.annotate('max: %.2f' %(maxY), (maxX, maxY), textcoords='data')
    plt.xlabel("Detector ID")
    plt.ylabel("N Digi Hits/ Spill")
    plt.locator_params(axis='x', nbins=10)
    plt.ticklabel_format(style='sci', axis='x', scilimits=(0,0))
    plt.title("DigiHits per cell E_th = %d MeV"%threshold)
    print("now we have keys and values")
    print("plt.bars plotted")
    #plt.rcParams["figure.figsize"] = (50,30)
    print("plt.bars plotted")
    #plt.xlim(0,700000)
    plt.plot(keys, values, ' ', label="total: %.2f"%sum)
    print("plot newest")
    plt.legend()"""
    #plt.savefig('simpledethist.png')
    plt.show()


def plotweightsHistogram(W):
    weights = {}
    for n,i in enumerate(W):
        if i not in weights:
            weights[i] = 1
        else:
            weights[i] += 1
    keys = weights.keys()
    values = weights.values()
    data, edges = np.histogram(W, bins = 100)
    print(len(keys), len(values))
    ax = plt.figure().add_subplot(111)
    print(keys, values)
    print(np.dot(np.array(list(keys)), np.array(list(values))))
    #ax.set_xticks(values)
    #ax.set_xticklabels(values)
    plt.yscale('log')
    plt.xscale('log')
    #plt.xlim(0,10)
    plt.plot(keys, values, 'b+')
    print(len(keys), len(values))
    plt.title("histogram of weights. total events: %i"%len(W))
    plt.show()

def plotHeatmap(segs, E, W, pos, Eth = 0.045, rotation = False):
    segments = {}
    for n, detID in enumerate(segs):
        if E[n] >= Eth:
            if detID not in segments:
                segments[detID] = [W[n], pos[n][0], pos[n][1], pos[n][2]]
            else:
                segments[detID][0] += W[n]
        else: None
    segval=list(segments.values())
    points = np.array(segval) # extract dictionary values to 2 dim np array
    fig = plt.figure(figsize=(12.5,10))
    ax = plt.axes(projection='3d')

    # Data for three-dimensional scattered points
    n, x, y, z = points[:,0], points[:,1], points[:,2], points[:,3]
    plot = ax.scatter3D(x, z, y, c = n, cmap='viridis', norm=matplotlib.colors.LogNorm())

    max_range = np.array([x.max()-x.min(), y.max()-y.min(), z.max()-z.min()]).max() / 2.0

    mid_x = (x.max()+x.min()) * 0.5
    mid_y = (y.max()+y.min()) * 0.5
    mid_z = (z.max()+z.min()) * 0.5

    ax.set_xlim(mid_x - max_range, mid_x + max_range)
    ax.set_ylim(mid_y - max_range, mid_y + max_range)
    ax.set_zlim(mid_z - max_range, mid_z + max_range)


    cbar = plt.colorbar(plot)
    cbar.set_label("# weightedHits")
    ax.set_xlabel('x')
    ax.set_ylabel('z')
    ax.set_zlabel('y')

    if rotation:
        for n, angle in enumerate(range(0, 360, 5)):
            print(angle)
            ax.view_init(35, angle)
            fig.savefig('./plots/rotateHits/weightedfig%03d.png'%n, dpi = 100)
    plt.show()

def homogeneitycheck(W):
    """check if lists contains of mixed values"""
    init = W[0]
    for i in W:
        if i != init:
            return False
        init = i
    return True

E = []
segs = []
W = []
pos = []

muononly = input("Are you only interested in Muon Hits ? y/n ")
if str(muononly) == "y":
    muononly = True
else:
    muononly = False

with file:
    reader = csv.reader(file)#, quoting=csv.QUOTE_NONNUMERIC)
    for n, row in enumerate(list(reader)):
        print(row)
        hit = row
        if muononly:
            if ((float(hit[3]) == 13.0) or (float(hit[3]) == -13.0)):
                segs.append(hit[0])
                E.append(float(hit[1]))
                W.append(float(hit[2]))
                pos.append([float(row[4]), float(row[5]), float(row[6])])
            else:
                None
        else:
            segs.append(hit[0])
            try:
                try:
                    E.append(float(hit[1]))
                    W.append(float(hit[2]))
                except:
                    #print(len(hit))
                    E.append(float(hit[1].strip('[]')))
                    print(E)
                    W.append(float(hit[2].strip('[]')))
            except:
                print(n))
            pos.append([float(row[3]),float(row[4]),float(row[5])])
print("E:      ",E)
print("lists loaded after", time.time()-start)
#print(E)
#print(W)
weightedhits = 0
hitff = 0
mweightedhits = 0
for e in range(len(E)):
    compare = float(E[e])
    if compare >= 0.045:
        #print(E[e])
        weightedhits += 1/(float(W[e]))
        mweightedhits += float(W[e])
        hitff += 1

print(weightedhits)
print("mweighted:", mweightedhits)
print(hitff)
print("fertig nach: ",time.time() - start)

choice = input("Heatmap (a) or Histogram (b) or Weighthistogram (d) or hitsPerCell (e) or all (anything else)? ")

if str(choice) == "a":
    print(choice)
    plotHeatmap(segs, E,W,pos, rotation = True)
elif str(choice) == "b":
    print(choice)
    plotHistogram(E,W)
elif str(choice) == "d":
    print(choice)
    plotweightsHistogram(W)
elif str(choice) == "e":
    print(len(E))
    print("0")
    #plotDetIDHits(segs, E, W, threshold = 0)
    print("5")
    #plotDetIDHits(segs, E, W, threshold = 5)
    print("10")
    #plotDetIDHits(segs, E, W, threshold = 10)
    print("15")
    #plotDetIDHits(segs, E, W, threshold = 15)
    print("45")
    plotDetIDHits(segs, E, W, threshold = 45)
else:
    print(choice)
    plotHeatmap(segs,E,W,pos, rotation = True)
    input()
    plotHistogram(E,W)
    input()
    plotweightsHistogram(W)
