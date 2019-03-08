import numpy as np

import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox


def wczytaj_plik_danych(nazwa_pliku):
    """\
    Funkcja wczytuje dane ofert z pliku i zapisuje w liście
    :param nazwa_pliku: nazwa wczytywanego pliku  z ofertami
    :return: lista ofert
    """
    licz_ofert = 0
    lista = []
    with open(nazwa_pliku, "r") as plik_wej:
        for linia in plik_wej:
            linia = linia.strip()
            linia = linia.split(';')
            lista.append(linia)
            licz_ofert += 1
    return lista, licz_ofert


def wyznacz_wekt_sum_wierszy(macierz, wymiar):
    """\
    Funkcja wyznacza wektor składający się z sum poszczególnych wierszy macierzy
    :return:
    :param macierz: macierz na podstawie, której prowadzone są obliczenia
    :param wymiar: określa wymiar macierzy
    :return: zwraca wektor sum
    """
    wektor = np.zeros(wymiar)
    for i in range(wymiar):
        suma = 0
        for j in range(wymiar):
            suma += macierz[i][j]
        wektor[i] = suma
    return wektor


def wyznacz_wekt_sum_kolumn(macierz_porow, liczba_kryt):
    """\
    Funkcja wyznacza wektor składający się z sum poszczególnych kolumn macierzy porównań
    :return:
    :param macierz_porow: macierz_porow porównań parami
    :param liczba_kryt: określa liczbę uwzględnionych kryteriów
    :return: zwraca wektor sum
    """
    wektor = np.zeros(liczba_kryt)
    for j in range(liczba_kryt):
        suma = 0
        for i in range(liczba_kryt):
            suma += macierz_porow[i][j]
        wektor[j] = suma
    return wektor


def normalizuj_macierz(macierz_porow, wektor_sum, liczba_kryt):
    """\
    Funkcja wyznacza macierz znormalizowaną
    :param macierz_porow: macierz porównań parami
    :param wektor_sum: wektor sum poszczególnych kolumn macierzy porównań
    :param liczba_kryt: określa liczbę uwzględnionych kryteriów
    :return: zwraca macierz znormalizowaną
    """
    # normalizacja macierzy poprzez dzielenie poszczególnych elementów przez odpowiadające im obliczone sumy kolumn
    macierz_normal = np.zeros((liczba_kryt, liczba_kryt))
    for j in range(liczba_kryt):
        for i in range(liczba_kryt):
            macierz_normal[i][j] = macierz_porow[i][j] / wektor_sum[j]
    return macierz_normal


def wyznacz_wekt_prioryt(macierz_normal, liczba_kryt):
    """\
    Funkcja wyznacza wektor składający się z obliczonych priorytetów
    :param macierz_normal: macierz znormalizowaną
    :param liczba_kryt: określa liczbę uwzględnionych kryteriów
    :return: zwraca wektor priorytetów
    """
    wektor_prioryt = np.zeros(liczba_kryt)
    for i in range(liczba_kryt):
        suma = 0
        for j in range(liczba_kryt):
            suma += macierz_normal[i][j]
        wektor_prioryt[i] = suma / liczba_kryt
    return wektor_prioryt


def wyznacz_macierz_waz_kolumn(macierz_porow, wektor_prioryt, liczba_kryt):
    """\
    Funkcja wyznacza macierz ważonych kolumn
    :param macierz_porow: macierz_porow porównań parami
    :param wektor_prioryt: wektor priorytetów
    :param liczba_kryt: określa liczbę uwzględnionych kryteriów
    :return: zwraca macierz ważonych kolumn
    """
    macierz_waz_kol = np.zeros((liczba_kryt, liczba_kryt))
    for j in range(liczba_kryt):
        for i in range(liczba_kryt):
            macierz_waz_kol[i][j] = macierz_porow[i][j] * wektor_prioryt[j]
    return macierz_waz_kol


def wyznacz_wekt_waz_sum(macierz_waz, liczba_kryt):
    """\
    Funkcja wyznacza wektor składający się z ważonych sum
    :param macierz_waz: macierz ważonych kolumn
    :param liczba_kryt: określa liczbę uwzględnionych kryteriów
    :return: zwraca wektor ważonych sum poszczególnych wierszy
    """
    wektor_waz_sum = np.zeros((liczba_kryt, 1))
    for i in range(liczba_kryt):
        for j in range(liczba_kryt):
            wektor_waz_sum[i] += macierz_waz[i][j]
    return wektor_waz_sum


def sprawdz_spojnosc_macierzy(wektor_waz_sum, wektor_prioryt, liczba_kryt):
    """\
    Funkcja sprawdza spójność macierzy poprzez wyznaczenie i sprawdzenie współczynników spójności CI i CR
    :param wektor_waz_sum: wektor ważonych sum poszczególnych wierszy
    :param wektor_prioryt: wektor priorytetów
    :param liczba_kryt: określa liczbę uwzględnionych kryteriów
    :return: false - w przypadku braku spójności, true - w przypadku zachowanej spójności
    """
    # obliczenie wspołczynnika lamdba - wsp niespójności
    iloraz = np.zeros((liczba_kryt, 1))
    for i in range(liczba_kryt):
        if wektor_prioryt[i] != 0:
            iloraz[i] = wektor_waz_sum[i] / wektor_prioryt[i]

    suma_ilorazow = 0
    for j in range(liczba_kryt):
        suma_ilorazow += iloraz[j]

    lam_max = suma_ilorazow / liczba_kryt

    # obliczenie indeksu spójności CI (consistent index)
    indeks_spojnosci = (lam_max - liczba_kryt) / (liczba_kryt - 1)

    # oblicznie współczynnika spójności CR = CI / CR
    # wspołczynnik random index
    tablica_ri = np.array([0, 0, 0.58, 0.90, 1.12, 1.24, 1.32, 1.44, 1.45, 1.49, 1.51, 1.53, 1.56, 1.57, 1.59])
    random_index = tablica_ri[liczba_kryt - 1]

    wsp_spojnosci = indeks_spojnosci / random_index
    return indeks_spojnosci, wsp_spojnosci


