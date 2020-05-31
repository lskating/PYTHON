"""
def draw_point_line(size, border, point):
	# default boeder = 50
	# point_pos[num_w][num_h](x_pos, y_pos)
	for num_w in range(int((size[0] - 2 * border) / border)):
		pos_temp = []
		for num_h in range(int((size[1] - 2 * border) / border)):
			pos_temp.append([num_w*border + 50, num_h*border + 50])
		point.append(pos_temp)
	# draw vertical line
	for item in point:
		# h_pos.append(item[1])
		start_pos, end_pos = (item[0][0],item[0][1]), (item[len(item) - 1][0],item[len(item) - 1][1])
		# print(start_pos, end_pos)
		pygame.draw.line(screen, line_color, start_pos, end_pos, 1)
	# draw herizonal line
# print(point_pos[0])								# x_pos = 50, y_pos = 50 ~ 550
# print(point_pos[0][0])							# x_pos = 50, y_pos = 50
# print(point_pos[0][len(point_pos[0]) - 1])		# x_pos = 50, y_pos = 550
# # draw_chessboard_line(pos)

	# pygame.draw.line(screen, line_color, start_pos, end_pos, wodth=1)
	# 		TypeError: line() takes no keyword arguments
	# 		error: width --> wodth
"""




# Gobang game 
# Author: simon 
# e-mail: 2441873702@qq.com
# Date  : 2020.05.28

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
	for num_w in range(int((width - 1.5 * border) / border)):
		for num_h in range(int((height - 1.5 * border) / border)):
			rect_point.append([num_w*border + 50, num_h*border + 50])
	for item in rect_point:
		s_rect = item[0], item[1], border, border
		pygame.draw.rect(background, line_color, s_rect, 1)
	return rect_point

# 需要遍历坐标点查看当前位置
# 判断是否结束游戏

def game_over(delay_time):
	import time
	time.sleep(delay_time)
	print("game over!")


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
			draw_flag = True 

	rect_point = []
	background.fill(bg_color)
	draw_chessboard_rect(background, rect_point, border)
	draw_font(background, string=wlc_str)

	count ,black_num, white_num = 0, 0, 0
	for position in mouse_pos:
		# position calculate:
		position[0] = round(position[0] / 50) * 50
		position[1] = round(position[1] / 50) * 50

		# print(position)
		if count % 2 == 0:
			chess_down(background, position, BLACK)
			black_num = black_num + 1
		else:
			chess_down(background, position, WHITE)
			# pygame.draw.circle(background, WHITE, position, 20, 0)
			white_num = white_num + 1
		count = count + 1


	"""
	# screen.blit(black_chess, black_chess_rect)
	if pygame.display.get_active():	
		white_chess_rect = white_chess_rect.move(1, 1)
	screen.blit(white_chess, white_chess_rect)
	"""
	

	screen.blit(background, (0, 0))
	fclock.tick(fps)	# fps each second
	pygame.display.update()
