import numpy as np

from model import PcfgParser

class Parser:
	
	def __init__(self, config):

		if config['rules'] is not None:
			self.__encode_rules(config['rules'])

		#self.parser = PcfgParser(self.T, self.Q)

		#if config['training'] is not None:
		#	pass

	def parse(self, sequences):
		pass

	def __encode_vocabulary(self, vocab, n_nonterm):
		pass

	def __encode_rules(self, rules):

		self.nonterm_to_index = {}
		self.term_to_index = {}
		t_index = 0

		# first we index all of our terminals and non_terminals
		for (index, start_symbol) in enumerate(rules):

			self.nonterm_to_index[start_symbol] = index
			
			for rule in rules[start_symbol]:

				if len(rule[0].split()) == 1: # terminal

					term = rule[0]

					if term not in self.term_to_index:
						
						self.term_to_index[term] = t_index
						t_index +=1

		index += 1
		self.T = np.zeros((index, index, index), dtype=float)
		self.Q = np.zeros((index, t_index), dtype=float)

		for (index, start_symbol) in enumerate(rules):

			for rule in rules[start_symbol]:

				if len(rule[0].split()) == 1:
					self.Q[index, self.term_to_index[rule[0]]] = rule[1]
				else:
					lhs, rhs = rule[0].split()
					self.T[index, self.nonterm_to_index[lhs], self.nonterm_to_index[rhs]] = rule[1]