def main(tablica, wybor_kryt, wektor_dod):
    wektor_sum_gw_osob = []
    wektor_sum_gw_mienie = []
    wektor_licz_rat = []
    wektor_jed_rat = []
    wektor_obszar = []

    # określa liczbę kryteriów
    liczba_kryteriow = 5

    # wczytanie pliku
    lista_ofert, liczba_ofert = wczytaj_plik_danych("przyklad_ofert.txt")

    # liczba porównań wyliczona z liczby kryteriów
    liczba_prownan = (liczba_kryteriow * (liczba_kryteriow - 1)) / 2

    # wektor wartości porównań
    wektor_wej = np.zeros(int(liczba_prownan))

    # pobranie unormowanych ocen z interfejsu użytkownika
    wektor_wej[0] = tablica[0]
    wektor_wej[1] = tablica[1]
    wektor_wej[2] = tablica[2]
    wektor_wej[3] = tablica[3]
    wektor_wej[4] = tablica[4]
    wektor_wej[5] = tablica[5]
    wektor_wej[6] = tablica[6]
    wektor_wej[7] = tablica[7]
    wektor_wej[8] = tablica[8]
    wektor_wej[9] = tablica[9]

    tablica_eliminacja_kryt = wybor_kryt

    # wyznaczenie macierzy porównan parami

    # utworzenie macierzy porównań liczba_kryteriow x liczba_kryteriow
    macierz_porownan = np.zeros((liczba_kryteriow, liczba_kryteriow))

    licznik_kol = 0
    licznik_elem = 0
    for i in range(liczba_kryteriow):
        for j in range(liczba_kryteriow):
            if i == j:
                macierz_porownan[i][j] = 1
            else:
                if j >= licznik_kol:
                    macierz_porownan[i][j] = wektor_wej[licznik_elem]
                    macierz_porownan[j][i] = 1 / macierz_porownan[i][j]
                    licznik_elem += 1
        licznik_kol += 1

    print("\nMacierz porównań")
    print(macierz_porownan)

    # wyznacznie wartości sum poszczególnych kolumn w macierzy porównań
    wektor_sum_kolumn = wyznacz_wekt_sum_kolumn(macierz_porownan, liczba_kryteriow)
    print("\nSumy kolumn macierzy")
    print(wektor_sum_kolumn)

    # normalizacja macierzy poprzez dzielenie poszczególnych elementów przez odpowiadające im obliczone sumy kolumn
    macierz_znormalizowana = normalizuj_macierz(macierz_porownan, wektor_sum_kolumn, liczba_kryteriow)
    print("\nMacierz znormalizowana")
    print(macierz_znormalizowana)

    # metoda przybliżona
    # wyznaczenie wektora priorytetów - obliczenie średniej wartości dla poszczególnych wierszy macierzy znormalizowanej
    wektor_priorytetow = wyznacz_wekt_prioryt(macierz_znormalizowana, liczba_kryteriow)
    print("\nWektor priorytetów")
    print(wektor_priorytetow)

    # wyznaczenie macierzy ważonych kolumn
    macierz_wazonych_kol = wyznacz_macierz_waz_kolumn(macierz_porownan, wektor_priorytetow, liczba_kryteriow)
    print("\nMacierz ważonych kolumn")
    print(macierz_wazonych_kol)

    # wyznaczenie wektora ważonych sum - sumowanie warotości elementów z poszczególnych wierszy
    wektor_wazonych_sum = wyznacz_wekt_waz_sum(macierz_wazonych_kol, liczba_kryteriow)
    print("\nWektor ważonych sum dla kryteriów")
    print(wektor_wazonych_sum)

    wektor_wazonych_sum_kryt = wektor_wazonych_sum

    # obliczenie spójności macierzy
    CR = 0
    indeks_spoj, wspol_spoj = sprawdz_spojnosc_macierzy(wektor_wazonych_sum, wektor_priorytetow, liczba_ofert)
    print("Indeks spójności dla macierzy wynosi ", indeks_spoj)
    print("Współczynnik spójności dla macierzy wynosi ", wspol_spoj)
    if indeks_spoj >= 0.1:
        print("Błąd. Indeks spójności CI nie spełnia warunku CI < 0.1")
    if wspol_spoj >= 0.1:
        CR = wspol_spoj
        print("Błąd. Współczynnik spójności CR nie spełnia warunku CR < 0.1")

    # porownanie ofert według kryteriów
    # ===============================================================================================================
    # porównanie według kryterium suma_gwarancyjna_w_przypadku_szkód_na_osobie
    print("\n\nPorównanie według kryterium suma gwarancyjna w przypadku szkód na osobie")

    #  liczba porównań wyliczona z liczby kryteriów
    # liczba_prownan = (liczba_ofert * (liczba_ofert - 1)) / 2

    # wektor wartości porównań
    # wektor_wej = np.zeros(int(liczba_prownan))

    # utworzenie macierzy porównań liczba_ofert x liczba_ofert
    macierz_porownan = np.zeros((liczba_ofert, liczba_ofert))
    np.fill_diagonal(macierz_porownan, 1)

    k = 1
    roznica = 0
    for i in range(liczba_ofert):
        wart_i = int(lista_ofert[i][1])

        for j in range(k, liczba_ofert):
            wart_j = int(lista_ofert[j][1])
            roznica = int(lista_ofert[j][1]) - int(lista_ofert[i][1])
            if lista_ofert[j][1] == lista_ofert[i][1]:
                macierz_porownan[i][j] = 1
                macierz_porownan[j][i] = 1
            else:
                if wektor_dod[3] == 0:

                    if roznica / wart_i >= 0.4:
                        macierz_porownan[i][j] = 1 / 7
                        macierz_porownan[j][i] = 1 / macierz_porownan[i][j]
                    if roznica / wart_i < 0.4:
                        macierz_porownan[i][j] = 1 / 3
                        macierz_porownan[j][i] = 1 / macierz_porownan[i][j]
                    if roznica / wart_i < -0.4:
                        macierz_porownan[i][j] = 7
                        macierz_porownan[j][i] = 1 / macierz_porownan[i][j]
                    if roznica / wart_i >= -0.4:
                        if roznica / wart_i < 0:
                            macierz_porownan[i][j] = 3
                            macierz_porownan[j][i] = 1 / macierz_porownan[i][j]

                if wektor_dod[3] != 0:

                    if roznica / wart_i >= 0.4:
                        macierz_porownan[i][j] = 1 / 5
                        macierz_porownan[j][i] = 1 / macierz_porownan[i][j]
                    if roznica / wart_i < 0.4:
                        macierz_porownan[i][j] = 1 / 3
                        macierz_porownan[j][i] = 1 / macierz_porownan[i][j]
                    if roznica / wart_i < -0.4:
                        macierz_porownan[i][j] = 5
                        macierz_porownan[j][i] = 1 / macierz_porownan[i][j]
                    if roznica / wart_i >= -0.4:
                        if roznica / wart_i < 0:
                            macierz_porownan[i][j] = 3
                            macierz_porownan[j][i] = 1 / macierz_porownan[i][j]
        k += 1

    print("\nMacierz porównań ofert dla kryterium suma gwarancyjna w przypadku szkód na osobie")
    print(macierz_porownan)

    # wyznacznie wartości sum poszczególnych kolumn w macierzy porównań
    wektor_sum_kolumn = wyznacz_wekt_sum_kolumn(macierz_porownan, liczba_ofert)
    print("\nSumy kolumn macierzy")
    print(wektor_sum_kolumn)

    # normalizacja macierzy poprzez dzielenie poszczególnych elementów przez odpowiadające im obliczone sumy kolumn
    macierz_znormalizowana = normalizuj_macierz(macierz_porownan, wektor_sum_kolumn, liczba_ofert)
    print("\nMacierz znormalizowana")
    print(macierz_znormalizowana)

    # metoda przybliżona
    # wyznaczenie wektora priorytetów - obliczenie średniej wartości dla poszczególnych wierszy macierzy znormalizowanej
    wektor_priorytetow = wyznacz_wekt_prioryt(macierz_znormalizowana, liczba_ofert)
    print("\nWektor priorytetów")
    print(wektor_priorytetow)

    # wyznaczenie macierzy ważonych kolumn
    macierz_wazonych_kol = wyznacz_macierz_waz_kolumn(macierz_porownan, wektor_priorytetow, liczba_ofert)
    print("\nMacierz ważonych kolumn")
    print(macierz_wazonych_kol)

    # wyznaczenie wektora ważonych sum - sumowanie warotości elementów z poszczególnych wierszy
    wektor_wazonych_sum = wyznacz_wekt_waz_sum(macierz_wazonych_kol, liczba_ofert)
    print("\nWektor ważonych sum")
    print(wektor_wazonych_sum)

    # obliczenie spójności macierzy

    indeks_spoj, wspol_spoj = sprawdz_spojnosc_macierzy(wektor_wazonych_sum, wektor_priorytetow, liczba_ofert)
    print("Indeks spójności dla macierzy wynosi ", indeks_spoj)
    print("Współczynnik spójności dla macierzy wynosi ", wspol_spoj)
    if indeks_spoj >= 0.1:
        print("Błąd. Indeks spójności CI nie spełnia warunku CI < 0.1")
    if wspol_spoj >= 0.1:
        print("Błąd. Współczynnik spójności CR nie spełnia warunku CR < 0.1")

    # zapisanie wartości wektora priorytów dla sum gwaratowanych na osobie
    wektor_sum_gw_osob = wektor_priorytetow

    # ==============================================================================================================
    # porównanie według kryterium suma_gwarancyjna_w_przypadku_szkód_na_mieniu
    print("\n\nPorównanie według kryterium suma gwarancyjna w przypadku szkód na mieniu")

    # wektor_sum_gw_mienie = []
    # utworzenie macierzy porównań liczba_ofert x liczba_ofert
    macierz_porownan = np.zeros((liczba_ofert, liczba_ofert))
    np.fill_diagonal(macierz_porownan, 1)

    k = 1
    roznica = 0
    for i in range(liczba_ofert):
        wart_i = int(lista_ofert[i][2])

        for j in range(k, liczba_ofert):
            wart_j = int(lista_ofert[j][2])
            roznica = int(lista_ofert[j][2]) - int(lista_ofert[i][2])
            if lista_ofert[j][2] == lista_ofert[i][2]:
                macierz_porownan[i][j] = 1
                macierz_porownan[j][i] = 1
            else:
                if wektor_dod[3] != 0:

                    if roznica / wart_i >= 0.4:
                        macierz_porownan[i][j] = 1 / 7
                        macierz_porownan[j][i] = 1 / macierz_porownan[i][j]
                    if roznica / wart_i < 0.4:
                        macierz_porownan[i][j] = 1 / 3
                        macierz_porownan[j][i] = 1 / macierz_porownan[i][j]
                    if roznica / wart_i < -0.4:
                        macierz_porownan[i][j] = 7
                        macierz_porownan[j][i] = 1 / macierz_porownan[i][j]
                    if roznica / wart_i >= -0.4:
                        if roznica / wart_i < 0:
                            macierz_porownan[i][j] = 3
                            macierz_porownan[j][i] = 1 / macierz_porownan[i][j]

                if wektor_dod[3] == 0:

                    if roznica / wart_i >= 0.4:
                        macierz_porownan[i][j] = 1 / 5
                        macierz_porownan[j][i] = 1 / macierz_porownan[i][j]
                    if roznica / wart_i < 0.4:
                        macierz_porownan[i][j] = 1 / 3
                        macierz_porownan[j][i] = 1 / macierz_porownan[i][j]
                    if roznica / wart_i < -0.4:
                        macierz_porownan[i][j] = 5
                        macierz_porownan[j][i] = 1 / macierz_porownan[i][j]
                    if roznica / wart_i >= -0.4:
                        if roznica / wart_i < 0:
                            macierz_porownan[i][j] = 3
                            macierz_porownan[j][i] = 1 / macierz_porownan[i][j]


        k += 1

    print("\nMacierz porównań ofert dla kryterium suma gwarancyjna w przypadku szkód na mieniu")
    print(macierz_porownan)

    # wyznacznie wartości sum poszczególnych kolumn w macierzy porównań
    wektor_sum_kolumn = wyznacz_wekt_sum_kolumn(macierz_porownan, liczba_ofert)
    print("\nSumy kolumn macierzy")
    print(wektor_sum_kolumn)

    # normalizacja macierzy poprzez dzielenie poszczególnych elementów przez odpowiadające im obliczone sumy kolumn
    macierz_znormalizowana = normalizuj_macierz(macierz_porownan, wektor_sum_kolumn, liczba_ofert)
    print("\nMacierz znormalizowana")
    print(macierz_znormalizowana)

    # metoda przybliżona
    # wyznaczenie wektora priorytetów - obliczenie średniej wartości dla poszczególnych wierszy macierzy znormalizowanej
    wektor_priorytetow = wyznacz_wekt_prioryt(macierz_znormalizowana, liczba_ofert)
    print("\nWektor priorytetów")
    print(wektor_priorytetow)

    # wyznaczenie macierzy ważonych kolumn
    macierz_wazonych_kol = wyznacz_macierz_waz_kolumn(macierz_porownan, wektor_priorytetow, liczba_ofert)
    print("\nMacierz ważonych kolumn")
    print(macierz_wazonych_kol)

    # wyznaczenie wektora ważonych sum - sumowanie warotości elementów z poszczególnych wierszy
    wektor_wazonych_sum = wyznacz_wekt_waz_sum(macierz_wazonych_kol, liczba_ofert)
    print("\nWektor ważonych sum")
    print(wektor_wazonych_sum)

    # obliczenie spójności macierzy
    indeks_spoj, wspol_spoj = sprawdz_spojnosc_macierzy(wektor_wazonych_sum, wektor_priorytetow, liczba_ofert)
    print("Indeks spójności dla macierzy wynosi ", indeks_spoj)
    print("Współczynnik spójności dla macierzy wynosi ", wspol_spoj)
    if indeks_spoj >= 0.1:
        print("Błąd. Indeks spójności CI nie spełnia warunku CI < 0.1")
    if wspol_spoj >= 0.1:
        print("Błąd. Współczynnik spójności CR nie spełnia warunku CR < 0.1")

    # zapisanie wartości wektora priorytów dla sum gwaratowanych na mieniu
    wektor_sum_gw_mienie = wektor_priorytetow

    # ===============================================================================================================
    # porównanie według kryterium liczba_rat;
    print("\n\nPorównanie według kryterium liczba rat")

    # wektor_licz_rat = []

    macierz_porownan = np.zeros((liczba_ofert, liczba_ofert))
    np.fill_diagonal(macierz_porownan, 1)

    k = 1
    roznica = 0
    for i in range(liczba_ofert):
        wart_i = int(lista_ofert[i][3])

        for j in range(k, liczba_ofert):
            wart_j = int(lista_ofert[j][3])
            roznica = int(lista_ofert[j][3]) - int(lista_ofert[i][3])
            if lista_ofert[j][3] == lista_ofert[i][3]:
                macierz_porownan[i][j] = 1
                macierz_porownan[j][i] = 1
            else:
                if wektor_dod[0] == 0.2:
                    if roznica == 1:
                        macierz_porownan[i][j] = 3
                        macierz_porownan[j][i] = 1 / macierz_porownan[i][j]
                    elif roznica == 2:
                        macierz_porownan[i][j] = 5
                        macierz_porownan[j][i] = 1 / macierz_porownan[i][j]
                    elif roznica > 2:
                        macierz_porownan[i][j] = 7
                        macierz_porownan[j][i] = 1 / macierz_porownan[i][j]
                    else:
                        if roznica == -1:
                            macierz_porownan[i][j] = 1 / 3
                            macierz_porownan[j][i] = 1 / macierz_porownan[i][j]
                        elif roznica == -2:
                            macierz_porownan[i][j] = 1 / 5
                            macierz_porownan[j][i] = 1 / macierz_porownan[i][j]
                        elif roznica < -2:
                            macierz_porownan[i][j] = 1 / 7
                            macierz_porownan[j][i] = 1 / macierz_porownan[i][j]

                # wybór duża liczna rat
                if wektor_dod[0] == 5:
                    if roznica == 1:
                        macierz_porownan[i][j] = 1 / 3
                        macierz_porownan[j][i] = 1 / macierz_porownan[i][j]
                    elif roznica == 2:
                        macierz_porownan[i][j] = 1 / 5
                        macierz_porownan[j][i] = 1 / macierz_porownan[i][j]
                    elif roznica > 2:
                        macierz_porownan[i][j] = 1 / 7
                        macierz_porownan[j][i] = 1 / macierz_porownan[i][j]
                    else:
                        if roznica == -1:
                            macierz_porownan[i][j] = 3
                            macierz_porownan[j][i] = 1 / macierz_porownan[i][j]
                        elif roznica == -2:
                            macierz_porownan[i][j] = 5
                            macierz_porownan[j][i] = 1 / macierz_porownan[i][j]
                        elif roznica < -2:
                            macierz_porownan[i][j] = 7
                            macierz_porownan[j][i] = 1 / macierz_porownan[i][j]
        k += 1

    print("\nMacierz porównań ofert dla kryterium liczba rat")
    print(macierz_porownan)

    # wyznacznie wartości sum poszczególnych kolumn w macierzy porównań
    wektor_sum_kolumn = wyznacz_wekt_sum_kolumn(macierz_porownan, liczba_ofert)
    print("\nSumy kolumn macierzy")
    print(wektor_sum_kolumn)

    # normalizacja macierzy poprzez dzielenie poszczególnych elementów przez odpowiadające im obliczone sumy kolumn
    macierz_znormalizowana = normalizuj_macierz(macierz_porownan, wektor_sum_kolumn, liczba_ofert)
    print("\nMacierz znormalizowana")
    print(macierz_znormalizowana)

    # metoda przybliżona
    # wyznaczenie wektora priorytetów - obliczenie średniej wartości dla poszczególnych wierszy macierzy znormalizowanej
    wektor_priorytetow = wyznacz_wekt_prioryt(macierz_znormalizowana, liczba_ofert)
    print("\nWektor priorytetów")
    print(wektor_priorytetow)

    # wyznaczenie macierzy ważonych kolumn
    macierz_wazonych_kol = wyznacz_macierz_waz_kolumn(macierz_porownan, wektor_priorytetow, liczba_ofert)
    print("\nMacierz ważonych kolumn")
    print(macierz_wazonych_kol)

    # wyznaczenie wektora ważonych sum - sumowanie warotości elementów z poszczególnych wierszy
    wektor_wazonych_sum = wyznacz_wekt_waz_sum(macierz_wazonych_kol, liczba_ofert)
    print("\nWektor ważonych sum")
    print(wektor_wazonych_sum)

    # obliczenie spójności macierzy
    indeks_spoj, wspol_spoj = sprawdz_spojnosc_macierzy(wektor_wazonych_sum, wektor_priorytetow, liczba_ofert)
    print("Indeks spójności dla macierzy wynosi ", indeks_spoj)
    print("Współczynnik spójności dla macierzy wynosi ", wspol_spoj)
    if indeks_spoj >= 0.1:
        print("Błąd. Indeks spójności CI nie spełnia warunku CI < 0.1")
    if wspol_spoj >= 0.1:
        print("Błąd. Współczynnik spójności CR nie spełnia warunku CR < 0.1")

    # zapisanie wartości wektora liczby rat
    wektor_licz_rat = wektor_priorytetow

    # porównanie według kryterium wysokość_jednej_raty

    # wektor_jed_rat = []
    print("\n\nPorównanie według kryterium wysokość jednej raty")

    # wektor_licz_rat = []

    macierz_porownan = np.zeros((liczba_ofert, liczba_ofert))
    np.fill_diagonal(macierz_porownan, 1)

    k = 1
    iloraz = 1
    for i in range(liczba_ofert):
        wart_i = int(lista_ofert[i][4])

        for j in range(k, liczba_ofert):
            wart_j = int(lista_ofert[j][4])
            iloraz = int(lista_ofert[j][4]) / int(lista_ofert[i][4])
            if lista_ofert[j][4] == lista_ofert[i][4]:
                macierz_porownan[i][j] = 1
                macierz_porownan[j][i] = 1
            else:
                # niska rata
                if wektor_dod[1] == 0.2:
                    if iloraz > 1:
                        if iloraz <= 1.5:
                            macierz_porownan[i][j] = 3
                            macierz_porownan[j][i] = 1 / macierz_porownan[i][j]
                        if iloraz > 1.5:
                            if iloraz <= 2:
                                macierz_porownan[i][j] = 5
                                macierz_porownan[j][i] = 1 / macierz_porownan[i][j]
                            if iloraz > 2:
                                if iloraz > 3:
                                    macierz_porownan[i][j] = 9
                                    macierz_porownan[j][i] = 1 / macierz_porownan[i][j]
                                else:
                                    macierz_porownan[i][j] = 7
                                    macierz_porownan[j][i] = 1 / macierz_porownan[i][j]
                    if iloraz < 1:
                        if iloraz > 0.75:
                            macierz_porownan[i][j] = 1 / 3
                            macierz_porownan[j][i] = 1 / macierz_porownan[i][j]
                        else:
                            if iloraz < (1/3):
                                macierz_porownan[i][j] = 1 / 9
                                macierz_porownan[j][i] = 1 / macierz_porownan[i][j]
                            else:
                                if iloraz < 0.5:
                                    macierz_porownan[i][j] = 1 / 7
                                    macierz_porownan[j][i] = 1 / macierz_porownan[i][j]
                                else:
                                    macierz_porownan[i][j] = 1 / 5
                                    macierz_porownan[j][i] = 1 / macierz_porownan[i][j]

                # wybór wysoka rata
                if wektor_dod[1] == 5:
                    if iloraz > 1:
                        if iloraz <= 1.5:
                            macierz_porownan[i][j] = 1 / 3
                            macierz_porownan[j][i] = 1 / macierz_porownan[i][j]
                        if iloraz > 1.5:
                            if iloraz <= 2:
                                macierz_porownan[i][j] = 1 / 5
                                macierz_porownan[j][i] = 1 / macierz_porownan[i][j]
                            if iloraz > 2:
                                if iloraz > 3:
                                    macierz_porownan[i][j] = 1 / 9
                                    macierz_porownan[j][i] = 1 / macierz_porownan[i][j]
                                else:
                                    macierz_porownan[i][j] = 1 / 7
                                    macierz_porownan[j][i] = 1 / macierz_porownan[i][j]
                    if iloraz < 1:
                        if iloraz > 0.75:
                            macierz_porownan[i][j] = 3
                            macierz_porownan[j][i] = 1 / macierz_porownan[i][j]
                        else:
                            if iloraz < (1/3):
                                macierz_porownan[i][j] = 9
                                macierz_porownan[j][i] = 1 / macierz_porownan[i][j]
                            else:
                                if iloraz < 0.5:
                                    macierz_porownan[i][j] = 7
                                    macierz_porownan[j][i] = 1 / macierz_porownan[i][j]
                                else:
                                    macierz_porownan[i][j] = 5
                                    macierz_porownan[j][i] = 1 / macierz_porownan[i][j]
        k += 1

    print("\nMacierz porównań ofert dla kryterium wysokość jednej raty")
    print(macierz_porownan)

    # wyznacznie wartości sum poszczególnych kolumn w macierzy porównań
    wektor_sum_kolumn = wyznacz_wekt_sum_kolumn(macierz_porownan, liczba_ofert)
    print("\nSumy kolumn macierzy")
    print(wektor_sum_kolumn)

    # normalizacja macierzy poprzez dzielenie poszczególnych elementów przez odpowiadające im obliczone sumy kolumn
    macierz_znormalizowana = normalizuj_macierz(macierz_porownan, wektor_sum_kolumn, liczba_ofert)
    print("\nMacierz znormalizowana")
    print(macierz_znormalizowana)

    # metoda przybliżona
    # wyznaczenie wektora priorytetów - obliczenie średniej wartości dla poszczególnych wierszy macierzy znormalizowanej
    wektor_priorytetow = wyznacz_wekt_prioryt(macierz_znormalizowana, liczba_ofert)
    print("\nWektor priorytetów")
    print(wektor_priorytetow)

    # wyznaczenie macierzy ważonych kolumn
    macierz_wazonych_kol = wyznacz_macierz_waz_kolumn(macierz_porownan, wektor_priorytetow, liczba_ofert)
    print("\nMacierz ważonych kolumn")
    print(macierz_wazonych_kol)

    # wyznaczenie wektora ważonych sum - sumowanie warotości elementów z poszczególnych wierszy
    wektor_wazonych_sum = wyznacz_wekt_waz_sum(macierz_wazonych_kol, liczba_ofert)
    print("\nWektor ważonych sum")
    print(wektor_wazonych_sum)

    # obliczenie spójności macierzy
    indeks_spoj, wspol_spoj = sprawdz_spojnosc_macierzy(wektor_wazonych_sum, wektor_priorytetow, liczba_ofert)
    print("Indeks spójności dla macierzy wynosi ", indeks_spoj)
    print("Współczynnik spójności dla macierzy wynosi ", wspol_spoj)
    if indeks_spoj >= 0.1:
        print("Błąd. Indeks spójności CI nie spełnia warunku CI < 0.1")
    if wspol_spoj >= 0.1:
        print("Błąd. Współczynnik spójności CR nie spełnia warunku CR < 0.1")

    # zapisanie wartości wektora liczby rat
    wektor_jed_rat = wektor_priorytetow

    # obszar_obowiązujący
    # wektor_obszar = []
    print("\n\nPorównanie według kryterium obszar obowiązujący")

    # wektor_licz_rat = []
    macierz_porownan = np.zeros((liczba_ofert, liczba_ofert))
    np.fill_diagonal(macierz_porownan, 1)

    k = 1
    for i in range(liczba_ofert):
        wart_i = lista_ofert[i][5]

        for j in range(k, liczba_ofert):
            wart_j = lista_ofert[j][5]
            if lista_ofert[j][5] == lista_ofert[i][5]:
                macierz_porownan[i][j] = 1
                macierz_porownan[j][i] = 1
            else:
                # niska rata
                if wektor_dod[2] == 0:
                    if wart_j == "Polska":
                        macierz_porownan[i][j] = 1
                        macierz_porownan[j][i] = 1 / macierz_porownan[i][j]
                    if wart_j == "UE":
                        macierz_porownan[i][j] = 3
                        macierz_porownan[j][i] = 1 / macierz_porownan[i][j]
                    if wart_j == "UE i poza":
                        macierz_porownan[i][j] = 3
                        macierz_porownan[j][i] = 1 / macierz_porownan[i][j]

                # wybór wysoka rata
                if wektor_dod[2] == 1:
                    if wart_j == "UE":
                        macierz_porownan[i][j] = 1
                        macierz_porownan[j][i] = 1 / macierz_porownan[i][j]
                    if wart_j == "Polska":
                        macierz_porownan[i][j] = 3
                        macierz_porownan[j][i] = 1 / macierz_porownan[i][j]
                    if wart_j == "UE i poza":
                        macierz_porownan[i][j] = 3
                        macierz_porownan[j][i] = 1 / macierz_porownan[i][j]

                if wektor_dod[2] == 5:
                    if wart_j == "UE i poza":
                        macierz_porownan[i][j] = 1
                        macierz_porownan[j][i] = 1 / macierz_porownan[i][j]
                    if wart_j == "Polska":
                        macierz_porownan[i][j] = 3
                        macierz_porownan[j][i] = 1 / macierz_porownan[i][j]
                    if wart_j == "UE":
                        macierz_porownan[i][j] = 3
                        macierz_porownan[j][i] = 1 / macierz_porownan[i][j]

        k += 1

    print("\nMacierz porównań ofert dla kryterium obszar obowiązujący")
    print(macierz_porownan)

    # wyznacznie wartości sum poszczególnych kolumn w macierzy porównań
    wektor_sum_kolumn = wyznacz_wekt_sum_kolumn(macierz_porownan, liczba_ofert)
    print("\nSumy kolumn macierzy")
    print(wektor_sum_kolumn)

    # normalizacja macierzy poprzez dzielenie poszczególnych elementów przez odpowiadające im obliczone sumy kolumn
    macierz_znormalizowana = normalizuj_macierz(macierz_porownan, wektor_sum_kolumn, liczba_ofert)
    print("\nMacierz znormalizowana")
    print(macierz_znormalizowana)

    # metoda przybliżona
    # wyznaczenie wektora priorytetów - obliczenie średniej wartości dla poszczególnych wierszy macierzy znormalizowanej
    wektor_priorytetow = wyznacz_wekt_prioryt(macierz_znormalizowana, liczba_ofert)
    print("\nWektor priorytetów")
    print(wektor_priorytetow)

    # wyznaczenie macierzy ważonych kolumn
    macierz_wazonych_kol = wyznacz_macierz_waz_kolumn(macierz_porownan, wektor_priorytetow, liczba_ofert)
    print("\nMacierz ważonych kolumn")
    print(macierz_wazonych_kol)

    # wyznaczenie wektora ważonych sum - sumowanie warotości elementów z poszczególnych wierszy
    wektor_wazonych_sum = wyznacz_wekt_waz_sum(macierz_wazonych_kol, liczba_ofert)
    print("\nWektor ważonych sum")
    print(wektor_wazonych_sum)

    # obliczenie spójności macierzy
    indeks_spoj, wspol_spoj = sprawdz_spojnosc_macierzy(wektor_wazonych_sum, wektor_priorytetow, liczba_ofert)
    print("Indeks spójności dla macierzy wynosi ", indeks_spoj)
    print("Współczynnik spójności dla macierzy wynosi ", wspol_spoj)
    if indeks_spoj >= 0.1:
        print("Błąd. Indeks spójności CI nie spełnia warunku CI < 0.1")
    if wspol_spoj >= 0.1:
        print("Błąd. Współczynnik spójności CR nie spełnia warunku CR < 0.1")

    # zapisanie wartości wektora liczby rat
    wektor_obszar = wektor_priorytetow

    # utworzenie macierzy z wektorów porównań
    macierz_ranking = np.stack(
        (wektor_sum_gw_osob, wektor_sum_gw_mienie, wektor_licz_rat, wektor_jed_rat, wektor_obszar), axis=-1)
    print("\n\nMacierz dla rankingu końcowego")
    print(macierz_ranking)

    # przemnożenie macierzy rankingu przez wagi kryteriów
    # print(wektor_wazonych_sum_kryt)
    macierz_ranking_tmp = np.zeros((liczba_ofert, liczba_kryteriow))
    for i in range(len(macierz_ranking)):
        for j in range(len(wektor_wazonych_sum_kryt)):
            macierz_ranking_tmp[i][j] = macierz_ranking[i][j] * wektor_wazonych_sum_kryt[j]

    if CR < 0.1:
        macierz_ranking = macierz_ranking_tmp
    else:
        for i in range(len(macierz_ranking)):
            for j in range(len(wektor_wazonych_sum_kryt)):
                macierz_ranking_tmp[i][j] = macierz_ranking[i][j] / 5

    print("\n\nMacierz dla rankingu końcowego z uwzględnieniem wag")
    print(macierz_ranking)

    wektor_sum_wier = wyznacz_wekt_sum_wierszy(macierz_ranking, liczba_ofert)
    print("\n\nWektor sum priorytetów ofert")
    print(wektor_sum_wier.T)

    # znajdź wartość najwięszą w rankingu
    wartosc_mak = 0
    ind_wektora = 0
    for i in range(liczba_ofert):
        if wektor_sum_wier[i] > wartosc_mak:
            wartosc_mak = wektor_sum_wier[i]
            ind_wektora = i

    print("\n\nAlgorytm sugeruje wybranie oferty nr ", ind_wektora + 1)

    return ind_wektora + 1


