"""Resonanzkurve. Ein mechanisches System wurde mit unterschiedlichen
Frequenzen 𝑓 angeregt und die Amplitude 𝐴 der erzwungenen Schwingung gemessen"""
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import scipy.optimize



f = np.array([0.2, 0.5, 0.57, 0.63, 0.67, 0.71, 0.8, 1.0, 1.33]) # angeregte Frequenz [Hz]
A = np.array([0.84, 1.42, 1.8, 2.1, 2.22, 2.06, 1.45, 0.64, 0.3]) # Amplitude [cm]

d_A = np.array([0.04, 0.07, 0.09, 0.11, 0.11, 0.10, 0.08, 0.03, 0.02]) # Messungenauigkeit Amplitude [cm]


# Funktion, welche die Amplitude des schwingungsfaehigen Systems
# in Abhängigkeit der anregenden Frequenz und 3 Paramtern zurückgibt
def func(f, A_0, f_0, delta):
    f2 = f_0**2
    return A_0 * f2 / np.sqrt((f**2-f2)**2 + (delta*f/np.pi)**2)

# Optimiere die Funktion
popt, pcov = scipy.optimize.curve_fit(func, f, A, [0.8, 1.0, 2.0])

A_0_opt, f_0_opt, delta_opt = popt

fig = plt.figure()
ax = fig.add_subplot(1,1,1)
ax.set_ylabel("Amplitude [cm]")
ax.set_xlabel("Frequenz [Hz]")
ax.grid()

# Plotte die Funktion mit optimierten Parametern
f_fit = np.linspace(np.min(f), np.max(f), 500)
A_fit = func(f_fit, A_0_opt, f_0_opt, delta_opt)
ax.plot(f_fit, A_fit, "-", zorder=2)

# Plotte die Messwerte
ax.errorbar(f, A, yerr=d_A, fmt=".", capsize=2, zorder=1)

plt.show()