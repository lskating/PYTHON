"""
# -------------------------------------encoding: UTF-8-------------------------------------
# Name   : Gobang game 
# Author : simon 
# e-mail : 2441873702@qq.com
# Date   : 2020.05.28 19:09
# version: v2.1
# http://www.pyinstaller.org/downloads.html
# http://www.ico51.cn/ 
# https://tool.oschina.net/commons?type=3
# to-do : 增加结束判定，数据统计等，可实现重复游戏 ———— done
# to-do : 添加人机对战模式：目前只能完成鼠标点击前两次的棋子添加动作，但仍存在bug，
          可能有棋子重合的情况——需要对随机候选序列进行剔除，排除可能的选项

# bug 1 : 当鼠标点击到画布棋盘外仍可显示棋子 ———— fixed
# bug 2 : 棋子会覆盖之前已经绘制的位置 ———— fixed
# bug 3 : 棋子数量达到一定时，不会判定结果 ———— fixed
# bug 4 : 在resize到最大化或者是放大后，下面边框无法放置棋子 ———— fixed
# bug 5 : 在可下棋时，无法使用ESC退出游戏 ———— fixed
--------------------------------------------------------------------------------------------
"""

import pygame
import pygame.freetype
import random

# fps setting
fps = 300

# default str value
size = width, height = 800, 600
border = 50 
wlc_str = "Welcome to gobang game!"
successor = ""

# default color
bg_color = (190,190,190) # grey
line_color = 0,0,0

# chess color
WHITE = 255,255,255
BLACK = 0,0,0
RED = 255,0,0
BLUE = 0,0,255
GREEN = 0,255,0
font_color = 0,0,0

pygame.init()
fclock = pygame.time.Clock()
# pygame Surface
screen = pygame.display.set_mode(size, pygame.RESIZABLE)
background = pygame.Surface(screen.get_size())
caption = "Gobang Game"
pygame.display.set_caption(caption)
icon = pygame.image.load('gobang_logo.png')
pygame.display.set_icon(icon)


def draw_font(background, string, font_size, font_color, position=(0,0)):
	# font_type = pygame.freetype.Font('C://Windows//Fonts//msyh.ttc', 1)
	font_type = pygame.freetype.Font('./consola.ttf', 1)	
	font_rect = font_type.render_to(background, position, string, fgcolor=font_color, size=font_size)
	screen.blit(background, (0, 0))

def draw_chessboard_rect(background, rect_point, border):
	x_num = int((width - 1.5 * border) / border)
	y_num = int((height - 1.5 * border) / border)
	for num_w in range(x_num):
		for num_h in range(y_num):
			rect_point.append([num_w*border + 50, num_h*border + 50])
	for item in rect_point:
		s_rect = item[0], item[1], border, border
		pygame.draw.rect(background, line_color, s_rect, 1)
	return rect_point

def success(position):
	for item in position:
		# 行 +
		if [item[0]+1,item[1]] in position:
			if [item[0]+2,item[1]] in position:
				if [item[0]+3,item[1]] in position:
					if ([item[0]+4,item[1]] in position):
						# print("success!")
						return True
		# 行 -
		elif [item[0]-1,item[1]] in position:
			if [item[0]-2,item[1]] in position:
				if [item[0]-3,item[1]] in position:
					if ([item[0]-4,item[1]] in position):
						# print("success!")
						return True
		# 列 +
		elif [item[0],item[1]+1] in position:
			if [item[0],item[1]+2] in position:
				if [item[0],item[1]+3] in position:
					if [item[0],item[1]+4] in position:
						return True
		# 列 -
		elif [item[0],item[1]-1] in position:
			if [item[0],item[1]-2] in position:
				if [item[0],item[1]-3] in position:
					if [item[0],item[1]-4] in position:
						return True
		# 斜对角 + 
		elif [item[0]+1,item[1]+1] in position:
			if [item[0]+2,item[1]+2] in position:
				if [item[0]+3,item[1]+3] in position:
					if [item[0]+4,item[1]+4] in position:
						# print("success!")
						return True
		# 斜对角 - 
		elif [item[0]-1,item[1]-1] in position:
			if [item[0]-2,item[1]-2] in position:
				if [item[0]-3,item[1]-3] in position:
					if [item[0]-4,item[1]-4] in position:
						# print("success!")
						return True
		# 反对角 +
		# fix bug 3
		elif [item[0]+1,item[1]-1] in position:
			if [item[0]+2,item[1]-2] in position:
				if [item[0]+3,item[1]-3] in position:
					if [item[0]+4,item[1]-4] in position:
						# print("success!")
						return True
		# 反对角 -
		# fix bug 3
		elif [item[0]-1,item[1]+1] in position:
			if [item[0]-2,item[1]+2] in position:
				if [item[0]-3,item[1]+3] in position:
					if [item[0]-4,item[1]+4] in position:
						# print("success!")
						return True