def center_window(w, h):
    # get screen width and height
    ws = root.winfo_screenwidth()
    hs = root.winfo_screenheight()
    # calculate position x, y
    x = (ws / 2) - (w / 2)
    y = (hs / 2) - (h / 2)
    root.geometry('%dx%d+%d+%d' % (w, h, x, y))


# ======================================================================================================
klawisze = []
klawisze_wybor_kryt = []
root = tk.Tk()

center_window(666, 320)
tk.Tk.title(root, "Aplikacja wspomagania wyboru ubezpieczenia")
tk.Tk.minsize(root, width=760, height=400)
root.withdraw()

com = messagebox.showinfo("Witaj użytkowniku",
                          "Witaj w programie wspomagającym decyzję wyboru ubezpieczenia.\n\n" + \
                          "Aby wybrać odpowiednie ubezpieczenie, uzupełnij stosunek kryteriów " + \
                          "do pozostałych kryteriów, a następnie naciśnij przycisk DALEJ.")
root.wm_deiconify()
kryteria = ["Suma gwarantowana w przypadku szkód na osobie", "Suma gwarantowana w przypadku szkód na mieniu",
            "Liczba rat", "Wysokość jednej raty", "Obszar obowiązujący"]


# Podpiecie klawiszy
def podepnij_klawisze(klawisze, klawisze_wybor_kryt):
    try:
        klawisze.append(float(ca0.get()))
        klawisze.append(float(ca1.get()))
        klawisze.append(float(ca2.get()))
        klawisze.append(float(ca3.get()))
        klawisze.append(float(ca4.get()))
        klawisze.append(float(ca5.get()))
        klawisze.append(float(ca6.get()))
        klawisze.append(float(ca7.get()))
        klawisze.append(float(ca8.get()))
        klawisze.append(float(ca9.get()))

    except:
        com2 = messagebox.showerror("Bład", "Podane wartości nie są liczbami")

    klawisze_wybor_kryt.append(cb_liczba_rat.get())
    klawisze_wybor_kryt.append(cb_wysokosc_raty.get())
    klawisze_wybor_kryt.append(cb_obszar.get())
    klawisze_wybor_kryt.append(cb_gwarancyjna.get())


