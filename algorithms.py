import numpy as np


def inside_outside(sequence, T, Q, pi):
    """Inside-outside algorithm for PCFG to compute the marginals
        Args:
            sequence: an iterable containing token indices
            T: a trilinear function, mapping two vectors into another vector - transition rules for non-terminals of the grammar
            Q: a linear function - transition for terminals of the grammar
        Returns:
            alpha, beta - inside and outside probabilities
    """
    non_terminals_num, terminals_num, sequence_len = T.shape[0], Q.shape[1], len(sequence)
    alpha = np.zeros((sequence_len, sequence_len, non_terminals_num))
    beta = np.zeros((sequence_len, sequence_len, non_terminals_num))

    # Inside base case:
    for i, token in enumerate(sequence):
        alpha[i][i] = Q[:, token]

    # Inside recursion
    for j in range(0, sequence_len):
        for i in range(0, j)[::-1]:
            cur_sum = np.zeros_like(alpha[i][j])
            for k in range(i, j):
                cur_sum += np.einsum('ijk,j,k->i', T, alpha[i][k], alpha[k+1][j])
            alpha[i][j] += np.copy(cur_sum)

    # Outside base case, uniform probabilities of each symbol
    beta[0][sequence_len - 1] = pi
    
    # Outside recursion
    for j in range(0, sequence_len)[::-1]:
        for i in range(0, j + 1):
            cur_sum = np.zeros_like(beta[i][j])
            for k in range(0, i):
                cur_sum += np.einsum('ijk,i,j->k', T, beta[k][j], alpha[k][i-1])
            for k in range(j + 1, sequence_len):
                cur_sum += np.einsum('ijk,i,k->j', T, beta[i][k], alpha[j+1][k])    
            beta[i][j] += np.copy(cur_sum)

    
    return alpha, beta



def inside_outside_einsum(sequence, T, Q, pi):
    """Inside-outside algorithm for PCFG to compute the marginals

        Args:
            sequence: an iterable containing token indices
            T: a trilinear function, mapping to vectors into another vector - transition rules for non-terminals of the grammar
            Q: a linear function - transition for terminals of the grammar
            pi: a distribution over the initial state
        Returns:
            alpha, beta - inside and outside probabilities
    """
    non_terminals_num, terminals_num, sequence_len = T.shape[0], Q.shape[1], len(sequence)
    alpha = np.zeros((sequence_len, sequence_len, non_terminals_num))
    beta = np.zeros((sequence_len, sequence_len, non_terminals_num))

    # Inside base case:
    for i, token in enumerate(sequence):
        alpha[i][i] = Q[:, token]

    # Inside recursion
    for j in range(0, sequence_len):
        for i in range(0, j):
            print(alpha[i, i:j].reshape(j-i, -1).shape)
            print(alpha[i+1:j+1, j].reshape(j-i, -1).shape)
            alpha[i][j] = np.einsum(
                'ijk,jl,kl->i',
                T,
                alpha[i, i:j].reshape(j-i, -1),
                alpha[i+1:j+1, j].reshape(j-i, -1)
            )

    # Outside base case, uniform probabilities of each symbol
    beta[0][sequence_len - 1] = pi
    # Outside recursion
    for j in range(0, sequence_len):
        for i in range(0, j + 1):
            if (i > 0):
                beta[i][j] += np.einsum('ijk,li,lj->k', T, beta[:i, j, :], alpha[:i, i-1, :])
            if (j < sequence_len - 1):
                beta[i][j] += np.einsum('ijk,li,lk->j', T, beta[i, j+1:sequence_len, :], alpha[j+1, j+1:sequence_len, :])

    return alpha, beta


def maximize_labeled_recall(mu):
    
    gamma = np.zeros((mu.shape[0], mu.shape[1]), dtype=float)
    gamma_splits = np.zeros((mu.shape[0], mu.shape[1]), dtype=int)
    gamma_indices = np.zeros((mu.shape[0], mu.shape[1]), dtype=int)
    
    for i in range(gamma.shape[0]):
        gamma_indices[i, i] = np.argmax(mu[i, i])
        gamma[i, i] = mu[i, i, gamma_indices[i, i]]

    for j in range(mu.shape[1]):
        for i in range(j)[::-1]:
            
            split_vals = gamma[i, i:j] + gamma[i+1:j+1, j]
            split = np.argmax(split_vals)

            gamma_splits[i, j] = split
            gamma_indices[i, j] = np.argmax(mu[i, j])
            gamma[i, j] = split_vals[split] + mu[i, j, gamma_indices[i, j]]

    return gamma_splits, gamma_indices
