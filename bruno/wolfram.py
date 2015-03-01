import re
import wolframalpha

class Wolfram():
	def __init__(self):
		self.client = wolframalpha.Client("U2JXWW-P3LYR9XYR6")


	def print_solution(self, expr):
		expr = re.sub(r"\*\*\(_\d+\)", "", expr)
		expr = re.sub(r"_\d+", "", expr)

		print "Searching for solution for equation:"
		print "\t %s" % expr
		res = self.client.query(expr)
		solution = filter(lambda x: x.title == "Solutions", res.pods)
		if not solution:
			solution = filter(lambda x: x.title == "Solution", res.pods)
		if not solution:
			solution = filter(lambda x: x.title == "Derivative", res.pods)
		sol = solution[0].text
		print ""
		print "***"
		print "found solution: %s" % sol
		print "***"
		print ""