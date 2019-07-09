import random

def ball():
	ball_list =[]
	while 1:
		a = random.randint(1,33)
		if a not in ball_list:
			ball_list.append(a)
		if len(ball_list)==6:
			break
	ball_list.sort()
	ball_list.append(random.randint(1,16))
	print(ball_list)

ball()