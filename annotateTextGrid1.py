#Initialization begins
#---------------------
import os

#Configure PRAAT
import sys
if "C:\\PRAAT" not in sys.path:
    sys.path.append("C:\\PRAAT")
#Assuming PRAAT in C:\PRAAT
#Get PRAAT from : http://www.praat.org/

from christPyLib import generalUtility
from christPyLib import dspUtil
from christPyLib import matplotlibUtil
from christPyLib import praatUtil
from christPyLib import myWave
import copy

#Initialization ends
#-------------------

# we assume that you have a couple of audio files in this directory, which 
# you'd like to annotate - change as needed

path = '/Users/ch/data/programming/python/lib/demo/'
# we'll only deal with WAV files in this example
suffix = 'wav'

# look for audio files in the directory
for fName in os.listdir(path):
    if fName.split('.')[-1] == suffix:
        print fName
        
        # safeguard: do not create a new TextGrid if there's already one (to 
        # prevent yourself from accidentally overwriting already performed
        # annotations)
        fileNameOnly = generalUtility.getFileNameOnly(fName)
        outputFileName = path + fileNameOnly + '.TextGrid'
        if os.path.isfile(outputFileName):
            print "\tWARNING: TextGrid already exists"
        else:
        
            # open audio file to get duration
            numChannels, numFrames, fs, data = myWave.readWaveFile(path + fName)
            n = len(data[0])
            duration = float(n) /float(fs)
            
            # create a new PraatTextGrid object. make sure to indicate the sample
            # duration
            textGrid = praatTextGrid.PraatTextGrid(0, duration)
            
            # create a new interval tier (you may want to change the tier label)
            intervalTier = praatTextGrid.PraatIntervalTier("myAnnotation")
            
            # add an empty element to the interval tier (to prevent Praat from 
            # crashing when working with the generated TextGrid)
            intervalTier.add(0, duration, "")
            
            # add the interval tier to the TextGrid
            textGrid.add(intervalTier)
            
            # finally, save the TextGrid in the same directory as the WAV file
            textGrid.save(outputFileName)