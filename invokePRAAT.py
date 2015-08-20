#Initialization begins
#---------------------
import os

#Configure PRAAT
import sys
if "C:\\PRAAT" not in sys.path:
    sys.path.append("C:\\PRAAT")
#Assuming PRAAT in C:\PRAAT
#Get PRAAT from : http://www.praat.org/

from matplotlib import pyplot as plt
from christPyLib import generalUtility
from christPyLib import dspUtil
from christPyLib import matplotlibUtil
from christPyLib import praatUtil
from christPyLib import myWave
import copy

#Initialization ends
#-------------------

fName = 'WilhelmScream.wav'

# for this to work our sound file needs to be in the same directory as this 
# Python script, and we need to get the path of that script:
path = sys.path[0] + '/'
fileNameOnly = generalUtility.getFileNameOnly(fName)

# calculate the Intensity data using Praat
dataT, dataI = praatUtil.calculateIntensity(path + fName)

# normalize the dB data, since it's not calibrated
dataI -= dataI.max()

# generate the graph
graph = matplotlibUtil.CGraph(width = 8, height = 3)
graph.createFigure()
ax = graph.getArrAx()[0]
ax.plot(dataT, dataI, linewidth = 2)
ax.set_xlabel("Time [s]")
ax.set_ylabel("SPL [dB]")
ax.set_title(fileNameOnly)
graph.padding = 0.1
graph.adjustPadding(bottom = 2, right = 0.5)
ax.grid()

# It is not aesthetically pleasing when graph data goes to all the way to the 
# upper and lower edges of the graph. I prefer to have a little space.
matplotlibUtil.setLimit(ax, dataI, 'y', rangeMultiplier = 0.1)

# every doubling of sound pressure level (SPL) results in an increase of SPL by
# 6 dB. Therefore, we need to change the y-axis ticks
matplotlibUtil.formatAxisTicks(ax, 'y', 6, '%d')

# finally, save the graph to a file
plt.savefig(fileNameOnly + "_intensity.png")