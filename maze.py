#!/usr/bin/python3

import requests

base_url = 'http://ec2-34-216-8-43.us-west-2.compute.amazonaws.com'
myuid = '104928444'

marked_dict = {}
#GAME_OVER = False # responsible for checking 
curr_level = False # responsible for checking if current level is solved
noTime = False

def changeDir(d):
	if (d == 'LEFT'):
		return 'RIGHT'
	if (d == 'RIGHT'):
		return 'LEFT'
	if (d == 'UP'):
		return 'DOWN'
	if (d== 'DOWN'):
		return 'UP'

def solveMaze(d, t, w, h):

	#global GAME_OVER
	global curr_level

	if curr_level == True:
		return True

	r = requests.post('{}/game?token={}'.format(base_url, t), data = {'action': '{}'.format(d)}).json()
	result = r['result']

	if result in ('WALL', 'OUT_OF_BOUNDS'):
		return False
	elif result == 'END':
		curr_level = True
		return True

	details = requests.get('{}/game?token={}'.format(base_url, t)).json()

	x = details['current_location'][0]
	y = details['current_location'][1]

	global marked_dict
	marked_dict[(x, y)] = True


	status = details['status']

	global noTime

	if status == "NONE":
		noTime = True
		return False

	print(result + " Coordinate {} {}".format(x, y))

	
	L = False
	R = False
	U = False
	D = False

	# check if left direction is marked 

	k1 = ((x-1),y)
	k2 = ((x+1),y)
	k3 = (x,(y-1))
	k4 = (x,(y+1))


	if x > 0 and (not marked_dict.get(k1, False)):
		#print("Moving LEFT")
		L = solveMaze("LEFT", t, w, h)

	if x < (w - 1) and (not marked_dict.get(k2, False)):
		#print("Moving RIGHT")
		R = solveMaze("RIGHT", t, w, h)

	if y > 0 and (not marked_dict.get(k3, False)):
		#print("Moving UP")
		U = solveMaze("UP", t, w, h)

	if y < (h - 1) and (not marked_dict.get(k4, False)):
		#print("Moving DOWN")
		D = solveMaze("DOWN", t, w, h)

	#print("End reached for {} {}".format(x, y))

	v = (L or R or U or D)
    
    # if the previous move does not generate any solution, go back
	if not v:
		requests.post('{}/game?token={}'.format(base_url, t), 
				data = {'action': '{}'.format(changeDir(d))}).json()
		return False
	else:
		return True


def playMaze(details, TOKEN):

	global marked_dict
	global curr_level
	#global GAME_OVER

	#total_levels = details['total_levels'] #5

	#print (total_levels)

	#for k in range(total_levels):

	marked_dict = {}

	curr_level = False 	# current level is not over
						# need to be set to false for every iteration


	status = details['status']

	if status in ("NONE", "GAME_OVER"):
		#GAME_OVER = False
		return
	elif status == "FINISHED":
		#GAME_OVER = True
		return

	w = details['maze_size'][0]
	h = details['maze_size'][1]

	x = details['current_location'][0]
	y = details['current_location'][1]

	marked_dict[(x, y)] = True

	print(x)
	print(y)
	print(w)
	print(h)

	if x > 0: 
		print("LEFT")
		if solveMaze("LEFT", TOKEN, w, h) == True:
			print (1)
			return 

	if x < (w - 1): 
		print("RIGHT")
		if solveMaze("RIGHT", TOKEN, w, h) == True:
			print (1)
			return 

	if y > 0: 
		print("UP")
		if solveMaze("UP", TOKEN, w, h) == True:
			print (1)
			return 

	if y < (h - 1): 
		print("DOWN")
		if solveMaze("DOWN", TOKEN, w, h) == True:
			print (1)
			return

	
def main():


	# data is a dictionary
	# make a post call to get the token of a session (represent the beginning of a session)
	r = requests.post('{}/session'.format(base_url), data = {'uid': myuid}).json()
	TOKEN = r['token']

	# use the token we get from post call to make a get request
	details = requests.get('{}/game?token={}'.format(base_url, TOKEN)).json()

	while details['status'] != 'FINISHED':

		# use the token we get from post call to make a get request
		details = requests.get('{}/game?token={}'.format(base_url, TOKEN)).json()

		noTime = False

		if details['status'] in ("NONE", "GAME_OVER"):
			return

		print(details['levels_completed'])
		print(details['status'])

		if details['levels_completed'] == 5:
			print ('yes!!')
			return
 
		playMaze(details, TOKEN)

	print (details['status'])


if __name__ == '__main__':
	main()




















