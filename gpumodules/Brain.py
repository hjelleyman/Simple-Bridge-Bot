"""Summary

Deleted Attributes:
    brain (TYPE): Description
    vec (TYPE): Description
"""
import numpy as np
import itertools

class Brain:

	"""Summary
	
	Attributes:
	    arrays (TYPE): Description
	    signiture (TYPE): Description
	
	Deleted Attributes:
	    keys (list): Description
	"""
	
	def __init__(self, signiture = '3_2_4', arrays = None):
		"""Summary
		
		Args:
		    signiture (str, optional): The shapes of the arrays and relevant operations.
		    arrays (None, optional): Description
		"""
		self.signiture = signiture
		self.arrays = arrays
		if arrays == None:
			self.gen_structure()

	def gen_structure(self):
		"""Summary
		"""
		self.arrays = {}

		nodelens = [int(a) for a in self.signiture.split('_')]
		for i in range(len(nodelens)):
			for j in range(i+1, len(nodelens)):
				self.arrays[(i,j)]  = np.random.uniform(-1,1,[nodelens[i],nodelens[j]])


	def decide(self, vec):
		"""Summary
		
		Args:
		    vec (np.ndarray): Description
		
		Returns:
		    TYPE: Description
		"""
		nodelens = [int(a) for a in self.signiture.split('_')]
		inputs = {i: np.zeros([vec.shape[0],int(nodelens[i])]) for i in range(len(nodelens))}

		inputs[0] = vec
		for a in range(len(self.arrays.keys())):
			i,j = list(self.arrays.keys())[a]
			out = np.einsum('ij,jk->ik',inputs[i], self.arrays[(i,j)])
			inputs[j] = inputs[j] + out

		return inputs[max(inputs.keys())]


	def add_layer(self, n = 5):
		"""Summary
		
		Args:
		    n (int, optional): Description
		"""
		nodelens = [int(a) for a in self.signiture.split('_')]
		nodelens = nodelens[:-1] + [n] + [nodelens[-1]]
		nlayers = len(nodelens)
		arrays = {}
		keys = [key for key in itertools.product(range(nlayers), repeat = 2) if key[1]>key[0]]

		# print(keys)

		for a in range(len(keys)):
			i,j = keys[a]
			if i != nlayers-2 and j != nlayers-2:
				j2 = min(j,nlayers-2)
				arrays[(i,j)] = self.arrays[(i,j2)]
			else:
				arrays[(i,j)] = np.zeros([nodelens[i],nodelens[j]])

		self.arrays = arrays

		self.signiture = '_'.join([str(a) for a in nodelens])

	def add_node(self, layer = 1):
		"""Summary
		
		Args:
		    layer (int, optional): Description
		"""
		for key in self.arrays.keys(): 
			if layer == key[0]:
				b = np.random.uniform(1,-1,self.arrays[key].shape + np.array([1,0]))
				b[:-1,:] = self.arrays[key]
				self.arrays[key] = b
			if layer == key[1]:
				b = np.random.uniform(1,-1,self.arrays[key].shape + np.array([0,1]))
				b[:,:-1] = self.arrays[key]
				self.arrays[key] = b

		nodelens = [int(a) for a in self.signiture.split('_')]
		nodelens[layer] += 1
		self.signiture = '_'.join([str(a) for a in nodelens])

	def remove_node(self, layer = 1, node_index = 0):
		"""Summary
		
		Args:
		    layer (int, optional): Description
		    node_index (int, optional): Description
		"""
		for key in self.arrays.keys(): 
			if layer == key[0]:
				self.arrays[key] = np.delete(self.arrays[key], node_index, 0)
			if layer == key[1]:
				self.arrays[key] = np.delete(self.arrays[key], node_index, 1)
		
		nodelens = [int(a) for a in self.signiture.split('_')]
		nodelens[layer] -= 1
		self.signiture = '_'.join([str(a) for a in nodelens])

	def add_edge(self, layer_1 = 0, layer_2 = 0, node_1 = 0, node_2 = 0):
		"""Summary
		
		Args:
		    layer_1 (int, optional): Description
		    layer_2 (int, optional): Description
		    node_1 (int, optional): Description
		    node_2 (int, optional): Description
		"""
		try:
			self.arrays[(layer_1, layer_2)][node_1,node_2] = np.random.uniform(-1, 1)
		except:
			pass

	def remove_edge(self, layer_1 = 0, layer_2 = 0, node_1 = 0, node_2 = 0):
		"""Summary
		
		Args:
		    layer_1 (int, optional): Description
		    layer_2 (int, optional): Description
		    node_1  (int, optional): Description
		    node_2  (int, optional): Description
		"""
		try:
			self.arrays[(layer_1, layer_2)][node_1,node_2] = 0
		except:
			pass

	def copy(self):

		new_Brain = Brain(signiture = self.signiture, arrays = self.arrays)

		return new_Brain

def evolve(brain, probabilities = [0.2]*4):

	new_layer_prob, new_node_prob, remove_node_prob, remove_edge_prob = probabilities

	random_vector = np.random.uniform(0,1,[4])
	nodelens      = [int(a) for a in brain.signiture.split('_')]
	brain         = brain.copy()


	if random_vector[0] <= new_layer_prob:
		
		brain.add_layer(n = 1)



	if random_vector[1] <= new_node_prob and len(nodelens) > 2:
		
		layer = np.random.choice(np.arange(1,len(nodelens)-1))
		brain.add_node(layer = layer)



	if random_vector[2] <= remove_node_prob and len(nodelens) > 2:
		
		layer      = np.random.choice(np.arange(1,len(nodelens)))
		node_index = np.random.choice(np.arange(nodelens[layer]))
		
		brain.remove_node(layer = layer, node_index = node_index)



	if random_vector[3] <= remove_edge_prob:

		layer_1      = np.random.choice(np.arange(len(nodelens)-1))
		node_index_1 = np.random.choice(np.arange(nodelens[layer_1]))

		layer_2      = np.random.choice(np.arange(layer_1,len(nodelens)))
		node_index_2 = np.random.choice(np.arange(nodelens[layer_2]))

		brain.remove_edge(layer_1 = layer_1, layer_2 = layer_2, node_1 = node_index_1, node_2 = node_index_2)

	return brain



if __name__ == '__main__':

	brain = Brain(signiture = '2_2_3')

	vec = np.array([[1,10]])
	print(brain.decide(vec))
