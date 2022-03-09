'''
Class, that holds the whole data
'''

import tarfile
from scanObservation import observation
import sys
import os

class dataContainter:
    def __init__(self, tarName = None):
        '''
        Initializes dataContainer class
        '''
        self.tmpDirName = '.tmpSimpleDataReductor'
        self.fitBoundsChannels = [ 
            [10, 824],
            [1224, 2872],
            [3272, 4086]
        ]
        if(tarName != None):
            self.__openTheArchive(tarName)
            self.__processData()

    def __openTheArchive(self, tarName):
        '''
        Opens the archive and lists the insides of it
        '''
        archive = tarfile.open(tarName, 'r')
        self.scansList = archive.getnames()
        os.mkdir(self.tmpDirName)
        archive.extractall(path='./' + self.tmpDirName)
    
    def __processData(self):
        '''
        processes the tared data
        '''
        self.obs = observation(self.tmpDirName, self.scansList)
        os.system("rm " + self.tmpDirName + "/*")
        os.rmdir(self.tmpDirName)
        #self.obs.proceed_scans()
        #self.obs.proceed_scans()
