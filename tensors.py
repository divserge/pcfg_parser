import numpy as np
import scipy.io as sio
from sktensor import dtensor, ktensor, cp_als, tucker
from sktensor.core import ttm
from copy import deepcopy
import time



class BaseTensor:
    """
    A base class for multilinear function
    """
    def __init__(self, data, rank = 2):
        """
        Args:
            data: np.ndarray : the underlying multi-dimensional array
            rank: 
        Returns:
            BaseTensor object
        """
        self.rank = rank
        self.ktensor = cp_als(dtensor(data),self.rank)[0]
        
    def dot(self, vectors, modes):
        """
        Args:
            vectors: 
            modes: 
        Returns:
            convolution:
        """
        factors = deepcopy(self.ktensor.U)
        # print(self.ktensor.lmbda)
        for ind,i in zip(modes,range(len(modes))):
            factors[ind] = (vectors[i].T).dot(factors[ind]).reshape((1,self.rank))
        convolution = ktensor(factors,self.ktensor.lmbda).toarray().squeeze()
        return convolution

class TuckerTensor:
    """
    A base class for multilinear function
    """
    def __init__(self, data, rank=(2,2,2)):
        """
        Args:
            data: np.ndarray : the underlying multi-dimensional array
            rank: tucker rank
        Returns:
            BaseTensor object
        """
        self.rank = rank
        self.core, self.factors = tucker.hooi(dtensor(data),self.rank,maxIter=20)
        


    def dot(self, vectors, modes):
        """
        Args:
            vectors: vectors to convolve
            modes:
        Returns:
            convolution:
        """
        factors = deepcopy(self.factors)
        # print(self.ktensor.lmbda)
        for ind,i in zip(modes,range(len(modes))):
            factors[ind] = (vectors[i].T).dot(factors[ind]).reshape((1,self.rank[ind]))
        convolution = ttm(self.core,factors).squeeze()
        return convolution


# n = 10
# R = 5


# u1 = np.random.random([n, R])
# u2 = np.random.random([n, R])
# u3 = np.random.random([n, R])

# v = np.random.random([n, 1])
# g = np.zeros([R, R, R])
# np.fill_diagonal(g, 1.)



# a = ktensor([u1,u2,u3])
# a = a.toarray()
# vec1 = np.einsum('ijk,jb,kc',a, v, v)

# modes= [1,2]

# for r in range(1,6):
#     tensor = BaseTensor(a,rank=r)
#     vec = tensor.dot([v,v],modes)
#     print('canon',r, np.linalg.norm(vec-vec1)/np.linalg.norm(vec1))

# for r in range(1,6):
#     ttensor = TuckerTensor(a,(r,r,r))
#     vec = ttensor.dot([v,v],modes)
#     print('tucker',r, np.linalg.norm(vec-vec1)/np.linalg.norm(vec1))


# n = 100
# a = np.random.random((n,n,n))
# v = np.random.random([n, 1])
# #a = np.einsum('ijk,ai,bj,ck', g, u1, u2, u3)
# vec1 = np.einsum('ijk,jb,kc',a, v, v)

# # a = np.einsum('ijk,ai,bj,ck', g, u1, u2, u3)
# # print(a.shape)
# # vec1 = np.einsum('ijk,bj,ck',a, v, v)
# # t = ktensor(dtensor(a))


# for r in range(1,10):
#     tensor = BaseTensor(a,[0],[1,2],rank=r)
#     vec = tensor.dot([v,v])
#     print('canon',r, np.linalg.norm(vec-vec1)/np.linalg.norm(vec1))

# for r in range(1,10):
#     ttensor = TuckerTensor(a,[0],[1,2],(r,r,r))
#     vec = ttensor.dot([v,v])
#     print('tucker',r, np.linalg.norm(vec-vec1)/np.linalg.norm(vec1))

# n=100
# random_tensor = np.random.random((n,n,n))
# random_vector = np.random.random(n)
# # random_vector = np.ones(n)

# random_vector = np.random.random([n, 1])
# vec1 = np.einsum('ijk,bj,ck',random_tensor, random_vector, random_vector)

# # dt = dtensor(random_tensor)
# # vec1 = dt.ttv((random_vector,random_vector),[1,2])

# tensor = BaseTensor(random_tensor,[0],[1,2],100)
# vec = tensor.dot([random_vector,random_vector])
# print(np.linalg.norm(vec-vec1)/np.linalg.norm(vec1))


# ttensor = TuckerTensor(random_tensor,[0],[1,2],(100,100,100))
# vec = ttensor.dot([random_vector,random_vector])
# print(np.linalg.norm(vec-vec1)/np.linalg.norm(vec1))

# t = time.time()
# for i in range(100):
#     random_vector = np.random.random(n)
#     vec = tensor.dot([random_vector,random_vector])
#     vec2 = ttensor.dot([random_vector,random_vector])
#     print(np.linalg.norm(vec2-vec))
# print(time.time()-t)

# dt = dtensor(random_tensor)
# t = time.time()
# for i in range(100):
#     random_vector = np.random.random(n)
#     vvec1 = dt.ttv((random_vector,random_vector),[1,2])
# print(time.time()-t)