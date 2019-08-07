import sys
import numpy as np
from copy import deepcopy

filename = sys.argv[1]
probability = float(sys.argv[2])
file = open(filename,"r")

line = file.readline()
args = line.split( )
n = len(args)
grid = np.zeros((n,n))

for i in range(n):
	grid[0,i] = int(args[i])

for i in range(n-1):
	line = file.readline()
	args = line.split( )
	for j in range(n):
		grid[i+1][j] = int(args[j])

numStates = n**2
numActions = 4 # left = 0 right = 1 up = 2 down = 3

startState = -1
endStates = []
discount = 0.9

def validArray(i,j):
	validAction = []
	validState = []
	row = []
	col = []

	if(grid[i][j] != 1):
		if(j>0):
			if(grid[i][j-1] != 1):
				validAction.append(0)
				validState.append(i*n+j-1)
				row.append(i)
				col.append(j-1)
		if(j<n-1):
			if(grid[i][j+1] != 1):
				validAction.append(1)
				validState.append(i*n+j+1)
				row.append(i)
				col.append(j+1)
		if(i>0):
			if(grid[i-1][j] != 1):
				validAction.append(2)
				validState.append((i-1)*n+j)
				row.append(i-1)
				col.append(j)
		if(i<n-1):
			if(grid[i+1][j] != 1):
				validAction.append(3)
				validState.append((i+1)*n+j)
				row.append(i+1)
				col.append(j)
	return validAction, validState, row, col


transitions = [[[] for _ in range(numActions)] for _ in range(numStates)]
for i in range(n):
	for j in range(n):
		if(grid[i][j]==1):
			continue
		if(grid[i][j]==2):
			startState = i*n+j
		elif(grid[i][j]==3):
			endStates.append(str(i*n+j))
			continue

		validAction, validState, row, col = validArray(i,j)
		numValid = len(validAction)

		for u in range(numValid):
			for v in range(numValid):
				if(u==v):
					if(grid[row[u]][col[u]]==3):
						transitions[i*n+j][validAction[u]].append((validState[u], 10000.0, probability+(1-probability)/numValid))
					else:
						transitions[i*n+j][validAction[u]].append((validState[u], -1.0, probability+(1-probability)/numValid))
				else:
					if(probability == 1.0):
						continue
					if(grid[row[v]][col[v]]==3):
						transitions[i*n+j][validAction[u]].append((validState[v], 10000.0, (1-probability)/numValid))
					else:
						transitions[i*n+j][validAction[u]].append((validState[v], -1.0, (1-probability)/numValid))

print("numStates",numStates)
print("numActions",numActions)
print("start",startState)
print("end",' '.join(endStates))

for i in range(numStates):
	for j in range(numActions):
		for items in transitions[i][j]:
			print("transition",i,j,items[0],items[1],items[2])

print("discount",discount)