def skaluj_klawisze_dodatkowe(klawisze_wybor_kryt):
    wartosc_zwr = 1
    dl_wekt = len(klawisze_wybor_kryt)
    wektor_przes = np.zeros(dl_wekt)

    if klawisze_wybor_kryt[0] == "Duża":
        wektor_przes[0] = 5
    elif klawisze_wybor_kryt[0] == "Mała":
        wektor_przes[0] = 0.2
    else:
        com2 = messagebox.showerror("Bład", "Podane wartości są nieprawidłowe.\n\n Popraw liczbę rat.")
        return wektor_przes, wartosc_zwr

    if klawisze_wybor_kryt[1] == "Wysoka":
        wektor_przes[1] = 5
    elif klawisze_wybor_kryt[1] == "Niska":
        wektor_przes[1] = 0.2
    else:
        com2 = messagebox.showerror("Bład", "Podane wartości są nieprawidłowe.\n\n Popraw wysokość raty.")
        return wektor_przes, wartosc_zwr

    if klawisze_wybor_kryt[2] == "Polska":
        wektor_przes[2] = 0
    elif klawisze_wybor_kryt[2] == "UE":
        wektor_przes[2] = 1
    elif klawisze_wybor_kryt[2] == "UE i poza":
        wektor_przes[2] = 5
    else:
        com2 = messagebox.showerror("Bład", "Podane wartości są nieprawidłowe.\n\n Popraw obszar.")
        return wektor_przes, wartosc_zwr

    if klawisze_wybor_kryt[3] == "S. gwarancyjna na osobie":
        wektor_przes[3] = 0
    elif klawisze_wybor_kryt[3] == "S. gwarancyjna na mieniu":
        wektor_przes[3] = 5
    else:
        com2 = messagebox.showerror("Bład", "Podane wartości są nieprawidłowe.\n\n Popraw sumę gwarancyjną.")
        return wektor_przes, wartosc_zwr
    wartosc_zwr = 0
    return wektor_przes, wartosc_zwr


