import math
import matplotlib.pyplot as mplib
import numpy as np
import scipy

#Will be using this time with fixed value of n (39 as stated fo reasons below but this may change)
def erlangForm(n, aZero):
    numerator = (aZero ** n) / (math.factorial(n))
    denominator = 0
    for b in range(n + 1):
        denominator += (aZero ** b) / math.factorial(b)
    er = numerator/denominator
    return er

def generateCalls(numberToGenerate):
    startTime = np.random.uniform(0, 3600, numberToGenerate)  # generating desired number of values for start times
    startTime.sort()                                          # ordering start times sequentially

    duration = scipy.stats.lognorm.rvs(scale=180, s=1.1, size=numberToGenerate)  # scale should be 3mins or 180 secs (this is the mean)
                                                                                 # may need to fiddle scale, this is std. dev value and may need to be altered somewhat to be more reflective of reality

    allCallInfo = []
    for x in range(numberToGenerate):
        templist = []
        templist.append(startTime[x])
        templist.append(duration[x])
        allCallInfo.append(templist)  # create list of 2 element lists that contains the start times and durations of each call

    return allCallInfo

def runSimulation(runTime, numberCalls, numberChannels, callInfo):
    allCallInfo = callInfo
    currentAvailChannels = numberChannels
    droppedCalls = 0

    for callAttemptNo in range(numberCalls):  # all calls to be attempted
        for time in range(runTime):  # int representation of time in seconds

            if allCallInfo[callAttemptNo] == None:
                break  # do nothing, we don't need to worry about it anymore, call either handled properly or dropped


            # call has finished, can move on
            elif time > (round(allCallInfo[callAttemptNo][0]) + allCallInfo[callAttemptNo][1]):
                currentAvailChannels += 1
                allCallInfo[callAttemptNo] = None  # remove info about call, no longer care about it


            # call is ready to begin, can it be handled?
            elif time == round(allCallInfo[callAttemptNo][0]):  # start time, need to round to nearest second
                if currentAvailChannels != 0:
                    currentAvailChannels -= 1  # taking control of a channel, remove it from those available
                    # dont remove from list


                elif currentAvailChannels == 0:  # no channels free
                    allCallInfo[callAttemptNo] = None  # drop call from list of all calls, it is no longer needed
                    droppedCalls += 1

    return droppedCalls #returns the total number of calls that were dropped for a given simulation run

def monteCarlo(numberSimulations):

    gosValuesActuallyObservedBySimulation = []


    #Each simulation run randomly generates a slightly different set of call data, i.e. start times and durations, for the known number of
    #channels needed to meet the demand.
    #These differences result in different real world values for the GoS offered by the system based on these differing inputs
    for i in range(numberSimulations):
        calls = generateCalls(600)
        droppedCalls = runSimulation(3600, 600, 42, calls)  #returns an actual integer value for the number of calls dropped in a given simulation run

        gosValuesActuallyObservedBySimulation.append(droppedCalls/600) #calculation of 'real-world' gos value and recording this

        print("Sim run no.: ", i)

    averageGoSFromSimualtionRuns = sum(gosValuesActuallyObservedBySimulation)/len(gosValuesActuallyObservedBySimulation)    #Mean of simulation GoS
    print(averageGoSFromSimualtionRuns)

    fig, ax = mplib.subplots()
    ax.scatter([1], [0.007397146595099745], marker='o', color='blue', label="Expected GoS Value ")

    mplib.boxplot(gosValuesActuallyObservedBySimulation)    #Making plot of actual GoS values observed during all simulations, using boxplot as is most useful for showing the relevant data here

    mplib.ylabel('Grade of Service Observed in Monte Carlo Sim Runs')

    mplib.title("Boxplot Showing Range Of GoS Values Observed")
    mplib.legend(bbox_to_anchor=(1, 0), bbox_transform=ax.transAxes, loc="lower right", ncol=1)

    mplib.show()







__main__ = True
actualGoS = []  #save results of each of multiple runs here to find true mean, etc

while(__main__):
    print('main loop')

    monteCarlo(50) #runs 100 simulations


    #mplib.plot() plot erlangForm function result (y-axis value) for given traffic offered (x-axis value)
    #mplib.plot() plot actual observed GoS values from monte carlo function (these saved to list/array)
    #can then compare predicted results of Erlang-B formula against what we actually saw for the traffic offered

    __main__ = False    #end of program
