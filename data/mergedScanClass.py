'''
Klasa, przechowująca merged skany
Data utworzenia: 05.03.2022
Właściciel: Michał Durjasz
'''

from scanClass import scan
import numpy as np
class mergedScan:
    
    def __init__(self, scan1, scan2):
        '''
        Prosta metoda inicjująca klasę mergedScan
        pols to polaryzacje z pełną wstęgą
        '''
        self.pols = self.__mergeScans(scan1, scan2)

    
    def fitCheby(self, bbc, order, ranges):
        '''
        metoda ma za zadanie dopasować wielomien
        do danych z zakresów przekazanych w 
        ranges
        zwraca tablice X i Y wielomianu, dodatkowo również rezydua dopasowania
        potrzebne przy generowaniu ostatecznej tablicy z widmem
        '''
        fitCHans, fitData = self.__getDataFromRanges(bbc, ranges)
        poly = np.polyfit(fitCHans, fitData, order)
        polyTabX = np.linspace(1, self.numberOfChannels, self.numberOfChannels)
        polyTabY = np.polyval(poly, polyTabX)
        polyTabResiduals = self.pols[bbc] - polyTabY
        return polyTabX, polyTabY, polyTabResiduals

    def __getDataFromRanges(self, bbc, ranges):
        fitData = []
        chans = np.linspace(1, self.numberOfChannels, self.numberOfChannels)
        fitChans = []
        for i in ranges:
            fitData.extend(self.pols[bbc][i[0]:i[1]])
            fitChans.extend(chans[i[0]:i[1]])
        return np.asarray(fitChans), np.asarray(fitData)

    def __mergeScans(self, scan1, scan2):
        '''
        Ta metoda jest wywoływana tylko w __INIT__ 
        i ma na celu połączenie wynikowych widm z dwóch
        kolejnych skanów. Skany finalne przechowywane są w 
        spectr_bbc_final i powinny mieć 4 BBC, ale metoda
        i tak sama sprawdza, czy tak jest w istocie
        '''
        # ZAŁOŻENIE: każde BBC ma równą ilość kanałów!
        self.numberOfBBC = len(scan1.spectr_bbc_final)
        self.numberOfChannels = len(scan1.spectr_bbc_final[0])
        tmpScans = np.zeros( (self.numberOfBBC, self.numberOfChannels), dtype=np.float64 )
        for i in range(self.numberOfBBC):
            tmpScans[i] = scan1.spectr_bbc_final[i] / 1000.0 - scan2.spectr_bbc_final[i] / 1000.0
        return tmpScans