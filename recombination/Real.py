import numpy as np
import sys
from mimicD.recombination.util import *


'''
/***************/
Linear
/***************/
type : recombination class.
	generate 0.5X+0.5Y, 1.5X-0.5Y, -0.5X+1.5Y childrens from X Y parents.
	pick up two greater childrens from three.
Field : fitness -> <Fitness class>
'''
class Linear:

	def __init__(self, fitness, point = None):
		self.fitness = fitness

	def getOffspring(self, parents):
		checkPare(parents)

		#####matching
		father, mother = setPares(parents) #<np array> (N/2, D)

		#####generate offspring
		offspring1 = 0.5*(father+mother)
		offspring2 = 1.5*father-0.5*mother
		offspring3 = 1.5*mother-0.5*father
		offspring = np.stack((offspring1, offspring2, offspring3), axis = 1) #(N/2, 3, D)
		
		selection = []
		for offs in offspring:
			#offs -> <np array> (3, D)
			evaluation = self.fitness.getFitness(type(parents)(offs)) #<np array> (3, )
			eval_sort = np.argsort(-evaluation)

			selection.append(np.stack((offs[eval_sort[0]], offs[eval_sort[1]]), axis = 0)) #(2, D)

		selection = np.concatenate(selection, axis = 0) #(N, D)

		return type(parents)(selection, parents.generation)


'''
/**************/
BLX_alpha
/**************/
type : recombination class
input : 
'''
class BLX_alpha:

	def __init__(self, alpha = 0.5):
		self.alpha = alpha

	def getOffspring(self, parents):
		checkPare(parents)
		
		N, D = parents.individuals.shape
		father, mother = setPares(parents) #<np array> (N/2, D)

		center = (father+mother)/2.
		delta = np.abs(father-mother)

		u1 = np.random.rand(int(N/2), D)
		u2 = np.random.rand(int(N/2), D)

		offspring1 = center+(2.*u1-1.)*(0.5+self.alpha)*delta #(N/2, D)
		offspring2 = center+(2.*u2-1.)*(0.5+self.alpha)*delta #(N/2, D)
		offspring = np.concatenate((offspring1, offspring2)) #(N, D)

		return type(parents)(offspring, parents.generation)