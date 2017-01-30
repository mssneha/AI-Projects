import copy
from collections import defaultdict
#Open a file
f = open("input_test.txt", "r")
f1 = open("debug1.txt","w")
n = int(f.readline().rstrip('\n').strip())
mode = f.readline().rstrip('\n').strip()
youPlay = f.readline().rstrip('\n').strip()
depth = int(f.readline().rstrip('\n').strip())


column_names = { 1 : 'A', 2 : 'B', 3 : 'C', 4 : 'D', 5 : 'E', 6 : 'F', 7 : 'G', 8 : 'H', 9 : 'I',
	10 : 'J', 11 : 'K', 12 : 'L', 13 : 'M', 14 : 'N', 15 : 'O', 16 : 'P', 17 : 'Q', 18 : 'R',
	19 : 'S', 20 : 'T', 21 : 'U', 22 : 'V', 23 : 'W', 24 : 'X', 25 : 'Y', 26 : 'Z'}

x_blank_space = []
y_blank_space = []

if youPlay == 'O':
	opponent = 'X'
else: 
	opponent = 'O'


cell_values = [[0 for i in range(n+1)] for i in range(n+1)]
		
#function returns unoccupied spaces
def blank_spaces(board_state):
	blank_spaces = {}
	#Getting blank spaces in the board
	for x in range(1,n+1):
		for y in range(1,n+1):
			if board_state[x][y] == '.':
				if len(blank_spaces) == 0:
					blank_spaces [x] = []
					blank_spaces [x].append(y)
				else:
					flag = 1
					for key in blank_spaces.keys():
						if(x == key):
							blank_spaces [key].append(y)
							flag = 0
							break
					if(flag == 1):
						blank_spaces[x] = []
						blank_spaces[x].append(y)
	return blank_spaces

def possible_raid_positions(board_state, play):
	raid_positions = []
	for x in range(1,n+1):
		for y in range(1,n+1):
			if(board_state[x][y] == play):
				if(x > 1):
					top = board_state[x-1][y]
					if(top == '.'):
						pos = [x-1, y]
						if(not pos in raid_positions):
							raid_positions.append(pos)

				if(x < n):
						bottom = board_state[x+1][y]
						if(bottom == '.'):
							pos = [x+1, y]
							if(not pos in raid_positions):
								raid_positions.append(pos)

				if(y > 1):
						left = board_state[x][y-1]
						if(left == '.'):
							pos = [x,y-1]
							if(not pos in raid_positions):
								raid_positions.append(pos)


				if(y < n):
						right = board_state[x][y+1]
						if(right == '.'):
							pos = [x,y+1]
							if(not pos in raid_positions):
								raid_positions.append(pos)
	return raid_positions





#Actions
def apply(board_state,x,y,play, raid_positions):
	actions_board_states_dict = {}
	modified_board_state = copy.deepcopy(board_state)
	
	modified_board_state[x][y] = play
	actions_board_states_dict["Stake"] = modified_board_state
	if ([x, y] in raid_positions):
			if(x > 1):
				top_x = x-1
				top_y = y
			else:
				top_x = 0
				top_y = 0
			if(x < n):
				bottom_x = x+1
				bottom_y = y
			else:
				bottom_x = 0
				bottom_y = 0
			if(y > 1):
				left_x = x
				left_y = y-1
			else:
				left_x = 0
				left_y = 0
			if(y < n):
				right_x = x
				right_y = y+1
			else:
				right_x = 0
				right_y = 0
			if(play == 'O'):
				opponent = 'X'
			elif(play == 'X'):
				opponent = 'O'
			left = modified_board_state[left_x][left_y]
			right = modified_board_state[right_x][right_y]
			bottom = modified_board_state[bottom_x][bottom_y]
			top = modified_board_state[top_x][top_y]
			if(left == opponent or right == opponent or bottom == opponent or top == opponent):
				conquered_board_state = copy.deepcopy(modified_board_state)
				if(conquered_board_state[left_x][left_y] == opponent):
					conquered_board_state[left_x][left_y] = play
				if(conquered_board_state[right_x][right_y] == opponent):
					conquered_board_state[right_x][right_y] = play
				if(conquered_board_state[bottom_x][bottom_y] == opponent):
					conquered_board_state[bottom_x][bottom_y] = play
				if(conquered_board_state[top_x][top_y] == opponent):
					conquered_board_state[top_x][top_y] = play	
				actions_board_states_dict["Raid"] = conquered_board_state 
	return actions_board_states_dict

#Evaluation function
def EVAL(board_state):
	max_points = 0
	min_points = 0
	total_value = 0
	for x in range(1, n+1):
		for y in range(1, n+1):
			if board_state[x][y] == youPlay:
				max_points += int(cell_values[x][y])
			elif board_state[x][y] == opponent:
				min_points += int(cell_values[x][y])
	total_value = max_points - min_points
	return total_value
				
