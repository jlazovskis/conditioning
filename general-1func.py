from __future__ import division
# Name: Conditioning number program for varieties defined by a single function
# Description: Contains all the main functions for finding the conditioning number of a codim 1 variety in P^n
# Created: 2016-08-26
# Author: Janis Lazovskis

# Import packages
import math
import sympy as sp
import itertools as it

# Declare variables, create a list of them, define input data class
class variety:
    def __init__(self):
        self.varlist = [] # variables to be used (e.g. [x0, x1, x2, x3] )
        self.points = []  # points to be tested (e.g. [[0,1,1,1],[1,0,1,1],[1,0,2,2]] )
        self.func = 0     # defining function (e.g. x0*x0*x1 - x2*x3*x3 +x0*x1*x2 + x2*x2*x2 )

# Import other files
import helpers
import curves

# Conditioning number finder (projective, n+1 coords)
# (class variety) -> (list of real number)
# If everything is fine with the input class, this function finds the conditioning number of the 
# input class variety of dimension n > 1. If the surface is not smooth or the points are wrong, it
# returns an empty list and prints a reason.
def cnumgen(data):
    # List of conditioning numbers
    cnumlist = []
    # Dimension of variety currently being considered
    curdim = len(data.varlist)-1
    # Declare dictionary of groups of points to keep track
    pdict = {}
    pdict[curdim] = []
    # Declare dictionary of directions of projections 
    fdict = {}
    fdict[curdim] = []
    # Find all n-tuples of points
    for pgroup in list(it.combinations(data.points,curdim)):
        for direc in range(curdim+1):
            if canproj(list(pgroup),direc) == True:
                pdict[curdim] += [map(lambda x: helpers.proj(x,direc), list(pgroup))]
                fdict[curdim] += [[direc]]
    while curdim > 2:
        curdim -= 1
        pdict[curdim] = []
        fdict[curdim] = []
        for pgroup in pdict[curdim+1]:
            for qgroup in list(it.combinations(pgroup,curdim)):
                for direc in range(curdim+1):
                    if canproj(list(qgroup),direc) == True:
                        pdict[curdim] += [map(lambda x: x[:direc]+x[direc+1:], list(qgroup))]
                        fdict[curdim] += [fdict[curdim+1][pdict[curdim+1].index(pgroup)] + [direc]]
    print pdict
    print fdict

# (list of (list of real number)), real number -> boolean 
# Checks if a list of points in projective space can be projected to an affine piece
def canproj(lst,coord):
    for p in lst:
        if helpers.iszero(p[coord]) == True:
            return False
    return True