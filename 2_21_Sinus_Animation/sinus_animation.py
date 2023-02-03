import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.animation


# f(x,t) = cos(k*x - w*t)
x = np.linspace(0,20,500)
k = 1.0     # Kreiszahl
w = 1.0     # Kreisfrequenz
delta_t = 0.02  # Zeitschrittweite

fig = plt.figure()

ax = fig.add_subplot(1,1,1)
ax.set_title("Cosine Animation")
ax.set_xlim(x[0], x[-1])
ax.set_ylim(-1.1, 1.1)
ax.set_xlabel("x location")
ax.set_ylabel("cos(k*x - w*t)")
ax.grid()

# create text field to show current timestamp
text = ax.text(0.0, 1.05, "")

# create a plot which can be manipulated in update function. First content is irrelevant
plot, = ax.plot(x, x*0)

def update(n):
    """ Calculate the sine values for the n-th timestep
    and update the corresponding axis elements"""

    # calc new function values
    t = n * delta_t
    u = np.cos(k*x - w*t)

    # update plot
    plot.set_ydata(u)

    # update text
    text.set_text(f"{t:5.1f}")

    # return tuple with updated graphic elements to be rendered
    return plot, ax

# create animation object
ani = mpl.animation.FuncAnimation(fig, update, interval=30, blit=True)

# start animation
plt.show()