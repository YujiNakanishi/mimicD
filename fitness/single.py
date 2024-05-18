'''
/******************************************/
module : mimicD version 2.0
File name : fitness.single.py
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
from mimicD import penalty

'''
/*****************/
Unconstrained
/*****************/
type : fitness class for unconstrained and single optimization
field : function -> <function>
						input -> <np array> (N, D)
						output -> <np array> (N, )
'''
class Unconstrained:

	def __init__(self, function):
		self.function = function

	def getFitness(self, solution):
		print("can't use unconstrained class directory")
		sys.exit()


	'''
	/******************/
	searchElite
	/******************/
	process : return elite from solution
	input : solution, k
		solution -> <solution class>
		k -> <int> num of elite
	output : elites, elite_fitness
		elite -> <solution class>
		elite_evaluation -> <np array> evaluatioin score of elites 
	'''
	def searchElite(self, solution, k = 1):
		evaluation = self.getFitness(solution) #(N, )
		elite_idx = np.argsort(-evaluation)[:k]

		elites = type(solution)(solution.individuals[elite_idx], solution.generation)
		elite_evaluation = evaluation[elite_idx]

		return elites, elite_evaluation

'''
/*****************/
Unconstrained
/*****************/
type : fitness class for constrained and single optimization
field : function, penalties
	function -> <function>
				input -> <np array> (N, D)
				output -> <np array> (N, )
	penalties -> list of penalty class
'''
class Constrained(Unconstrained):
	def __init__(self, function, penalties):
		self.function = function
		self.penalties = penalties

	'''
	/******************/
	searchElite
	/******************/
	process : return feasible elite from solution
	input : solution, k
		solution -> <solution class>
		k -> <int> num of elite
	output : elites, elite_fitness
		elite -> <solution class>
		elite_evaluation -> <np array> evaluatioin score of elites 
	'''
	def searchFeasibleElite(self, solution, k):
		feasible_solution = penalty.Feasibles(solution, self.penalties) #<solution class>

		if feasible_solution is None:
			return None, None
		elif k > len(feasible_solution):
			return None, None
		else:
			return self.searchElite(feasible_solution, k)