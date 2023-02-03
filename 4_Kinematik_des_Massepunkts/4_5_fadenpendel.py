"""Simulation der Bewegung eines Fadenpendels
r(t) = L * [sin(phi(t)), -cos(phi(t))], wobei von kleinen 
Maximalauslenkungen phi0 und der deshalb guten Approximation
phi(t) = phi0 * cos(omega*t) mit omega = 2*pi/T ausgeht"""

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.animation

# Definieren der Parameter
L = 3.0         # Länge des Fadenpendels [m]
T = 3.47        # Periode einer Pendelbewegung [s]
phi0_deg = 10.0 # Maximalauslenkung des Pendels [°]
phi0_rad = np.radians(phi0_deg)

def pendel_position(L, phi0, T, t):
    """Gibt die x,y Koordinaten eines Pendels der Länge L 
    mit kleiner Maximalauslenkung phi0, Periodendauer T zum
    Zeitpunkt t zurück"""
    omega = 2 * np.pi / T
    phi = phi0 * np.cos(omega * t)
    x = L * np.sin(phi)
    y = - L * np.cos(phi)
    return np.array([x, y])

def pendel_geschwindigkeit(L, phi0, T, t):
    """Gibt den Geschwindigkeitsvektor der Pendelbewegung
    zu einem Zeitpunkt t zurück"""
    omega = 2 * np.pi / T
    cos_phi = phi0 * np.cos(omega * t)
    sin_phi = phi0 * np.sin(omega * t)
    x = - L * omega * np.cos(cos_phi) * sin_phi
    y = - L * omega * np.sin(cos_phi) * sin_phi
    return np.array([x, y])

# Erstelle Zeitarray für eine Periode
t = np.linspace(0, T, 1000)

# Berechne die Position des Pendels zu den Zeitpunkten
r = pendel_position(L, phi0_rad, T, t)

# Berechne die Geschwindigkeit des Pendels (analytisch)
v = pendel_geschwindigkeit(L, phi0_rad, T, t)

# Approximiere die Beschleunigung des Pendels
a = (v[:,1:] - v[:,:-1]) / (t[1] - t[0])

# Erstelle die Figure
fig = plt.figure()
ax = fig.add_subplot(1,1,1)
ax.set_xlabel('x [m]')
ax.set_ylabel('y [m]')
ax.set_xlim(-L*np.sin(phi0_rad)-L/3, L*np.sin(phi0_rad)+L/3)
ax.set_ylim(-L-L/8, 0.3)
ax.set_aspect('equal')
ax.grid()

# Erzeuge Plots für den Faden und die Position des Endpunktes
faden, = ax.plot([], [])
ende, = ax.plot([], [], 'o', color='red')

# Erzeuge 2 Pfeile für Geschwindigkeit und Beschleunigung
style = mpl.patches.ArrowStyle.Simple(head_length=6, head_width=3)
arrow_v = mpl.patches.FancyArrowPatch((0, 0), (0, 0), color='red', arrowstyle=style)
arrow_a = mpl.patches.FancyArrowPatch((0, 0), (0, 0), color='black', arrowstyle=style)

# Füge die Grafikobjekte zur Axes hinzu
ax.add_artist(arrow_v)
ax.add_artist(arrow_a)

def update(n):
    # Aktualisiere die Plots
    faden.set_data([0, r[0,n]], [0, r[1,n]])
    ende.set_data(r[:,n])

    # Aktualisiere die Pfeile
    arrow_v.set_positions(r[:,n], r[:,n] + v[:,n])
    if n < a.shape[1]:
        arrow_a.set_positions(r[:,n], r[:,n] + a[:,n])
    return faden, ende, arrow_a, arrow_v

# Erzeuge das Animationsobjekt
ani = mpl.animation.FuncAnimation(fig, update, interval=30, frames=t.size, blit=True)

plt.show()