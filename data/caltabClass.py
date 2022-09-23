'''
Class that holds caltab
There can be numerous caltab instances, so this should be taken into account
'''

import numpy as np
from os import remove as rm

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
            self.freqRange = freqRange
            self.__loadCaltab(filename)
            self.label=label
            
    def __loadCaltab(self, filename):
        '''
        C'mon, it's pretty straightforward what it does, really xD
        download file and load, then remove temporary file
        Simple
        '''
        # validating if these are URL
        # LHC
        self.lhcMJDTab, self.lhcCoeffsTab = np.loadtxt(filename[0], usecols=(0,1), unpack=True)
        
        # RHC
        self.rhcMJDTab, self.rhcCoeffsTab = np.loadtxt(filename[1], usecols=(0,1), unpack=True)
        rm('tmpCalTab')
        self.lhcMJDTab += 50000.0
        self.rhcMJDTab += 50000.0

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