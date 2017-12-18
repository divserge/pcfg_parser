
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
		mu = alpha * beta


	def collect_statistics(self, seq, alpha, beta):
		
		inner_sum = np.einsum('rpd,sdq->rspq', beta[:, :, :-1], beta[:, 1:, :])

		p, q = np.meshgrid(np.arange(beta.shape[1]), np.arange(beta.shape[1]))

		numerator_zero_mask = np.where(q <= p)
		denominator_zero_mask = np.where(q < p)

		alpha_masked = deepcopy(alpha)
		alpha_masked[:, denominator_zero_mask] = 0.

		denominator = np.einsum('jpq,jpq->j', alpha_masked, beta)

		alpha_masked[:, numerator_zero_mask] = 0.

		numerator = np.einsum('jpq,jrs,rspq->jrs', alpha, self.T_data, inner_sum)

		self.T_temp += numerator / denominator[:, np.newaxis, np.newaxis]
		self.Q_temp[:, seq] += np.einsum('jhh,jhh->j', alpha, beta) / denominator

	def recompute_parameters(self):
		
		self.T_data = self.T_temp / (self.T_temp.sum(axis = [1, 2])[:, np.newaxis, np.newaxis] + self.Q_temp.sum(axis = 1)[:, np,newaxis, np.newaxis])
		self.Q = self.Q_temp / (self.Q_temp.sum(axis = 1)[:, np.newaxis] + self.T_temp.sum(axis = [1, 2])[:, np.newaxis])

		self.T = self.tensor_wrapper(self.T_data, [0], [1, 2])

		self.T_temp = np.zeros_like(self.T_temp)
		self.Q_temp = np.zeros_like(self.Q_temp)