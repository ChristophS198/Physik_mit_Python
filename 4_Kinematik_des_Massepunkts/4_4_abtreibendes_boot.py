"""Simulation eines Bootes, welches mit konstanter Geschwindigkeit
auf ein ruhendes Ziel zusteuert. Dabei wird es durch eine Strömung
mit konstanter Geschwindigkeit abgetrieben und der Bootsfahrer richtet
das Boot immer neu auf das ruhende Ziel aus."""

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.animation

# Festlegen der Parameter
r0_boot = np.array([-5.0, -5.0])    # Anfangsposition des Bootes [m]
r_ziel = np.array([20.0, 5.0])      # Position des ruhenden Ziels [m]
v_wasser = np.array([0.0, -1.5])    # Geschwindigkeit der Wasserströmung [m/s]
v0_boot = 3.0                       # Betrag der Geschwindigkeit des Boots [m/s]
dt = 0.02                           # Zeitschritt der Simulation [s]

# Anlegen von Listen für die Position, Geschwindigkeit des Bootes
# und der Zeit
r_boot = [r0_boot]
v_boot = []
t = [0]

# Festlegen der Abbruchkriterien
t_max = 500             # Maximale Dauer der Simulation [s]
epsilon = v0_boot * dt   # Abbruch wenn der Abstand kleiner epsilon ist [m]

while True:
    # Berechnen des aktuellen Richtungs- und Geschwindigkeitsvektors 
    delta_r = r_ziel - r_boot[-1]
    v_boot.append(v0_boot * delta_r / np.linalg.norm(delta_r) + v_wasser)

    # Überprüfen der Abbruchkriterien
    if (t[-1] > t_max) or (np.linalg.norm(delta_r) < epsilon):
        break

    # Aktualisieren der Position des Bootes und des Zeitschritts
    r_boot.append(r_boot[-1] + v_boot[-1] * dt)
    t.append(t[-1] + dt)

# Umwandeln der Listen in Arrays
t = np.array(t)
r_boot = np.array(r_boot)
v_boot = np.array(v_boot)
a_boot = (v_boot[1:,:] - v_boot[:-1,:]) / dt

# Erstellen der Figure
fig = plt.figure()
ax = fig.add_subplot(1,1,1)
ax.set_xlabel('x [m]')
ax.set_ylabel('y [m]')
ax.set_aspect('equal')
ax.grid()

# Anlegen von Plots für das Ziel, die Bootskurve und den Ort 
# des Boots für die Animation
target, = ax.plot(r_ziel[0], r_ziel[1], 'o', color='red')
boot, = ax.plot(r_boot[:,0], r_boot[:,1])
boot_sim, = ax.plot([], [], 'o', color='blue')

# Erzeuge 2 Pfeile
style = mpl.patches.ArrowStyle.Simple(head_length=6, head_width=3)
arrow_v = mpl.patches.FancyArrowPatch((0, 0), (0, 0), color='red', arrowstyle=style)
arrow_a = mpl.patches.FancyArrowPatch((0, 0), (0, 0), color='black', arrowstyle=style)

# Füge die Grafikobjekte zur Axes hinzu
ax.add_artist(arrow_v)
ax.add_artist(arrow_a)

def update(n):
    # Aktualisieren der Position des Bootes
    boot_sim.set_data(r_boot[n])

    # Lege den Anfangs- und den Zielpunkt des v/a Pfeils fest
    arrow_v.set_positions(r_boot[n], r_boot[n] + v_boot[n])
    if n < a_boot.shape[0]:
        arrow_a.set_positions(r_boot[n], r_boot[n] + a_boot[n])

    return boot_sim, arrow_v, arrow_a

ani = mpl.animation.FuncAnimation(fig, update, interval=30, frames=t.size, blit=True)

plt.show()