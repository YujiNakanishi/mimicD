import numpy as np
import sys
from mimicD.city import *

'''
/*************/
RandomReset
/*************/
Random Resetting
Field : Range, p
	Range -> <list> (D, 2)
		if None -> no limitation for any elements. stepping is from -sys.maxsize-1 to sys.maxsize
		if element is None -> no limitation. stepping is from -sys.maxsize-1 to sys.maxsize
		if element is (None, x) -> stepping is from -sys.maxsize-1 to x
		if element is (x, None) -> stepping is from x to sys.maxsize
		if element is (x, y) -> stepping is from x to y
	p -> <float> probability
'''
class RandomReset:
	def __init__(self, Range, p):
		self.Range = Range
		self.p = p

	def mutate(self, solution):
		N, D = solution.shape() #num of individuals

		if self.Range is None:
			step = np.random.randint(-sys.maxsize-1, sys.maxsize, (N, D))
		else:
			step = []
			for ran in self.Range:
				if ran is None:
					step.append(np.random.randint(-sys.maxsize-1, sys.maxsize, N))
				elif ran[0] is None:
					step.append(np.random.randint(-sys.maxsize-1, ran[1], N))
				elif ran[1] is None:
					step.append(np.random.randint(ran[0], sys.maxsize, N))
				else:
					step.append(np.random.randint(ran[0], ran[1], N))

			step = np.stack(step, axis = 1)
		
		prob = np.random.rand(N, D)
		prob = (prob < self.p)
		mutation = prob*step + (prob==False)*solution.individuals

		return type(solution)(mutation, solution.generation)


'''
/*************/
Creep
/*************/
Creep stepping
Field : step,  p, limit
	step -> <list> (D, )
		if element is None -> stepsize = sys.maxsize
	p -> <float> probability
	limit -> <list> (D, 2)
		if None -> no limitation
		if element is None -> no limitation with respect to this gene
		if [None, x] -> upper limitation
		if [x, None] -> lower limitation
		if [x, y] -> both
'''
class Creep:

	def __init__(self, step, p, limit = None):
		self.step = step
		self.p = p
		self.limit = limit

	def mutate(self, solution):
		N, D = solution.shape()

		#####decide step size
		mutation = []
		for s in self.step:
			if s is None:
				mutation.append(np.random.randint(-sys.maxsize, sys.maxsize, N))
			else:
				mutation.append(np.random.randint(-s, s, N))
		mutation = np.stack(mutation, axis = 1) #(N, D)

		#####mutation
		prob = np.random.rand(N, D)
		prob = (prob < self.p)
		mutation = solution.individuals+prob*mutation

		if self.limit is None:
			return type(solution)(mutation, solution.generation)
		else:
			for idx, lim in enumerate(self.limit):
				if lim is None:
					pass
				else:
					if not(lim[1] is None):
						lim_u = lim[1] #uppper limitation
						judge = (mutation[:,idx] > lim_u)
						mutation[:,idx] = judge*np.ones(N)*lim_u+(judge==False)*mutation[:,idx]
					if not(lim[0] is None):
						lim_l = lim[0] #lower limitation
						judge = (mutation[:,idx] < lim_l)
						mutation[:,idx] = judge*np.ones(N)*lim_l+(judge==False)*mutation[:,idx]

			return type(solution)(mutation, solution.generation)