import kiwi
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

MODE_BEST = 0
MODE_TOP = 1
MODE_CL = 2
mode = MODE_BEST

INPUT_RECT = (drawing.SMALL_SQUARE, 60*drawing.SCALE + drawing.BIG_SQUARE, drawing.BIG_SQUARE, drawing.BIG_SQUARE)
INPUT_BOUNDING_BOX = (drawing.SMALL_SQUARE, 60*drawing.SCALE + drawing.BIG_SQUARE, drawing.SMALL_SQUARE + drawing.BIG_SQUARE, 60*drawing.SCALE + drawing.BIG_SQUARE + drawing.BIG_SQUARE)
input_placeholder = Placeholder('xxx', INPUT_RECT[0], INPUT_RECT[1])

def init():
	return
	#input_placeholder.draw_square()

def next_placeholder(placeholders_in_use, x=None, y=None, big=True, noexponent=False):
	if x:
		placeholder = Placeholder(placeholders.pop(0), x=x, y=y, big=big, noexponent=noexponent)
	else:
		placeholder = Placeholder(placeholders.pop(0), noexponent=noexponent)
	placeholders_in_use.append(placeholder)
	placeholders_in_use =  sorted(placeholders_in_use, key= lambda p: -p.x - p.size)
	placeholder.draw_square()
	if mode == MODE_CL:
		placeholder.fill_with_text(str(placeholders_in_use.index(placeholder)))
	return placeholder

def return_all_placeholders():
	while placeholders_in_use:
		placeholder = placeholders_in_use.pop()
		placeholders.append(placeholder.string)


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

def get_solution(expr):
	y = 60*drawing.SCALE + drawing.BIG_SQUARE * 2
	drawing.draw_small_label("Finding solution...", 0, y+50)
	images = wolfram.get_solutions(expr)
	pygame.draw.rect(drawing.screen, drawing.black, (0, y+50, 1000, 1000), 0)
	for title, image in images:
		drawing.draw_small_label(title, 0, y+50)
		y += drawing.SMALL_SQUARE

		myimage = pygame.image.load(image)
		imagerect = myimage.get_rect()
		imagerect = imagerect.move((0, y+50))
		size = imagerect.size
		width = size[0]
		height = size[1]
		"""
		ideal_height = 150
		scale = ideal_height / float(height)
		scale = 1
		size = (int(width * scale), int(height * scale))
		myimage = pygame.transform.scale(myimage, size)
		"""
		myimage = drawing.inverted(myimage)
		drawing.screen.blit(myimage, imagerect)
		pygame.display.flip()
		y += height

def reset(expr):
	pygame.draw.rect(drawing.screen, drawing.black, (0, 0, 1000, 1000), 0)
	pygame.display.update()
	return_all_placeholders()
	expr = "%s" % next_placeholder(placeholders_in_use)
	init()
	return expr

def go():
	init()
	pygame.draw.rect(drawing.screen, drawing.blue, (0, 0, 400*drawing.SCALE, 267*drawing.SCALE), 2)
	pygame.display.update()

	expr = "%s" % next_placeholder(placeholders_in_use)

	while True:

		events = pygame.event.get()
		for event in events:
		    if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
		    	return
		    if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
		    	expr = reset(expr)
		    	break


		bounding_boxes = [placeholder.get_kiwi_coords() for placeholder in placeholders_in_use]
		if mode == MODE_BEST:
			box_index , new_val = kiwi.newBox(bounding_boxes + [INPUT_BOUNDING_BOX])
		elif mode == MODE_CL:
			box_index = int(raw_input('index: '))
			new_val = raw_input('val: ')

		if box_index == -1 or box_index == len(bounding_boxes):
			get_solution(expr)
			continue
		if box_index == -2:
			expr = reset(expr)
			continue

		to_replace = placeholders_in_use[box_index]
		to_replace.fill()
		to_replace.fill_with_text(new_val, nosquare=True)

		has_exponent = False
		if (new_val not in subscript and not to_replace.noexponent):
			if new_val not in ops and False:
				(x, y) = to_replace.get_coords_of_next_exponent_square()
				if not to_replace.big:
					for p in placeholders_in_use:
						if p.x >= x:
							p.shift_and_redraw()
				new_val += "**(%s)" % next_placeholder(placeholders_in_use, x, y, False).string
				has_exponent = True

			(x, y) = to_replace.get_coords_of_next_square(has_exponent)
			next_main_placeholder = next_placeholder(placeholders_in_use, x, y, to_replace.big)
			if not to_replace.noexponent:
				expr = remove_previous_placeholders(expr, to_replace)
			expr = expr.replace(to_replace.string, new_val + next_main_placeholder.string)
		elif to_replace.noexponent:
			(x, y) = to_replace.get_coords_of_next_square(has_exponent)
			next_main_placeholder = next_placeholder(placeholders_in_use, x, y, to_replace.big, noexponent=True)
			expr = expr.replace(to_replace.string, new_val + next_main_placeholder.string)
		else:
			(x1, y1) = to_replace.get_coords_of_next_exponent_square()
			(x2, y2) = to_replace.get_coords_of_next_subponent_square()
			new_val += "^(%s)V(%s)V" % (
				next_placeholder(placeholders_in_use, x1, y1, False).string, 
				next_placeholder(placeholders_in_use, x2, y2, False, noexponent=True).string)

			(x, y) = to_replace.get_coords_of_next_square(has_exponent)
			next_main_placeholder = next_placeholder(placeholders_in_use, x, y, to_replace.big)
			expr = expr.replace(to_replace.string, new_val + next_main_placeholder.string)
		return_placeholder(to_replace)
		if mode == MODE_CL:
			for placeholder in placeholders_in_use:
				placeholder.fill_with_text(str(placeholders_in_use.index(placeholder)))
		if new_val not in ops:	
			get_solution(expr)
go()