def success_judge(chess_dict_all):
	black_pos = []
	white_pos = []
	global successor
	for item in chess_dict_all:
		x = item.split(",", 1)
		if chess_dict_all[item] == "white":
			white_pos.append([int(x[0]),int(x[1])])
		elif chess_dict_all[item] == "black":
			black_pos.append([int(x[0]),int(x[1])])
		else:
			pass

	if success(white_pos) and not success(black_pos):
		successor = "White"
		return True
	elif success(black_pos) and not success(white_pos):
		successor = "Black"
		return True
	elif not success(white_pos) and not success(black_pos):
		successor = ""
		return False


def game_over(background, delay_time):
	import time,sys
	draw_font(background, "game over!", 20, RED, (300,30))
	time.sleep(delay_time)
	sys.exit()


def check_three(position, check_buffer):
	check_buffer = []
	for item in position:
		# 行 +
		if [item[0]+1,item[1]] in position:
			if [item[0]+2,item[1]] in position:
				check_buffer.append(item)
				check_buffer.append([item[0]+1,item[1]])
				check_buffer.append([item[0]+2,item[1]])
				# print("success!")
				return True
		else:
			return False
		"""
		# 行 -
		if [item[0]-1,item[1]] in position:
			if [item[0]-2,item[1]] in position:
				check_buffer.append(item)
				check_buffer.append([item[0]+1,item[1]])
				check_buffer.append([item[0]+2,item[1]])
				# print("success!")
				return True
		# 列 +
		elif [item[0],item[1]+1] in position:
			if [item[0],item[1]+2] in position:
				check_buffer.append(item)
				check_buffer.append([item[0]+1,item[1]])
				check_buffer.append([item[0]+2,item[1]])
				return True
		# 列 -
		elif [item[0],item[1]-1] in position:
			if [item[0],item[1]-2] in position:
				check_buffer.append(item)
				check_buffer.append([item[0]+1,item[1]])
				check_buffer.append([item[0]+2,item[1]])
				return True
		# 斜对角 + 
		elif [item[0]+1,item[1]+1] in position:
			if [item[0]+2,item[1]+2] in position:
				check_buffer.append(item)
				check_buffer.append([item[0]+1,item[1]])
				check_buffer.append([item[0]+2,item[1]])
				# print("success!")
				return True
		# 斜对角 - 
		elif [item[0]-1,item[1]-1] in position:
			if [item[0]-2,item[1]-2] in position:
				check_buffer.append(item)
				check_buffer.append([item[0]+1,item[1]])
				check_buffer.append([item[0]+2,item[1]])
				# print("success!")
				return True
		# 反对角 +
		# fix bug 3
		elif [item[0]+1,item[1]-1] in position:
			if [item[0]+2,item[1]-2] in position:
				check_buffer.append(item)
				check_buffer.append([item[0]+1,item[1]])
				check_buffer.append([item[0]+2,item[1]])
				# print("success!")
				return True
		# 反对角 -
		# fix bug 3
		elif [item[0]-1,item[1]+1] in position:
			if [item[0]-2,item[1]+2] in position:
				check_buffer.append(item)
				check_buffer.append([item[0]+1,item[1]])
				check_buffer.append([item[0]+2,item[1]])
				# print("success!")
				return True
		"""
		# else:
		# 	return False


