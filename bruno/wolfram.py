import re
import wolframalpha

import urllib2
import StringIO



class Wolfram():
	def __init__(self):
		self.client = wolframalpha.Client("U2JXWW-P3LYR9XYR6")


	def get_solutions(self, expr):
		solutions = []
		image = None
		expr = re.sub(r"\*\*\(_\d+\)", "", expr)
		expr = re.sub(r"_\d+", "", expr)

		expr = re.sub(r'(I\^)\((.*)\)(V)\((.*)\)(V)', r'integral from \4 to \2 of ', expr)

		print "Searching for solution for equation:"
		print "\t %s" % expr
		res = self.client.query(expr)

		possible_titles = [
			"Solutions", 
			"Solution", 
			"Exact result", 
			"Computation result",
			"Derivative", 
			"Definite integral", 
			"Indefinite integral"]


		solution_found = False
		for title in possible_titles:
			solution = filter(lambda x: x.title == title, res.pods)
			print title
			print solution
			if solution:
				if title == "Solutions":
					try:
						pod = solution[0]
						for text in pod.node.itertext():
							if text.strip():
								solution_found = True
								solutions.append("%s: %s" % (pod.title, text.strip()))
					except:
						pass
				else:
					solution = solution[0]
					solution_found = True
					solutions.append("%s: %s" % (solution.title, solution.text))


		for pod in res.pods:
			if pod.title not in  ["Plot", "Plots"]:
				continue

			child = pod.main.node.getchildren()[1]
			src = child.get('src')
			width = int(child.get('width'))
			height = int(child.get('height'))
			f = StringIO.StringIO()
			imgRequest = urllib2.Request(src)
			image = urllib2.urlopen(imgRequest).read()
			f.write(image)
			break
		return solutions, f
