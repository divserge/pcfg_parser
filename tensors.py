import numpy as np
from copy import deepcopy

class BaseTensor:
    """
    A base class for multilinear function
    """
    def __init__(self, data, up_indices, down_indices):
        """
        Args:
            data: np.ndarray : the underlying multi-dimensional array
            up_indices: iterable: indices, which will not be contracted in the dot function
            down_indices: iterable: indices, along which the contraction is done in the dot function
        Returns:
            BaseTensor object
        """
        self.data = deepcopy(np.transpose(data, up_indices + down_indices))
        
    def dot(self, vectors):
        """
        Args:
            data: np.ndarray : the underlying multi-dimensional array
            up_indices: iterable: indices, which will not be contracted in the dot function
            down_indices: iterable: indices, along which the contraction is done in the dot function
        Returns:
            BaseTensor object
        """
        print(self.data)
        print(list(np.arange(len(self.data.shape))))
        print(vectors)
        print(list(np.arange(len(self.data.shape)))[-len(vectors.shape):])

        return np.einsum(
            self.data,
            list(np.arange(len(self.data.shape))),
            vectors,
            list(np.arange(len(self.data.shape)))[-len(vectors.shape):]
        )



