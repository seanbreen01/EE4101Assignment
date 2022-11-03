import math
import matplotlib.pyplot as mplib
import numpy as np
import random
import scipy

#Will be usign this time with fixed value of n (39 as stated fo reasons below but this may change)
def erlangForm(n, aZero):

    numerator = (aZero ** n) / (math.factorial(n))
    denominator = 0
    for b in range(n + 1):
        denominator += (aZero ** b) / math.factorial(b)
    er = numerator/denominator
    return er

#Seems to be working as intended
def callStartTime():
    print('nada')
    np.random.uniform(0, 60, 1)  # randomly generating call start times in 60 minute window, with 0.01 hour resolution (6 secs)
    print('call start time')
    print(np.random.uniform(0, 60, 10)) #changing final param effects number of call start times generated - would want it to be 600 if doing all at once


#Working as needed now, can just fiddle std. dev as needed later on
def callDuration():
    print('call durations')
    print( scipy.stats.lognorm.rvs(scale=3, s=1/120, size=600) )        #3 min mean, 1/120 st dev., 600 samples
    #return this value in future


def monteCarlo(channelsAvailMax, trafficOff):
    print('monte carlo randomisation')
    callsDropped = 0  # number of calls dropped to be decided
    currentChannelsAvail = channelsAvailMax     #start with all channels available for use
    allChannelsUsed = False



    if(allChannelsUsed == True):
        callsDropped +=1        #update calls dropped total


    #how to calculate actual GoS provided?

    totalCallsAttempted = 600                #should be this value no?
    actualGradeOfService = callsDropped / totalCallsAttempted

    resultForThisRun = 0  # obvious change needed here

    actualGoS.append(resultForThisRun)  # recording the actual GoS observed in a given run of the simulation

#Minimum number of channels deemed to be appropriate = 39 (if using GoS of 0.025) -> this may change so watch out
#Have to create Monte Carlo simulation for calls and work on Part 1 stuff w/ graphing also
#Know our number of channels is 39 from part 1 and aZero is 30 Erlangs

callAttempts = 600
avgDuration = 0.05      #3 minutes expressed as fraction of an hour

#log normal dist for call durations - will need to site source for this but shouldn't be too hard found all going well
#or maybe gamma if I feel like it? - largely similar




#Duration of each call is randomly generated using appropriate call holding / time duration distribution -> find this online and work from it

__main__ = True
actualGoS = []  #save results of each of multiple runs here to find true mean, etc

while(__main__):
    print('main loop')

    channelsAvailable = 39  #can change this var as needed - depends on GoS used in part 1 so variable just handier to use - prob should be 42 for 1% GoS
    trafficOffered = 30     #Erlangs

    traffic = np.linspace(0, 601, 20)   #alter step size as needed

    monteCarlo(channelsAvailable, trafficOffered)   #feed in n value
    callStartTime()
    callDuration()

    #mplib.plot() plot erlangForm function result (y-axis value) for given traffic offered (x-axis value)
    #mplib.plot() plot actual observed GoS values from monte carlo function (these saved to list/array)
    #can then compare predicted results of Erlang-B formula against what we actually saw for the traffic offered

    __main__ = False