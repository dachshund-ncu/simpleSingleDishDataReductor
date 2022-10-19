'''
Klasa, przechowująca pojedynczy skan
Data utworzenia: 05.03.2022
Właściciel: Michał Durjasz

This file is part of the Simple Single-Dish Data Reeductor package (SSDDR)
'''

# -- importujemy potrzebne moduły --
# -- numpy --
from calendar import EPOCH
from numpy import exp, nan, int64, sin, cos, asarray, sqrt, mean, pi, radians, zeros, inf, complex128, linspace, loadtxt
from numpy.fft import fft
# -----------
# -- math i mpmath --
from math import copysign
from cmath import sqrt as math_sqrt
from mpmath import nint
# -----------
# -- astropy --
from astropy.time import Time
from astropy.coordinates import SkyCoord, FK5
import astropy.units as u
# -------------
# -- sys --
from sys import argv, exit
from os import path
# ---------
# -- barycorrpy --
import barycorrpy
# ----------------

class scan:

    # -- metoda inicjująca klasę --
    def __init__(self, filename, onOFF = False):
        self.isOnOff = onOFF
        # -- stałe --
        self.c = 2.99792458e+5
        self.NN = 8192

        # -- tablica z częstotliwościami restf --
        self.template_restfreqs = [1420.405751, 1612.23101, 1665.40184, 1667.35903, 1720.52998 ,6668.518,6030.747, 6035.092, 6049.084, 6016.746, 4765.562, 4592.976, 4593.098, 4829.664, 2178.595]
        
        # -- zapisujemy pierwszy atrybut - nazwę pliku .DAT --
        self.fname = filename
    
        # -- czytamy dalej --
        self.read_header_and_data()

    # -- metoda wczytująca plik .DAT --
    def read_header_and_data(self):
        # -- wczytujemy plik do pamięci --
        try:
            fle = open(self.fname, 'r+')
            a = fle.readlines()
            fle.close() 
        except FileNotFoundError:
            print("-----> File \"%s\" does not exist! Exiting..." % self.fname)
            print("-----------------------------------------")
            exit()

        # -- czytamy dalej --
        # nazwa źródła
        self.sourcename = a[0].split("\'")[1].strip()
        self.INT = float( (a[0].split())[1])

        # rektascensja
        tmp = a[1].split()
        self.RA = float(tmp[1]) + float(tmp[2]) / 60.0 + float(tmp[3]) / 3600.0
        self.rah = int(tmp[1])
        self.ram = int(tmp[2])
        self.ras = int(tmp[3])

        # deklinacja
        # jeśli pierwsza liczba (stopnie) jest większa od zera
        if float(tmp[4]) > 0:
            self.DEC = float(tmp[4]) + float(tmp[5]) / 60.0 + float(tmp[6]) / 3600.0
        # jeśli pierwsza liczba jest równa zero, sprawdzamy znak przed
        elif float(tmp[4]) == 0.0:
            # jeśli jest minus, lecimy z ujemnym dec
            if tmp[4][0] == '-':
                self.DEC = -1.0 * (-1.0 * float(tmp[4]) + float(tmp[5]) / 60.0 + float(tmp[6]) / 3600.0)
            # jeśli jest plus lub nic nie ma (jak na kurachen.org), lecimy z dodatnim dec
            else:
                self.DEC = float(tmp[4]) + float(tmp[5]) / 60.0 + float(tmp[6]) / 3600.0
        
        # jeśli pierwsza liczba (stopnie) jest mniejsza od zera
        else:
            self.DEC = -1.0 * (-1.0 * float(tmp[4]) + float(tmp[5]) / 60.0 + float(tmp[6]) / 3600.0)

        self.decd = int(tmp[4])
        self.decm = int(tmp[5])
        self.decs = int(tmp[6])
        # epoka
        self.epoch = float(tmp[7])

        # azymut i elewacja
        tmp = a[2].split()
        self.AZ = float(tmp[1]) # azymut
        self.EL = float(tmp[2]) # elewacja
        self.azd = int(self.AZ)
        self.azm = int(60 * (self.AZ % 1))
        self.eld = int(self.EL)
        self.elm = int(60 * (self.EL % 1))
        # czas
        tmp = a[4].split()
        # UT
        self.UTh = float(tmp[1]) # godzina UT
        self.UTm = float(tmp[2]) # minuta UT
        self.UTs = float(tmp[3]) # sekunda UT
        # ST
        self.STh = int(tmp[4]) # godzina ST
        self.STm = int(tmp[5]) # minuta ST
        self.STs = int(tmp[6]) # sekunda ST
        # data
        tmp = a[5].split()
        self.lsec = float(tmp[1]) # sekunda linukskowa
        self.dayn = float(tmp[2]) # dzień roku
        self.year = float(tmp[7]) # rok
        # szukamy miesiąca
        self.monthname = tmp[4]
        self.monthtab = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
        self.month = float(self.monthtab.index(self.monthname)) + 1
        self.day = float(tmp[5])
        
        # -- reszta dat - przeliczamy je --
        # na początek konstruujemy formatkę: YYYY-MM-DDTHH:MM:SS 
        self.isotime = str(int(self.year)) + "-"# + str(int(self.month))

        if len(str(int(self.month))) == 1:
            self.isotime = self.isotime + "0" + str(int(self.month)) + "-"
        else:
            self.isotime = self.isotime + str(int(self.month)) + "-"

        if len(str(int(self.day))) == 1:
            self.isotime = self.isotime + "0" + str(int(self.day)) + "T"
        else:
            self.isotime = self.isotime + str(int(self.day)) + "T"

        if len(str(int(self.UTh))) == 1:
            self.isotime = self.isotime + "0" + str(int(self.UTh)) + ":"
        else:
            self.isotime = self.isotime + str(int(self.UTh)) + ":"

        if len(str(int(self.UTm))) == 1:
            self.isotime = self.isotime + "0" + str(int(self.UTm)) + ":"
        else:
            self.isotime = self.isotime + str(int(self.UTm)) + ":"

        if len(str(int(self.UTs))) == 1:
            self.isotime = self.isotime + "0" + str(int(self.UTs))
        else:
            self.isotime = self.isotime + str(int(self.UTs))

        # nasza formatka nazywa się "isotime" i służy jako argument 
        # do funkcji "Time" z pakietu astropy.time
        # -- oblczamy czasy --
        self.tee = Time(self.isotime, format="isot", scale="utc")
        self.decimalyear = self.tee.decimalyear
        self.jd = self.tee.jd
        self.mjd = self.tee.mjd

        # -- tworzymy stringi do zapisu w pliku --
        # tym razem chodzi o coś w stylu 270421
        self.datestring = ""
        if len(str(int(self.day))) == 1:
            self.datestring = self.datestring + "0" + str(int(self.day))
        else:
            self.datestring = self.datestring + str(int(self.day))

        if len(str(int(self.month))) == 1:
            self.datestring = self.datestring + "0" + str(int(self.month))
        else:
            self.datestring = self.datestring + str(int(self.month))
        
        self.datestring = self.datestring + str(int(self.year - 2000))

        # -- częstotliwości --
        self.freq = []
        self.freqa = []
        self.rest = []
        self.bbcfr = []
        self.bbcnr = []
        self.polnames = []
        self.bw = []
        self.vlsr = []
        self.lo = []
        self.tsys = []

        tmp = a[6].split()
        for i in range(len(tmp)-1):
            self.freq.append(float(tmp[i+1]))
        
        tmp = a[7].split()
        for i in range(len(tmp)-1):
            self.freqa.append(float(tmp[i+1]))

        tmp = a[8].split()
        for i in range(len(tmp)-1):
            self.rest.append(float(tmp[i+1]))

        tmp = a[9].split()
        for i in range(len(tmp)-1):
            self.bbcfr.append(float(tmp[i+1]))

        tmp = a[10].split()
        for i in range(len(tmp)-1):
            self.bbcnr.append(int(tmp[i+1]))

        tmp = a[11].split()
        for i in range(len(tmp)-1):
            self.bw.append(float(tmp[i+1]))

        tmp = a[12].split()
        for i in range(len(tmp)-1):
            self.polnames.append(tmp[i+1])

        tmp = a[13].split()
        for i in range(len(tmp)-1):
            self.vlsr.append(float(tmp[i+1]))

        tmp = a[14].split()
        for i in range(len(tmp)-1):
            self.lo.append(float(tmp[i+1]))

        tmp = a[15].split()
        for i in range(len(tmp)-1):
            self.tsys.append(float(tmp[i+1]))
        
        self.freq = asarray(self.freq)
        self.freqa = asarray(self.freqa)
        self.rest = asarray(self.rest)
        self.bbcfr = asarray(self.bbcfr)
        self.bbcnr = asarray(self.bbcnr)
        self.polnames = asarray(self.polnames)
        self.bw = asarray(self.bw)
        self.vlsr = asarray(self.vlsr)
        self.lo = asarray(self.lo)
        self.tsys = asarray(self.tsys)

        self.read_data(a[19:])

    def read_data(self, a):
        # -- deklarujemy kontenery dla konkretnych BBC --
        self.auto = []
        self.bbc1I = []
        self.bbc2I = []
        self.bbc3I = []
        self.bbc4I = []
        self.no_of_channels = 4097
        # -- zapełniamy BBC --
        for i in range(self.no_of_channels):
            tmp = a[i].split()
            self.bbc1I.append(float(tmp[1]))
        for i in range(self.no_of_channels, 2*self.no_of_channels):
            tmp = a[i].split()
            self.bbc2I.append(float(tmp[1]))
        for i in range(2*self.no_of_channels, 3*self.no_of_channels):
            tmp = a[i].split()
            self.bbc3I.append(float(tmp[1]))
        for i in range(3*self.no_of_channels, 4*self.no_of_channels):
            tmp = a[i].split()
            self.bbc4I.append(float(tmp[1]))
        
	
        # -- wycinamy kanał 1313 --
        self.bbc4I[1312] = self.bbc4I[1311]
        self.bbc4I[1313] = self.bbc4I[1311]
        self.bbc4I[1314] = self.bbc4I[1311]

        # -- agregujemy do jednej tablicy --
        self.auto.append(self.bbc1I)
        self.auto.append(self.bbc2I)
        self.auto.append(self.bbc3I)
        self.auto.append(self.bbc4I)

        # -- zamieniamy na numpy array --
        self.auto = asarray(self.auto)
        # ----- Koniec czytania danych --

    def correct_auto(self, scannr = 1):
        
        # deklarujemy na początek tablice numpy
        self.average = zeros(4)
        self.auto0tab = zeros(4)
        self.multiple = zeros(4, dtype=int64)
        self.Nmax = zeros(4, dtype=int64)
        self.bias0 = zeros(4)
        self.zero_lag_auto = zeros(4)
        self.r0 = zeros(4)

        # pętla po BBC do korekcji funkcji autokorelacji
        for i in range(len(self.auto)):
            # średnia z ostatnich 240 kanałów
            self.average[i] = mean(self.auto[i][3857:])

            # tabliza z wartościami z pierwszych kanałów
            # pierwszy kanał na każdym BBC nie jest częścią
            # funkcji autokorelacji
            self.auto0tab[i] = self.auto[i][0]

            # obliczamy prawdziwą ilość "samples accumulated"
            # i zabezpieczamy się przed dzieleniem przez zero
            if self.average[i] == 0.0:
                self.multiple[i] = 0
            else:
                self.multiple[i] = int(nint(self.auto0tab[i] / self.average[i]))
            
            # liczymy Nmax
            # i zabezpieczamy się przed dzieleniem przez zero
            if self.multiple[i] == 0:
                self.Nmax[i] = 0
            else:
                self.Nmax[i] = int(self.auto0tab[i] / self.multiple[i])
            
            # liczymy bias
            # i zabezpieczamy się przed dzieleniem przez zero
            if self.Nmax[i] == 0:
                self.bias0[i] = 0.0
            else:
                self.bias0[i] = self.average[i] / self.Nmax[i] - 1

            # pozbywamy się intencjonalnego biasu z funkcji autokorelacji
            self.auto[i] = self.auto[i] - self.Nmax[i]

            # gromadzimy informacje na temat "zero lag autocorrelation"
            self.zero_lag_auto[i] = self.auto[i][1]

            # liczymy r0 (do statystyk, chyba nie będzie później używane)
            # i zabezpieczamy się przed dzieleniem przez zero
            if self.Nmax[i] == 0:
                self.r0[i] = 0.0
            else:
                self.r0[i] = self.zero_lag_auto[i] / self.Nmax[i]

            # normalizujemy całą funkcję autokorelacji
            # i zabezpieczamy się przed dzieleniem przez 0
            if self.zero_lag_auto[i] == 0.0:
                self.auto[i] = zeros(len(self.auto[i]))
            else:
                self.auto[i] = self.auto[i] / self.zero_lag_auto[i]
            
            # teraz korekcja na kwantyzację sygnału
            # punkt po punkcie
            for j in range(len(self.auto[i])):
                # by uniknąć "nan"
                tmp_number = self.__correctACF(self.auto[i][j], self.r0[i], self.bias0[i])
                if tmp_number is None:
                    self.auto[i][j] = 0.0
                else:
                    self.auto[i][j] = tmp_number

    def hanning_smooth(self):
        # wygładzamy funkcję autokorelacji
        for i in range(len(self.auto)):
            for j in range(1,len(self.auto[i]), 1):
                cosine = cos(pi * (j-1) / self.NN )**2.0
                self.auto[i][j] = self.auto[i][j] * cosine
    
    # argumenty: RA po prrecesji(decimal h), DEC po precesji (decimal deg), szerokość geograficzna(decimal deg), długość geograficzna(decimal deg), wysokość nad geoidą (m)
    def doppset(self, source_JNOW_RA, source_JNOW_DEC, szer_geog, dl_geog, height):
        # -------------- PRĘDKOŚCI --------------------
        # -- liczymy prędkość wokół barycentrum + rotacja wokół własnej osi --
        # rzutowane na źródło
        # metoda wykonuje precesję sama z siebie, toteż podajemy współrzędne na epokę 2000 przed precesją
        '''
        OBSOLETE:
        #self.baryvel, hjd = helcorr(obs_long = dl_geog, obs_lat = szer_geog, obs_alt = height, ra2000 = self.RA*15, dec2000 = self.DEC, jd=self.tee.jd) #self.tee to obiekt czasu (astropy.time)
        05.06.2022: we stopped using HELCORR, 'cause it utilizes obsolete doppset method
        '''
        bar = barycorrpy.get_BC_vel(self.tee, ra = self.RA * 15, dec = self.DEC, lat = szer_geog, longi=dl_geog, alt = height, epoch=2000)
        self.baryvel = bar[0][0] / 1000.0
        # -- liczymy prędkość w lokalnym standardzie odniesienia --
        # rzutowane na źródło
        self.lsrvel = self.__lsr_motion(source_JNOW_RA, source_JNOW_DEC, self.decimalyear)

        # -- prędkość dopplerowska to będzie ich suma --
        self.Vdop = self.baryvel + self.lsrvel
        # ----------------------------------------------

        
        # --------------- ROTACJA WIDMA ----------------
        # sprawdzamy, czy nasze rest jest w tablicy z template
        for i in range(len(self.auto)): # iteracja po indeksach
            for tmp_ind in self.template_restfreqs: # iteracja po templatkach
                # - jeśli znajdziemy int(nasza_częstotliwość) w templatce, to zamiast -
                # - restfreq z pliku używamy tego z templatki -
                if int(self.rest[i]) == int(tmp_ind):
                    self.rest[i] = tmp_ind
                    break
        

        # - deklarujemy tablice -
        self.fvideo = zeros(4)
        self.kanalf = zeros(4, dtype=int64)
        self.q = zeros(4)
        self.kanalv = zeros(4)


        # --- rotowanie oryginalnego widma ---
        # przesuwamy linię na 1/4 wstęgi (1/2 jeśli robimy obserwacje OnOff)
        if self.isOnOff:
            self.lo[0] = self.lo[0] - (self.bw[0] / 4)
        else:
            self.lo[0] = self.lo[0] - (self.bw[0] / 4)
        # faktyczna częstotliwość obserwowana
        self.fsky = self.rest - self.rest * (-self.Vdop + self.vlsr) / self.c
        # częstotliwość bbc linii widmowej
        self.f_IF = self.fsky - self.lo[0]

        # krótka pętla licząca
        self.NNch = len(self.auto[0]) - 1 # faktyczna ilość kanałów

        for i in range(len(self.auto)): # po BBC
            # fvideo
            self.fvideo[i] = self.f_IF[i] - copysign(self.bbcfr[i], self.f_IF[i])
            # kanalf (linia w domenie częstotliwości)
            self.kanalf[i] = int(self.NNch * abs(self.fvideo[i]) / self.bw[i] + 1)
            # q (położenie linii na wstędze)
            if self.fvideo[i] < 0.0:
                self.kanalf[i] = self.NNch - self.kanalf[i] + 1
                self.q[i] = (-self.fvideo[i] / self.bw[i])
            else:
                self.q[i] = 1.0 - self.fvideo[i] / self.bw[i] - 1.0 / self.NNch

        # robimy kanalv
        self.kanalv = self.NNch - self.kanalf + 1
        # prędkość w kanale 1024 w spoektrum częstotliwości
        if self.isOnOff:
            targetChan = 1024
        else:
            targetChan = 1024
        self.v1024f = self.vlsr + (targetChan - self.kanalf) * (-self.c * self.bw) / (self.rest * self.NNch)
        # prędkość w kanale 1024 w spektrum prędkości
        self.v1024v = self.vlsr + (targetChan - self.kanalv) * (self.c * self.bw) / (self.rest * self.NNch)
        
        # ilość kanałów, o które trzeba przerotować widmo 
        self.fc = self.q * self.NNch - targetChan
        self.fcBBC = self.fc

        # -- przygotowujemy dane do fft --
        self.fr = - (self.fc+1) * 2.0 * pi / self.NN

        # -- przygotowujemy tablicę do FFT --
        self.auto_prepared_to_fft = zeros((4, self.NN), dtype=complex128) # docelowa
        # --- rotujemy funkcję autokorelacji (mnożymy przez exp(sqrt(-1) * self.fr)) --
        for w in range(len(self.auto)): # iteruje po BBC
            phases = linspace(0, int(self.NN / 2)-1, int(self.NN / 2)) * self.fr[w] # fazy
            shift_coeffs = exp(math_sqrt(-1) * phases)
            # shifted auto array
            tmpwp = self.auto[w][1:] * shift_coeffs
            # non-mirror part
            self.auto_prepared_to_fft[w][:int(self.NN / 2)] = tmpwp
            # mirror part
            self.auto_prepared_to_fft[w][int(self.NN / 2)+1:] = tmpwp[::-1][:-1].conjugate() # odwracamy znakiem część zespoloną

            self.auto_prepared_to_fft[w][4096] = (0 + 0j)
        # --------------
        
    # -- liczy kilka parametrów --
    def do_statistics(self):
        # liczymy rmean
        self.rMean = self.bias0 * 100.0

        # liczymy ACF0
        self.ACF0 = self.r0

        # liczymy niepewności
        self.V_sigma = zeros(4)
        for i in range(len(self.auto)):
            self.V_sigma[i] = self.__clipLevel(self.r0[i])
    
    # -- skaluje widmo w mili kelwinach --
    def scale_tsys_to_mK(self):
        # pętla po 4 bbc
        for i in range(len(self.auto)):
            self.tsys[i] = self.tsys[i] * 1000.0
            if self.tsys[i] < 0.0:
                self.tsys[i] = 1000.0 * 1000.0

    def make_transformata_furiata(self):

        # -- wykonujemy transformatę furiata --
        # deklarujemy tablice, by oszczędzić czas
        self.spectr_bbc = zeros((4, self.NN))
        self.spectr_bbc_final = zeros((4,int(self.NN / 2)))
        # pętla po BBC
        for i in range(len(self.auto)):

            # przywołujemy numpy.fft.fft by policzyć transformatę
            self.spectr_bbc[i] = fft(self.auto_prepared_to_fft[i]).real

            # sprawdzamy, czy należy wziąć widmo dolne czy górne:
            # to zapewne zależy od lustrzanki (HIGH vs LOW)
            # najlepwniej zawsze będzie widmo górne brane
            # jako iż lustrzanka LOW była tylko w spektroskopii L
            if self.fvideo[i] > 0: # jak tak, to górne
                self.spectr_bbc_final[i] = self.spectr_bbc[i][int(self.NN / 2):]
            else: # jak nie, to dolne
                self.spectr_bbc_final[i] = self.spectr_bbc[i][:int(self.NN / 2)]

    # -- kalibruje dane w tsys --
    def calibrate_in_tsys(self):
        for i in range(len(self.auto)):
            self.spectr_bbc_final[i] = self.spectr_bbc_final[i] * self.tsys[i]

    # -- wyświetla rozszerzone informacje o procedurze --
    def extended_print(self):
        print('f(LSR)/MHz   f(sky)      LO1(RF)    LO2(BBC)   fvideo   v(Dopp) [km/s] V(LSR)')
        #print(tab[i].rest[0], tab[i].fsky[0], tab[i].lo[0], tab[i].bbcfr[0], tab[i].fvideo[0], -Vdop, tab[i].vlsr)
        print('%.3f    %.3f    %.3f    %.3f    %.3f    %.3f       %.3f' % (self.rest[0], self.fsky[0], self.lo[0], self.bbcfr[0], self.fvideo[0], -self.Vdop, self.vlsr[0]))
        print('====> Frequency domain: line is in', self.kanalf[0], '=', round(self.v1024f[0],3), 'km/s')
        print('====> Velocity domain: line is in', self.kanalv[0], '=', round(self.v1024v[0],3), 'km/s')
        print('Output spectra were rotated by', round(self.fcBBC[0],3), 'channels')
        if self.fvideo[0] > 0:
            date6 = ' (USBeff)'
        else:
            date6 = ' (LSBeff)'
        print('ACFs', date6, 'Nmax =', int(self.Nmax[3]), '    BBC1   ', '  BBC2   ', '   BBC3   ', '  BBC4')
        print("r0 =                                %.4f    %.4f    %.4f    %.4f" % (self.ACF0[0], self.ACF0[1], self.ACF0[2], self.ACF0[3]))
        print("rmean (bias of 0) =                 %.4f    %.4f    %.4f    %.4f" % (self.rMean[0], self.rMean[1], self.rMean[2], self.rMean[3]))
        print("Threshold (u=V/rms) =               %.4f    %.4f    %.4f    %.4f" % (self.V_sigma[0], self.V_sigma[1], self.V_sigma[2], self.V_sigma[3]))

    # ---- POMOCNICZE METODY PRYWATNE ----

    # -- oblicza prędkość słońca względem LSR (local standard of rest) --
    # -- rzutowaną na kierunek, w którym jest źródełko --
    # -- RA i DEC podawane muszą być w STOPNIACH --
    # -- i poprawione na PRECESJĘ --
    def __lsr_motion(self, ra,dec,decimalyear):
        
        # -- zacztnamy --
        vSun0 = 20.0

        # -- współrzędne apeksu słońca z 1900 --
        ras = 18.0 * pi / 12.0 # radiany
        decs = 30.0 * pi / 180.0 # radiany
        # -- obiekt skycoord - apeks słońca w roku 1900 --
        sunc = SkyCoord(ras*u.rad, decs*u.rad, frame=FK5, equinox="B1900")
        # deklarujemy nowy frame z epoką jak nasze obserwacje
        sunc_now = FK5(equinox="J" + str(decimalyear))
        # przechodzimy między frame'ami
        sunc_new = sunc.transform_to(sunc_now)
        # ekstra*ujemy współrzędne i zamieniamy na radiany
        dec_new = radians((sunc_new.dec*u.degree).value)
        ra_new = radians((sunc_new.ra*u.degree).value)
        
        # -- zamieniamy ra i dec na radiany --
        ra = radians(ra)
        dec = radians(dec)
        # -- funkcje na przekazanych współrzędnych
        cdec = cos(dec)
        sdec = sin(dec)

        # -- obliczamy prędkość słońca względem local standard of rest --
        # -- w kierunku ra i dec --
        vSun = vSun0 * ( sin(dec_new) * sdec + cos(dec_new) * cdec * cos(ra-ra_new))
        return vSun
        # -------------

    # -- metoda: correctACF --
    # nakłada na funkcję autokorelacji krektę na 2 i 3 - poziomową kwantyzację
    # przyjmuje w argumencie pojedynczy punkt
    def __correctACF(self, autof, r0, rMean):
        '''
        Oblicza korekcję do funkcji autokorelacji dla kilku przypadków
        3- i 2- poziomowego autokorelatora
        autof - funkcja autokorelacji (jeden punkt dokładnie)
        r0 - współczynnik korelacji dla zerowego zapóźnienia
        bias0 - średni współczynnik dla ogona funkcji autokorelacji (większe zapóźnienia)

        Ta metoda jest w całości przeportowana z programu A2S, który jest napisany w języku Fortran77 przez K. Borkowskiego
        '''
        if rMean <= 1e-5:
            # -- limituemy funkcję autokorelacji między 0 i 1
            # tak powinna być znormalizowana (1 w zerowym zapóźnieniu)
            r = min([1.0, abs(autof)])
            if r0 > 0 and r0 < 0.3:
                r = r * 0.0574331 # tak jest w a2s
                rho= r*(60.50861 + r*(-1711.23607 + r*(26305.13517 - r*167213.89458)))/0.99462695104383
                correct_auto = copysign(rho, autof)
                return correct_auto
            elif r0 > 0.3 and r0 < 0.9:
                # trzypoziomoy autokorelator
                r = r * 0.548506
                rho = (r*(2.214 + r*(0.85701 + r*(-7.67838 + r*(22.42186 - r*24.896)))))/0.998609598617374
                correct_auto = copysign(rho, autof)
                return correct_auto
            elif r0 > 0.9:
                rho = sin(1.570796326794897*r)
                correct_auto = copysign(rho, autof)
                return correct_auto
        else:
            autof2 = autof **2.0
            if (abs(autof)) < 0.5:
                fac = 4.167810515925 - r0*7.8518131881775
                a = -0.0007292201019684441 - 0.0005671518541787936*fac
                b =  1.2358980680949918 + 0.03931789097196692*fac
                c = -0.11565632506887912 + 0.08747950965746415*fac
                d =  0.01573239969731158 - 0.06572872697836053*fac
                correct_auto = a + (b + (c + d*autof2)*autof2)*autof
                return correct_auto
            elif (autof > 0.5):
                correct_auto = -1.1568973833585783 + 10.27012449073475*autof - 27.537554958512125*autof2 + 40.54762923890069*autof**3 - 28.758995213769058*autof2**2 + 7.635693826008257*autof**5 + 0.218044850 * (0.53080867 - r0) * cos(3.12416*(autof-0.49721))
                return correct_auto
            else:
                correct_auto = -0.0007466171982634772 + autof*(1.2660000881004778 + autof2*(-0.4237089538779861 + autof2*(1.0910718879007775 + autof2*(-1.452946181286572 + autof2*0.520334578982730)))) + 0.22613222 * (0.53080867 - r0) * cos(3.11635*(autof-0.49595))
                return correct_auto
    
    # -- metoda: Clip level --
    # -- skopiowana z oryginalnego A2S --
    def __clipLevel(self, ratio):
        Err = 1 - ratio
        x = 0
        for i in range(100):
            dE = self.__erf(x + 0.01) - self.__erf(x)
            if dE == 0.0:
                return inf
            x = x + (Err-self.__erf(x)) * 0.01 / dE
            if abs(Err-self.__erf(x)) < 0.0001:
                return sqrt(2.0) * x
            else:
                continue

    # -- pomocnicza metoda do Clip Level --
    def __erf(self, x):
        t = 1.0 / (1+0.3275911*x)
        erf= 1.0 - t*(0.254829592 + t*(-0.284496736 + t*(1.421413741 + t*(-1.453152027 + t*1.061405429))))*exp(-x**2)
        return erf
    # ----------------------------------