#Max function
def MAX_VAL(board_state, level):
	if level == depth or (not blank_spaces(board_state)):
		return EVAL(board_state)
	level += 1
	val = float("-inf")
	blank_positions = blank_spaces(board_state)
	raid_positions = possible_raid_positions(board_state, youPlay)
	for key in blank_positions.keys():
		for y in range(0, len(blank_positions.get(key))):
			states = [] 
			actions_board_states_dict = apply(board_state,key,blank_positions.get(key)[y], youPlay, raid_positions)
			stake_board_state = actions_board_states_dict.get("Stake")
			states = [ stake_board_state ]
			if actions_board_states_dict.get("Raid"):
				raid_board_state_w_conquer = actions_board_states_dict.get("Raid")
				states.append(raid_board_state_w_conquer)
			for state in states:
				val = max(val,MIN_VAL(state, level))
	return val

#Min function
def MIN_VAL(board_state, level):
	if level == depth or (not blank_spaces(board_state)):
		return EVAL(board_state)
	level += 1
	val = float("inf")
	
	blank_positions = blank_spaces(board_state)
	raid_positions = possible_raid_positions(board_state, opponent)

	for key in blank_positions.keys():
		for y in range(0, len(blank_positions.get(key))):
			states = []
			actions_board_states_dict = apply(board_state,key,blank_positions.get(key)[y], opponent, raid_positions)
			stake_board_state = actions_board_states_dict.get("Stake")
			states = [ stake_board_state ]
			if actions_board_states_dict.get("Raid"):
				raid_board_state_w_conquer = actions_board_states_dict.get("Raid")
				states.append(raid_board_state_w_conquer)
			for state in states:
				val = min(val, MAX_VAL(state, level))
	return val

#Max function
def A_MAX_VAL(board_state, level, alpha, beta):
	if level == depth or (not blank_spaces(board_state)):
		return EVAL(board_state)
	val = float("-inf")
	blank_positions = blank_spaces(board_state)
	raid_positions = possible_raid_positions(board_state, youPlay)
	for key in blank_positions.keys():
		for y in range(0, len(blank_positions.get(key))):
			states = []
			actions_board_states_dict = apply(board_state,key,blank_positions.get(key)[y], youPlay, raid_positions)
			stake_board_state = actions_board_states_dict.get("Stake")
			states = [ stake_board_state ]
			if actions_board_states_dict.get("Raid"):
				raid_board_state_w_conquer = actions_board_states_dict.get("Raid")
				states.append(raid_board_state_w_conquer)
			for state in states:
				val = max(val,A_MIN_VAL(state, level+1, alpha, beta))
				if (val >= beta):
					return val
				alpha = max(alpha, val)
	return val

#Min function
def A_MIN_VAL(board_state, level, alpha, beta):
	if level == depth or (not blank_spaces(board_state)):
		return EVAL(board_state)
	val = float("inf")
	
	blank_positions = blank_spaces(board_state)
	raid_positions = possible_raid_positions(board_state, opponent)
	for key in blank_positions.keys():
		for y in range(0, len(blank_positions.get(key))):
			states = []
			actions_board_states_dict = apply(board_state,key,blank_positions.get(key)[y], opponent, raid_positions)
			stake_board_state = actions_board_states_dict.get("Stake")
			states = [ stake_board_state ]
			if actions_board_states_dict.get("Raid"):
				raid_board_state_w_conquer = actions_board_states_dict.get("Raid")
				states.append(raid_board_state_w_conquer)

			for state in states:
				val = min(val,A_MAX_VAL(state, level+1, alpha, beta))
				if val <= alpha:
					return val
				beta = min(beta, val)
	return val

