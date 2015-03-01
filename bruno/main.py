import pygame
import re
import sympy
from sympy import sympify, pretty_print
from wolfram import Wolfram
import drawing

placeholders = ['_1', '_2', '_3', '_4', '_5', '_6', '_7, _8, _9']
placeholders_in_use = []

def next_placeholder():
	placeholder = placeholders.pop(0)
	placeholders_in_use.append(placeholder)
	return placeholder

def return_placeholder(placeholder):
	placeholders.insert(0, placeholder)
	placeholders_in_use.remove(placeholder)

def remove_previous_placeholders(s, placeholder):
	index = s.index(placeholder)
	s2 = s[index:]
	s1 = s[:index]
	for placeholder in re.findall(r"_\d+", s1):
		return_placeholder(placeholder)

	s1 = re.sub(r"\*\*\(_\d+\)", "", s1)
	s1 = re.sub(r"_\d+", "", s1)
	return s1+s2

def process_for_printing(s):
	#turn placeholders into vaars
	for placeholder in re.findall(r"_\d+", s):
		sympy.var(placeholder)

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


ops = ["+", "/", "*", "="]
wolfram = Wolfram()
drawing.init()

def go():

	expr = "%s" % next_placeholder()

	while True:
		print expr
		to_replace = raw_input("What variable to replace: ")
		if (to_replace == ''):
			wolfram.print_solution(expr)
		else:	
			to_replace = filter(lambda p: p == to_replace, placeholders_in_use)[0]

			new_val = raw_input("new value: ")
			if new_val not in ops:
				new_val += "**(%s)" % next_placeholder()
			expr = remove_previous_placeholders(expr, to_replace)

			expr = expr.replace(to_replace, new_val + next_placeholder())

			return_placeholder(to_replace)

go()

