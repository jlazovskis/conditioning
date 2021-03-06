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
    global cnumlist
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
                toplist[tlind].func = data.func.subs({data.varlist[direc]:1})
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
        global cnumlist
        cnumlist += cnumaff(pointnode,'null')

# Conditioning number finder (affine, 2 coords)
# (class variety, variable) -> (list of real number)
# If everything is fine with the input class, this function finds the conditioning number of the 
# input class variety in affine 2-space. If the curve is not smooth or the points are wrong, it
# returns an empty list and prints a reason.
def cnumaff(affdata,projvar):
    condlist = []
    # Check curve is smooth in given affine piece
    if helpers.issmooth(affdata) == False:
        print "Warning: Curve is not smooth when projecting to coordinate " + str(projvar)
        return []
    # Check affine piece contains input points
    if helpers.haspoints(affdata) == False:
        print "Warning: Some points are not on curve when projecting to affine coordinate " + str(projvar)
        return []
    # Find the value of the Jacobian at each given point
    dlist = []
    jacaff = sp.Matrix([affdata.func]).jacobian(affdata.varlist)
    for p in affdata.points:
        dlist.append(jacaff.subs({affdata.varlist[0]:p[0], affdata.varlist[1]:p[1]}))
    # Find the conditioning numbers for every pair of points
    for p1 in affdata.points[:-1]:
        for p2 in affdata.points[affdata.points.index(p1)+1:]:
            # Get reciprocals of Jacbian slopes
            rj1 = helpers.reciprocal(dlist[affdata.points.index(p1)])
            rj2 = helpers.reciprocal(dlist[affdata.points.index(p2)])
            # Proceed if normals are not parallel
            if helpers.parcheck(rj1,rj2) == False:
                s,t = sp.var('s,t')
                sollist = sp.solve([p1[0]+s*rj1[0] - p2[0] - t*rj2[0], p1[1]+s*rj1[1] - p2[1] - t*rj2[1]],s,t)
                currcondlist = [abs(sollist[s]) * helpers.mynorm(rj1), abs(sollist[t]) * helpers.mynorm(rj2)]
                # Use found conditioning numbers if they are realistic
                if max(currcondlist)/min(currcondlist) < 2:
                    condlist += currcondlist
    return condlist