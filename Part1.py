import math
import matplotlib.pyplot as mplib
import numpy as np


# Erlang formula equation function
# n: channels available for use
# aZero: traffic offered to network
def erlangForm(n, aZero):

    numerator = (aZero ** n) / (math.factorial(n))
    denominator = 0
    for b in range(n + 1):
        denominator += (aZero ** b) / math.factorial(b)
    er = numerator/denominator
    return er


#                                   A0^n
#                                  ------
#                                    n!
# erlang formula: E1(n, A0) = -----------------
#                                   A0^j
#                         sumj=0->n------
#                                    j!


desiredGoS = 0.025
results = []


t = 0
while True:                                   #guaranteed to enter loop at least once

    results.append(erlangForm(t, 30))
    if results[t] <= desiredGoS:
        break                                 #have reached a number of channels for which the GoS is acceptable

    t+= 1                                     #increment counter

for x in results:
    print( 'No. of channels: ' + str(results.index(x)) )
    print(x)

xAxis = np.linspace(0, len(results), 1)

mplib.plot(results)
#mplib.plot(np.reciprocal(results) )
mplib.xlabel('Number of Channels')
mplib.ylabel('Grade of Service (lower better)')

mplib.title("Plot of Grade of Service for Given Number of Channels Available")

mplib.legend()

mplib.show()

#Think change acceptable GoS to 1% rather than 2.5%

