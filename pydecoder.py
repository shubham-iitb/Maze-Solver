import sys
import numpy as np
from copy import deepcopy

gridfilename = sys.argv[1]
value_and_policy_file_name = sys.argv[2]
probability = float(sys.argv[3])
gridfile = open(gridfilename,"r")

# Taking inputs --

line = gridfile.readline()
args = line.split( )
n = len(args)
grid = np.zeros((n,n))

for i in range(n):
	grid[0,i] = int(args[i])

for i in range(n-1):
	line = gridfile.readline()
	args = line.split( )
	for j in range(n):
		grid[i+1][j] = int(args[j])

startState = -1
endState = -1
for i in range(n):
	for j in range(n):
		if(int(grid[i][j]==2)):
			startState = i*n+j
		elif(int(grid[i][j]==3)):
			endState = i*n+j

numStates = n**2
numActions = 4 # left = 0 right = 1 up = 2 down = 3

vandpfile = open(value_and_policy_file_name,"r")

policy = []
for i in range(numStates):
	line = vandpfile.readline()
	args = line.split( )
	policy.append(int(float(args[1])))

def position(s):
	return(int(s/n),int(s%n))

def validArray(i,j):
	validAction = []
	validState = []

	if(grid[i][j] != 1):
		if(j>0):
			if(grid[i][j-1] != 1):
				validAction.append(0)
				validState.append(i*n+j-1)
		if(j<n-1):
			if(grid[i][j+1] != 1):
				validAction.append(1)
				validState.append(i*n+j+1)
		if(i>0):
			if(grid[i-1][j] != 1):
				validAction.append(2)
				validState.append((i-1)*n+j)
		if(i<n-1):
			if(grid[i+1][j] != 1):
				validAction.append(3)
				validState.append((i+1)*n+j)
	return validAction, validState


s = startState
moves = []
while(1):
	if(s == endState):
		break
	i,j = position(s)
	validAction, validState = validArray(i,j)
	prob = []

	for item in validAction:
		if(policy[s]==item):
			prob.append(probability+(1-probability)/len(validAction))
		else:
			prob.append((1-probability)/len(validAction))

	move = np.random.choice(validAction, 1, p=prob)
	moves.append(move)
	if(move==0):
		s-=1
	elif(move==1):
		s+=1
	elif(move==2):
		s-=n
	elif(move==3):
		s+=n

	# moves.append(policy[s])
	# if(policy[s]==0):
	# 	s-=1
	# elif(policy[s]==1):
	# 	s+=1
	# elif(policy[s]==2):
	# 	s-=n
	# elif(policy[s]==3):
	# 	s+=n

for i in range(len(moves)):
	if(moves[i]==0):
		moves[i] = "W"
	elif(moves[i]==1):
		moves[i] = "E"
	elif(moves[i]==2):
		moves[i] = "N"
	elif(moves[i]==3):
		moves[i] = "S"

print (" ".join(moves))