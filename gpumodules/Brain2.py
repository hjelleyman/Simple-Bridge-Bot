"""Summary

Deleted Attributes:
	brain (TYPE): Description
	vec (TYPE): Description
"""
import cupy as cp
import numpy as np
import itertools
import networkx as nx
import matplotlib.pyplot as plt
import random

class Brain:
	"""Summary
	
	Deleted Attributes:
		keys (list): Description
		arrays (TYPE): Description
		signiture (TYPE): Description
		genes (TYPE): Description
		inovation_no (TYPE): Description
	
	Attributes:
		Adj (TYPE): Description
		genes (list): Description
		graph (TYPE): Description
		idno (int): Description
		nin (TYPE): Description
		nout (TYPE): Description
		cpulses (int): Description
	"""
	idno = 0 
	def __init__(self, nin = 10, nout = 10, network = None, genes = None):
		"""Summary
		
		Args:
			nin (int, optional): Description
			nout (int, optional): Description
			network (None, optional): Description
			genes (None, optional): Description
		
		Deleted Parameters:
			inovation_no (int, optional): Description
		"""
		self.nin   = nin
		self.nout  = nout
		self.idno = Brain.idno
		self.idno += 1
		self.cpulses = 1

		if genes == None:
			self.genes = []
		else:
			self.genes = genes

		if network == None:
			self.gen_structure()

		
	def gen_structure(self):
		"""Summary
		"""
		self.Adj = cp.random.rand(self.nin, self.nout)




	def decide(self, vec):
		"""Summary
		
		Args:
			vec (TYPE): Description
		
		Returns:
			TYPE: Description
		"""

		expected_in = self.Adj.shape[0]

		newvec = cp.zeros([1,expected_in])
		newvec[:,:self.nin] = cp.array(vec, dtype = float)

		matrix = self.Adj.copy()
		output = cp.matmul(newvec, matrix)
		
		return output[0].tolist()

	def copy(self):
		"""Summary
		
		Returns:
			TYPE: Description
		"""
		new_Brain = Brain()
		new_Brain.Adj = self.Adj.copy()
		new_Brain.nin = self.nin
		new_Brain.nout = self.nout
		new_Brain.cpulses = self.cpulses
		return new_Brain

def evolve(brain, probabilities = [0.2]*3):
	"""Evolves a parent adj to make a child brain based on parameters.
	
		1) Probability of an edge change.
		2) Probability of adding a node.
		3) Probability of changing number of pulses.
	
	Args:
		brain (TYPE): Description
		probabilities (TYPE, optional): Description
	
	Returns:
		TYPE: Description
	"""
	adj = brain.Adj
	adj = change_edges(adj, probabilities[0])
	# adj = add_nodes(adj, probabilities[1])
	# brain.cpulses = change_pulseno(brain.cpulses, probabilities[2])
	brain.Adj = adj
	return brain

def change_edges(brain, probability = 1e-3):
	"""Summary
	
	Args:
		brain (TYPE): Description
		probability (float, optional): Description
	
	Returns:
		TYPE: Description
	"""
	change    = cp.random.choice([False,True],size = brain.shape, p = [1-probability, probability])
	new_edges = cp.random.rand(*brain.shape)
	brain[change] = new_edges[change]

	return brain

def add_nodes(brain, probability):
	"""Summary
	
	Args:
		brain (TYPE): Description
		probability (TYPE): Description
	"""
	randno = random.random()
	n = int(-cp.log(randno / probability))
	new_Brain = brain.copy()
	if n > 0:
		new_Brain = cp.random.rand(brain.shape[0]+n,brain.shape[0]+n)
		new_Brain[:brain.shape[0],:brain.shape[0]] = brain
	
	return new_Brain

def change_pulseno(cpulses, probability):
	randno = random.random()
	if randno < probability:
		cpulses = cpulses + cp.random.choice([-1,1])

	if cpulses < 1:
		cpulses = 1
	return cpulses



if __name__ == '__main__':
	pass