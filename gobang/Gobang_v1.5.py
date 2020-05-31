# Name   : Gobang game 
# Author : simon 
# e-mail : 2441873702@qq.com
# Date   : 2020.05.27 19:02
# version: v5
# http://www.pyinstaller.org/downloads.html   ------>   exe
# http://www.ico51.cn/ 
# https://tool.oschina.net/commons?type=3
# https://github.com/nkiiiiid/Kivy-CN   ---->   apk
# to-do : 增加结束判定，数据统计等，可实现重复游戏 ———— done 2020/05/27
# bug 1 : 当鼠标点击到画布棋盘外仍可显示棋子 ———— fixed 2020/05/28
# bug 2 : 棋子会覆盖之前已经绘制的位置 ———— fixed 2020/05/28
# bug 3 : 棋子数量达到一定时，不会判定结果 ———— partial fixed 2020/05/28
# bug 4 : 在resize到最大化或者是放大后，下面边框无法放置棋子 ———— fixed 2020/05/28


import pygame
import pygame.freetype


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
		if [item[0]-1,item[1]] in position:
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


def success_judge(chess_dict):
	black_pos = []
	white_pos = []
	global white_num
	global black_num
	global successor
	for item in chess_dict:
		x = item.split(",", 1)
		if chess_dict[item] == "white":
			white_pos.append([int(x[0]),int(x[1])])
			white_num = len(white_pos)
		elif chess_dict[item] == "black":
			black_pos.append([int(x[0]),int(x[1])])
			black_num = len(black_pos)
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

def game_mode(num = 1):
	if num == 1:
		# machine challenge
		pass
	else:
		# two person
		pass


# put chess down 
def draw_chess(background, position, color):
	pygame.draw.circle(background, color, position, 20, 0)


mouse_pos = []
black_position = []
white_position = []
white_num = 0
black_num = 0
end_flag = False
key_flag = False
reset_flag = False
info_flag = False
game_info = [total, white_win, black_win] = [0, 0, 0]

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
				if end_flag:
					if event.key == pygame.K_ESCAPE:
						quit_flag = True
					elif event.key == pygame.K_RETURN:
						reset_flag = True
						info_flag = False
			elif event.type == pygame.VIDEORESIZE:
				size = width, height = event.size[0], event.size[1]
				screen = pygame.display.set_mode(size, pygame.RESIZABLE)
				background = pygame.Surface(screen.get_size())

			elif not end_flag:
				if event.type == pygame.MOUSEBUTTONDOWN:
					mouse_pos.append([event.pos[0],event.pos[1]])	# .pos --> tuple = (x_pos,y_pos)

	if quit_flag:
		game_over(background, 0)
	else:
		pass

	if reset_flag:
		mouse_pos = []
		white_num = 0
		black_num = 0
		chess_dict = {}
		reset_flag = False

	rect_point = []
	background.fill(bg_color)
	draw_chessboard_rect(background, rect_point, border)
	draw_font(background, wlc_str, 20, BLACK, position=(10,20))
	
	chess_dict = {}
	count = 0
	for position in mouse_pos:
		# position calculate:
		position[0] = round(position[0] / 50) * 50
		position[1] = round(position[1] / 50) * 50

		# if (width//50 > (position[0]/50) > 0) and (height//50 > (position[1]//50) > 0):		# fix bug 4
		if (round(width/50) > (position[0]/50) > 0) and (round(height/50) > (position[1]//50) > 0):
			key = str(position[0]//50)+","+str(position[1]//50)
			# print(key)
			# chess_flag : None -> no, "white" -> white chess, "black" -> black chess

			if key not in chess_dict:
				key_flag = True
				# chess_flag = None
				if count % 2 == 0:
					chess_color = BLACK
					chess_flag = "black"
				else:
					chess_color = WHITE
					chess_flag = "white"
				count = count + 1
				# 归一化
				new_dict = {key : chess_flag}
				chess_dict.update(new_dict)
				draw_chess(background, position, chess_color)
			else:
				key_flag = False

	draw_font(background, "total:{}  white wins:{}  black wins:{}".format(game_info[0],game_info[1],game_info[2]), 20, BLACK, ((width-450),10))
	draw_font(background, "white chesses:{}  black chesses:{}".format(white_num,black_num), 20, BLACK, ((width-425),30))
	end_flag = success_judge(chess_dict)
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

