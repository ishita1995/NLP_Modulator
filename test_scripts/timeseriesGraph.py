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
import numpy
import copy

#Initialization ends
#-------------------

# script control
fName = 'WilhelmScream.wav' # we will create a scolling display of this file
fps = 25 # frame rate of the generated video
videoBitrate = 8000000 # compression: define the quality of the generated movie
deleteTmpFiles = True # we'll delete the temporary graph files once we're done
displayDuration = 2 # how many seconds of data to display
cursorOffset = 0.5 # offset of the display cursor within the display window

# define the structure of the generated tmp files
fileNameOnly = generalUtility.getFileNameOnly(fName)
fileNameStructure = fileNameOnly + '_%05d.png'

# get the user's tmp directory, where we'll store all temporary data
tmpDataDir = generalUtility.getUserTmpDir()

# get the current directory, where we'll store the generated movie
userPath = path = sys.path[0] + '/'

# calculate the Intensity data using Praat and prepare data for plotting
dataT, dataI = praatUtil.calculateIntensity(path + fName)
dataI -= dataI.max()
intensityTimeStep = dataT[1] - dataT[0]
fsIntensity = 1.0 / intensityTimeStep

# read the sound data and prepare it for plotting
numChannels, numFrames, fs, data = myWave.readWaveFile(fName)
sampleData = data[0] # take the left (and only) channel in the file
dataTsound = numpy.zeros(numFrames)

for i in range(numFrames):
    dataTsound[i] = float(i) / float(fs) # time offsets
    
# loop over the data
timeStep = 1.0 / fps
duration = numFrames / float(fs)
t = 0
frameCount = 0
arrImageFileNames = [] # we'll store the names of the generated files here, so
                       # we can delete them when we clean up
                       
while t < duration:
    tStart = t - cursorOffset
    tEnd = tStart + displayDuration
    frameCount += 1
    print "Frame %d at t = %f seconds" % (frameCount, t)
    
    # generate the graph
    graph = matplotlibUtil.CGraph(width = 8, height = 6)
    graph.setRowRatios([6, 4]) # set the ratio fo the row heights
    graph.createFigure()
    arrAx = graph.getArrAx()
    
    # plot the waveform: need to determine the data that is shown
    # watch out: tStart can be negative, tEnd can be larger than the sound 
    # duration
    offsetL = int(round(tStart * float(fs))) # theoretical lower offset
    offsetU = int(round(tEnd * float(fs))) # theoretical upper offset
    offsetLreal = offsetL # real (potentially corrected) lower offset
    if offsetLreal < 0: offsetLreal = 0 
    offsetUreal = offsetU # real (potentially corrected) upper offset
    if offsetU >= numFrames: offsetUreal = numFrames - 1
    
    ax = arrAx[0]
    ax.plot(dataTsound[offsetLreal:offsetUreal], \
        sampleData[offsetLreal:offsetUreal], linewidth = 2)
    ax.plot([t, t], [-1000, 1000], color='red') # time cursor
    ax.set_xlabel("Time [s]")
    ax.set_ylabel("Pressure [arbitrary]")
    ax.set_xlim(tStart, tEnd)
    ax.set_title(fileNameOnly)
    ax.grid()
    matplotlibUtil.setLimit(ax, sampleData, 'y', rangeMultiplier = 0.1)
    
    # plot the intensity: need to determine the data that is shown
    # watch out: tStart can be negative, tEnd can be larger than the sound 
    # duration
    offsetL = int(round(tStart * float(fsIntensity))) # theoretical lower offset
    offsetU = int(round(tEnd * float(fsIntensity))) # theoretical upper offset
    offsetLreal = offsetL # real (potentially corrected) lower offset
    if offsetLreal < 0: offsetLreal = 0 
    offsetUreal = offsetU # real (potentially corrected) upper offset
    if offsetU >= len(dataI): offsetUreal = numFrames - 1
    ax = arrAx[1]
    ax.plot(dataT[offsetLreal:offsetUreal], \
        dataI[offsetLreal:offsetUreal], linewidth = 2, color='orange')
    ax.plot([t, t], [-1000, 1000], color='red') # time cursor
    ax.set_xlabel("Time [s]")
    ax.set_ylabel("SPL [dB]")
    ax.set_xlim(tStart, tEnd)
    ax.grid()
    matplotlibUtil.setLimit(ax, dataI, 'y', rangeMultiplier = 0.1)
    matplotlibUtil.formatAxisTicks(ax, 'y', 6, '%d')
    
    # finalize the graph 
    graph.padding = 0.1
    graph.adjustPadding(left = 1.2, right = 0.5, bottom = 1.2, hspace = 0.4)
    
    # finally, save the graph to the tmp dir. note that the frame number is part
    # of the file name
    graphFileName = tmpDataDir + (fileNameStructure % frameCount)
    plt.savefig(graphFileName)
    arrImageFileNames.append(graphFileName)
    
    # very important: increase the time, to avoid an endless loop
    t += timeStep
    
# now we should have a bunch of graphs (with ever increasing time offset) in 
# our tmp directory. let's convert them into a movie
aviOutputFileName = userPath + generalUtility.getFileNameOnly(fName) + '.avi'
print "generating AVI file " + aviOutputFileName
generalUtility.createMovie(arrImageFileNames, aviOutputFileName, \
    videoFps = fps, audioFileName = userPath + fName, \
    deleteImageFiles = deleteTmpFiles, fileNameStructure = fileNameStructure, \
    overwriteAviFile = True, videoBitrate = videoBitrate)
print "done."