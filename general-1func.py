from __future__ import division
# Name: Conditioning number program for varieties defined by a single function
# Description: Contains all the main functions for finding the conditioning number of a codim 1
# variety in P^n
# Created: 2016-08-26
# Author: Janis Lazovskis

# Import packages
import math
import sympy as sp
import itertools as it

# Define data classes
# Class variety: describes a variety, its defining function, and points on it
class variety:
    def __init__(self):
        self.varlist = [] # variables to be used (e.g. [x0, x1, x2, x3] )
        self.points = []  # points to be tested (e.g. [[0,1,1,1],[1,0,1,1],[1,0,2,2]] )
        self.func = 0     # defining function (e.g. x0*x0*x1 - x2*x3*x3 +x0*x1*x2 + x2*x2*x2 )

# Class pnode: a function, a collection of points satisfying the function, the parent and children
# nodes
class pnode:
    def __init__(self):
        self.func = 0      # defining function
        self.points = []   # points satisfying the defining function
        self.varlist = []  # variables to be used
        self.parent = None # parent pnode (None if none)
        self.children = [] # list of children pnodes (empty if none)

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
    ddict = {}
    ddict[curdim] = []
    # Declare dictionary of function defining variety 
    fdict = {}
    fdict[curdim] = []
    # Find all n-tuples of points
    for pgroup in list(it.combinations(data.points,curdim)):
        # Project to all possible directions
        for direc in range(curdim+1):
            if canproj(list(pgroup),direc) == True:
                pdict[curdim] += [map(lambda x: helpers.proj(x,direc), list(pgroup))]
                ddict[curdim] += [[direc]]
                fdict[curdim] += [[data.func.subs(data.varlist[direc]:1)]]
    while curdim > 2:
        curdim -= 1
        pdict[curdim] = []
        ddict[curdim] = []
        fdict[curdim] = []
        for pgroup in pdict[curdim+1]:
            for qgroup in list(it.combinations(pgroup,curdim)):
                useddirec = ddict[curdim+1][pdict[curdim+1].index(pgroup)]
                unuseddirec = [x for x in range(len(data.varlist)) if x not in useddirec]
                # Calculate hyperplane spanned by points in qgroup
                hypeq = sp.Matrix(curdim+1,curdim+1,lambda i,j: 1)
                matind = 0
                # Add variable names in first row
                for varind in unuseddirec:
                    hypeq[0:matind] = sp.Matrix([data.varlist[varind]])
                    matind += 1
                matind = 1
                # Add points in other rows
                for q in qgroup:
                    hypeq[matind,0:-1] = sp.Matrix(q).T
                    matind += 1


                # Project to directions not already considered
                
                do

                for direc in unuseddirec:
                    direcind = unuseddirec.index(direc)
                    if canproj(list(qgroup),direcind) == True:
                        pdict[curdim] += [map(lambda x: x[:direcind]+x[direcind+1:], list(qgroup))]
                        ddict[curdim] += [ddict[curdim+1][pdict[curdim+1].index(pgroup)] + [direc]]
                        # Calculate hyperplane spanned by chosen points
                        hypeq = sp.Matrix(curdim+1,curdim+1,lambda i,j: 1)
                        matind = 0
                        # Add variable names in first row
                        for varind in [x for x in range(len(data.varlist)) if x not in ddict[2][pind]]:
                            hypeq[0:matind] = sp.Matrix([data.varlist[varind]])
                            matind += 1
                        matind = 1
                        # Add points in other rows
                        for p in pdict[curdim][-1]:
                            hypeq[matind,0:-1] = sp.Matrix(p).T
                        sol = sp.det(hypeq)
                        do 

    for pind in range(len(pdict[2])):
        # Declare variety class to pass to intersection finder
        dim1var = variety()
        # Add only relevant variables
        for varind in [x for x in range(len(data.varlist)) if x not in ddict[2][pind]]:
            dim1var.varlist.append(data.varlist[varind])
        # Add only relevant points
        dim1var.points += pdict[2][pind]

    print pdict
    print fdict

# (list of (list of real number)), real number -> boolean 
# Checks if a list of points in projective space can be projected to an affine piece
def canproj(lst,coord):
    for p in lst:
        if helpers.iszero(p[coord]) == True:
            return False
    return True