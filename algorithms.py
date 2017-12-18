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
    non_terminals_num, terminals_num, sequence_len = T.shape[0], Q.shape[1], len(sequence)
    alpha = np.zeros((sequence_len, sequence_len, non_terminals_num))
    beta = np.zeros((sequence_len, sequence_len, non_terminals_num))

    # Inside base case:
    for token, i in enumerate(sequence):
        alpha[i][i] = Q[:, token]

    # Inside recursion
    for j in range(0, sequence_len):
        for i in range(0, j):
            cur_sum = np.zeros_like(alpha[i][j])
            for k in range(i, j):
                cur_sum += np.tensordot(np.tensordot(T, alpha[i][k], axes=(1, 0)),
                                alpha[k+1][j], axes=(1, 0))
            alpha[i][j] = np.copy(cur_sum)

    # Outside base case, uniform probabilities of each symbol
    beta[0][sequence_len - 1] = 1. / non_terminals_num
    
    # Outside recursion
    for j in range(0, sequence_len):
        for i in range(0, j + 1):
            cur_sum = np.zeros_like(beta[i][j])
            for k in range(1, i):
                cur_sum += np.tensordot(np.tensordot(T, beta[k][j], axes=(0, 0)),
                                alpha[k][i-1], axes=(0, 0))
            for k in range(j + 1, sequence_len):
                cur_sum += np.tensordot(np.tensordot(T, beta[i][k], axes=(0, 0)),
                                alpha[j+1][k], axes=(1, 0))
            beta[i][j] = np.copy(cur_sum)
    return alpha, beta
