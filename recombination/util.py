import sys
import numpy as np


def checkPare(parents):
	if (len(parents)%2) != 0:
		print("Error@checkPare process")
		print("num of parents should even number")
		sys.exit()

'''
/**************/
setPares
/**************/
process : decide pares from parents
input : parents -> <solution class>
output : father, mother -> <np array> (N, D)
'''
def setPares(parents):
	mating_pool = np.copy(parents.individuals)
	np.random.shuffle(mating_pool)

	N, D = mating_pool.shape
	mating_pool = mating_pool.reshape(int(N/2), 2, D)

	return mating_pool[:,0,:], mating_pool[:,1,:]