"""Simulation der Bewegung eines Massepunkts auf der Kreisbahn"""

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.animation

# Parameter der Simulation
R = 3.0                     # Radius der Kreisbahn [m]
T = 12.0                    # Umlaufdauer [s]
dt = 0.02                   # Zeitschrittweiter [s]
omega = 2 * np.pi / T       # Winkelgeschwindigkeit [1/s]

# Gib das analytische Ergebnis aus
print(f'Bahngeschwindigkeit:       {R*omega:.3f} m/s')
print(f'Zentripetalbeschleunigung: {R*omega**2:.3f} m/s²')

# Erzeuge ein Array von Zeitpunkten für eine Umlauf
# Für eine dauerhafte Simulation reicht die Simulation eines Umlaufs
t = np.arange(0, T, dt)

# Erzeuge ein leeres n x 2 - Array für die Ortskurve
r = np.empty((t.size, 2))

# Berechne die Position des Massepunktes für jeden Zeitpunkt
r[:,0] = R * np.cos(omega * t)
r[:,1] = R * np.sin(omega * t)

# Berechne den Geschwindigkeits- und Beschleunigugnsvektor
v = (r[1:,:] - r[:-1,:]) / dt
a = (v[1:,:] - v[:-1,:]) / dt

# Erzeuge eine Figure und ein Axis Objekt
fig = plt.figure()
ax = fig.add_subplot(1,1,1)
ax.set_xlabel('x [m]')
ax.set_ylabel('y [m]')
ax.set_xlim(-(R+0.2), R+0.2)
ax.set_ylim(-(R+0.2), R+0.2)
ax.grid()

# Erzeuge eine leeren Plot
plot, = ax.plot([], [], 'o', color='red')

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
    if n < r.shape[0]:
        arrow_v.set_positions(r[n], r[n]+v[n])
        # Lege den Anfangs- und den Zielpunkt des
        # Beschleunigugnspfeiles fest
        if n < r.shape[0]-1:
            arrow_a.set_positions(r[n], r[n]+a[n])
    
    # Aktualisiere die Position des Massepunktes
    plot.set_data(r[n])

    return plot, arrow_v, arrow_a

# Erzeuge das Animationsobjekt und starte die Animation
ani = mpl.animation.FuncAnimation(fig, update, interval=30, frames=t.size, blit=True)
plt.show()