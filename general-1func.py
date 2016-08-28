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

# Define global structures
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

# List cnumlist: a list of conditioning numbers. Global because helper functions need to use it too
cnumlist = []

# Import other files
import helpers
import curves

# Conditioning number finder (projective, n+1 coords)
# (class variety) -> (list of real number)
# If everything is fine with the input class, this function finds the conditioning number of the 
# input class variety of dimension n > 1. If the surface is not smooth or the points are wrong, it
# returns an empty list and prints a reason.
def cnumgen(data):
    # Reset list of conditioning numbers
    cnumlist = []
    # Dimension of variety currently being considered
    curdim = len(data.varlist)-1
    # Create list of pnodes in affine n-space 
    toplist = []
    tlind = 0
    for pgroup in list(it.combinations(data.points,curdim)):
        # Project to all possible directions
        for direc in range(curdim+1):
            if canproj(list(pgroup),direc) == True:
                toplist.append(pnode())
                toplist[tlind].func = data.func.subs(data.varlist[direc]:1)
                toplist[tlind].points = map(lambda x: helpers.proj(x,direc), list(pgroup))
                toplist[tlind].varlist = data.varlist[:direc] + data.varlist[direc+1:]
                tlind += 1
    for topnode in toplist:
        childify(topnode,curdim)
    if cnumlist == []:
        print "No conditioning numbers found"
    else:
        print "Minimum conditioning number found is "+str(min(cnumlist))
        print "Complete list of conditioning numbers found is:"
    return cnumlist

# Projection checker
# (list of (list of real number)), real number -> boolean 
# Checks if a list of points in projective space can be projected to an affine piece
def canproj(lst,coord):
    for p in lst:
        if helpers.iszero(p[coord]) == True:
            return False
    return True

# Recursive children-creator or conditioning-number-finder
# (class pnode), real num -> void
# If dim>1, finds all the children of pnode and records them in the children attribute. If dim=1,
# finds conditioning number and adds it to cnumlist
def childify(pointnode, dim):
    if dim > 2:
        pind = 0
        # Calculate hyperplane spanned by points
        hypeq = sp.Matrix(dim+1,dim+1,lambda i,j: 1)
        # Add first row of variables
        hypeq[0,0:-1] = sp.Matrix([pointnode.varlist])
        # Add points
        hypeq[1:,0:-1] = sp.Matrix(list(pointnode.points))
        sol = sp.det(hypeq)
        for varname in pointnode.varlist:
            varind = pointnode.varlist.index(varname)
            # Make sure variable can be expressed in terms of other vars
            if sol.has(varname):
                for pgroup in list(it.combinations(pointnode.points,dim-1)):
                    # Make sure choice of dim-1 points (projected) are in general position
                    plist = map(lambda x: x[0:varind] + x[varind+1:], list(pgroup))
                    if helpers.iszero(sp.det(sp.Matrix(plist))) == False:
                        # Declare new child pnode:
                        pointnode.children.append(pnode())
                        pointnode.children[pind].func = pointnode.func.subs({varname:sp.solve(sol,varname)[0]})
                        pointnode.children[pind].points = plist
                        pointnode.children[pind].varlist = [x for x in pointnode.varlist if x not in [varname]]
                        pointnode.children[pind].parent = pointnode
                        # Childify new child pnode
                        childify(pointnode.children[pind],dim-1)
                        pind += 1
    else:
        cnumlist += cnumaff(pointnode,'null')