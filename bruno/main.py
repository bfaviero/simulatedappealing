import pygame
import re
import sympy
from sympy import sympify, pretty_print
from wolfram import Wolfram
import drawing
from placeholder import Placeholder

placeholders = ['_' + str(i) for i in range(0, 10)]
print placeholders
placeholders_in_use = []

def next_placeholder(x=None, y=None, big=True, noexponent=False):
	if x:
		placeholder = Placeholder(placeholders.pop(0), x=x, y=y, big=big, noexponent=noexponent)
	else:
		placeholder = Placeholder(placeholders.pop(0), noexponent=noexponent)
	placeholders_in_use.append(placeholder)
	placeholder.fill_with_text(placeholder.string)
	placeholder.draw_square()
	return placeholder

def return_placeholder(placeholder):
	placeholders.insert(0, placeholder.string)
	placeholders_in_use.remove(placeholder)

def remove_previous_placeholders(s, placeholder):
	print "placeholder"
	print s
	print placeholder.string
	try:
		index = s.index(placeholder.string)
		s2 = s[index:]
		s1 = s[:index]
		for placeholder_string in re.findall(r"_\d+", s1):
			placeholder = filter(lambda p: p.string == placeholder_string, placeholders_in_use)[0]
			placeholder.fill()
			return_placeholder(placeholder)

		s1 = re.sub(r"\*\*\(_\d+\)", "", s1)
		s1 = re.sub(r"_\d+", "", s1)
		return s1+s2
	except:
		return s

def process_for_printing(s):
	#turn placeholders into vaars
	for placeholder_string in re.findall(r"_\d+", s):
		sympy.var(placeholder_string)

	#turn adjacent things into multiplication
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


ops = ["+", "/", "*", "=", 'D', '(']
subscript = ["I", "S"]
wolfram = Wolfram()


def go():

	expr = "%s" % next_placeholder()
	while True:
		print expr
		to_replace = raw_input("What variable to replace: ")
		if (to_replace == ''):
			images = wolfram.get_solutions(expr)
			y = 100 + drawing.BIG_SQUARE
			for title, image in images:
				drawing.draw_small_label(title, 0, y)
				y += drawing.SMALL_SQUARE

				myimage = pygame.image.load(image)
				imagerect = myimage.get_rect()
				imagerect = imagerect.move((0, y))
				size = imagerect.size
				width = size[0]
				height = size[1]
				ideal_height = 150
				scale = ideal_height / float(height)
				scale = 1
				size = (int(width * scale), int(height * scale))
				myimage = pygame.transform.scale(myimage, size)
				myimage = drawing.inverted(myimage)
				drawing.screen.blit(myimage, imagerect)
				pygame.display.flip()
				y += height

		else:	
			print to_replace
			to_replace = filter(lambda p: p.string == to_replace, placeholders_in_use)[0]
			new_val = raw_input("new value: ")
			to_replace.fill()
			to_replace.fill_with_text(new_val)

			has_exponent = False
			if (new_val not in subscript and not to_replace.noexponent):
				if new_val not in ops:
					(x, y) = to_replace.get_coords_of_next_exponent_square()
					if not to_replace.big:
						for p in placeholders_in_use:
							if p.x >= x:
								p.shift_and_redraw()
					new_val += "**(%s)" % next_placeholder(x, y, False).string
					has_exponent = True

				(x, y) = to_replace.get_coords_of_next_square(has_exponent)
				next_main_placeholder = next_placeholder(x, y, to_replace.big)
				if not to_replace.noexponent:
					expr = remove_previous_placeholders(expr, to_replace)
				expr = expr.replace(to_replace.string, new_val + next_main_placeholder.string)
			elif to_replace.noexponent:
				(x, y) = to_replace.get_coords_of_next_square(has_exponent)
				next_main_placeholder = next_placeholder(x, y, to_replace.big, noexponent=True)
				expr = expr.replace(to_replace.string, new_val + next_main_placeholder.string)
			else:
				(x1, y1) = to_replace.get_coords_of_next_exponent_square()
				(x2, y2) = to_replace.get_coords_of_next_subponent_square()
				new_val += "^(%s)V(%s)V" % (
					next_placeholder(x1, y1, False).string, 
					next_placeholder(x2, y2, False, noexponent=True).string)

				(x, y) = to_replace.get_coords_of_next_square(has_exponent)
				next_main_placeholder = next_placeholder(x, y, to_replace.big)
				expr = expr.replace(to_replace.string, new_val + next_main_placeholder.string)
			return_placeholder(to_replace)

go()

