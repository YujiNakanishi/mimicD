'''
/******************************************/
module : mimicD version 2.0
File name : city.py
Author : Yuji Nakanishi
Latest update : 2021/3/24
/******************************************/
list of some functions with respect to Solution

'''

import numpy as np

'''
/**************/
isIn
/**************/
process : check wheter individuals in solution1 is also in solution2 or not.
input : solution1, solution2 -> <Solution class>
output : <np array> (N, ). if in, True.
'''
def SisIn(solution1, solution2):
	return np.array([(sol in solution2()) for sol in solution1()])

'''
/**************/
remove
/**************/
process : remove individuals from solution1 which is also in solution2 
input : solution1, solution2 -> <Solution class>
output : <Solution class>
'''
def Sremove(solution1, solution2):
	judge = (isIn(solution1, solution2) == False)
	new_individuals = solution1.individuals[judge]

	return type(solution1)(new_individuals, solution1.generation)

def Scopy(solution):
	return type(solution)(solution.individuals.copy(), solution.generation)


def Sconcatenate(solutions):
	individuals = np.concatenate([s.individuals.copy() for s in solutions], axis = 1)
	oldest_gene = np.max(np.array([s.generation for s in solutions]))

	return type(solutions[0])(individuals, oldest_gene)