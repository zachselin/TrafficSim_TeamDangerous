import matplotlib.pyplot as plt
import numpy as np

# throughput
autothru = np.array([284.1, 283.0, 375.0, 416.2, 444.3, 452.4])
bufferthru = np.array([284.1, 335.2, 387.9, 432.5, 453.4, 462.4])
mixthru = np.array([452.4, 449.5, 446.0, 446.8, 456.7, 462.4])

x = np.array([0, 20, 40, 60, 80, 100])

# speed slices as thresholds of max speed
normalcarslices = np.array([ 0.1642,  0.0715  ,   0.1078 ,  0.1565 ,  0.4998])
bufferslices = np.array([0. ,       0. ,    4803.8,  439453.6,  703131.4]) / 1147388.2
autoslices = np.array([0. ,       0. ,    9675. ,  602105.6,  723053.4]) / 1334834.

xslice = np.array([10, 30, 50, 70, 90])



line = [x[0], x[-1]]
expectedy = [478, 478]
attemptedy = [583.3, 583.3]
flaty = [0, 0]

"""
plt.title("Autonomous -> BufferBuilder - Concentration Shift\nlanes: 5   simulatons: 100   ticks: 10000   cars/min: 350")
plt.ylabel("Car Throughput")
plt.xlabel("BufferBuilder Concentration % (remaining is Autonomous)")

expected = plt.plot(line, expectedy)
plt.setp(expected, color='r')

#zero = plt.plot(line, flaty)
#plt.setp(expected, color='r')

attempted = plt.plot(line, attemptedy)

thru = plt.plot(x, mixthru)
plt.setp(thru, color='b')

att = "Attempted Input"
plt.text(45, attemptedy[0]-10, att, fontsize=8, ha='center', va='top', wrap=True)

exp = "Expected Throughput"
plt.text(45, expectedy[0]-10, exp, fontsize=8, ha='center', va='top', wrap=True)

exp = "Actual Throughput"
plt.text(45, mixthru[2]+9, exp, rotation=0, fontsize=8, ha='center', va='top', wrap=True)
"""

# display slices
plt.title("Proportion of Time Spent Going X of MPH Speed Limit\nlanes: 5   simulatons: 100   ticks: 10000   cars/min: 350")
plt.ylabel("Proportion of Total Time Spent")
plt.xlabel("Nearest Percent of Maxspeed (green=auto, orange=buffer, blue=normal)")

nslices = plt.plot(xslice, normalcarslices)
bslices = plt.plot(xslice, bufferslices)
aslices = plt.plot(xslice, autoslices)

    
# Display window
plt.show()