"""
chess_dict
chess_dict_mouse
chess_dict_machine
"""
# 算法 most important 
# 初始化位置
# 检查敌方是否有3个及以上直接相连的位置并检查是否有连成5个的可能性，
# 若有则堵截靠近落点，若无则落点于己方3个及以上直接相连且有连成5个的可能性的位置旁边
# 
# def get_machine_chess_position(mouse_position, machine_position):
# 	check_buffer = []
# 	print(check_three)
# 	if check_three(mouse_position, check_buffer):
# 		print(check_buffer)
# 		# 需要堵截
# 		return machine_position

def draw_chess_position(mode_flag, mouse_position, machine_position, chess_dict_all, chess_dict_mouse, chess_dict_machine):
	import time
	# normalize position initial
	mouse_position_nor = []
	machine_position_nor = []
	new_mouse_dict = []
	new_mechine_dict = []
	count = 0
	# draw mouse_position
	for position in mouse_position:
		# position rounding:
		position = [round(position[0] / 50) * 50, round(position[1] / 50) * 50]

		# if (width//50 > (pos[0]/50) > 0) and (height//50 > (pos[1]//50) > 0):		# fix bug 4
		if (round(width/50) > (position[0]/50) > 0) and (round(height/50) > (position[1]//50) > 0):
			position_nor = [position[0]//50, position[1]//50]			# normalize [0, 1]
			key = str(position_nor[0])+","+str(position_nor[1])			# key of chess_dict_mouse < chess_dict_all
			# print(key)
			# chess_flag : None -> no, "white" -> white chess, "black" -> black chess

			mouse_position_nor.append(position_nor)					# normalize [[]]
			# print(len(machine_position_nor))
			if key not in chess_dict_all:
				# this condition can draw chess circle
				draw_chess_flag = True
				# draw counter 
				if mode_flag:
					# machine challenge
					chess_color, chess_flag = BLACK, "black"
					new_mouse_dict = {key : chess_flag}
					draw_one_chess(background, position, chess_color)		# un-normalize position of persons
					chess_dict_mouse.update(new_mouse_dict)
					chess_dict_all.update(new_mouse_dict)

					for item_num in range(len(mouse_position_nor)):
						if not mouse_position_nor:							# when mouse_position_nor = [] --> continue
							continue
						# item = mouse_position_nor[item_num]
						# # first and second chess random [] 
						# temp = [[item[0]-1, item[1]-1], [item[0],item[1]-1], [item[0]+1, item[1]-1],[item[0]-1, item[1]], 
						# [item[0]+1, item[1]], [item[0]-1, item[1]+1], [item[0]+2, item[1]-1], [item[0]+1, item[1]-1]]
						# for item_temp in temp:
						# 	if (item_temp in mouse_position_nor) or (item_temp in machine_position_nor):
						# 		del item_temp
						# if item_num == 0:
						# 	machine_position_nor.append([4,5])
						# 	# machine_position_nor.append(temp[first_chess])
						# elif item_num == 1:
						# 	machine_position_nor.append([5,5])
						# 	# machine_position_nor.append(temp[second_chess])
						else:
							machine_position_nor.append([mouse_position_nor[item_num][0]+1,mouse_position_nor[item_num][1]+1])
							# break
						if len(machine_position_nor) > 0:
							for pos in machine_position_nor:
								machine_key = str(pos[0])+","+str(pos[1])
								if machine_key not in chess_dict_all:
									draw_chess_flag = True
									chess_color, chess_flag = WHITE, "white"
									new_mechine_dict = {machine_key : chess_flag}
									position = [pos[0] * 50, pos[1] * 50]		# un-normalize position of machine
									draw_one_chess(background, position, chess_color)
									chess_dict_machine.update(new_mechine_dict)
									chess_dict_all.update(new_mechine_dict)
				else:
					# two person
					if count % 2 == 0:
						chess_color, chess_flag = BLACK, "black"
					else:
						chess_color, chess_flag = WHITE, "white"
					count = count + 1
					new_mouse_dict = {key : chess_flag}
					draw_one_chess(background, position, chess_color)		# un-normalize position of persons
					chess_dict_mouse.update(new_mouse_dict)
					chess_dict_all.update(new_mouse_dict)
			else:
				draw_chess_flag = False


	# check_buffer = []
	# for item in mouse_position:
	# 	if [item[0]+1,item[1]] in mouse_position:
	# 		if [item[0]+2,item[1]] in mouse_position:
	# 			check_buffer.append(item)
	# 			check_buffer.append([item[0]+1,item[1]])
	# 			check_buffer.append([item[0]+2,item[1]])
	# 			print("check success!")

	# # 归一化 mouse_position
	# mouse_position = []
	# for item in chess_dict_mouse:
	# 	x = item.split(",", 1)
	# 	mouse_position.append([int(x[0]),int(x[1])])
	# # time.sleep(0.5)		# 延时的位置应该如何放置？鼠标点击后立即绘制一个颜色的棋子，一定延时后machine给出另一颗棋子
	


	# for item in mouse_position:
	# 	if len(mouse_position) >= 1:
	# 		# 随机函数由于每次循环都会选择一个不同的数字，所以不能使用随机函数来直接进行选择，但是可以间接操作



# put chess down 
def draw_one_chess(background, position, color):
	pygame.draw.circle(background, color, position, 20, 0)


mouse_position = []
machine_position = []
black_position = []
white_position = []
end_flag = False
draw_chess_flag = False
reset_flag = False
info_flag = False
mode_flag = False	# True-->machine, False-->two persons
game_info = [total, white_win, black_win] = [0, 0, 0]
first_chess = int(random.random()*5)
second_chess = int(random.random()*5)

# print(game_info[1])

while True:

	quit_flag = False

	# event manage
	for event in pygame.event.get():
		# quit
		if not quit_flag:
			if event.type == pygame.QUIT:
				quit_flag = True
				break
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					quit_flag = True
				if end_flag:
					if event.key == pygame.K_RETURN:
						reset_flag = True
						info_flag = False
			elif event.type == pygame.VIDEORESIZE:
				size = width, height = event.size[0], event.size[1]
				screen = pygame.display.set_mode(size, pygame.RESIZABLE)
				background = pygame.Surface(screen.get_size())

			elif not end_flag:
				if event.type == pygame.MOUSEBUTTONDOWN:
					mouse_position.append([event.pos[0],event.pos[1]])	# .pos --> tuple = (x_pos,y_pos)

	if quit_flag:
		game_over(background, 0)
	else:
		pass

	if reset_flag:
		mouse_position = []
		machine_position = []
		first_chess = int(random.random()*5)
		second_chess = int(random.random()*5)
		reset_flag = False

	rect_point = []
	background.fill(bg_color)
	draw_chessboard_rect(background, rect_point, border)
	draw_font(background, wlc_str, 20, BLACK, position=(10,20))
	
	chess_dict_all = {}
	chess_dict_mouse = {}
	chess_dict_machine = {}

	draw_chess_position(not mode_flag, mouse_position, machine_position, chess_dict_all, chess_dict_mouse, chess_dict_machine)
	print("chess_dict_all = ",chess_dict_all)
	print("chess_dict_mouse = ",chess_dict_mouse)
	print("chess_dict_machine = ",chess_dict_machine)

	draw_font(background, "total:{}  white wins:{}  black wins:{}".format(game_info[0],game_info[1],game_info[2]), 20, BLACK, ((width-450),10))
	end_flag = success_judge(chess_dict_all)
	if end_flag:
		draw_font(background, "Congradulations! "+successor+" wins!", 20, RED, (int((width-300)/2),30))
		draw_font(background, "Please press ENTER to restart!", 40, WHITE, (int((width-650)/2),int((height-50)/2)))
		if not info_flag:
			total = total + 1
			if successor == "White":
				white_win = white_win + 1
			elif successor == "Black":
				black_win = black_win + 1
			game_info = [total, white_win, black_win]
			info_flag = not info_flag

	screen.blit(background, (0,0))
	fclock.tick(fps)
	pygame.display.update()

