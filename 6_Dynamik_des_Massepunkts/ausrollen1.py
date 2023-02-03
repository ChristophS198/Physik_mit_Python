"""Simulation des Ausrollens eines Fahrzeugs mit dem
2 Euler-Verfahren (eindimensionale Bewegung)."""

import numpy as np
import matplotlib.pyplot as plt

# Definieren der Parameter
t_max = 20      # Zeitdauer die simuliert werden soll [s]
dt = 0.2        # Zeitschrittweite [s]
m = 15.0        # Masse des Fahrzeugs [kg]
b = 2.5         # Reibungskoeffizient [kg/m]
x0 = 0.0        # Anfangsort
v0 = 10.0       # Anfangsgeschwindigkeit [m/s]


def F(v):
    """Kraft als Funktion der Geschwindigkeit v."""
    return -b * v * np.abs(v)

# Lege Arrays für das Simulationsergebnis an
# Da wir bereits wissen wie viele Zeitschritte wir simulieren
t = np.arange(0, t_max, dt)
x = np.empty(t.size)
v = np.empty(t.size)

# Lege die Anfangsbedingungen fest
x[0] = x0
v[0] = v0

# Simulationsschleife
for i in range(t.size-1):
    x[i+1] = x[i] + v[i] * dt
    v[i+1] = v[i] + F(v[i]) / m * dt


# Erzeuge eine Figure
fig = plt.figure(figsize=(9,4))
fig.set_tight_layout(True)

# Plotte das Geschwindigkeits-Zeit-Diagramm
ax1 = fig.add_subplot(1,2,1)
ax1.set_xlabel('t [s]')
ax1.set_ylabel('v [m/s]')
ax1.grid()
ax1.plot(t, v0 / (1 + v0 * b / m * t), '-b', label='analytisch')
ax1.plot(t, v, '.r', label='simuliert')
ax1.legend()

# Plotte das Weg-Zeit-Diagramm 
ax2 = fig.add_subplot(1,2,2)
ax2.set_title(f'Große Zeitschrittweite dt={dt:.2f}')
ax2.set_xlabel('t [s]')
ax2.set_ylabel('x [m/s]')
ax2.grid()
ax2.plot(t, m / b * np.log(1 + v0 * b / m * t), '-b', label='analytisch')
ax2.plot(t, x, '.r', label='simuliert')
ax2.legend()

plt.show()