'''
/******************************************/
module : mimicD version 3.0
File name : __init__.py
Author : Yuji Nakanishi
Latest update : 2021/3/25
/******************************************/
mimicD assumes optimization = maximization


Class list:
Function list:
'''

import numpy as np
import sys
from mimicD.city import *
from mimicD import fitness, mutation, recombination, penalty, selection

'''
/******************/
Solution
/******************/
type : class
Field : individuals, generation
	individuals -> <np array> (N, D)
	generation -> <int> generation
'''
class Solution:

	def __init__(self, individuals, generation = 1):
		self.individuals = individuals.copy()
		self.generation = generation

	def __len__(self):
		return len(self.individuals)

	def __getitem__(self, index):
		return self.individuals[index]

	def __call__(self):
		return self.individuals

	def __str__(self):
		print(self.individuals)
		return ""

	def shape(self):
		return self.individuals.shape

	'''
	/******************/
	split
	/******************/
	process : split gene
	input : idx -> <tuple> index
	output : <list> solution class
	Note : if idx = (2, 4) with respect to (100, 8) solution
		splited solution shape is (100, 2), (100, 2) and (100, 4)
	'''
	def split(self, index):
		individuals = self.individuals.copy()
		split_individuals = []

		index = [0]+[i for i in index]

		for i in range(len(index)-1):
			split_individuals.append(individuals[:,index[i]:index[i+1]])
		split_individuals.append(individuals[:,index[-1]:])

		solutions = [type(self)(si, self.generation) for si in split_individuals]

		return solutions