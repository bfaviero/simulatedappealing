import pygame
import re
import sympy
from sympy import sympify, pretty_print
from wolfram import Wolfram
import drawing
from placeholder import Placeholder

placeholders = ['_1', '_2', '_3', '_4', '_5', '_6', '_7, _8, _9']
placeholders_in_use = []

def next_placeholder(x=None, y=None, big=True):
	if x:
		placeholder = Placeholder(placeholders.pop(0), x=x, y=y, big=big)
	else:
		placeholder = Placeholder(placeholders.pop(0))
	placeholders_in_use.append(placeholder)
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


ops = ["+", "/", "*", "=", 'D', '(', ')']
wolfram = Wolfram()

def go():

	expr = "%s" % next_placeholder()

	while True:
		print expr
		to_replace = raw_input("What variable to replace: ")
		if (to_replace == ''):
			expr = expr.replace('D', 'd/dx')
			wolfram.print_solution(expr)
		else:	
			print to_replace
			to_replace = filter(lambda p: p.string == to_replace, placeholders_in_use)[0]
			new_val = raw_input("new value: ")
			to_replace.fill_with_text(new_val)

			has_exponent = False

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
			expr = remove_previous_placeholders(expr, to_replace)
			expr = expr.replace(to_replace.string, new_val + next_main_placeholder.string)

			return_placeholder(to_replace)

go()

