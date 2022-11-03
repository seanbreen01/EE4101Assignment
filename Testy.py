from numpy import exp
from scipy.stats import lognorm
import matplotlib.pyplot as plt
import numpy as np
fig, ax = plt.subplots(1, 1)
#Calculate the first four moments:

s = 0.954    #std dev of ~180secs/3 mins
mean, var, skew, kurt = lognorm.stats(s, moments='mvsk')

sigma = 0.05
mean = 0.083
randomNumber = lognorm.rvs(s=sigma, scale=exp(0.083))
#print(randomNumber)
print(np.random.lognormal(mean, sigma)-1)
print(60*(np.random.lognormal(mean, sigma)-1))


#Display the probability density function (pdf):

x = np.linspace(lognorm.ppf(0.01, s),
                lognorm.ppf(0.99, s), 100)
ax.plot(x, lognorm.pdf(x, s),
       'r-', lw=5, alpha=0.6, label='lognorm pdf')
#Alternatively, the distribution object can be called (as a function) to fix the shape, location and scale parameters. This returns a “frozen” RV object holding the given parameters fixed.

#Freeze the distribution and display the frozen pdf:

rv = lognorm(s)
ax.plot(x, rv.pdf(x), 'k-', lw=2, label='frozen pdf')
#Check accuracy of cdf and ppf:

vals = lognorm.ppf([0.001, 0.5, 0.999], s)
np.allclose([0.001, 0.5, 0.999], lognorm.cdf(vals, s))
#True
#Generate random numbers:

r = lognorm.rvs(s, size=1000)
#And compare the histogram:

ax.hist(r, density=True, histtype='stepfilled', alpha=0.2)
ax.legend(loc='best', frameon=False)
plt.show()