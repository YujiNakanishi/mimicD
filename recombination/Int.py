import numpy as np
import sys
from mimicD.recombination.util import *

'''
/*****************/
OnePointX
/*****************/
type : recombination class
	split gene at the point 1~(D-1) each other.
	children are generated  by exchanging these.
'''
class OnePointX:

	def getOffspring(self, parents):
		checkPare(parents)
		N, D = parents.individuals.shape

		father, mother = setPares(parents) #<np array> (N/2, D)

		partition = np.random.randint(1, D, int(N/2))

		children = []
		for f, m, p in zip(father, mother, partition):
			f_head = f[:p]
			f_tail = f[p:]
			m_head = m[:p]
			m_tail = m[p:]

			child1 = np.concatenate((f_head, m_tail)) #(D, )
			child2 = np.concatenate((m_head, f_tail)) #(D, )
			child = np.stack((child1, child2), axis = 0) #(2, D)
			children.append(child)

		children = np.concatenate(children, axis = 0) #(N, D)

		return type(parents)(children, parents.generation)


'''
/**************/
Switch
/**************/
type recombination class.
Field : pc -> <float> should be 0. < pc < 1.
'''
class Switch:

	def __init__(self, pc = 0.5):
		self.pc = pc

	def getOffspring(self, parents):
		checkPare(parents)

		father, mother = setPares(parents) #<np array> (N/2, D)

		mask = np.random.rand(father.shape[0], father.shape[1]) #(N/2, D)
		mask = (mask < self.pc).astype(int)

		child1 = father*mask+mother*(mask==0) #(N/2, D)
		child2 = father*(mask==0)+mother*mask

		children = np.concatenate((child1, child2))

		return type(children, parents.generation)

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
		offspring1 = (0.5*(father+mother)).astype(int)
		offspring2 = (1.5*father-0.5*mother).astype(int)
		offspring3 = (1.5*mother-0.5*father).astype(int)
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

		offspring1 = (center+(2.*u1-1.)*(0.5+self.alpha)*delta).astype(int) #(N/2, D)
		offspring2 = (center+(2.*u2-1.)*(0.5+self.alpha)*delta).astype(int) #(N/2, D)
		offspring = np.concatenate((offspring1, offspring2)) #(N, D)

		return type(parents)(offspring, parents.generation)