#Minimax function
def MINIMAX_DECISION(board_state):
	import collections
	moves = collections.OrderedDict()
	values = collections.OrderedDict()
	dict_board_state = {}
	level = 1
	blank_positions = blank_spaces(board_state)

	if(blank_positions):
		raid_positions = possible_raid_positions(board_state, youPlay)

	for key in blank_positions.keys():
		for y in range(0, len(blank_positions.get(key)))
			actions_values_dict = {} 
			position = column_names.get(blank_positions.get(key)[y])+ str(key)
			actions_board_states_dict = apply(board_state,key,blank_positions.get(key)[y], youPlay, raid_positions)
			stake_board_state = actions_board_states_dict.get("Stake")			
			actions_values_dict["Stake"]= MIN_VAL(stake_board_state, level)
			if actions_board_states_dict.get("Raid"):
				raid_board_state_w_conquer = actions_board_states_dict.get("Raid")
				actions_values_dict["Raid w conquer"] = MIN_VAL(raid_board_state_w_conquer, level)

			pos_max_actions = [k for k,v in actions_values_dict.items() if v == max(actions_values_dict.values())]
			#print("position: "+position+" pos_max_actions: ",pos_max_actions)
			if("Stake" in pos_max_actions):
				pos_max_action = "Stake"
				values[position] = actions_values_dict.get("Stake")
				dict_board_state[position] = stake_board_state
			else:
				pos_max_action = "Raid"
				values[position] = actions_values_dict.get("Raid w conquer")
				dict_board_state[position] = raid_board_state_w_conquer

			moves[position] = pos_max_action

	max_keys = [k for k,v in values.items() if v == max(values.values())]
	flag = 0
	print(values)
	print(max_keys)
	max_key = " "
	for key in max_keys:	
		if(moves.get(key) == "Stake"):
			flag = 1
			max_key = key
			break
	if(flag == 0):
		for key in max_keys:
			if(moves.get(key) == "Raid"):
				max_key = key
				break
			
	return max_key, moves.get(max_key), dict_board_state.get(max_key)

#Minimax Alphabeta function
def ALPHABETA_DECISION(board_state):
	import collections
	moves = collections.OrderedDict()
	values = collections.OrderedDict()
	dict_board_state = {}
	level = 1
	val = float("-inf")
	blank_positions = blank_spaces(board_state)
	
	if(blank_positions):
		raid_positions = possible_raid_positions(board_state, youPlay)

	for key in blank_positions.keys():
		for y in range(0, len(blank_positions.get(key))):
			alpha = float("-inf")
			beta = float("inf")
			actions_values_dict = {}
			position = column_names.get(blank_positions.get(key)[y])+ str(key)
			
			actions_board_states_dict = apply(board_state,key,blank_positions.get(key)[y], youPlay, raid_positions)
			stake_board_state = actions_board_states_dict.get("Stake")
			
			actions_values_dict["Stake"] = A_MIN_VAL(stake_board_state, level, alpha, beta)
			val = actions_values_dict["Stake"]
			if val >= beta:
				return val, "Stake", stake_board_state
			alpha = max(alpha, val)
			
			if actions_board_states_dict.get("Raid"):
				raid_board_state_w_conquer = actions_board_states_dict.get("Raid")
				actions_values_dict["Raid w conquer"] = A_MIN_VAL(raid_board_state_w_conquer, level, alpha, beta)
				val = actions_values_dict["Raid w conquer"]
				if val >= beta:
					return val, "Raid", raid_board_state_w_conquer
				alpha = max(alpha, val)
				
			pos_max_actions = [k for k,v in actions_values_dict.items() if v == max(actions_values_dict.values())]
		
			if("Stake" in pos_max_actions):
				pos_max_action = "Stake"
				values[position] = actions_values_dict.get("Stake")
				dict_board_state[position] = stake_board_state
			else:
				pos_max_action = "Raid"
				values[position] = actions_values_dict.get("Raid w conquer")
				dict_board_state[position] = raid_board_state_w_conquer
 
			moves[position] = pos_max_action


	max_keys = [k for k,v in values.items() if v == max(values.values())]
	print(values, max_keys)
	print("moves: ",moves)
	flag = 0
	max_key = " "
	for key in max_keys:	
		if(moves.get(key) == "Stake"):
			flag = 1
			max_key = key
			break
	if(flag == 0):
		for key in max_keys:
			if(moves.get(key) == "Raid"):
				max_key = key
				break	

	return max_key, moves.get(max_key), dict_board_state.get(max_key)

#Output to file
def output_to_file(position, move_type, final_board_state):
	f = open("output.txt","w")
	f.write(position+" "+move_type)
	for x in range(1, n+1):
		f.write("\n")
		for y in range(1, n+1):
			f.write(final_board_state[x][y])

	f.close()



# Main
def main():
	#Read cell values of board
	for x in range(1,n+1):
		line = f.readline().rstrip('\n').split()
		for y in range(0,len(line)):
			z = y + 1
			cell_values[x][z] = line[y]

	board_state = [[0 for i in range(n+1)] for i in range(n+1)]

	#Read board states
	for x in range(1,n+1):
		line = f.readline().rstrip('\n').strip()
		for y in range(0,len(line)):
			z = y + 1
			board_state[x][z] = line[y]
	if(mode == "MINIMAX"):
		position, move_type, max_board_state = MINIMAX_DECISION(board_state)
	elif(mode == "ALPHABETA"):
		position, move_type, max_board_state = ALPHABETA(board_state)

	output_to_file(position, move_type, max_board_state)

main()
