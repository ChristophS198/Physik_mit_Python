"""Berechne """
import numpy as np
import math
import scipy.integrate
import matplotlib as mpl
import matplotlib.pyplot as plt

# Gemessene Schwingungsdauern [s].
T = np.array([2.05, 1.99, 2.06, 1.97, 2.01,
                2.00, 2.03, 1.97, 2.02, 1.96])

E_T = np.mean(T)
sigma = np.std(T, ddof=1)
delta_T = sigma / np.sqrt(T.size)

print(f"Mittelwert:           <T> = {E_T:.2f} s")
print(f"Standardabweichung: sigma = {sigma:.2f} s" )
print(f"Mittlerer Fehler: Delta T = {delta_T:.2f} s")

lower_limit = 1.95
upper_limit = 2.05

def gauss(x, sigma, mean):
    a = 1 / (np.sqrt(2*math.pi)*sigma)
    return a * np.exp(- (x-mean)**2 / (2*sigma**2))

def num_integration(f, lower, upper, step):
    sum = 0
    i = lower+step/2.0
    while i < upper:
        sum += f(i)*step
        i += step
    return sum

# Use mean and sigma from above calculations
def f_special(x):
    a = 1 / (np.sqrt(2*math.pi)*sigma)
    return a * np.exp(- (x-E_T)**2 / (2*sigma**2))

integral_value = num_integration(f_special, lower_limit, upper_limit, 0.01)
p, err = scipy.integrate.quad(f_special, lower_limit, upper_limit)
print(f"Portion betwenn [{lower_limit:.2f}, {upper_limit:.2f}]: {integral_value:.3f}")
print(f"Ergebnis der Integration: {p}")
print(f"Fehler der Integration: {err}")
integral_value = num_integration(f_special, lower_limit, upper_limit, 0.01)

x = np.linspace(0, 4, 500)
fig = plt.figure()
ax = fig.add_subplot(1,1,1)
# ax.set_ylim(0.0, 8)
ax.set_xlim(1.5, 2.5)

ax.plot(x, f_special(x))

plt.show()