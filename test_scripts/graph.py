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
import numpy
import matplotlib.cm as cm
from christPyLib import generalUtility
from christPyLib import dspUtil
from christPyLib import matplotlibUtil
from christPyLib import praatUtil
from christPyLib import myWave
import copy

#Initialization ends
#-------------------

outputPath = '' # substitute the output path here
# instantiate the graph container
graph = matplotlibUtil.CGraph(
    width = 8,
    height = 8,
    dpi = 72,
    lineWidth = 1.5,
    padding = 0.06,
    fontSize = 13,
    fontFamily = 'serif',
    fontFace = 'Times New Roman',
    fontWeight = 'normal'
)

# define the layout and create the graph
graph.setRowRatios([3, 2, 5])
graph.setColumns([1, 2, 2])
arrAx = graph.createFigure()

# for demonstration purposes: add a title for each panel, so we know which
# ax reference points to which panel
for i, ax in enumerate(arrAx):
    ax.set_title("panel " + str(i+1))
    
#######################
# ----- PANEL 1 ----- #
#######################

# invent some data
duration = 0.5 # [s]
fs = 1000 # [Hz] sampling frequency
f0 = 40 # [Hz] frequency of the sine wave we'll create
n = int(round(duration * float(fs)))
arrData = numpy.zeros(n)
arrT = numpy.zeros(n)
for i in range(n):
    A = 1.0 - float(i) / n # amplitude [0..1] - create a decaying sinusoid
    t = float(i) / float(fs)
    arrT[i] = t
    arrData[i] = A * numpy.sin(numpy.pi * 2.0 * t * float(f0))
    
# plot the data in the top panel
ax = arrAx[0]
ax.plot(arrT, arrData, linewidth = graph.lineWidth)
ax.grid()
ax.set_xlabel("Time [s]")
ax.set_ylabel("Amplitude")
matplotlibUtil.formatAxisTicks(ax, 'y', 1) # adapt the x axis ticks

##############################
# ----- PANELS 2 and 3 ----- #
##############################

# extract parts of the data and plot in next row
n = len(arrData)
for i in range(2):
    idx1 = (n / 2) * i
    idx2 = idx1 + n / 4
    ax = arrAx[i + 1]
    ax.plot(arrT[idx1:idx2], arrData[idx1:idx2], linewidth = graph.lineWidth)
    ax.grid()
    ax.set_xlabel("Time [s]")
    ax.set_ylabel("Amplitude")
    matplotlibUtil.setLimit(ax, arrData[idx1:idx2], 'y', 0.1)
    
#######################
# ----- PANEL 4 ----- #
#######################
    
# create a noisy data distribution and plot in bottom left panel. fit a 
# polinomial to the data
n = 100
arrX = range(n)
arrY = numpy.zeros(n)

for i in arrX:
    arrY[i] = numpy.sqrt(i) + numpy.random.random() * 3
    
ax = arrAx[-2]
ax.plot(arrX, arrY, 'o', markersize = 5, alpha = 0.6, color='green')
matplotlibUtil.plotPolyFit(ax, arrX, arrY, degrees = 2, fontSize = 10, \
    lineSize = 3, lineColor = 'red', txtX = 10, txtY = 1.6, numDigitsEq = 5)
ax.grid()

#######################
# ----- PANEL 5 ----- #
#######################

# create and plot a 3D array with isocontours
ax = arrAx[-1]
numIsocontours = 10
arrX = numpy.arange(0, 1, 0.02)
arrY = numpy.arange(0, 1, 0.02)
arrZ = numpy.zeros((len(arrY), len(arrX)))

for idxY, y in enumerate(arrY):
    for idxX, x in enumerate(arrX):
        arrZ[idxY][idxX] = 100.0 * (numpy.sqrt(x) + y * y)
        #print x, y, numpy.sqrt(x) + y * y
        
matplotlibUtil.plotIsocontours(ax, arrX, arrY, arrZ, colorMap = cm.afmhot, \
     numIsocontours = 6, contourFontSize = 10)
ax.grid()

# finalize and save the graph        
graph.adjustPadding(left = 2.5,  right = 1.0,  top = 1.0,  bottom = 1.0, \
    hspace = 0.45,  wspace = 0.5)
graph.addPanelNumbers(numeratorType = matplotlibUtil.NUMERATOR_TYPE_ROMAN, \
    fontSize = 16, fontWeight = 'bold', \
    countEveryPanel = True, format = '(%s)', offsetLeft = 0.1, offsetTop = 0.00)
fileName = outputPath + 'matplotlibUtilDemo'
plt.savefig(fileName + '.png')
plt.savefig(fileName + '.svg')