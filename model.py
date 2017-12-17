
from algorithms import inside_outside
from tensors import BaseTensor


class PcfgParser:
	
	def __init__(self, rules):
		pass

	def fit(self, sentences):
		
		sequences = self.__transform_text(sentences):

		for k in range(max_iter):
			
			for seq in sequences:
				alpha, beta = inside_outside(seq, self.T, self.Q)
				self.collect_statistics(seq, alpha, beta)
			
			self.recompute_parameters()


	def parse_tree(self, seq):

		alpha, beta = inside_outside(self.__transform_text([seq])[0], self.T, self.Q)


	def collect_statistics(self, seq, alpha, beta):
		

	def recompute_parameters(self):
		pass