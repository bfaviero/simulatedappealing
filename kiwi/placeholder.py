from drawing import *

class Placeholder:
	def __init__(self, string, x=BIG_SQUARE, y=60*SCALE, big=True, noexponent=False):
		self.big = big
		self.size = BIG_SQUARE if big else SMALL_SQUARE
		self.draw_label_fn = draw_big_label if big else draw_small_label
		self.draw_square_fn = draw_big_square if self.big else draw_small_square
		self.string = string
		self.x = x
		self.y = y
		self.noexponent = noexponent

	def draw_square(self, color=white):
		return
		self.draw_square_fn(self.x, self.y, color=color)

	def fill(self):
		return
		self.draw_square_fn(self.x, self.y, color=black, width=0)

	def shift_and_redraw(self):
		if not self.noexponent:
			self.fill()
			self.x += BIG_SQUARE
			self.draw_square()

	def fill_with_text(self, s, nosquare=False):
		self.fill()
		if nosquare:
			self.draw_square(black)
		else:
			self.draw_square()
		self.draw_label_fn(s, self.x, self.y)

	def get_coords_of_next_exponent_square(self):
		return (self.x+self.size, self.y-SMALL_SQUARE)

	def get_coords_of_next_subponent_square(self):
		return (self.x+self.size, self.y + 2 * SMALL_SQUARE)

	def get_coords_of_next_square(self, has_exponent=False):
		offset = SMALL_SQUARE if has_exponent else 0
		return (self.x+self.size+offset, self.y)

	def get_kiwi_coords(self):
		return (self.x, self.y, self.x+self.size, self.y+self.size)

	def __str__(self):
		return self.string