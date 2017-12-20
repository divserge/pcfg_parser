import numpy as np

from model import PcfgParser

class Parser:
	
	def __init__(self, config):

		if config['rules'] is not None:
			self.__encode_rules(config['rules'])

		self.__parser = PcfgParser(self.T, self.Q, self.pi)

		#if config['training'] is not None:
		#	pass

	def parse(self, sentence):
		
		sequence = [self.term_to_index[w] for w in sentence.split()]
		splits, syms = self.__parser.parse_tree(sequence)

		return self.__split_string(sentence.split(), 0, len(sentence.split()) - 1, splits, syms)


	def __encode_vocabulary(self, vocab, n_nonterm):
		pass

	def __encode_rules(self, rules):

		self.nonterm_to_index = {}
		self.index_to_nonterm = []
		self.term_to_index = {}
		t_index = 0

		# first we index all of our terminals and non_terminals
		for (index, start_symbol) in enumerate(rules):

			self.nonterm_to_index[start_symbol] = index
			self.index_to_nonterm.append(start_symbol)
			
			for rule in rules[start_symbol]:

				if len(rule[0].split()) == 1: # terminal

					term = rule[0]

					if term not in self.term_to_index:
						
						self.term_to_index[term] = t_index
						t_index +=1

		index += 1

		# conditional distributions for non-terminal and terminal transitions
		self.T = np.zeros((index, index, index), dtype=float)
		self.Q = np.zeros((index, t_index), dtype=float)
		
		# distribution over the root terminal
		self.pi = np.zeros(self.Q.shape[0], dtype=float)
		self.pi[self.nonterm_to_index['S']] = 1.0

		for (index, start_symbol) in enumerate(rules):

			for rule in rules[start_symbol]:

				if len(rule[0].split()) == 1:
					self.Q[index, self.term_to_index[rule[0]]] = rule[1]
				else:
					lhs, rhs = rule[0].split()
					self.T[index, self.nonterm_to_index[lhs], self.nonterm_to_index[rhs]] = rule[1]

	def __split_string(self, seq, fr, to, splits, syms):

	    if fr == to:
	        return (self.index_to_nonterm[syms[fr, to]], seq[fr])
	    else:
	        return (
	        	self.index_to_nonterm[syms[fr, to]],
	            self.__split_string(seq, fr, fr + splits[fr, to], splits, syms),
	            self.__split_string(seq, fr + splits[fr, to] + 1, to, splits, syms)
	        )