# Przeskalowanie wartosci
def skaluj_klawisze(tablica_klawiszy, klawisze_wybor_kryt):
    podepnij_klawisze(tablica_klawiszy, klawisze_wybor_kryt)
    iterator = 0
    for elem in tablica_klawiszy:
        if elem == 0:
            tablica_klawiszy[iterator] = 1 / 9
        elif elem == 1:
            tablica_klawiszy[iterator] = 1 / 9
        elif elem == 2:
            tablica_klawiszy[iterator] = 1 / 7
        elif elem == 3:
            tablica_klawiszy[iterator] = 1 / 5
        elif elem == 4:
            tablica_klawiszy[iterator] = 1 / 3
        elif elem == 5:
            tablica_klawiszy[iterator] = 1
        elif elem == 6:
            tablica_klawiszy[iterator] = 3
        elif elem == 7:
            tablica_klawiszy[iterator] = 5
        elif elem == 8:
            tablica_klawiszy[iterator] = 7
        elif elem == 9:
            tablica_klawiszy[iterator] = 9
        elif elem == 10:
            tablica_klawiszy[iterator] = 9
        elif elem > 10:
            tablica_klawiszy[iterator] = 9
        else:
            tablica_klawiszy[iterator] = 1 / 9
        iterator += 1


def run():
    skaluj_klawisze(klawisze, klawisze_wybor_kryt)

    [wektor_kl_dod, wynik_skalowania] = skaluj_klawisze_dodatkowe(klawisze_wybor_kryt)

    if wynik_skalowania == 0:
        nr_oferty = main(klawisze, klawisze_wybor_kryt, wektor_kl_dod)
        root.withdraw()
        com3 = messagebox.showinfo("Powodzenie", "Udało się znaleźć ofertę!\nSzczegóły znajdziesz w nowym oknie.")
        root2 = tk.Tk()
        ws = root2.winfo_screenwidth()
        hs = root2.winfo_screenheight()
        w = 330
        h = 50
        # calculate position x, y
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2)
        root2.geometry('%dx%d+%d+%d' % (w, h, x, y))
        tk.Tk.title(root2, "Twoja osobista oferta")
        label_X = tk.Label(root2, text="Algorytm sugeruje wybranie oferty oznaczonej numerem " + str(nr_oferty))
        label_X.grid(column=0, row=0)
        root.destroy()
        btn_EXIT = tk.Button(root2, text="EXIT", command=quit)
        btn_EXIT.grid(column=0, row=1)
        klawisze.clear()
        klawisze_wybor_kryt.clear()
    else:
        klawisze.clear()
        klawisze_wybor_kryt.clear()


