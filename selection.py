'''
/******************************************/
module : mimicD version 2.0
File name : selection.py
Author : Yuji Nakanishi
Latest update : 2021/3/24
/******************************************/
selection procedure is defined by class.
you can create original selection class as long as this new class has "Select" function.
Futhermore, input of "getOffspring" should have only solution class and evaluation(np array or Fitness class).
'''

import numpy as np
from mimicD.city import *

'''
/****************/
GENITOR
/****************/
type selection class
	return the greatest individuals
Field : candidate_num -> <int> candidate number. should be lower than individuals
'''
class GENITOR:

	def __init__(self, candidate_num):
		self.candidate_num = candidate_num

	'''
	/*******************/
	Select
	/*******************/
	input : solution, evaluation
		solution -> <solution class>
		evaluation -> <np array> or <Fitness class>
			<np array> -> (N, ) evaluation score of each individuals
			<Fitness class> -> calc score here
	'''
	def Select(self, solution, evaluation):
		if type(evaluation) != np.ndarray:
			evaluation = evaluation.getFitness(solution)
		####from here, evaluation -> <np array> (N, )

		index = np.argsort(-evaluation)
		survivor = np.copy(solution.individuals[index[:self.candidate_num]])

		return type(solution)(survivor, solution.generation)


'''
/****************/
FPS
/****************/
type selection class
	return individuals by FPS
Field : selection_num -> <int> selection number. if None, equal to solution num.
'''
class FPS:

	def __init__(self, selection_num = None):
		self.selection_num = selection_num

	def Select(self, solution, evaluation):
		selection_flag = False
		if self.selection_num is None:
			self.selection_num = len(solution)
			selection_flag = True

		if type(evaluation) != np.ndarray:
			evaluation = evaluation.getFitness(solution)
		####from here, evaluation -> <np array> (N, )

		probability = evaluation/np.sum(evaluation)
		selection_index = np.random.choice(len(solution), self.selection_num, p = probability)

		if selection_flag:
			self.selection_num = None

		return type(solution)(solution.individuals[selection_index], solution.generation)



def choose_winner(solution, evaluation, k, replacement, choose_index):
	candidate_index = np.random.choice(choose_index, k, replace = False)
	candidate = solution.individuals[candidate_index] #(k, D)
	candidate_evaluation = evaluation[candidate_index] #(k, )

	if replacement == False:
		choose_index = choose_index[np.isin(choose_index, candidate_index) == Falses]

	winner = candidate[np.argmax(candidate_evaluation)] #(D, )

	return choose_index, winner


'''
/****************/
FPS
/****************/
type selection class
	return individuals by Tournament
Field : k, selection_num, replacement
	k -> <int> num of individual in one game
	selection_num -> <int> selection number. if None, equal to solution num.
	replacement -> <bool> wheter let loser try another game or not.
'''
class Tournament:

	def __init__(self, k = 2, selection_num = None, replacement = True):
		self.k = k
		self.selection_num = selection_num
		self.replacement = replacement

	def Select(self, solution, evaluation):
		selection_flag = False
		if self.selection_num is None:
			self.selection_num = len(solution)
			selection_flag = True

		selection_cpy = Scopy(solution)

		if type(evaluation) != np.ndarray:
			evaluation = evaluation.getFitness(solution)
		####from here, evaluation -> <np array> (N, )

		choose_index = np.arange(len(solution))

		selection_individuals = []

		for itr in range(self.selection_num):
			choose_index, winner = choose_winner(solution, evaluation, self.k, self.replacement, choose_index)
			selection_individuals.append(winner)

		selection_individuals = np.stack(selection_individuals, axis = 0)

		if selection_flag:
			self.selection_num = None


		return type(solution)(selection_individuals, solution.generation)