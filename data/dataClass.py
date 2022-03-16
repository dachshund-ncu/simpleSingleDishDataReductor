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
        
        self.actualBBC = 1
        self.fitOrder = 10
        
        self.stack = []
        self.scansInStack = []
        self.meanStack = []
        self.freqSwitchMode = True
        self.velTab = self.__generateVelTab()
        


    def fitChebyForScan(self, bbc, order, scannr):
        '''
        Fits polynomial for specified BBC, with specified order and for 
        specified scan, returns tables X and Y with polynomial and fit residuals
        '''
        polyTabX, polyTabY, self.polyTabResiduals = self.obs.mergedScans[scannr].fitCheby(bbc, order, self.fitBoundsChannels)
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

    def addToStack(self, scanIndex):
        if self.__checkIfStacked(scanIndex):
            print(f"-----> scan no. {scanIndex+1} is already stacked!")
            return
        x,y,residuals, = self.fitChebyForScan(self.actualBBC, self.fitOrder, scanIndex)
        self.stack.append(residuals)
        self.scansInStack.append(scanIndex)

    def calculateSpectrumFromStack(self):
        if len(self.stack) == 0:
            return [-1]
        else:
            return np.mean(self.stack, axis=0)

    def deleteFromStack(self, scanIndex):
        if not self.__checkIfStacked(scanIndex):
            print(f"-----> scan no. {scanIndex+1} was not stacked, so it cannot be removed!")
            return
        i = self.scansInStack.index(scanIndex)
        self.scansInStack.pop(i)
        self.stack.pop(i)

    def __checkIfStacked(self, indexNo):
        if indexNo in self.scansInStack:
            return True
        else:
            return False
    
    def setLHCTab(self):
        self.LHCTab = np.mean(self.stack, axis=0)
    def setRHCTab(self):
        self.RHCTab = np.mean(self.stack, axis=0)

    def __generateVelTab(self):
        '''
        It is to make and return proper array of Radial Velocity, with respect to the local standard of rest (LSR)
        Generally, the data is rotated to this frame upon loading, so here we are just generating the table straightfoward
        Nothing really complicated
        '''
        velocity = self.obs.scans[0].vlsr # km/s
        restfreq = self.obs.scans[0].rest # MHz
        if (self.freqSwitchMode):
            freq_rang = self.obs.scans[0].bw / 2.0 # MHz
            nchans = self.obs.scans[0].NNch / 2.0
        else:
            freq_rang = self.obs.scans[0].bw
            nchans = self.obs.scans[0].NNch

        c = 299792.458 # km/s
        beta = velocity / c
        gamma  = 1.0 / np.sqrt(1.0 - beta**2.0)
        fcentr = restfreq * (gamma * (1.0 - beta))
        fbegin = fcentr - freq_rang / 2.0
        fend = fcentr + freq_rang / 2.0
        #self.auto_prepared_to_fft = zeros((4, self.NN), dtype=complex128) # docelowa
        freqsTab = np.zeros((4, int(nchans)), dtype=np.float64)
        velsTab = np.zeros((4, int(nchans)), dtype=np.float64)
        for i in range(len(fbegin)):
            freqsTab[i] = np.linspace(fbegin[i], fend[i], int(nchans))
            velsTab[i] = - c * ( (freqsTab[i] / restfreq[i] ) - 1.0 )
        return velsTab

    def removeChannels(self, BBC, scanNumber, removeTab):
        self.obs.mergedScans[scanNumber].removeChannels(BBC, removeTab)
    
    def cancelRemoval(self, BBC, scanNumber):
        self.obs.mergedScans[scanNumber].cancelRemove(BBC)