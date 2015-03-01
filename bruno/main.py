import wolframalpha
import pygame
import re
import sympy
from sympy import sympify, pretty_print

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

class Placeholder:
	def __init__(self, string, x=None, y=None, big=False, previous_placeholder=None, coords=None):
		self.string = string
		if coords: 
			self.x = coords[0]
			self.y = coords[1]
		else:
			self.x = x
			self.y = y
		if previous_placeholder:
			self.big = previous_placeholder.big
		else:
			self.big = big

	def fill(self):
		f = draw_big_square if self.big else draw_small_square
		f(self.x, self.y, color=black)

	def fill_with_text(self, s):
		if self.big:
			f = draw_big_label
		else:
			f = draw_small_label
		f(s, self.x, self.y)

	def get_coords_of_next_exponent_square(self):
		size = BIG_SQUARE if self.big else SMALL_SQUARE
		return (self.x+size, self.y-SMALL_SQUARE)

	def get_coords_of_next_square(self):
		size = BIG_SQUARE if self.big else SMALL_SQUARE
		return (self.x+size, self.y)

	def __str__(self):
		return self.string



placeholders = ['_1', '_2', '_3', '_4', '_5', '_6', '_7, _8, _9']
placeholders_in_use = []



def next_placeholder():
	placeholder = placeholders.pop(0)
	placeholders_in_use.append(placeholder)
	return placeholder

def return_placeholder(placeholder):
	placeholders.insert(0, placeholder)
	placeholders_in_use.remove(placeholder)

def process_for_placeholder(s, placeholder):
	index = s.index(placeholder)
	s2 = s[index:]
	s1 = s[:index]
	for placeholder in re.findall(r"_\d+", s1):
		return_placeholder(placeholder)

	s1 = re.sub(r"\*\*\(_\d+\)", "", s1)
	s1 = re.sub(r"_\d+", "", s1)
	return s1+s2

def process_for_printing(s):
	for placeholder in re.findall(r"_\d+", s):
		sympy.var(placeholder)
	s = re.sub(r"\)_", ")*_", s)
	s = re.sub(r'(\d+)([a-z])', r'(\1*\2)', s)
	return s

def pp(s):
	string = process_for_printing(expr)
	string = re.sub(r'(.*)=(.*)', r'Eq(\1,\2)', string)
	sympifyed = sympify(string)
	print ""
	sympy.pprint(sympifyed, use_unicode=False)
	print ""

bars = ["x", "y", "z"]
ops = ["+", "/", "*", "="]

client = wolframalpha.Client("U2JXWW-P3LYR9XYR6")

def print_solution(expr):
	expr = re.sub(r"\*\*\(_\d+\)", "", expr)
	expr = re.sub(r"_\d+", "", expr)

	res = client.query(expr)
	solution = filter(lambda x: x.title == "Solutions", res.pods)
	if not solution:
		solution = filter(lambda x: x.title == "Solution", res.pods)
	sol = solution[0].text
	print "found solution: %s" % sol

expr = "%s" % next_placeholder()




while True:
	print expr
	to_replace = raw_input("What variable to replace: ")
	if (to_replace == ''):
		pp(expr)
		try:
			print_solution(expr)
		except:
			pass
	else:	
		to_replace = filter(lambda p: p == to_replace, placeholders_in_use)[0]
		return_placeholder(to_replace)
		new_val = raw_input("new value: ")
		if new_val not in ops:
			new_val += "**(%s)" % next_placeholder()
		expr = process_for_placeholder(expr, to_replace)
		expr = expr.replace(to_replace, new_val + next_placeholder())

