import numpy as np 

x = np.arange(1,10)
x = x.reshape(1,9)

A = x*x.transpose()
print(x.shape)
print(A)