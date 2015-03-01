import pygame

red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
darkBlue = (0,0,128)
white = (255,255,255)
black = (0,0,0)
pink = (255,200,200)

SCALE = 3
SCREEN_SIZE = int(400*SCALE)
SMALL_SQUARE = int(10*SCALE)
SMALL_FONT = int(8*SCALE)
BIG_SQUARE = int(20*SCALE)
BIG_FONT = int(18*SCALE)

pygame.init()
small_font = pygame.font.SysFont('Arial', SMALL_FONT)
big_font = pygame.font.SysFont('Arial', BIG_FONT)
screen = pygame.display.set_mode((1280, 720))

def inverted(img):
  inv = pygame.Surface(img.get_rect().size, pygame.SRCALPHA)
  inv.fill((255,255,255,255))
  inv.blit(img, (0,0), None, pygame.BLEND_RGB_SUB)
  return inv

def draw_small_square(x, y, color=white, width=1):
	draw_square(x, y, size=SMALL_SQUARE, color=color, width=width)

def draw_big_square(x, y, color=white, width=1):
	draw_square(x, y, size=BIG_SQUARE, color=color, width=width)

def draw_square(x, y, size, color=white, screen=screen, width=1):
	pygame.draw.rect(screen, color, (x, y, size, size), width)
	pygame.display.update()

def draw_label(s, x, y, font, color=white):
	label = font.render(s, 1, color)
	screen.blit(label, (x, y))
	pygame.display.update()

def draw_small_label(s, x, y):
	draw_label(s, x, y, font=small_font)

def draw_big_label(s, x, y):
	draw_label(s, x, y, font=big_font)