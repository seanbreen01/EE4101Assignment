import numpy as np
import scipy
import matplotlib.pyplot as mplib

startTime = np.random.uniform(0, 3600, 600)  #generating 600 second values for start time
startTime.sort()

duration = scipy.stats.lognorm.rvs(scale=180, s=1.1, size=600)    #scale should be 3mins or 180 secs (this is the mean)
                                                                  #may need to fiddle scale, this is std. dev value and may need to be altered somewhat to be more reflective of reality
allCallInfo = []
for x in range(600):

    templist = []
    templist.append(startTime[x])
    templist.append(duration[x])
    allCallInfo.append(templist)        #create list of 2 element lists that contains the start times and durations of each call


maxChannels = 39
currentAvailChannels = maxChannels
droppedCalls = 0


for callAttemptNo in range(600):        #all calls to be attempted
    for time in range(3600):   #int representation of time in seconds

        if allCallInfo[callAttemptNo] == None:
            break    #do nothing, we don't need to worry about it anymore, call either handled properly or dropped


        #call has finished, can move on
        elif time > (round(allCallInfo[callAttemptNo][0]) + allCallInfo[callAttemptNo][1]):
            currentAvailChannels += 1
            allCallInfo[callAttemptNo] = None   #remove info about call, no longer care about it


        #call is ready to begin, can it be handled?
        elif time == round(allCallInfo[callAttemptNo][0]): #start time, need to round to nearest second
            if currentAvailChannels != 0:
                currentAvailChannels -= 1              #taking control of a channel, remove it from those available
                #dont remove from list


            elif currentAvailChannels == 0:         #no channels free
                allCallInfo[callAttemptNo] = None   #drop call from list of all calls, it is no longer needed
                droppedCalls += 1




print('dropped calls: ' + str(droppedCalls))
print(allCallInfo)
print('curr avail after' + str(currentAvailChannels) )




