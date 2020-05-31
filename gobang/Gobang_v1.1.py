# Name  : Gobang game 
# Author: simon 
# e-mail: 2441873702@qq.com
# Date  : 2020.05.27 17:56
# version: v2
# To-do : 实现胜负功能判断
# bug 1 : 当鼠标点击到画布棋盘外仍可显示棋子
# bug 2 : 棋子会覆盖之前已经绘制的位置 ———— fixed


import pygame,sys
import pygame.freetype

pygame.init()

fps = 300 # fps setting
fclock = pygame.time.Clock()

# default str value
size = width, height = 800, 600
border = 50 
wlc_str = "Welcom to gobang game!"

# default color
bg_color = (128,138,135)#pygame.Color("white")
line_color = pygame.Color("black")
# chess color
WHITE = 255,255,255
BLACK = 0,0,0
font_color = 0,0,0

# pygame Surface
screen = pygame.display.set_mode(size, pygame.RESIZABLE)
background = pygame.Surface(screen.get_size())

caption = "Gobang Game"
pygame.display.set_caption(caption)

"""
# chess pic path
# black_chess = pygame.image.load("./black.png")
# black_chess_rect = black_chess.get_rect()
# white_chess = pygame.image.load("./white.png")
# white_chess_rect = white_chess.get_rect()
# print(black_chess_rect)		#<rect(0, 0, 65, 64)>
"""

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

def success_judge(chess_dict):
	# {'10,5': 2, '9,6': 1, '10,9': 2, '12,9': 1, '12,7': 2, '9,7': 1, '6,7': 2}

	pass

def game_over(delay_time):
	import time
	time.sleep(delay_time)
	print("game over!")

# put chess down 
def chess_down(background, position, color):
	pygame.draw.circle(background, color, position, 20, 0)




mouse_pos = []
while True:
	# event manage
	for event in pygame.event.get():
		# quit
		if event.type == pygame.QUIT:
			game_over(0.1)
			sys.exit()
		# window resize
		elif event.type == pygame.VIDEORESIZE:
			size = width, height = event.size[0], event.size[1]
			screen = pygame.display.set_mode(size, pygame.RESIZABLE)
			background = pygame.Surface(screen.get_size())
		elif event.type == pygame.MOUSEBUTTONDOWN:
			mouse_pos.append([event.pos[0],event.pos[1]])	# .pos --> tuple = (x_pos,y_pos)


	rect_point = []
	background.fill(bg_color)
	draw_chessboard_rect(background, rect_point, border)
	draw_font(background, string=wlc_str)

	chess_dict = {}
	count, black_num, white_num = 0, 0, 0
	for position in mouse_pos:
		# position calculate:
		position[0] = round(position[0] / 50) * 50
		position[1] = round(position[1] / 50) * 50

		key = str(position[0]//50)+","+str(position[1]//50)
		# flags 
		# 0 -- no
		# 1 -- white
		# 2 -- black

		if key in chess_dict:
			# cannot put down the chess
			print("can't put chess here!")
		else:
			# flags = 0
			if count % 2 == 0:
				chess_color = BLACK
				flags = 2
				black_num = black_num + 1
			else:
				chess_color = WHITE
				flags = 1
				# pygame.draw.circle(background, WHITE, position, 20, 0)
				white_num = white_num + 1
			count = count + 1
			# 归一化
			new_dict = {key : flags}
			chess_dict.update(new_dict)
			chess_down(background, position, chess_color)

	success_judge(chess_dict)
	print(chess_dict)
	screen.blit(background, (0, 0))
	fclock.tick(fps)	# fps each second
	pygame.display.update()
