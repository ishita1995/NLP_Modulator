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

# path that contains all the annotated wave files
path = '/Users/ch/data/programming/python/lib/demo/'
csvFileName = 'TextGridAnalysis.csv'

# open the output file
csvFile = open(path + csvFileName, 'w')
csvFile.write("file, tStart, tEnd, label\n")

# look for all TextGrids in the directory
for fName in os.listdir(path):
    if fName.split('.')[-1] == 'TextGrid':
        fileNameOnly = generalUtility.getFileNameOnly(fName)
        print fileNameOnly
        
        # instantiate a new TextGrid object
        textGrid = praatTextGrid.PraatTextGrid(0, 0)
        # initialize the TextGrid object from the TextGrid file
        # arrTiers is an array of objects (either PraatIntervalTier or 
        # PraatPointTier)
        arrTiers = textGrid.readFromFile(fName)
        numTiers = len(arrTiers)
        if numTiers != 1:
            raise Exception("we expect exactly one Tier in this file")
            
        # get the first tier in the file and check it's name (and we assume that 
        # there's exactly one tier in the file
        tier = arrTiers[0]
        if tier.getName() != 'myAnnotation':
            # ignore the text grid if the name of the Tier does not match the 
            # name that was given in the script that generated the TextGrid
            print "\tWARNING: unexpected tier (%s) in file %s. Skipping this file." \
                % (tier.getName(), fName)
        else:
            # now loop over all the defined intervals in the tier.
            for i in range(tier.getSize()):
            
                # only consider those intervals that are actually labelled.
                if tier.getLabel(i) != '':
                    interval = tier.get(i)
                    print "\t", interval
                    
                    # write to CSV file
                    csvFile.write("%s, %f, %f, %s\n" % (fileNameOnly, \
                        interval[0], interval[1], interval[2]))
            
csvFile.close()
            