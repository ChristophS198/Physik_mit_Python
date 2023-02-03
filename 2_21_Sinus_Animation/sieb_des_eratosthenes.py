# Calculate primes based on the "Sieb des Eratosthenes"

import numpy as np


# Return primes up to a max value N
def get_prime(N):
    if N < 2: 
        print("Argument N too small no primes can be found!")
        return 0
    if N == 2:
        return 2
    else:
        marked = np.zeros(N,dtype=bool)
        # iterate from 2 up to sqrt(N), because larger values are already covered
        for i in range(2,round(np.sqrt(N)+1)):
            # get indices of multiples of current i. +/-2 because index has an offset of
            # 2 when related to prime numbers (marked starts with 0, primes start with 2)
            idx = np.arange(i*i, N+2, i, dtype=int) - 2
            marked[idx] = True
        # return all elements still containing False
        return np.where(marked==False)[0]+2

print(get_prime(120))