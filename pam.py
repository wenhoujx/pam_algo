# author : Wenshuai Hou
# email  : wenhoujx@gmail.com

import matplotlib as plt
from pylab import *
import collections
import copy
import pdb
import numpy as np
from scipy.spatial.distance import cdist
import random

'''
overall data structure:
    data : N x dim, each row is a data point.
    medoids :   -2  total cost based on current medoids.
                -1  a list of medoids.
                0...k   each one has a list of data indices that belongs to the cluster 0 ... k respectively.
'''
def clustering(data, medoids):
    ''' 
    compute the belonging of each data point according to current medoids centers, and eucludiean distance. 
    '''
    
    # pdb.set_trace()
    med_idx = medoids[-1]
    med  = data[med_idx]
    k       = len(med_idx)
    

    dis = cdist(data, med)
    best_med_it_belongs_to = dis.argmin(axis = 1)
    for i in range(k):
        medoids[i] =where(best_med_it_belongs_to == i)

def total_cost(data, medoids):
    '''
    compute the total cost based on current setting.
    '''
    med_idx = medoids[-1];
    k       = len(med_idx);
    cost    = 0.0;

    med = data[ med_idx] 
    dis = cdist( data, med, 'euclidean') 
    cost = dis.min(axis = 1).sum()
    
    # rewrite using the cdist() function, which should be way faster
    # for i in range(k):
    #     med = data[med_idx[i]]
    #     for j in medoids[i]:
    #         cost = cost + np.linalg.norm(med - data[j])
    # 
    medoids[-2] = [cost]


def kmedoids( data, k):
    '''
    given the data and # of clusters, compute the best clustering based on the algorithm provided in wikipedia: google pam algorithm.
    
    '''
    # cur_medoids compare with old_medoids, convergence achieved if no change in the list of medoids in consecutive iterations. 
    # tmp_medoids is cur_medoids swapped only one pair of medoid and non-medoid data point. 
    # best_medoids is the best tmp_medoids through all possible swaps. 

    N               = len(data)
    cur_medoids     = {}
    cur_medoids[-1] = range(k)
    clustering(data, cur_medoids)
    total_cost(data, cur_medoids)
    old_medoids     = {}
    old_medoids[-1] = []
    
    iter_counter = 1
    # stop if not improvement.
    while not set(old_medoids[-1]) == set(cur_medoids[-1]):
        print 'iteration couter:' , iter_counter
        iter_counter = iter_counter + 1 
        best_medoids = copy.deepcopy(cur_medoids)
        old_medoids  = copy.deepcopy(cur_medoids)
        # pdb.set_trace()
        # iterate over all medoids and non-medoids
        for i in range(N):
            for j in range(k):
                if not i ==j :
                    # swap only a pair
                    tmp_medoids        = copy.deepcopy(cur_medoids)
                    tmp_medoids[-1][j] = i

                    clustering(data, tmp_medoids)
                    total_cost(data, tmp_medoids)
                    # pick out the best configuration.
                    if( best_medoids[-2] > tmp_medoids[-2]):
                        best_medoids = copy.deepcopy(tmp_medoids)
        cur_medoids = copy.deepcopy(best_medoids)
        print 'current total cost is ', cur_medoids[-2]
    return cur_medoids


if __name__ =='__main__':
    dim = 2
    N =1000 

    # create datas with different normal distributions.
    d1 = np.random.normal(1, .2, (N,dim))
    d2 = np.random.normal(2, .5, (N,dim))
    d3 = np.random.normal(3, .3, (N,dim))
    data = np.vstack((d1,d2,d3))
    
    # need to change if more clusters are needed . 
    k = 3
    medoids = kmedoids(data, k)
    # plot different clusters with different colors.
    scatter( data[medoids[0], 0] ,data[medoids[0], 1], c = 'r') 
    scatter( data[medoids[1], 0] ,data[medoids[1], 1], c = 'g') 
    scatter( data[medoids[2], 0] ,data[medoids[2], 1], c = 'y') 
    scatter( data[medoids[-1], 0],data[medoids[-1], 1] , marker = 'x' , s = 500)
    show()
    savefig('kmedoids.png')


