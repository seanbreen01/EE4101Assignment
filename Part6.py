import math
import matplotlib.pyplot as mplib
import numpy as np
import scipy

#Will be using this time with fixed value of n (42 as stated fo reasons below but this may change)
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


    totalCallAttemptsForDay = 600 / 0.089  # Calculates total call attempts for the 24hr period based on given information
    totalCallAttemptsForDay = round(totalCallAttemptsForDay)

    proportionOfDailyCallAttemptsByHour = [0.0009, 0.0005, 0.0004, 0.0004, 0.0008, 0.0044, 0.0168, 0.051, 0.0813,
                                           0.0794, 0.0743, 0.0795, 0.0881, 0.089, 0.0866, 0.0848, 0.0821, 0.068, 0.047,
                                           0.0306, 0.0183, 0.0095, 0.0043, 0.002]  # As described by variable name

    minChannelsNeededStatic = []    #Unaltered copy of channels needed, used in subsequent calculations

    # Calculating number of channels minimally necessary to achieve 1% GoS value for traffic in the given hour
    for t in range(24):
        channelsNeeded = 0
        while erlangForm(channelsNeeded, ((round(proportionOfDailyCallAttemptsByHour[t] * totalCallAttemptsForDay)) * 3) / 60) > 0.01:
            channelsNeeded += 1

        minChannelsNeededStatic.append(channelsNeeded)


    #Modify part 5 code so that blocks of K channels are deactivated as necessary
    #We will prioritise energy saving over GoS offered by the system
    #In practice this means that if the system minimally needs 25 channels to offer a 1% GoS, and the value of K is 7
    #Then the system will have 42 - 3*K = 21 channels available

    #Outermost loop controls the number of voice channels that can be deactivated at once
    for blockSize in range(10):
        print("Current Block Size: ", blockSize+1)
        gosValuesActuallyObservedBySimulationForDay = []
        minChannelsNeededByHour = []  # Channels to be used by hour based on blocksize, changes each run

        for h in range(24):
            maxReduction = 42 - minChannelsNeededStatic[h]

            trueReduction = math.ceil(maxReduction/(blockSize+1)) #Finding multiple of block size to reduce channels available by, round up to nearest integer value as we are prioritising energy saving over GoS provided

            #Should always be some capacity provisioned, therefore check if subtract result greater than 0 before performing
            if (42 - ((blockSize+1)*trueReduction)) > 1:
                minChannelsNeededByHour.append(42 - ((blockSize+1) * trueReduction))
            else:
                minChannelsNeededByHour.append(42 - ((blockSize+1) * (trueReduction-1))) #Ensures at least one channel provisioned

        print(minChannelsNeededByHour)


        #Each simulation run randomly generates a slightly different set of call data, i.e. start times and durations, for the known number of
        #channels needed to meet the demand.
        #These differences result in different real world values for the GoS offered by the system based on these differing inputs

        for i in range(numberSimulations):
            gosValuesActuallyObservedBySimulationForHour = []

            #loop iterates through 24 hours of the day and corresponding (provided) proportion of call attempts, generating the 'real-world' GoS values seen by the system each hour
            for j in range(24):
                callsForThisHour = generateCalls(round(proportionOfDailyCallAttemptsByHour[j]*totalCallAttemptsForDay))

                droppedCallsForThisHour = runSimulation(3600, len(callsForThisHour), minChannelsNeededByHour[j], callsForThisHour)  #returns an actual integer value for the number of calls dropped in a given simulation run

                gosValuesActuallyObservedBySimulationForHour.append(droppedCallsForThisHour / len(callsForThisHour))


            gosValuesActuallyObservedBySimulationForDay.append(sum(gosValuesActuallyObservedBySimulationForHour)/len(gosValuesActuallyObservedBySimulationForHour) )#calculation of 'real-world' gos value and recording this

            print("Sim run no.: ", i)




        averageGoSFromSimualtionRuns = sum(gosValuesActuallyObservedBySimulationForDay)/len(gosValuesActuallyObservedBySimulationForDay)    #Mean of simulation GoS
        print("Simulation mean:",averageGoSFromSimualtionRuns)
        stdDevGoSFromSimulationRuns = np.std(gosValuesActuallyObservedBySimulationForDay)
        print("Simulation Std. Deviation:", stdDevGoSFromSimulationRuns)

        print("Channels used in this day, with reduction of channels ",(blockSize+1)," at a time: ", sum(minChannelsNeededByHour))
        print("Channels used if no optimisations carried out: ", 42 * 24)
        print("Percentage Reduction in power use: ", (((42*24)-sum(minChannelsNeededByHour))/(42*24))*100)

        fig, ax = mplib.subplots()
        #ax.scatter([1], [0.007397146595099745], marker='o', color='blue', label="Expected GoS Value ")
        mplib.boxplot(gosValuesActuallyObservedBySimulationForDay)    #Making plot of actual GoS values observed during all simulations, using boxplot as is most useful for showing the relevant data here
        mplib.ylabel('Grade of Service Observed in Monte Carlo Sim Runs')
        mplib.title("Boxplot Showing Range Of GoS Values Observed")
        #mplib.legend(bbox_to_anchor=(1, 0), bbox_transform=ax.transAxes, loc="lower right", ncol=1)
        mplib.show()


__main__ = True

while(__main__):
    print('Begin Simulations:')
    monteCarlo(2)
    __main__ = False    #end of program