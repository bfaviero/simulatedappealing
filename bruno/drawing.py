import pygame

red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
darkBlue = (0,0,128)
white = (255,255,255)
black = (0,0,0)
pink = (255,200,200)

SMALL_SQUARE = 10
SMALL_FONT = 8
BIG_SQUARE = 20
BIG_FONT = 18

pygame.init()
small_font = pygame.font.SysFont('Arial', SMALL_FONT)
big_font = pygame.font.SysFont('Arial', BIG_FONT)
screen = pygame.display.set_mode((400, 400))

def draw_small_square(x, y, color=red):
	draw_square(x, y, size=SMALL_SQUARE, color=color)

def draw_big_square(x, y, color=red):
	draw_square(x, y, size=BIG_SQUARE, color=color)

def draw_square(x, y, size, color=red, screen=screen):
	pygame.draw.rect(screen, color, (x, y, size, size), 1)
	print "done"
	pygame.display.update()

def draw_label(s, x, y, font, color=red):
	label = font.render(s, 1, color)
	screen.blit(label, (x, y))
	pygame.display.update()

def draw_small_label(s, x, y):
	draw_label(s, x, y, font=small_font)

def draw_big_label(s, x, y):
	draw_label(s, x, y, font=big_font)