import matplotlib as mpl
import matplotlib.pyplot as plt
import scipy.optimize
import numpy as np

mess = np.array([[5.8, 7.3, 8.9, 10.6, 11.2], # v [m/s]
                [0.1, 0.15, 0.22, 0.33, 0.36]]) # F [N]
d_v = np.array([0.3, 0.3, 0.2, 0.2, 0.1])
d_F = np.array([0.02, 0.02, 0.02, 0.02, 0.02])

# define function to be optimized
def func(v, b, n):
    return b * abs(v)**n

# optimize the function parameters
popt, pcov = scipy.optimize.curve_fit(func, mess[0,:], mess[1,:], [1,1])
b, n = popt
d_b, d_n = np.sqrt(np.diag(pcov))

# print the result of the curve fit
print(f"Ergebnis der Kurvenanpassung: F(v) = b*|v|^n")
print(f" b = {b:4.3f} +- {d_b:5.4f} kg/s.")
print(f" n = {n:4.3f} +- {d_n:5.4f} .")


fig = plt.figure()
ax = fig.add_subplot(1,1,1)
ax.set_xlabel("Stoemungsgeschw. v [m/s]")
ax.set_ylabel("Kraft F [N]")
ax.grid()

# plot the fitted curve
v_fit = np.linspace(np.min(mess[0,:]), np.max(mess[0,:]), 500)
F_fit = func(v_fit, b, n)
ax.plot(v_fit, F_fit, "-", zorder=2)

# plot the measured points + error
ax.errorbar(mess[0,:], mess[1,:], yerr=d_F, xerr=d_v, fmt=".", capsize=2, zorder=1)

plt.show()