ca0 = IntVar()
ca1 = tk.IntVar()
ca2 = tk.IntVar()
ca3 = tk.IntVar()
ca4 = tk.IntVar()
ca5 = tk.IntVar()
ca6 = tk.IntVar()
ca7 = tk.IntVar()
ca8 = tk.IntVar()
ca9 = tk.IntVar()

ca0 = ttk.Combobox(root, values=("0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"), width=5)
ca0.grid(column=2, row=0)
ca0.set(1)
ca1 = ttk.Combobox(root, values=("0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"), width=5)
ca1.grid(column=2, row=1)
ca1.set(1)
ca2 = ttk.Combobox(root, values=("0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"), width=5)
ca2.grid(column=2, row=2)
ca2.set(1)
ca3 = ttk.Combobox(root, values=("0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"), width=5)
ca3.grid(column=2, row=3)
ca3.set(1)
ca4 = ttk.Combobox(root, values=("0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"), width=5)
ca4.grid(column=2, row=4)
ca4.set(1)
ca5 = ttk.Combobox(root, values=("0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"), width=5)
ca5.grid(column=2, row=5)
ca5.set(1)
ca6 = ttk.Combobox(root, values=("0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"), width=5)
ca6.grid(column=2, row=6)
ca6.set(1)
ca7 = ttk.Combobox(root, values=("0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"), width=5)
ca7.grid(column=2, row=7)
ca7.set(1)
ca8 = ttk.Combobox(root, values=("0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"), width=5)
ca8.grid(column=2, row=8)
ca8.set(1)
ca9 = ttk.Combobox(root, values=("0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"), width=5)
ca9.grid(column=2, row=9)
ca9.set(1)
"""

ca0 = tk.Spinbox(root, from_=0, to=10,width=5)
ca0.grid(column = 2, row = 0)
ca1 = tk.Spinbox(root, from_=0, to=10,width=5)
ca1.grid(column = 2, row = 1)
ca2 = tk.Spinbox(root, from_=0, to=10,width=5)
ca2.grid(column = 2, row = 2)
ca3 = tk.Spinbox(root, from_=0, to=10,width=5)
ca3.grid(column = 2, row = 3)
ca4 = tk.Spinbox(root, from_=0, to=10,width=5)
ca4.grid(column = 2, row = 4)
ca5 = tk.Spinbox(root, from_=0, to=10,width=5)
ca5.grid(column = 2, row = 5)
ca6 = tk.Spinbox(root, from_=0, to=10,width=5)
ca6.grid(column = 2, row = 6)
ca7 = tk.Spinbox(root, from_=0, to=10,width=5)
ca7.grid(column = 2, row = 7)
ca8 = tk.Spinbox(root, from_=0, to=10,width=5)
ca8.grid(column = 2, row = 8)
ca9 = tk.Spinbox(root, from_=0, to=10,width=5)
ca9.grid(column = 2, row = 9)
"""
# Nazwy kryteriów jako label
for i in range(4):
    kryt_label_0 = tk.Label(root, text=kryteria[0], borderwidth=5).grid(column=0, row=i)
    # ca = ttk.Combobox(root, values=("0","1", "2", "3", "4", "5","6","7","8","9","10"),width=5).grid(column = 1, row = i)
    # print(i)
    if i < 4:
        kryt_label_5 = tk.Label(root, text=kryteria[i + 1], borderwidth=5).grid(column=4, row=i)

