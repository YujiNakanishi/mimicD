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
BinaryUniform
/**************/
type recombination class.
	binary uniform recombination
Field : pc -> <float> should be 0. < pc < 1.
'''
class BinaryUniform:

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