"""Berechnung und Darstellung der Flugbahn beim schiefen Wurf mit
Anfangshöhe in Abhängigkeit vom Abwurfwinkel"""

import numpy as np
import matplotlib.pyplot as plt
import math


# Definieren der Anfangsparameter
h0 = 10.0           # Anfangshöhe [m]
alpha_deg = 25.0    # Abwurfwinkel [°]
v_ab = 5.0          # Abwurfgeschwindigkeit [m/s]
g = 9.81            # Schwerebeschleunigung [m/s²]

# Umrechnen des Winkels in Bogenmaß
alpha = math.radians(alpha_deg)

# Berechnen der Anfangsposition und -geschwindigkeit beim Abwurf
v0 = v_ab * np.array([np.cos(alpha), np.sin(alpha)])

def schiefer_wurf(phi, h, v, dt):
    """Berechnet die Position des Massepunktes ausgehend von der Starthöhe
    h, Abwurfwinkel phi, Abwurfgeschwindigkeit (Norm) und der vergangenen Zeit"""
    # Umrechnen des Winkels in Bogenmaß
    alpha = math.radians(phi)
    print(alpha)
    # Berechnen der Anfangsposition und -geschwindigkeit beim Abwurf
    v0 = v * np.array([np.cos(alpha), np.sin(alpha)])
    r0 = np.array([0.0, h])

    a = np.array([0.0, -g])

    return r0 + v0 * dt  + .5 * a * dt**2

# Berechne den Auftreffzeitpunkt auf dem Boden (y = 0)
t_end = v0[1] / g + math.sqrt((v0[1] / g) ** 2 + 2 * h0 / g)

# Erzeuge ein 1000 x 1 - Array mit Zeitpunkten.
t = np.linspace(0, t_end, 1000)
t = t.reshape(-1,1)

# Auswerten der Position zu den erstellten Zeitpunkten
r = schiefer_wurf(alpha_deg, h0, v_ab, t)

# Erzeugen des Plots
fig = plt.figure()
ax = fig.add_subplot(1,1,1)
ax.set_xlabel('x [m]')
ax.set_ylabel('y [m]')
ax.grid()

plot = ax.plot(r[:,0], r[:,1])

plt.show()
