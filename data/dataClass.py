'''
Class, that holds the whole data
'''

import tarfile
from scanObservation import observation
import sys
import os
import numpy as np

class dataContainter:
    def __init__(self, tarName = None):
        '''
        Initializes dataContainer class
        '''
        self.noOfBBC = 4
        self.tmpDirName = '.tmpSimpleDataReductor'
        self.fitBoundsChannels = [ 
            [10, 824],
            [1224, 2872],
            [3272, 4086]
        ]
        if(tarName != None):
            self.__openTheArchive(tarName)
            self.__processData()
            self.zTab = self.__getZData()
            self.tsysTab = self.__getTsysData()
            self.totalFluxTab = self.__getTotalFluxData()
            self.timeTab = self.__getTimeData()
            self.mergedTimeTab = self.__getMergedTimeData()
        
        self.stack = []
        self.meanStack = []
        self.velTab = []


    def fitChebyForScan(self, bbc, order, scannr):
        '''
        Fits polynomial for specified BBC, with specified order and for 
        specified scan, returns tables X and Y with polynomial and fit residuals
        '''
        polyTabX, polyTabY, self.polyTabResiduals = self.obs.mergedScans[scannr].fitCheby(bbc-1, order, self.fitBoundsChannels)
        return polyTabX, polyTabY, self.__halveResiduals(self.polyTabResiduals)

    def __halveResiduals(self, residuals):
        chanCnt = int(len(residuals) / 2)
        self.tmpHalvedRes = (residuals[:chanCnt] - residuals[chanCnt:]) / 2.0
        return self.tmpHalvedRes

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
    
    def __calculateRMS(self, data):
        sum = 0.0
        no = 0
        for i in self.fitBoundsChannels:
            sum += np.sum( data[i[0]:i[1]] * data[i[0]:i[1]])
            no += (i[1] - i[0])
        return np.sqrt(1.0 / no * sum)

    def __getZData(self):
        ztb = [90.0 - scan.EL for scan in self.obs.scans]
        #print(ztb)
        return np.asarray(ztb)
    
    def __getTsysData(self):
        tsystb = []
        for i in range(self.noOfBBC):
            tsystb.append([scan.tsys[i] / 1000.0 for scan in self.obs.scans])
        return np.asarray(tsystb)

    def __getTotalFluxData(self):
        totalFlux = []
        for i in range(self.noOfBBC):
            totalFlux.append( [np.sum(np.sqrt(scan.pols[i] * scan.pols[i])) for scan in self.obs.mergedScans])
        return np.asarray(totalFlux)

    def __getTimeData(self):
        time = np.asarray([i.mjd for i in self.obs.scans])
        self.startEpoch = time.min()
        return (time - self.startEpoch) * 24.0

    def __getMergedTimeData(self):
        time = np.asarray([i.mjd for i in self.obs.mergedScans])
        time -= self.startEpoch
        time *= 24
        return time