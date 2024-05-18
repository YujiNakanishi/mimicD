'''
/******************************************/
module : mimicD version 2.0
File name : fitness.multi.py
Author : Yuji Nakanishi
Latest update : 2021/3/24
/******************************************/



fitness class, especially, "getFunction" can be defined by user.
this class has a function as a field which input is (N, D)s <np array> and output is (N, )s <np array> = evaluation score.
input of "getFunction" should be only solution class, and output of this should be (N, )s <np array>.


Class list:
Function list:
'''

import numpy as np
import sys
from mimicD.city import *
from mimicD import penalty


def NaiveSearch(evalfield, solution):
	individuals = np.copy(solution.individuals)

	_pareto = []

	for eval1, individual1 in zip(evalfield, individuals):
		dominated = False
		for eval2, individual2 in zip(evalfield, individuals):
			dominated = np.all(eval1 < eval2) #wheter individual1 is dominated by 2 or not.
			if dominated:
				break

		if dominated == False:
			_pareto.append(individual1)

	_pareto = np.stack(_pareto, axis = 0)
	
	return type(solution)(_pareto, solution.generation)


'''
/***************/
Unconstrained
/***************/
type : multi objective fitness
Field : multi_fitness -> <list> fitness class
'''
class Unconstrained:

	def __init__(self, multi_fitness):
		self.multi_fitness = multi_fitness

	def getEvalField(self, solution):
		evalfield = np.stack([fitness.getFitness(solution) for fitness in multi_fitness], axis = -1) #(N, m)
		return evalfield

	'''
	/**************/
	searchPareto
	/**************/
	process : return pareto individuals
	input : solution,  way
		solution -> <solution class>
		way -> <str> searching method
			"Naive" -> Naive search
	output : <solution> pareto individuals
	'''
	def searchPareto(self, solution, way = "Naive"):
		evalfield = self.getEvalField(solution)

		if way == "Naive":
			return NaiveSearch(evalfield, solution)
		else:
			print("unsupported")
			sys.exit()

	'''
	/**************/
	getNonDominatedRank
	/**************/
	process : return ranking
	input : solution,  way
		solution -> <solution class>
		way -> <str> searching method
			"Naive" -> Naive search
	output : <np array> (N, )  ranking
	'''
	def getNonDominatedRank(self, solution, way = "Naive"):
		ranking = np.zeros(len(solution))
		num = 0 #the number of ranked individuals
		MomentRank = 0

		candidate = Scopy(solution)

		while num < len(solution):
			MomentElite = self.searchPareto(candidate, way) #<solution class>
			ranked_individuals = SisIn(solution, MomentElite)
			ranking[ranked_individuals] = MomentRank

			MomentRank += 1
			num += np.sum(ranked_individuals)

			candidate = Sremove(candidate, MomentElite)

		return ranking