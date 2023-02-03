"""Calculate and plot the area of a polygon"""

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

# coordinates of the polygon
x_coords = np.array([0.0, 0.0, 1.0, 2.2, 2.8, 3.8, 4.6, 5.7, 6.4, 7.1, 7.6, 7.9, 7.9])
y_coords = np.array([1.0, 2.8, 3.3, 3.5, 3.4, 2.7, 2.4, 2.3, 2.1, 1.6, 0.9, 0.5, 0.0])
coords = np.zeros([x_coords.size,2])

for i in range(x_coords.size):
    coords[i] = [x_coords[i], y_coords[i]]

# calc the area with np.roll()
A = .5 * abs(np.sum((coords[:,0]*np.roll(coords[:,0],-1) + coords[:,1]*np.roll(coords[:,1],-1))))

# plot area
fig = plt.figure()

ax = fig.add_subplot(1,1,1)
x = np.append(coords[:,0], coords[0,0])
y = np.append(coords[:,1], coords[0,1])
plot = ax.plot(x, y)

plt.show()