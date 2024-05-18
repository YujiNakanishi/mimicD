'''
/******************************************/
module : mimicD version 2.0
File name : penalty.py
Author : Yuji Nakanishi
Latest update : 2021/3/24
/******************************************/
you can define penalty class.
penalty class should have Violation function.
Input of this is <np array> (N, D) and output is (N, )
penalty is always greater than zero. If zero -> feasible, and if large -> large penalty.

Class list:
Function list:
'''

import numpy as np
import sys

'''
/**************/
Faesible
/**************/
process : return feasible individuals
input : solution, penalties
	solution -> <solution class>
	penalties -> <list> penalty class
output : <solution class> feasible individuals
'''
def Feasibles(solution, penalties):
	feasible = np.ones(len(solution)).astype(bool)
	for _penalty in penalties:
		feasible *= _penalty.Feasible(solution)

	if np.all((feasible == False)):
		return None
	else:
		return type(solution)(solution.individuals[feasible], solution.generation)

'''
/**************/
Base
/**************/
type penalty base class
Field : constraint, weight
	constraint -> <function>
		input -> <np array> (N, D)
		output -> <np array> (N, ) raw penalty value
	weight -> <float>
'''
class Base:

	def __init__(self, constraint, weight = 1.):
		self.constraint = constraint
		self.weight = weight

	def Violation(self, solution):
		print("Base can't be used directory")
		sys.exit()

	'''
	/*************/
	Feasible
	/*************/
	process : return wheter feasible or not
	input : solution -> <solution class>
	output : judge -> <np array> (N, ) if True, feasible
	'''
	def Feasible(self, solution):
		judge = np.copy(self.Violation(solution))
		return (judge == 0)


class EqualZero(Base):
	def Violation(self, solution):
		penalty = np.copy(self.constraint(solution.individuals)) #<np array> (N, )
		penalty = np.abs(penalty)

		return self.weight*penalty

class Lower(Base):
	def Violation(self, solution):
		penalty = np.copy(self.constraint(solution.individuals)) #<np array> (N, )
		penalty[penalty < 0.] = 0.

		return self.weight*penalty

class Greater(Base):
	def Violation(self, solution):
		penalty = np.copy(self.constraint(solution.individuals)) #<np array> (N, )
		penalty[penalty > 0.] = 0.

		return -self.weight*penalty