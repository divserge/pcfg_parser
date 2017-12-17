import numpy as np

def inside_outside(sequence, T, Q):
	"""Inside-outside algorithm for PCFG to compute the marginals

        Args:
            sequence: an iterable containing token indices
            T: a trilinear function, mapping to vectors into another vector - transition rules for non-terminals of the grammar
            Q: a linear function - transition for terminals of the grammar
        Returns:
            alpha, beta - inside and outside probabilities
    """
	alpha, beta = None, None
	return alpha, beta


def maximize_labeled_recall(mu):
    """Given a tensor of marginals, produce the parse sequence

        Args:
            mu : np.ndarray (N, N, M) - a three-dimensional array of marginals
        Returns:
            gamma : np.ndarray(N, N) - an array of grammar symbols, spanning each of the segment, which maximizes the labeled recall metric


    """
    pass

def maximize_greedy(mu):
    pass