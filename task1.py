import sys
import numpy as np
from copy import deepcopy

filename = sys.argv[1]
file = open(filename,"r")

# Taking inputs --
line = file.readline()
args = line.split( )	
numStates = int(args[1])

line = file.readline()
args = line.split( )	
numActions = int(args[1])

line = file.readline()
args = line.split( )	
startState = int(args[1])

line = file.readline()
args = line.split( )	
endStates = []
if(args[1]!=-1):
	endStates = [int(x) for x in args[1:]]

discount = 0

transitions = [[[] for _ in range(numActions)] for _ in range(numStates)]
while 1:
	line = file.readline()
	args = line.split( )	
	if args[0]=='transition':
		transitions[int(args[1])][int(args[2])].append((int(args[3]),float(args[4]),float(args[5])))
	elif args[0]=='discount':
		discount = float(args[1])
		break

# Value Iteration

Vprev = np.zeros(numStates).astype(np.float64)
Vcurr = np.zeros(numStates).astype(np.float64)
Policy = np.zeros(numStates)
numIter = 0
while 1:
	numIter += 1
	loop = 0
	for s in range(numStates):
		if(len(endStates)>0 and (s in endStates)):
			Vcurr[s] = 0
			Policy[s] = -1
		else:
			val = []
			for a in range(numActions):
				totalSum = -1000.0
				if(len(transitions[s][a])>0):
					if(totalSum==-1000.0):
						totalSum = 0.0
						for items in transitions[s][a]:	
							totalSum += items[2] * (items[1] + discount*Vprev[items[0]])
				val.append(totalSum)

			if(max(val) == -1000.0):
				Policy[s] = -1
			else:
				Vcurr[s] = max(val)
				Policy[s] = val.index(max(val))
			if(abs(Vcurr[s]-Vprev[s]) > 10**(-16)):
				loop = 1

	if (loop==0):
		break;
	Vprev = deepcopy(Vcurr)

for i in range(numStates):
	print(round(Vcurr[i],11), int(Policy[i]))
print("iterations" , numIter)