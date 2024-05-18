import numpy as np

'''
/*****************/
Flip
/*****************/
Field : pc -> flipping prob
'''
class Flip:

	def __init__(self, pc):
		self.pc = pc

	def mutate(self, solution):
		mutation = np.random.rand(solution.individuals.shape[0], solution.individuals.shape[1])
		mutation = (mutation < self.pc).astye(int)

		mutation += solution.individuals
		mutation = (mutation == 1).astype(int)

		return type(solution)(mutation, solution.generation)