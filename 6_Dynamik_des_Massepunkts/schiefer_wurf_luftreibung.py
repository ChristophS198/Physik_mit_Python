"""Schiefer Wurf mit einem Tischtennisball."""

import numpy as np
import math
import scipy.integrate
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
alpha = math.radians(40.0)          # Abwurfwinkel [rad]
v0 = 20.0                           # Betrag der Abwurfgeschwindigkeit [m/s]
g = 9.81                            # Erdbeschleunigung [m/s²]
rho = 1.225                         # Luftdichte [kg/m³]

# Berechne den Vektor der Anfangsgeschwindigkeit [m/s]
v0 = np.array([v0 * math.cos(alpha), v0 * math.sin(alpha)])

def F(r, v):
    """Kraft als Funktion von Ort r und Geschwindigkeit v."""
    Fr = - 0.5 * rho * cwA * np.linalg.norm(v) * v
    Fg = m * g * np.array([0, -1])
    return Fr + Fg

def dgl(t, u):
    r, v = np.split(u, 2)
    return np.concatenate([v, F(r, v) / m])

def aufprall(t, u):
    """Ereignisfunktion: liefert einen Vorzeichenwechsel beim
    Auftreffen auf dem Erdboden (y=0)."""
    r, v = np.split(u, 2)
    return r[1]

# Beende die Simulation beim Auftreten des Ereignisses.
aufprall.terminal=True

# Lege den Zustandsvektor zum Zeitpunkt t=0 fest.
u0 = np.concatenate((r0, v0))

# Löse die Bewegungsgleichung bis zum Auftreffen auf der Erde.
result = scipy.integrate.solve_ivp(dgl, [0, np.inf], u0, dense_output=True, events=aufprall)

t_s = result.t
r_s, v_s = np.split(result.y, 2)

# Berechne die Interpolation auf einem feinen Raster.
t = np.linspace(0, np.max(t_s), 1000)
r, v = np.split(result.sol(t), 2)

# Plotte die Flugkurve des Balls
fig = plt.figure()
ax = fig.add_subplot(1,1,1)
ax.set_xlabel('x [m]')
ax.set_ylabel('y [m]')
ax.grid()

ball_kurve, = ax.plot(r[0,:], r[1,:])
ball, = ax.plot([], [], 'o', color='red')
ball_stuetz, = ax.plot(r_s[0,:], r_s[1,:], 'o', color='blue')

# Anlegen der Textfelder
text_t = ax.text(2.1, 1.4, '', color='blue')
text_v = ax.text(2.1, 1.2, '', color='red')
text_a = ax.text(2.1, 1.0, '')

# Erzeuge 2 Pfeile für Geschwindigkeit und Beschleunigung
style = mpl.patches.ArrowStyle.Simple(head_length=6, head_width=3)
arrow_v = mpl.patches.FancyArrowPatch((0, 0), (0, 0), color='red', arrowstyle=style)
arrow_a = mpl.patches.FancyArrowPatch((0, 0), (0, 0), color='black', arrowstyle=style)

# Füge die Grafikobjekte zur Axes hinzu
ax.add_artist(arrow_v)
ax.add_artist(arrow_a)

def update(n):
    ball.set_data(r[:,n])
    arrow_v.set_positions(r[:,n], r[:,n] + scal_v * v[:,n])
    a = F(r[:,n], v[:,n]) / m
    arrow_a.set_positions(r[:,n], r[:,n] + scal_a * a)

    # Aktualisiere die Textfelder.
    text_t.set_text(f't = {t[n]:.2f} s')
    text_v.set_text(f'v = {np.linalg.norm(v[:, n]):.1f} m/s')
    text_a.set_text(f'a = {np.linalg.norm(a):.1f} m/s²')

    return ball, ball_kurve, arrow_v, arrow_a, text_t, text_v, text_a

ani = mpl.animation.FuncAnimation(fig, update, interval=30, frames=t.size, blit=True)

plt.show()