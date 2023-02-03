"""Abwandlung der Hundekurve bei der der Mensch auf einer Kreisbahn 
mit konstanter Geschwindigkeit geht"""

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.animation

# Definieren der Anfangsposition [m]
r0_mensch = np.array([0.0, 0.0]) 
r0_hund = np.array([0.0, 10.0])

# Betrag der Geschwindigkeit von Hund und Mensch [m/s]
v0_mensch = 2.0
v0_hund = 3.0

# Radius der Kreibahn des Menschen [m]
R = 20.0

# Maximale Simulationsdauer [s]
t_max = 500

# Zeitschrittweite [s]
dt = 0.01

# Brich die Simulation ab, wenn der Abstand von Hund 
# und Mensch kleiner epsilon ist
epsilon = v0_hund * dt

# Anlegen der Listen für die Simulationsergebnisse
t = [0]
r_mensch = [r0_mensch]
r_hund = [r0_hund]
v_hund = []

def pos_mensch(r0, R, v, dt):
    """Gibt die Position des Menschen bei Bewegung auf einer Kreisbahn mit
    Radius R und Geschwindigkeit v zurück. Anfangsposition ist r0 zum Zeitpunkt 0"""
    # Berechne die Winkelgeschwindigkeit [1/s]
    omega = v / R 

    # Bestimmen der Position des Menschen auf seiner Kreisbahn
    drx = R * np.cos(omega * dt) + r0[0]
    dry = R * np.sin(omega * dt) + r0[1]

    # Zurückgeben der aktuellen Position
    return np.array([drx, dry])

# Simulationsschleife
while True:
    # Berechne die Gesdhwindigkeit des Hundes
    delta_r = r_mensch[-1] - r_hund[-1]
    v_hund.append(v0_hund * delta_r / np.linalg.norm(delta_r))

    # Überprüfen des Abbruchkriteriums
    if (t[-1] > t_max) or (np.linalg.norm(delta_r) < epsilon):
        break

    # Berechne die neuen Position von Hund und Mensch
    r_mensch_tmp = pos_mensch(r0_mensch, R, v0_mensch, t[-1])
    r_mensch.append(r_mensch_tmp)
    r_hund.append(r_hund[-1] + v_hund[-1] * dt)

    # Neuen Zeitpunkt bestimmen
    t.append(t[-1] + dt)

# Umwandeln der Listen zu numpy Arrays
r_mensch = np.array(r_mensch)
r_hund = np.array(r_hund)
t = np.array(t)
v_hund = np.array(v_hund)

# Bestimmen der Geschwindigkeit des Menschen: omega * R * [-sin(omega*t), cos(omega*t)]
v_mensch = v0_mensch * np.array([r_mensch[:,0], r_mensch[:,1]])

# Berechne den Beschleunigungsvektor des Hundes für alle
# Zeitpunkte. Achtung! Das Array a_hund hat eine Zeile
# weniger, als es Zeitpunkte gibt
a_hund = (v_hund[1:,:] - v_hund[:-1,:]) / dt 

# Erzeuge eine Figure und ein Axis-Object
fig = plt.figure()
ax = fig.add_subplot(1,1,1)
ax.set_xlabel("x [m]")
ax.set_ylabel("y [m]")
# ax.set_xlim(-0.2, 15)
# ax.set_ylim(-0.2, 10)
ax.set_aspect('equal')
ax.grid()

# Erzeuge den Plot für die Kreisbewegung des Menschen
T = 2 * np.pi * R / v0_mensch
t_umlauf = np.linspace(0, T, 500)
r_mensch_umlauf = pos_mensch(r0_mensch, R, v0_mensch, t_umlauf)
plot, = ax.plot(r_mensch_umlauf[0,:],r_mensch_umlauf[1,:], color='black')

# Erzeuge 2 leere Punktplots zum Anzeigen der aktuellen Positionen von Hund und Mensch
hund, = ax.plot([], [], 'o', color='blue')
mensch, = ax.plot([], [], 'o', color='red')

# Erzeuge 2 Pfeile
style = mpl.patches.ArrowStyle.Simple(head_length=6, head_width=3)
arrow_v = mpl.patches.FancyArrowPatch((0, 0), (0, 0), color='red', arrowstyle=style)
arrow_a = mpl.patches.FancyArrowPatch((0, 0), (0, 0), color='black', arrowstyle=style)

# Füge die Grafikobjekte zur Axes hinzu
ax.add_artist(arrow_v)
ax.add_artist(arrow_a)

def update(n):
    # Lege den Anfangs- und den Zielpunkt des
    # Geschwindigkeitspfeiles fest
    arrow_v.set_positions(r_hund[n], r_hund[n]+v_hund[n])

    # Lege den Anfangs- und den Zielpunkt des
    # Beschleunigugnspfeiles fest
    if n < a_hund.shape[0]:
        arrow_a.set_positions(r_hund[n], r_hund[n]+a_hund[n])

    # Aktualisiere die Position von Hund und Mensch
    hund.set_data(r_hund[n])
    mensch.set_data(r_mensch[n])

    return hund, mensch, arrow_v, arrow_a, plot

# Erzeuge das Animationsobjekt und starte die Animation
ani = mpl.animation.FuncAnimation(fig, update, interval=30, frames=t.size, blit=True)

plt.show()