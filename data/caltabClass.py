'''
Class that holds caltab
There can be numerous caltab instances, so this should be taken into account
'''

import numpy as np
import validators as valid
import requests

class caltab():
    def __init__(self, label = None, filename=None, freqRange = None):
        '''
        Initializes caltab instance. 
        << filename >> should be a list with two filenames:
        --> filename[0] - table with LHC
        --> filename[1] - table with RHC
        If filename is provided, it gets loaded at the start
        If not - only empty Caltab instance is initialized
        '''
        if not (filename is None):
            self.__loadCaltab(filename)
            self.label=label
            self.freqRange = freqRange

    def __loadCaltab(self, filename):
        '''
        C'mon, it's pretty straightforward what it does, really xD
        If filename[0] is an URL: download file and load
        If it is NOT an URL: just load
        Simple
        '''
        # validating if these are URL
        # LHC
        if valid.url(filename[0]):
            r = requests.get(filename[0], allow_redirects=True)
            open('CALTAB_L1', 'wb').write(r.content)
            self.lhcMJDTab, self.lhcCoeffsTab = np.loadtxt('CALTAB_L1', usecols=(0,1), unpack=True)
        else:
            self.lhcMJDTab, self.lhcCoeffsTab = np.loadtxt(filename[0], usecols=(0,1), unpack=True)
        
        # RHC
        if valid.url(filename[1]):
            r = requests.get(filename[1], allow_redirects=True)
            open('CALTAB_R1', 'wb').write(r.content)
            self.rhcMJDTab, self.rhcCoeffsTab = np.loadtxt('CALTAB_R1', usecols=(0,1), unpack=True)
        else:
            self.rhcMJDTab, self.rhcCoeffsTab = np.loadtxt(filename[1], usecols=(0,1), unpack=True)

        self.lhcMJDTab += 50000.0
        self.rhcMJDTab += 50000.0
        #[print(self.lhcMJDTab[i], self.lhcCoeffsTab[i]) for i in range(len(self.lhcMJDTab))]

    def findCoeffs(self, date):
        '''
        It aims to find cal coefficients, based on MJD date, provided as an argument
        '''
        coeffLHC = np.interp(date, self.lhcMJDTab, self.lhcCoeffsTab)
        coeffRHC = np.interp(date, self.rhcMJDTab, self.rhcCoeffsTab)
        return coeffLHC, coeffRHC

    def __findPrevAndNextEpoch(self, date):
        '''
        It iterates through the calibration table in order to find previous and next cal coeffs to interpolate
        '''
        pass

    def inRange(self, frequency):
        if frequency > self.freqRange[0] and frequency < self.freqRange[1]:
            return True
        else:
            return False