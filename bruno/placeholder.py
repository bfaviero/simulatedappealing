from drawing import *

class Placeholder:
	def __init__(self, string, x=0, y=100, big=True):
		self.big = big
		self.size = BIG_SQUARE if big else SMALL_SQUARE
		self.draw_label_fn = draw_big_label if big else draw_small_label
		self.draw_square_fn = draw_big_square if self.big else draw_small_square
		self.string = string
		self.x = x
		self.y = y

	def draw_square(self):
		self.draw_square_fn(self.x, self.y, color=red)

	def fill(self):
		self.draw_square_fn(self.x, self.y, color=black)

	def shift_and_redraw(self):
		self.fill()
		self.x += BIG_SQUARE
		self.draw_square()

	def fill_with_text(self, s):
		self.draw_label_fn(s, self.x, self.y)

	def get_coords_of_next_exponent_square(self):
		return (self.x+self.size, self.y-SMALL_SQUARE)

	def get_coords_of_next_square(self, has_exponent=False):
		offset = SMALL_SQUARE if has_exponent else 0
		return (self.x+self.size+offset, self.y)

	def __str__(self):
		return self.string