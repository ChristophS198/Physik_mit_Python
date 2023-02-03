"""Flugbahn einer Kanone unter Berücksichtigung
der Erddrehung (Coriolis-Kraft). Osten entspricht x-, 
Norden y- und z-Richtung nach oben (Höhe)"""

import numpy as np
import math
import scipy.integrate
import matplotlib.pyplot as plt

# Definieren der Parameter
m = 14.5                        # Masse des Körpers [kg]
cwA = 0.45 * math.pi * 8e-2**2  # Produkt aus c_w-Wert und Strinfläche [m²]
g = 9.81                        # Erdbeschleunigung [m/s²]
alpha = math.radians(42.0)      # Abschusswinkel [rad]
r0 = np.array([0, 0, 10.0])     # Anfangsort [m]
rho = 1.225                     # Luftdichte [kg/m³]
v0 = 150.0                      # Mündungsgeschwindigkeit [m/s]
theta = math.radians(49.4)      # Breitegrad (in etwa Nürnber) [rad]
omega = 7.292e-5                # Betrag der Winkelgeschwindigkeit der Erde (2*pi/(23h+56min)) [rad/s]

# Berechne den Vektor der Anfangsgeschwindigkeit [m/s].
# Wir schießen in östliche Richtung (x)
v0 = np.array([v0 * math.cos(alpha), 0, v0 * math.sin(alpha)])

# Vektor der Winkelgeschwindigkeit [rad/s]
omega = omega * np.array([0, math.cos(theta), math.sin(theta)])

def F(r, v):
    """Vektor der Kraft als Funktion von Ort r und
    Geschwindigkeit v."""
    Fg = m * g * np.array([0, 0, -1.0])
    Fr = - 0.5 * rho * cwA * np.linalg.norm(v) * v
    Fc = - 2.0 * m * np.cross(omega, v)
    return Fg + Fr + Fc

def dgl(t, u):
    r, v = np.split(u, 2)
    return np.concatenate([v, F(r,v) / m])

def aufprall(t, u):
    """Ereignisfunktion: liefert einen Vorzeichenwechsel beim
    Auftreffen auf dem Erdboden (z=0)."""
    r, v = np.split(u,2)
    return r[2]

# Beende die Simulation beim Auftreten des Ereignisses.
aufprall.terminal=True

# Lege den Zustandsvektor zum Zeitpunkt t=0 fest
u0 = np.concatenate((r0, v0))

# Löse die Bewegungsgleichung bis zum Auftreffen auf der Erde.
result = scipy.integrate.solve_ivp(dgl, [0, np.inf], u0, events=aufprall, dense_output=True)

t_s = result.t
r_s, v_s = np.split(result.y,2)

# Interpoliere die Bahnkurve in dem Zeitintervall bis zum Aufprall
t = np.linspace(0, np.max(t_s), 1000)
r, v = np.split(result.sol(t),2)

# Plotte die Bahnkurve in der x-y-Ebene und x-z-Ebene
fig = plt.figure()

# PLotte die Bahnkurve in der Seitenansicht
ax1 = fig.add_subplot(2,1,1)
ax1.tick_params(labelbottom=False)
ax1.set_ylabel('z [m]')
ax1.set_aspect('equal')
ax1.grid()
ax1.plot(r_s[0,:], r_s[2,:], '.b')
ax1.plot(r[0], r[2], '-b')

# Plotte die Bahnkurve in der Aufsicht
ax2 = fig.add_subplot(2,1,2)
ax2.set_xlabel('x [m]')
ax2.set_ylabel('y [m]')
ax2.grid()
ax2.plot(r_s[0], r_s[1], '.b')
ax2.plot(r[0], r[1], '-b')

# Zeige die Grafik an
plt.show()