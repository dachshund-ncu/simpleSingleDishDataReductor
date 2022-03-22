'''
Class, that holds the whole data
'''

import tarfile
from scanObservation import observation
from caltabClass import caltab
import sys
import os
import numpy as np
import configparser

class dataContainter:
    def __init__(self, tarName = None):

        '''
        CALTAB LOADING BLOCK
        '''
        self.caltabs = []
        self.__tryToLoadCaltabs()

        '''
        Initializes dataContainer class
        '''
        self.noOfBBC = 4
        self.actualBBC = 1
        self.fitOrder = 10
        self.freqSwitchMode = True
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
            self.velTab = self.__generateVelTab()
            self.properCaltabIndex = self.findProperCaltabIndex()

        
        # -- FINAL SPECTRUM --
        self.finalFitBoundChannels = [
            [10,20],
            [1100, 2038]
        ]
        self.stack = []
        self.scansInStack = []
        self.meanStack = []
        self.finalFitRes = []
        self.finalRHC = []
        self.finalLHC = []
        # --------------------
        



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
        print("-----> Loading archive \"" + tarName + "\"...")
        archive = tarfile.open(tarName, 'r')
        self.scansList = archive.getnames()
        os.mkdir(self.tmpDirName)
        archive.extractall(path='./' + self.tmpDirName)
    
    def __processData(self):
        '''
        processes the tared data
        '''
        self.obs = observation(self.tmpDirName, self.scansList)
        for i in self.scansList:
            os.remove(self.tmpDirName + "/" + i)
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

    def calculateSpectrumFromStack(self, calCoeff = 1.0):
        if len(self.stack) == 0:
            return [-1]
        else:
            self.meanStack = np.mean(self.stack, axis=0) * calCoeff
            self.finalFitRes = self.meanStack.copy()
            return self.finalFitRes

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
            velsTab[i] = velsTab[i][::-1]
        return velsTab

    def removeChannels(self, BBC, scanNumber, removeTab):
        self.obs.mergedScans[scanNumber].removeChannels(BBC, removeTab)
    
    def cancelRemoval(self, BBC, scanNumber):
        self.obs.mergedScans[scanNumber].cancelRemove(BBC)
    
    def fitChebyToFinalSpec(self, BBC):
        fitVels, fitData = self.__getDataFromRanges(BBC, self.finalFitBoundChannels)
        poly = np.polyfit(fitVels, fitData, self.fitOrder)
        polytabX = np.linspace(self.velTab.min(), self.velTab.max(), len(self.meanStack))
        polytabY = np.polyval(poly, polytabX)
        self.finalFitRes -= polytabY

    def __getDataFromRanges(self, BBC, ranges):
        fitData = []
        fitVels = []
        for i in ranges:
            fitData.extend(self.finalFitRes[i[0]:i[1]])
            fitVels.extend(self.velTab[BBC-1][i[0]:i[1]])
        #print(len(fitVels), len(fitData))
        return fitVels, fitData
    
    def convertVelsToChannels(self, BBC, velTab):
        chanTab = []
        for i in velTab:
            minChan = -1
            maxChan = -1
            # find minChan
            for j in range(len(self.velTab[BBC])):
                if i[0] < self.velTab[BBC][j]:
                    minChan = j
                    break
            # find maxChan
            for j in range(len(self.velTab[BBC])):
                if i[1] < self.velTab[BBC][j]:
                    maxChan = j
                    break
            if minChan != -1 and maxChan != -1:
                chanTab.append([minChan, maxChan])
        return chanTab
    
    def removeChansOnFinalSpectrum(self, channelsToRemove):
        for i in channelsToRemove:
            minChan = i[0]
            maxChan = i[1]
            print(f'------> Removing from channels {minChan} to {maxChan}')
            for j in range(minChan, maxChan, 1):
                self.finalFitRes[j] = self.__interpolateFinal(minChan, maxChan, j)

    def __interpolateFinal(self, minChan, maxChan, j):
        '''
        interpolate between specified channels for channel j
        '''
        y1 = self.finalFitRes[minChan]
        x1 = minChan
        y2 = self.finalFitRes[maxChan]
        x2 = maxChan
        a = (y1-y2) / (x1 - x2)
        b = y1 - a * x1
        return a * j + b
    
    def cancelChangesFinal(self):
        print(f'------> cancelling all of the changes!')
        self.finalFitRes = self.meanStack.copy()
    
    def clearStack(self, pol='LHC'):
        if pol == 'LHC':
            self.finalLHC = self.finalFitRes.copy()
        elif pol == 'RHC':
            self.finalRHC = self.finalFitRes.copy()
        
        self.meanStack = []
        self.stack = []
        self.stack = []
        self.scansInStack = []
        self.finalFitRes = []
    
    def clearStackedData(self):
        self.meanStack = []
        self.stack = []
        self.stack = []
        self.scansInStack = []
        self.finalFitRes = []

    def setActualBBC(self, BBC):
        self.actualBBC = BBC

    def getFinalPols(self):
        I = (self.finalLHC / 2.0) + (self.finalRHC / 2.0)
        V  = self.finalRHC - self.finalLHC
        return I, V, self.finalLHC, self.finalRHC
    
    def __tryToLoadCaltabs(self):
        try:
            print("-----> Loading caltabs...")
            confile = configparser.ConfigParser()
            confile.read('caltabPaths.ini')
            for i in confile.sections():
                label = i
                tab_paths = [confile[i]['lhcCaltab'], confile[i]['rhcCaltab']]
                freq_ranges = [ float(confile[i]['minFreq']), float(confile[i]['maxFreq'])]
                self.caltabs.append(caltab(i, tab_paths, freq_ranges))
                print(f"-----> Caltab loaded: {i} ({freq_ranges[0]} - {freq_ranges[1]} GHz)")
                print("-----> LHC:", confile[i]['lhcCaltab'])
                print("-----> RHC:", confile[i]['rhcCaltab'])
            print("-----------------------------------------")
        except:
            print("-----> No caltabs found!")
    
    def findProperCaltabIndex(self):
        '''
        Assumes the data is loaded
        '''
        properIndex = -1
        for i in range(len(self.caltabs)):
            if self.caltabs[i].inRange(self.obs.scans[0].rest[0] / 1000.0):
                properIndex = i
        return properIndex
    
    def printCalibrationMessage(self, calCoeff, epoch, lhc=True):
        print('-----------------------------------------')
        print(f'-----> CALIBRATION PROMPT:')
        print(f'-----> Using {self.caltabs[self.properCaltabIndex].label} to calibrate the data')
        print(f'-----> Coefficient is {calCoeff} for MJD {int(epoch)}')
        if lhc==True:
            maxEpoch = self.caltabs[self.properCaltabIndex].lhcMJDTab.max()
            minEpoch = self.caltabs[self.properCaltabIndex].lhcMJDTab.min()
        else:
            maxEpoch = self.caltabs[self.properCaltabIndex].rhcMJDTab.max()
            minEpoch = self.caltabs[self.properCaltabIndex].rhcMJDTab.min()

        if epoch < maxEpoch and epoch > minEpoch:
            print(f'-----> Epoch is placed between MJD {minEpoch} and {maxEpoch}')
            print(f'-----> Looks OK')
        else:
            print(f'-----> Epoch is placed OUTSIDE caltab (MJD from {minEpoch} to {maxEpoch}')
            print(f'-----> Check CAREFULLY if this is ok.')
        print('-----------------------------------------')