for i in range(3):
    kryt_label_1 = tk.Label(root, text=kryteria[1], borderwidth=5).grid(column=0, row=i + 4)
    # cb = ttk.Combobox(root, values=("0","1", "2", "3", "4", "5","6","7","8","9","10"),width=5).grid(column = 1, row = i+5)
    # print(i)
    if i < 3:
        kryt_label_6 = tk.Label(root, text=kryteria[i + 2], borderwidth=5).grid(column=4, row=i + 4)

for i in range(2):
    kryt_label_2 = tk.Label(root, text=kryteria[2], borderwidth=5).grid(column=0, row=i + 4 + 3)
    # cc = ttk.Combobox(root, values=("0","1", "2", "3", "4", "5","6","7","8","9","10"),width=5).grid(column = 1, row = i+5+4)
    if i < 2:
        kryt_label_7 = tk.Label(root, text=kryteria[i + 3], borderwidth=5).grid(column=4, row=i + 4 + 3)

for i in range(1):
    kryt_label_3 = tk.Label(root, text=kryteria[3], borderwidth=5).grid(column=0, row=i + 4 + 3 + 2)
    # cd = ttk.Combobox(root, values=("0","1", "2", "3", "4", "5","6","7","8","9","10"),width=5).grid(column = 1, row = i+5+4+3)
    if i < 1:
        kryt_label_8 = tk.Label(root, text=kryteria[i + 4], borderwidth=5).grid(column=4, row=i + 4 + 3 + 2)

