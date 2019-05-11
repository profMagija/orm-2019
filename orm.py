import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def majoriraj(x):
	"""majora dati nenegativni niz gresaka.

	>>> majoriraj(0.32)
	0.4
	>>> majoriraj(0.123)
	0.13
	"""
	st = -np.floor(np.log10(x))
	norm = x * (10**st)
	maj_norm = np.where(norm >= 2, np.ceil(norm), np.ceil(norm * 10) / 10)
	maj = np.where(x == 0, 0, maj_norm / (10**st))
	return maj

# putanja do podataka
# podaci imaju sledece kolone:
#   - u         : napon u voltima
#   - i         : struja u miliamperima
#   - t         : temperatura u stepenima celzijusa
#   - delta_t   : apsolutna greska temperature 
DATA_PATH = "podaci.csv"
C_TO_K = 274.15

# Ucitavamo podatke
podaci = pd.read_csv(DATA_PATH)

# pretvaramo struju iz miliampera u ampere
podaci.i = podaci.i / 1000

# pretvaramo temperaturu iz stepena C u K
podaci.t = C_TO_K + podaci.t

# greska napona je 1% + 3dg (0.3 V)
delta_u = majoriraj(0.01 * podaci.u + 0.3)

# greska struje je 1.5% + 3gd (0.3 mA = 0.0003 A)
delta_i = majoriraj(0.015 * podaci.i + 0.0003)

# P = U * I
p = podaci.u * podaci.i

# relativne greske struje i napona
rel_u = delta_u / podaci.u
rel_i = delta_i / podaci.i

# relativna greska proizvoda je zbir relativnih gresaka
rel_p = rel_u + rel_i
delta_p = majoriraj(rel_p * p)

################## NACRTAJ GRAFIK P(T) ########################

plt.title('Zavisnost temperature od snage') # naslov grafika
plt.xlabel('P [W]') # oznaka x-ose
plt.ylabel('T [K]') # oznaka y-ose

# plt.errorbar crta grafik sa oznakama gresaka
# plt.errorbar(podaci_x, podaci_y, greske_y, greske_x, format)
plt.errorbar(p, podaci.t, podaci.delta_t, delta_p, '.')
plt.savefig('grafik1.png')
plt.show()

##################### LINEARIZACIJA ZAVISNOSTI #########################
# eksponencijalnu zavisnost mozemo linearizovati tako sto logaritmujemo
# obe strane jednacine

#    P  =    T^n      *  B
# ln(P) = ln(T^n)     + ln(B)
# ln(P) =   n * ln(T) + ln(B)
#    y  =   n *   x   + k     <--- linearna funkcija

# y -> ln(P)
# x -> ln(T)
# koef pravca -> n
# odsecak -> ln(B)

# najpre logaritmujemo P i T
ln_p = np.log(p)
ln_t = np.log(podaci.t)

# racunamo apsolutnu gresku logaritma kao
# ∆ln(x) = ∆x / x
delta_ln_p = majoriraj(delta_p / p)
delta_ln_t = majoriraj(podaci.delta_t / podaci.t)


##############  LINEARNO FITOVANJE  ################


# polyfit nam vraca niz koeficijenata u fitovanom polinomu.
# u slucaju linearnog fita (stepen == 1) to ce biti
#    - koef pravca kao prvi element
#    - odsecak na y-osi kao drugi element

# u nasem slucaju,
#    koef pravca = n
#    odsecak = ln(B)

n, ln_b = np.polyfit(ln_t, ln_p, 1)
# b = np.exp(ln_b)
# exp je eksponencijalna funkcija e^x
print(' n =', n)
print(' B =', np.exp(ln_b))

######## NACRTAJ GRAFIK ln(P) od ln(T) ########
# cuvamo ga kao 'grafik2.png'

plt.title('Zavisnost ln(P) od ln(T)')
plt.xlabel('ln T')
plt.ylabel('ln P')
plt.errorbar(ln_t, ln_p, delta_ln_p, delta_ln_t, '.')

# linearnu funkciju crtamo tako sto uzmemo bilo koje podatke za x
# a y izracunamo kao y = n * x + k (linearna funkcija)
# u nasem slucaju:
#   - x = ln_t
#   - n = n
#   - k = ln_b
#   - pa je stoga y = n*ln_t + b
plt.plot(ln_t, n * ln_t + ln_b, 'r-')
plt.savefig('grafik2.png')
plt.show()


