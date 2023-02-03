"""Simulation der Hundekurve"""

from email.base64mime import header_length
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.animation 

# Startpostition (x,y) des Hundes [m]
r0_hund = np.array([0.0, 10.0])

# Startposition (x,y) des Menschen [m]
r0_mensch = np.array([0.0, 0.0])

# Vektor der Geschwindigkeit (vx,vy) des Menschen [m/s]
v0_mensch = np.array([2.0, 0.0])

# Betrag der Geschwindigkeit des Hundes [m/s]
v0_hund = 3.0

# Maximale Simulationsdauer [s]
t_max = 500

# Zeitschrittweite [s]
dt = 0.01

# Brich die Simulation ab, wenn der Abstand von Hund 
# und Mensch kleiner epsilon ist
epsilon = v0_hund * dt

# Lege Listen an, um das Simulationsergebnis zu speichern
# Arrays wären ungünstig, da wir vorab nicht wissen wie viele 
# Zeitschritte wir simulieren müssen
t = [0]
r_hund = [r0_hund]
r_mensch = [r0_mensch]
v_hund = []

# Simulationsschleife
while True:
    # Berechne den Geschwindigkeitsvektor des Hundes
    delta_r = r_mensch[-1]-r_hund[-1]
    v_hund.append(v0_hund * delta_r / np.linalg.norm(delta_r))

    # Überprüfe die Abbruchkriterien
    if (np.linalg.norm(delta_r) < epsilon) or (t[-1] > t_max):
        break
    
    # Berechne die neue Position von Hund und Mensch und die neue Zeit
    r_mensch.append(r_mensch[-1] + v0_mensch * dt)
    r_hund.append(r_hund[-1] + v_hund[-1] * dt)
    t.append(t[-1] + dt)

# Wandle die Listen in Arrays um, damit leichter gerechnet werden kann
t = np.array(t)
r_hund = np.array(r_hund)
v_hund = np.array(v_hund)
r_mensch = np.array(r_mensch)

# Berechne den Beschleunigungsvektor des Hundes für alle
# Zeitpunkte. Achtung! Das Array a_hund hat eine Zeile
# weniger, als es Zeitpunkte gibt
a_hund = (v_hund[1:,:] - v_hund[:-1,:]) / dt 

def analytical_x_position(r0_hund, v_hund, v_mensch, y):
    """Zum Zeitpunkt t0 befindet sich der Mensch im Koordinatenursprung
    und der Hund am Ort r0_hund. Zurückgegeben wird x Position Hundes 
    in Abhängigkeit von des y Position"""
    k = np.linalg.norm(v_mensch) / np.linalg.norm(v_hund)
    if k >= 1:
        print("Der Hund kann den Menschen nicht eiholen da er zu langsam ist!")
        return np.inf
    y0 = r0_hund[1]
    yd = y / y0
    x_hund = y0 / 2 * ((1 - yd**(1-k))/(1-k) - (1-yd**(1+k))/(1+k))
    return x_hund

# Berechne die Hundekurve anhand der analytischen Lösunge
# welche die x Position in Abhängigkeit der y Position des
# Hundes berechnet x_hund = x(y)
# Am Ende sollte die y Position von Hund und Mensch gleich sein 
y_end = r0_mensch[1]
y_hund = np.linspace(r0_hund[1], y_end)
x_hund = analytical_x_position(r0_hund, v0_hund, v0_mensch, y_hund)
    


# # Erzeuge eine Figure der Größe 10inch x 3inch
# fig = plt.figure(figsize=(10, 3))
# fig.set_tight_layout(True)

# # PLotte die Bahnkurve des Hundes
# ax1 = fig.add_subplot(1,3,1)
# ax1.set_xlabel("x [m]")
# ax1.set_ylabel("y [m]")
# ax1.set_aspect('equal')
# ax1.grid()
# ax1.plot(r_hund[:,0], r_hund[:,1])

# # Plotte den Abstand von Hund und Mensch
# ax2 = fig.add_subplot(1,3,2)
# ax2.set_xlabel('t [s]')
# ax2.set_ylabel('Abstand [m]')
# ax2.grid()
# ax2.plot(t,np.linalg.norm(r_hund-r_mensch, axis=1))

# # Plotte den Betrag der Beschleunigung
# ax3 = fig.add_subplot(1,3,3)
# ax3.set_xlabel('t [s]')
# ax3.set_ylabel('Beschl. [m/s²]')
# ax3.grid()
# ax3.plot(t[1:],np.linalg.norm(a_hund, axis=1))

# Erzeuge eine Figure und ein Axis-Object
fig = plt.figure()
ax = fig.add_subplot(1,1,1)
ax.set_xlabel("x [m]")
ax.set_ylabel("y [m]")
ax.set_xlim(-0.2, 15)
ax.set_ylim(-0.2, 10)
ax.set_aspect('equal')
ax.grid()

# Erzeuge den Plot für die analytischen Berechnung der Bahnkurve des Hundes
plot, = ax.plot(x_hund,y_hund, color='black')

# Erzeuge 2 leere Punktplots
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