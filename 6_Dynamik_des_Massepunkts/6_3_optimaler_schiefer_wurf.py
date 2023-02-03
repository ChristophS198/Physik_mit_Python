"""Schreiben Sie eine Funktion, die die Flugweite bei einem schiefen Wurf
mit Luftreibung in Abhängigkeit von der Anfangshöhe, dem Abwurfwinkel,
der Abwurfgeschwindigkeit und der sonstigen relevanten Parameter berechnet.
Benutzen Sie diese Funktion, um für den Tischtennisball aus Programm 6.6 den
optimalen Abwurfwinkel in Abhängigkeit von der Anfangsgeschwindigkeit darzustellen."""

from asyncio import events
import numpy as np
import math
import scipy.integrate
import scipy.optimize
import matplotlib as mpl
import matplotlib.pyplot as plt

# Skalierungsfaktoren für den Geschwindigkeitsvektor [1/s]
# und Beschleunigungsvektor [1/s²].
scal_v = 0.1
scal_a = 0.1

# Definieren der Parameter
m = 2.7e-3                          # Masse des Körpers
cwA = 0.45 * math.pi * 20e-3 ** 2   # Produkt aus c_w-Wert und Stirnfläche [m²].
r0 = np.array([0.0, 1.1])           # Anfangsort [m]
g = 9.81                            # Erdbeschleunigung [m/s²]
rho = 1.225                         # Luftdichte [kg/m³]

# Bereich von Abwurfgeschwindigkeit [m/s].
v0_min = 0.1
v0_max = 50

def wurfweite(alpha, r0, v0):

    alpha = math.radians(alpha)

    def F(r, v):
        """Berechne die Kraft in Abhängigkeit von Ort und Geschw."""
        Fr = - 0.5 * rho * cwA * np.linalg.norm(v) * v
        Fg = m * g * np.array([0, -1.0])
        return Fr + Fg

    def dgl(t, u):
        """Funktion der Differentialgleichung:
        u' = f(t, u)"""
        r, v = np.split(u, 2)
        return np.concatenate([v, F(r, v) / m])

    def aufprall(t, u):
        """Ereignisfunktion: liefert einen Vorzeichenwechsel beim
        Auftreffen auf dem Erdboden (y=0)"""
        r, v = np.split(u, 2)
        return r[1]

    aufprall.terminal=True

    # Berechne den Vektor der Anfangsgeschw. [m/s]
    v0 = np.array([v0 * math.cos(alpha), v0 * math.sin(alpha)])
    
    # Festlegen des Anfangszustands
    u0 = np.concatenate((r0, v0))

    # Löse die Bewegungsgleichung bis zum Auftreffen auf der Erde.
    result = scipy.integrate.solve_ivp(dgl, [0, np.inf], u0, events=aufprall)
    r, v = np.split(result.y, 2)

    return -r[0,-1]


# Erzeuge ein Array mit Anfangsgeschwindigkeiten.
v0 = np.linspace(v0_min, v0_max, 100)

# Erzeuge ein leeres Array, das für jede Anfangsgeschwindigkeit
# den optimalen Abwurfwinkel aufnimmt.
alpha = np.empty(v0.size)

# Führe für jeden Wert der Anfangsgeschwindigkeit die
# Optimierung durch. Die Geschwindigkeit muss als zusätzliches
# Argument an die Funktion func übergeben werden. Dies wird mit
# der Option arg=v bewirkt. Da der Winkel bei der Funktion func
# im Gradmaß angegeben wird, ist es sinnvoll, den Suchbereich
# mit bounds=(0, 90) auf den Bereich von 0 bis 90 Grad
# einzuschränken.
for i, v in enumerate(v0):
    result = scipy.optimize.minimize_scalar(wurfweite,bounds=(0, 90),
                                            args=(r0, v),
                                            method='bounded')
    alpha[i] = result.x

# Erzeuge eine Figure und ein Axes-Objekt.
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
ax.set_xlabel('Abwurfgeschwindigkeit [m/s]')
ax.set_ylabel('Optimaler Abwurfwinkel [°]')
ax.grid()

# Plott das Eregbnis.
ax.plot(v0, alpha)

# Zeige die Grafik an.
plt.show()
