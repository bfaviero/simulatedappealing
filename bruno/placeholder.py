from drawing import *

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