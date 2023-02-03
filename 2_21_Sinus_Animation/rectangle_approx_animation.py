"""Approximate a rectangular function f(x) with a 
Fourier sum: f(x) ~ 4/pi sum_k=0^inf( (sin(2*k+1)*x) / (2*k+1))"""

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.animation


# only plot values for interval [0, 2Pi]
x = np.linspace(0, 2*np.pi, 500)

fig = plt.figure()
ax = fig.add_subplot(1,1,1)
ax.set_title("Rectangle approx with Fourier sum")
ax.set_xlim(0, 2*np.pi)
ax.set_ylim(-1.3, 1.3)
ax.set_xlabel("x values")
ax.set_ylabel("y values")
ax.grid()

# create plot to be animated
plot, = ax.plot(x, x*0)

# add text field for current number of summands
text = ax.text(0.0, 1.05, "0")

# start with n=0 
rect_approx = x*0

# init function is called at startup of animation
# only used here so update(n) is only called once with n=0
def init():
    return plot, ax

# In each call of update a new summand of the Fourier
# approximation is added
def update(n):
    # for simplicity use global variable rect_approx so 
    # variables can be updated inside this function
    global rect_approx

    # update rectangular approx with additoinal summand
    rect_approx += 4.0/np.pi * (np.sin((2*n+1)*x)) / (2*n+1)
    plot.set_ydata(rect_approx)

    text.set_text(f"{n:}")
    return plot, ax


# ani = mpl.animation.FuncAnimation(fig, update,fargs=(rect_approx,), interval=100, blit=True)
ani = mpl.animation.FuncAnimation(fig, update, init_func=init, interval=100, blit=True)

plt.show()


