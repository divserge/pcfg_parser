import numpy as np

class BaseTensor:
	"""
	A base class for multilinear function
	"""
	def __init__(self, data):
		"""
	    Args:
	        data: np.ndarray : the underlying multi-dimensional array
	        up_indices: iterable: indices, which will not be contracted in the dot function
	        down_indices: iterable: indices, along which the contraction is done in the dot function
	    Returns:
	        BaseTensor object
	    """
		return data
		
	def dot(self, vectors):
		"""
	    Args:
	        data: np.ndarray : the underlying multi-dimensional array
	        up_indices: iterable: indices, which will not be contracted in the dot function
	        down_indices: iterable: indices, along which the contraction is done in the dot function
	    Returns:
	        BaseTensor object
	    """
		pass


