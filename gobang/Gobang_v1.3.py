# Name   : Gobang game 
# Author : simon 
# e-mail : 2441873702@qq.com
# Date   : 2020.05.27 19:02
# version: v3
# http://www.pyinstaller.org/downloads.html
# http://www.ico51.cn/ 
# bug 1 : 当鼠标点击到画布棋盘外仍可显示棋子 ———— fixed
# bug 2 : 棋子会覆盖之前已经绘制的位置 ———— fixed
# bug 3 : 棋子数量达到一定时，不会判定结果


import pygame
import pygame.freetype


# fps setting
fps = 300

# default str value
size = width, height = 800, 600
border = 50 
wlc_str = "Welcom to gobang game!"
successor = ""

# default color
bg_color = (128,138,135)	#pygame.Color("white")
line_color = 0,0,0

# chess color
WHITE = 255,255,255
BLACK = 0,0,0
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


def draw_font(background, string='Hello pygame!',font_size=20, positon=(0,0)):
	# font_type = pygame.freetype.Font('C://Windows//Fonts//msyh.ttc', 1)
	font_type = pygame.freetype.Font('./consola.ttf', 1)	
	font_rect = font_type.render_to(background, positon, string, fgcolor=font_color, size=font_size)
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

def success(positon):
	for item in positon:
		# 行
		if [item[0]+1,item[1]] in positon:
			if [item[0]+2,item[1]] in positon:
				if [item[0]+3,item[1]] in positon:
					if ([item[0]+4,item[1]] in positon):
						# print("success!")
						return True
		# 列
		elif [item[0],item[1]+1] in positon:
			if [item[0],item[1]+2] in positon:
				if [item[0],item[1]+3] in positon:
					if [item[0],item[1]+4] in positon:
						return True
		# 对角
		elif [item[0]+1,item[1]+1] in positon:
			if [item[0]+2,item[1]+2] in positon:
				if [item[0]+3,item[1]+3] in positon:
					if [item[0]+4,item[1]+4] in positon:
						# print("success!")
						return True
		else:
			return False


def success_judge(chess_dict):
	black_pos = []
	white_pos = []
	global successor
	# print(chess_dict)
	# {'10,4': 2, '10,5': 1, '6,4': 2, '6,5': 1, '8,7': 2, '5,7': 1, '6,9': 2, '9,4': 1, '9,6': 2, '10,8': 1}
	for item in chess_dict:
		x = item.split(",", 1)
		if chess_dict[item] == 1:
			white_pos.append([int(x[0]),int(x[1])])
		else:
			black_pos.append([int(x[0]),int(x[1])])
	
	print("white_pos = ", white_pos)
	print("black_pos = ", black_pos)

	if success(white_pos):
		successor = "white"
		return True
	elif success(black_pos):
		successor = "black"
		return True
	else:
		return False
"""
		if success(white_pos):
			successor = "white"
			return True
			continue
		elif success(black_pos):
			successor = "black"
			return True
			continue
"""

def game_over(background, delay_time):
	import time,sys
	draw_font(background, string="game over!")
	time.sleep(delay_time)
	sys.exit()


# put chess down 
def chess_down(background, position, color):
	pygame.draw.circle(background, color, position, 20, 0)



mouse_pos = []
black_position = []
white_position = []
key_flag = 0
endflag = False
while True:
	# event manage
	for event in pygame.event.get():
		# quit

		if event.type == pygame.QUIT:
			game_over(background, 0.3)
			
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				game_over(background, 0.1)

		# elif event.type == pygame.KEYDOWN:
		# 	if event.key == 'K_RETURN':
		# 		endflag = 0
		# window resize
		elif event.type == pygame.VIDEORESIZE:
			size = width, height = event.size[0], event.size[1]
			screen = pygame.display.set_mode(size, pygame.RESIZABLE)
			background = pygame.Surface(screen.get_size())
		elif endflag:
			continue
		elif event.type == pygame.MOUSEBUTTONDOWN:
			mouse_pos.append([event.pos[0],event.pos[1]])	# .pos --> tuple = (x_pos,y_pos)

	rect_point = []
	background.fill(bg_color)
	draw_chessboard_rect(background, rect_point, border)
	draw_font(background, string=wlc_str)

	chess_dict = {}
	count = 0
	for position in mouse_pos:
		# position calculate:
		position[0] = round(position[0] / 50) * 50
		position[1] = round(position[1] / 50) * 50

		if (width//50 > round(position[0]/50) > 0) and (height//50 > round(position[1]//50) > 0):
			key = str(position[0]//50)+","+str(position[1]//50)
			# print(key)
			# flags 
			# 0 -- no
			# 1 -- white
			# 2 -- black

			if key not in chess_dict:
				key_flag = 1
				# flags = 0
				if count % 2 == 0:
					chess_color = BLACK
					flags = 2
				else:
					chess_color = WHITE
					flags = 1
				count = count + 1
				# 归一化
				new_dict = {key : flags}
				chess_dict.update(new_dict)
				chess_down(background, position, chess_color)
			else:
				key_flag = 0
	print(chess_dict)
	endflag = success_judge(chess_dict)	# judgement advancement to fix bug 3
	if endflag:
		draw_font(background, string="Congradulations! "+successor+" wins!",font_size=20, positon=(300,20))
		# endflag = success_judge(chess_dict)		# error bug 3
	# endflag = success_judge(chess_dict)			# error bug 3



	screen.blit(background, (0,0))
	fclock.tick(fps)
	pygame.display.update()