for i in range(0):
    kryt_label_4 = tk.Label(root, text=kryteria[4], borderwidth=5).grid(column=0, row=i + 4 + 3 + 2 + 1)
    # ce = ttk.Combobox(root, values=("0,""1", "2", "3", "4", "5","6","7","8","9","10"),width=5).grid(column = 1, row = i+5+4+3+2)
    if i < 0:
        kryt_label_9 = tk.Label(root, text=kryteria[i + 5], borderwidth=5).grid(column=4, row=i + 4 + 3 + 2 + 1)

# zakres skali jako label
for i in range(10):
    bb = tk.Label(root, text="0", borderwidth=5).grid(column=1, row=i)
    dd = tk.Label(root, text="10", borderwidth=5).grid(column=3, row=i)

name_blank_line = tk.Label(root, text="", borderwidth=5).grid(column=0, row=11)
name_label = tk.Label(root, text="Proszę wybrać priorytety kryteriów", borderwidth=5).grid(column=0, row=12)
name_label_liczba_rat = tk.Label(root, text="Liczba rat", borderwidth=5).grid(column=1, row=12)
name_label_wysokosc_rat = tk.Label(root, text="Wyskość raty", borderwidth=5).grid(column=2, row=12)
name_label_obszar = tk.Label(root, text="Obszar", borderwidth=5).grid(column=3, row=12)
name_label_gwarancyjna = tk.Label(root, text="Suma gwarancyjna", borderwidth=5).grid(column=4, row=12)

cb_liczba_rat = tk.StringVar()
cb_wysokosc_raty = tk.StringVar()
cb_obszar = tk.StringVar()
cb_gwarancyjna = tk.StringVar()

cb_liczba_rat = ttk.Combobox(root, values=("Duża", "Mała"), width=5)
cb_liczba_rat.grid(column=1, row=13)
cb_liczba_rat.set("Duża")
cb_wysokosc_raty = ttk.Combobox(root, values=("Wysoka", "Niska"), width=7)
cb_wysokosc_raty.grid(column=2, row=13)
cb_wysokosc_raty.set("Wysoka")
cb_obszar = ttk.Combobox(root, values=("Polska", "UE", "UE i poza"), width=5)
cb_obszar.grid(column=3, row=13)
cb_obszar.set("UE")
cb_gwarancyjna = ttk.Combobox(root, values=("S. gwarancyjna na osobie", "S. gwarancyjna na mieniu"), width=25)
cb_gwarancyjna.grid(column=4, row=13)
cb_gwarancyjna.set("S. gwarancyjna na osobie")

przycisk_dalej = tk.Button(root, text="DALEJ", command=run)
przycisk_dalej.grid(column=2, row=14)
root.mainloop()

"""
if __name__ == '__main__':
    print("Program do wspomagania decyzji w wyborze ubezpieczenia\n")
    main()
"""
