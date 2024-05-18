'''
/******************************************/
module : mimicD version 3.0
File name : fitness.__init__.py
Author : Yuji Nakanishi
Latest update : 2021/3/25
/******************************************/


Class list:
Function list:
'''

import numpy as np
from mimicD.fitness import single, multi



'''
/*****************/
Windowing
/*****************/
process : window procedure
input : evaluation, window
	evaluation -> <np array> (N, ) evaluation score
	window -> <"least" or float> window step
		"least" -> value for making any evaluations greater than zero.
output : <np array> (N, ) fixed evaluation score.
'''
def Windowing(evaluation, window = "least"):
	if window == "least":
		window = np.min(evaluation)

	w_evaluation = evaluation+abs(window)

	return w_evaluation

'''
/*****************/
Deb2000
/*****************/
process : penalty containing evaluation score proposed by Deb(2000)
input : solution, evaluation, penalties
	solution -> <solution class>
	evaluation -> <np array> (N, ) evaluation score
	penalties -> <list> penalty
output : Deb2000_evaluation -> <np array> (N, )
'''
def Deb2000(solution, evaluation, penalties):
	feasible = np.ones(len(solution)).astype(bool)
	violation = np.zeros(len(solution))

	for _penalty in penalties:
		feasible *= _penalty.Feasible(solution)
		violation += _penalty.Violation(solution)

	if np.all((feasible==False)):
		return -violation
	else:
		feasible_evaluation = evaluation[feasible]

		Deb2000_evaluation = np.copy(evaluation)
		Deb2000_evaluation *= feasible

		fitness_level = np.min(feasible_evaluation)
		Deb2000_evaluation += (feasible==False)*(fitness_level-violation)

	return Deb2000_evaluation


'''
/***************/
getDistance
/***************/
process : return euclide distance between individuals
input : <solution class>
output : distance -> <np array> (N, N)
		distance[i, j] = euclide distance between solution[i] and solution[j]
'''
def getDistance(solution):
	blockA = np.expand_dims(solution.individuals, axis = 1)
	blockA = np.repeat(blockA, len(solution), axis = 1)
	blockB = np.expand_dims(solution.individuals, axis = 0)
	blockB = np.repeat(blockB, len(solution), axis = 0)

	distance = np.power(blockA-blockB, 2)
	distance = np.sum(distance, axis = -1)
	distance = np.sqrt(distance)

	return distance


'''
/***************/
Sharing
/***************/
process : sharing procedure toward evaluation score
input : solution, evaluation, alpha, sigma
	solution -> <solution class>
	evaluation -> <np array> (N, ) evaluation score
	alpha -> <float>
	sigma -> <float>
output : <np array> (N, )
'''
def Sharing(solution, evaluation, alpha, sigma):
	d = getDistance(solution)

	sh_d = 1.-np.power(d/sigma, alpha)
	sh_d[d>sigma] = 0.
	sum_sh_d = np.sum(sh_d, axis = 1)

	return evaluation/sum_sh_d