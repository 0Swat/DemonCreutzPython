import random
import matplotlib.pyplot as plt
import numpy as np
import math
import os

class Uklad:
    def __init__(self, szerokosc, wysokosc, x, demon):

        self.wysokosc = wysokosc
        self.szerokosc = szerokosc
        self.energiaDemona = demon # początkowa energia Demona

        self.tablica = [[1 for _ in range(szerokosc)] for _ in range(wysokosc)]

        self.kroki = list(range(x)) 
        self.energieUkladu = [0 for _ in range(x)]
        self.energieDemona = [0 for _ in range(x)]
        self.magnetyzacje = [0 for _ in range(x)]

        self.histogramEnergiiX = []
        self.histogramEnergiiY = []

        self.ustabilizowanyHistogramEnergiiX = []
        self.ustabilizowanyHistogramEnergiiY = []

        self.magnetyzacjeUstabilizowana = []
        self.krokiMagnetyzacjaUstabilizowana = []


        self.sredniaMagnetyzacja = 0
        self.sredniaMagnetyzacjaUstabilizowana = 0
        self.a = 0
        self.T = 0




    # Główna funkcja
    def Strzelaj(self):
        for skok in range(0, len(self.kroki)):
            if skok == 0:
                self.energieUkladu[0] = self.Energia()
                self.magnetyzacje[0] = self.Magnetyzacja()
                self.energieDemona[0] = self.energiaDemona
                self.histogramEnergiiY.append(1)
                self.histogramEnergiiX.append(self.energiaDemona)
            else:
                self.ZmienElementUkladu(skok)
                self.DodajElementDoHistogramuEnergii(skok)
                self.SortujHistogramEnergii()



    # Zwraca energię układu
    def Energia(self): 
        energiaUkladu = 0
        for i in range(0, self.wysokosc):
            for j in range(0, self.szerokosc):
                if i == self.szerokosc - 1:
                    energiaUkladu += (self.tablica[i][j] * self.tablica[0][j])
                else:
                    energiaUkladu += (self.tablica[i][j] * self.tablica[i + 1][j])
                if j == self.szerokosc - 1:
                    energiaUkladu += (self.tablica[i][j] * self.tablica[i][0])
                else:
                    energiaUkladu += (self.tablica[i][j] * self.tablica[i][j + 1])
        return energiaUkladu * -1
    
    # Zwraca magnetyzację układu
    def Magnetyzacja(self):
        suma = 0
        for i in range(0, self.wysokosc):
            for j in range(0, self.szerokosc):
                suma += self.tablica[i][j]
        return suma
    
    #Zwraca energię danej pozycji
    def EnergiaElementu(self, i, j):
        energia = 0
        if i == self.wysokosc - 1:
            energia += (self.tablica[i][j] * self.tablica[0][j])
        else:
            energia += (self.tablica[i][j] * self.tablica[i + 1][j])
        if j == self.szerokosc - 1:
            energia += (self.tablica[i][j] * self.tablica[i][0])
        else:
            energia += (self.tablica[i][j] * self.tablica[i][j + 1])

        if i == 0:
            energia += (self.tablica[i][j] * self.tablica[self.wysokosc-1][j])
        else:
            energia += (self.tablica[i][j] * self.tablica[i - 1][j])
        if j == 0:
            energia += (self.tablica[i][j] * self.tablica[i][self.szerokosc-1])
        else:
            energia += (self.tablica[i][j] * self.tablica[i][j - 1]) 
        
        return energia*-1
    

    # Dodaje daną energię na odpowiednie miejsce
    def DodajElementDoHistogramuEnergii(self, skok):
        for i in range(0, len(self.histogramEnergiiX)):
            if self.energieDemona[skok] == self.histogramEnergiiX[i]:
                self.histogramEnergiiY[i] += 1
                break
            elif i == len(self.histogramEnergiiX)-1:
                self.histogramEnergiiY.append(1)
                self.histogramEnergiiX.append(self.energieDemona[skok])


    # Sortuje Histogram Energii (X oraz Y względem X-ów)
    def SortujHistogramEnergii(self):
        combined_data = list(zip(self.histogramEnergiiX, self.histogramEnergiiY))
        sorted_data = list(sorted(combined_data, key=lambda x: x[0], reverse=False))
        temphistogramEnergiiX, temphistogramEnergiiY = list(zip(*sorted_data))
        self.histogramEnergiiX = list(temphistogramEnergiiX)
        self.histogramEnergiiY = list(temphistogramEnergiiY)


    # Wykonanie spina, jeżeli możliwe
    def ZmienElementUkladu(self, skok):
        # Wylosuj pozycje
        i = random.randint(0, self.wysokosc - 1)
        j = random.randint(0, self.szerokosc - 1)

        # Zaktualizuj energię Demona oraz układu
        delta = self.EnergiaElementu(i, j)
        self.tablica[i][j] *= -1
        delta -= self.EnergiaElementu(i, j)
        self.energieDemona[skok] = self.energieDemona[skok-1] + delta  
        self.energieUkladu[skok] = self.energieUkladu[skok - 1] - delta

        # Oblicz magnetyzację
        if self.tablica[i][j] == -1:
            self.magnetyzacje[skok] = self.magnetyzacje[skok - 1] - 2
        else:
            self.magnetyzacje[skok] = self.magnetyzacje[skok - 1] + 2

        # Jeśli energia Demona jest mniejsza niż zero, nieudany spin, pozostaje bez zmian
        if self.energieDemona[skok] < 0:
            self.tablica[i][j] *= -1
            self.energieDemona[skok] = self.energieDemona[skok-1]
            self.energieUkladu[skok] = self.energieUkladu[skok - 1]
            self.magnetyzacje[skok] = self.magnetyzacje[skok - 1]


    # Uzupełnia odpowiednio tablice zawierające dane po stabilizacji
    def Stabilizuj(self, do_energii, od_kroku, czy_linearyzacja):
        for i in range(0, len(self.histogramEnergiiY)):
            if self.histogramEnergiiX[i] <= do_energii:
                self.ustabilizowanyHistogramEnergiiX.append(self.histogramEnergiiX[i])
                self.ustabilizowanyHistogramEnergiiY.append(self.histogramEnergiiY[i])

        if czy_linearyzacja == True: 
            for i in range(0, len(self.ustabilizowanyHistogramEnergiiY)):
                self.ustabilizowanyHistogramEnergiiY[i] = math.log(self.ustabilizowanyHistogramEnergiiY[i])

        for i in range(0, len(self.magnetyzacje)):
                if i >= od_kroku:
                    for j in range(i, len(self.magnetyzacje)):
                        self.magnetyzacjeUstabilizowana.append(self.magnetyzacje[j])
                        self.krokiMagnetyzacjaUstabilizowana.append(j)
                    break


    # Obliczenia
    def Oblicz(self):

        if len(self.magnetyzacje) != 0:
            self.sredniaMagnetyzacja = (sum(self.magnetyzacje) / len(self.magnetyzacje))
        if len(self.magnetyzacjeUstabilizowana) != 0:
            self.sredniaMagnetyzacjaUstabilizowana = (sum(self.magnetyzacjeUstabilizowana) / len(self.magnetyzacjeUstabilizowana))

        N = len(self.ustabilizowanyHistogramEnergiiX)
        Sxy = 0
        Sx2 = 0
        Sy2 = 0
        Sx = 0
        Sy = 0

        for i in range(0, N):
            Sxy += self.ustabilizowanyHistogramEnergiiX[i]*self.ustabilizowanyHistogramEnergiiY[i]
            Sy2 += self.ustabilizowanyHistogramEnergiiY[i]**2
            Sx2 += self.ustabilizowanyHistogramEnergiiX[i]**2
            Sy += self.ustabilizowanyHistogramEnergiiY[i]
            Sx += self.ustabilizowanyHistogramEnergiiX[i]

        self.a = (N*Sxy - Sx*Sy)/(N*Sx2 - Sx**2)
        self.T= -1/self.a
    

    # ------------------ WYKRESY ------------------

    def WykresEnergiiDemona(self):
        plt.scatter(self.kroki, self.energieDemona, marker='o', s=10, color='b', label='Energia Demona')
        plt.title('Energia Demona w zależności od kroku. ED = {}'.format(self.energiaDemona))
        plt.xlabel('Krok')
        plt.ylabel('Energia Demona')
        plt.legend()
        plt.grid(False)
        plt.show()

    def WykresEnergiiUkladu(self):
        plt.scatter(self.kroki, self.energieUkladu, marker='o', s=10, color='b', label='Energia Układu')
        plt.title('Energia Układu w zależności od kroku. ED = {}'.format(self.energiaDemona))
        plt.xlabel('Krok')
        plt.ylabel('Energia Układu')
        plt.legend()
        plt.grid(False)
        plt.show()

    def UstabilizowanyWykresMagnetyzacji(self):
        plt.scatter(self.krokiMagnetyzacjaUstabilizowana, self.magnetyzacjeUstabilizowana, marker='o', s=5, linestyle='-', color='b', label='Magnetyzacja')
        plt.title('Ustabilizowana magnetyzacja w zależności od kroku. ED = {}'.format(self.energiaDemona))
        plt.xlabel('Krok')
        plt.ylabel('Magnetyzacja')
        plt.legend()
        plt.grid(False)
        plt.show()

    def WykresMagnetyzacji(self):
        plt.scatter(self.kroki, self.magnetyzacje, marker='o', s=5, linestyle='-', color='b', label='Magnetyzacja')
        plt.title('Magnetyzacja w zależności od kroku. ED = {}'.format(self.energiaDemona))
        plt.xlabel('Krok')
        plt.ylabel('Magnetyzacja')
        plt.legend()
        plt.grid(False)
        plt.show()

    def Histogram(self):
        plt.scatter(self.histogramEnergiiX, self.histogramEnergiiY, edgecolor='black')
        plt.title('Wykres punktowy wystąpień Energii Demona. ED = {}'.format(self.energiaDemona))
        plt.xlabel('Energia Demona')
        plt.ylabel('Ilość wystąpień')
        plt.grid(False) 
        plt.show()

    def HistogramStabilizacja(self):
        plt.scatter(self.ustabilizowanyHistogramEnergiiX, self.ustabilizowanyHistogramEnergiiY, edgecolor='black')
        plt.title('Wykres punktowy wystąpień Energii Demona po stabilizacji. ED = {}'.format(self.energiaDemona))
        plt.xlabel('Energia Demona')
        plt.ylabel('Ilość wystąpień po linearyzacji')
        plt.grid(False) 
        plt.show()





