import numpy as np
import sys

sys.path.append('../')

RULES = {
    'S': [('NP VP', 1.0)],
    'NP' : [('DET S_1', 0.25), ('DET N', 0.25), ('Mary', 0.25), ('John', 0.25)],
    'S_1' : [('ADJ N', 1.0)],
    'VP' : [('V NP', 1.0 / 3), ('VP PP', 1.0 / 3), ('eats', 1.0 / 3)],
    'DET' : [('a', 1.0)], 
    'ADJ' : [('tasty', 1.0 / 3) , ('ADV ADJ', 1.0 / 3), ('very', 1.0 / 3)],
    'ADV' : [('very', 1.0)], 
    'N' : [('fish', 1.0 / 4), ('fork', 1.0 / 4), ('dog', 1.0 / 4), ('boy', 1.0 / 4)],
    'V' : [('eats', 1.0)],
    'PP' : [('P NP', 1.0)],
    'P' : [('with', 1.0)],
}

