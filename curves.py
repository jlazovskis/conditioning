from __future__ import division
# Name: Conditioning number program for curves
# Description: Contains all the main functions for finding the conditioning number of a curve (that
# is, a variety defined by a single equation in P^2)
# Created: 2016-08-18
# Last modified: 2016-08-21
# Author: Janis Lazovskis

# Import packages
import math
import numpy as np
import sympy as sp

# Define input data class
class variety:
    def __init__(self):
        self.varlist = [] # variables to be used (e.g. [x0, x1, x2] ) 
        self.points = []  # points to be tested (e.g. [[1,1,0],[2,1,-2]] )
        self.func = 0     # defining function (e.g. x0*x0 + x1*x2 - x1*x0 )

# Import helper functions
import helpers

##
## Checker functions for varieties in 2 variables defined by one function
##

# Checks if smooth
# (class variety) -> boolean
# Returns True if the input class has a smooth function, False otherwise
def issmooth(data):
    jac = sp.Matrix([data.func]).jacobian(data.varlist)
    # Check if rank of Jacobian is trivially zero
    sol1 = sp.solve([jac[0],jac[1]],data.varlist[0],data.varlist[1],dict=True)
    if len(sol1) == 0:
        return True
    elif len(sol1) > 1:
        print "Warning: Input curve is singular at "+str(sol1)
        return False
    else:
        p = sp.var('p')
        sol2 = sp.solve(jac[0]*p + jac[1],p,dict=False)
        psol = sol2[0].subs(sol1[0])
        if helpers.iszero(psol) == False:
            print "Warning: Input curve's Jacobian has rank 0 with partial " + str(data.varlist[0]) + "coefficient " + str(psol)
            return False
        else:
            return True

# Checks if points are on curve
# (class variety) -> boolean
# Returns True if the input class points lie on the input class variety, False otherwise
def haspoints(data):
    c = 0
    for i in range(len(data.points)):
        val = data.func.subs({data.varlist[0]:data.points[i][0], data.varlist[1]:data.points[i][1]})
        if helpers.iszero(val) == False:
            c = 1
            print "Warning: Input point "+str(data.points[i])+" does not lie on the curve"
    if c == 1:
        return False
    else:
        return True

##
## Conditioning number finder for curves (projective varieties in 3 variables defined by one 
## function)
##

# Conditioning number finder
# (class variety) -> (list of real number)
# If everything is fine with the input class, this function finds the conditioning number of the 
# input class variety. If the curve is not smooth or the points are wrong, it returns an empty list
# and prints a reason.
def cnum_curve(data):
    cnum_list = []
    # Check if any of the input points are the origin
    if [0,0,0] in data.points:
        print "Warning: Input point [0, 0, 0] is not a valid point"
        return []
    # Project to each affine piece
    for n in [0,1,2]:
        affpiece = variety()
        for m in list(set([0,1,2])-set([n])):
            affpiece.varlist.append(data.varlist[m])
        for p in data.points:
            if helpers.iszero(p[n]) == False:
                affpiece.points.append(helpers.proj(p,n))
        affpiece.func = data.func.subs({data.varlist[n]:1})
        # Check curve is smooth in given affine piece
        if issmooth(affpiece) == False:
            print "Warning: Curve is not smooth when projecting to coordinate " + str(n)
            return []
        # Check affine piece contains input points
        if haspoints(affpiece) == False:
            print "Warning: Some points are not on curve when projecting to affine coordinate " + str(n)
            return []
        # Find the value of the Jacobian at each given point
        dlist = []
        jacaff = sp.Matrix([affpiece.func]).jacobian(affpiece.varlist)
        for p in affpiece.points:
            dlist.append(jacaff.subs({affpiece.varlist[0]:p[0], affpiece.varlist[1]:p[1]}))
        # Find the conditioning numbers for every pair of points
        for p1 in affpiece.points[:-1]:
            for p2 in affpiece.points[affpiece.points.index(p1)+1:]:
                # Get reciprocals of Jacbian slopes
                rj1 = helpers.reciprocal(dlist[affpiece.points.index(p1)])
                rj2 = helpers.reciprocal(dlist[affpiece.points.index(p2)])
                # Proceed if normals are not parallel
                if helpers.parcheck(rj1,rj2) == False:
                    s,t = sp.var('s,t')
                    sollist = sp.solve([p1[0]+s*rj1[0] - p2[0] - t*rj2[0], p1[1]+s*rj1[1] - p2[1] - t*rj2[1]],s,t)
                    cnum_list.append(abs(sollist[s]) * helpers.mynorm(rj1))
                    cnum_list.append(abs(sollist[t]) * helpers.mynorm(rj2))
    # Print and return result
    if cnum_list == []:
        print "No conditioning numbers were found"
        return []
    else:
        ans = min(cnum_list)
        print str(len(cnum_list))+" conditioning numbers were found."
        print "The smallest of these is "+str(ans)+"."
        return [ans]