def main():
 
    czytaj_z_pliku = False
    
    if czytaj_z_pliku == True:
        with open('init.txt', 'r') as file:
            lines = file.readlines()
        plik = list(map(int, lines[0].split()))

        szerokosc = plik[0]
        wysokosc = plik[1]
        ilosc_skokow = plik[2]+1
        ilosc_demon = plik[3]
        demon = plik[4:]
    
    else:
        szerokosc = 38
        wysokosc = 38
        ilosc_skokow = 20000
        ilosc_demon = 32
        demon = []
        for i in range(1, ilosc_demon+1):
            demon.append( 100  + (i-1)*50 )
        


    uklad = [0] * ilosc_demon

    for i in range(0, ilosc_demon):
        uklad[i] = Uklad(szerokosc, wysokosc, ilosc_skokow, demon[i])

    T = [0 for _ in range(ilosc_demon)]
    m = [0 for _ in range(ilosc_demon)]

    for i in range(0, ilosc_demon):
        
        os.system('cls')
        print("Progres: {} %...".format(int((i+1)*100/ilosc_demon)))

        uklad[i].Strzelaj()
        uklad[i].Stabilizuj(16, 10000, True)     #Argument 1: Tylko te i mniejsze energie Demona zostaną uwzględnione w histogramie
                                                #Argument 2: Od tego kroku włącznie zostanie wyświetlona magnetyzacja
                                                #Argument 3: Czy linearyzacja włączona?
        uklad[i].Oblicz()
                    
        #uklad[i].WykresEnergiiUkladu()
        #uklad[i].WykresEnergiiDemona()
        ##uklad[i].Histogram()
        ##uklad[i].HistogramStabilizacja()
        #uklad[i].WykresMagnetyzacji()
        #uklad[i].UstabilizowanyWykresMagnetyzacji()
        
        m[i] = uklad[i].sredniaMagnetyzacjaUstabilizowana/(wysokosc*szerokosc)
        T[i] = uklad[i].T

    # Wykres 
    plt.scatter(T, m, edgecolor='black')
    plt.title('Wykres m(T)')
    plt.xlabel('Temperatura')
    plt.ylabel('Średnia magnetyzacja')
    plt.grid(True) 
    plt.show()

if __name__ == "__main__":
    main()  