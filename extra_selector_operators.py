from __future__ import division
import random
import numpy as np

from functools import partial
from operator import attrgetter

def sel_LRS(individuals, k, fit_attr="fitness"):
    """Select *k* individuals from the input *individuals* using Linear Ranking selection.
     The selection is made by looking only at the first
    objective of each individual. The list returned contains references to
    the input *individuals*.
    :param individuals: A list of individuals to select from.
    :param k: The number of individuals to select.
    :param fit_attr: The attribute of individuals to use as selection criterion
    :returns: A list of selected individuals.
    This function uses the :func:`~random.random` function from the python base
    :mod:`random` module.
    """

    s_inds = sorted(individuals, key=attrgetter(fit_attr), reverse=True)

    num_ind=len(s_inds)
    p_list=[]
    for i in range(num_ind):
        p_list.append((num_ind-i)/(num_ind*(num_ind-1)))
    chosen = []
    v= 1/(num_ind-2.001)
    for i in range(k):
        u = random.random() * v
        j=0
        for p in p_list:
            if p <= u:
                chosen.append(s_inds[j])
                break
            j+=1

    return chosen