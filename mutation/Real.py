import numpy as np
from mimicD.city import *

'''
/*************/
Gauss
/*************/
gaussian mutation
Field : sigma -> variance
'''
class Gauss:
	def __init__(self, sigma):
		self.sigma = sigma

	def mutate(self, solution):
		mutation = solution.individuals + np.random.normal(0., self.sigma, solution.individuals.shape) #(N, D)

		return type(solution)(mutation, solution.generation)

'''
/*************/
SelfAdaptiveScalar
/*************/
self adaptive scalar mutation
Field : epsilon, tau
	epsilon -> <float> min value of variance
	tau -> <float> learning rate
Note : If you use this, all individuals should have variance information to optimize this.
		variance is stocked at individuals[i, -1]
'''
class SelfAdaptiveScalar:

	def __init__(self, epsilon, tau = None):
		self.epsilon = epsilon
		self.tau = tau

	def mutate(self, solution):
		N, D = solution.individuals.shape

		tau_flag = False
		if self.tau is None:
			self.tau = 1./np.sqrt(solution.generation)
			tau_flag = True
		
		mutation = Scopy(solution)
		#####update sigma value
		sigma = mutation.individuals[:,-1] #sigma
		sigma *= np.exp(np.random.normal(0., self.tau, N)) #(N, )
		sigma[sigma < self.epsilon] = self.epsilon
		sigma = sigma.reshape((-1, 1)) #(N, 1)

		#####
		mutation = solution.individuals[:,:-1] + sigma*np.random.normal(0., 1., (N, D-1)) #(N, D-1)
		mutation = np.concatenate((mutation, sigma), axis = -1)

		if tau_flag:
			self.tau = None

		return type(solution)(mutation, solution.generation)


'''
/*************/
SelfAdaptiveVector
/*************/
self adaptive vector mutation
Field : epsilon, tau1, tau2
	epsilon -> <float> min value of variance
	tau1,2 -> <float> learning rate
Note : If you use this, all individuals should have variance information to optimize this.
		variance is stocked at individuals[i, (D/2):]
'''
class SelfAdaptiveVector:

	def __init__(self, epsilon, tau1 = None, tau2 = None):
		self.epsilon = epsilon
		self.tau1 = tau1
		self.tau2 = tau2


	def mutate(self, solution):
		N, D = solution.individuals.shape
		oldest_gene = np.max(solution.generation)

		tau1_flag = False
		tau2_flag = False

		if self.tau1 is None:
			self.tau1 = 1./np.sqrt(2.*oldest_gene)
			tau1_flag = True

		if self.tau2 is None:
			self.tau2 = 1./np.sqrt(2.*oldest_gene)
			tau2_flag = True

		mutation = Scopy(solution)

		##########calc sigma
		sigma = mutation.individuals[:,-int(D/2):]

		#####collect random number from normal distribution
		global_normal = np.random.normal(0., 1., (N, 1))
		global_normal = np.repeat(global_normal, int(D/2), axis = 1) #(N, D/2)
		local_normal = np.random.normal(0., 1., (N, int(D/2)))

		sigma *= np.exp(self.tau2*global_normal+self.tau1*local_normal)
		epsilon = np.expand_dims(self.epsilon, axis = 0)
		epsilon = np.repeat(epsilon, N, axis = 0)
		bol = (sigma<epsilon)
		sigma[bol] = 0.; sigma += bol*epsilon

		###########mutate
		mutation.individuals[:,:-int(D/2)] += sigma*np.random.normal(0., 1., (N, int(D/2)))

		if tau1_flag:
			self.tau1 = None
		if tau2_flag:
			self.tau2 = None

		return mutation


'''
/*************/
Rechenberg
/*************/
Field : sigma, fitness, c, ps
	sigma -> <float> variance
	fitness -> <Fitness class>
	c -> <float> should be lower than 1.
	ps -> <float>
Note : This if for only single optimization
'''
class Rechenberg:

	def __init__(self, sigma, fitness, c = 0.05, ps = 1./5.):
		self.gauss_mutation = Gauss(sigma)
		self.ps = ps
		self.c = c
		self.fitness = fitness

	def mutate(self, solution):
		original_evaluation = self.fitness.getFitness(solution) #(N, )

		mutation = self.gauss_mutation.mutate(solution)
		mutation_evaluation = self.fitness.getFitness(solution) #(N, )

		judge = (mutation_evaluation > original_evaluation) #(N, )

		improved_frac = sum(judge)/len(solution)

		if improved_frac > self.ps:
			self.gauss_mutation.sigma *= self.c
		elif  improved_frac < self.ps:
			self.gauss_mutation.sigma /= self.c

		return mutation