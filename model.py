
from algorithms import inside_outside
from tensors import BaseTensor


class PcfgParser:
	
	def __init__(self, rules_nonterminal, rules_terminal, tensor_wrapper=BaseTensor):
		
		self.tensor_wrapper = tensor_wrapper
		
		self.T = self.tensor_wrapper(rules_nonterminal, [0], [1, 2])
		self.Q = deepcopy(rules_terminal)

		self.T_temp = np.zeros_like(rules_nonterminal)
		self.Q_temp = np.zeros_like(rules_terminal)

	def fit(self, sequences, max_iter):

		for k in range(max_iter):
			
			for seq in sequences:
				
				alpha, beta = inside_outside(seq, self.T, self.Q)
				self.collect_statistics(seq, alpha, beta)
			
			self.recompute_parameters()


	def parse_tree(self, seq):

		alpha, beta = inside_outside(self.__transform_text([seq])[0], self.T, self.Q)
		mu = 


	def collect_statistics(self, seq, alpha, beta):
		pass
		

	def recompute_parameters(self):
		
		self.T_temp = self.T_temp / self.T_temp.sum(axis = 0)[np.newaxis, :, :]
		self.Q_temp = self.Q_temp / self.Q_temp.sum(axis = 1)[:, np.newaxis]

		self.T = self.tensor_wrapper(self.T_temp, [0], [1, 2])
		self.Q_temp = deepcopy(self.Q_temp)

		self.T_temp = np.zeros_like(self.T_temp)
		self.Q_temp = np.zeros_like(self.Q_temp)