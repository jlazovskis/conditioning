from __future__ import division
# Name: Conditioning number program for curves
# Description: Contains all the main functions for finding the conditioning number of a curve (that
# is, a variety defined by a single equation in P^2)
# Created: 2016-08-18
# Last modified: 2016-08-24
# Author: Janis Lazovskis

# Import packages
import math
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
## Checker functions for affince varieties in 2 variables defined by one function
##

# Checks if smooth (affine, 2 coords)
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
            print "Warning: Input curve's Jacobian has rank 0 with partial " + str(data.varlist[0]) + " coefficient " + str(psol)
            return False
        else:
            return True

# Checks if points are on curve (affine, 2 coords)
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
## Conditioning number finder for curves 
##

# Conditioning number finder (projective, 3 coords)
# (class variety) -> (list of real number)
# This function is a wrapper for projective varieties, transforming them to affine varieties and 
# then calling cnumaff on each affine piece.
def cnumcurve(data):
    # List of conditioning numbers
    cnumlist = []
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
        cnumlist = cnumaff(affpiece,data.varlist(n))
    # Print and return result
    if cnumlist == []:
        print "No conditioning numbers were found"
        return []
    else:
        ans = min(cnumlist)
        print str(len(cnumlist))+" conditioning numbers were found."
        print "The smallest of these is "+str(ans)+"."
        return [ans]

# Conditioning number finder (affine, 2 coords)
# (class variety, variable) -> (list of real number)
# If everything is fine with the input class, this function finds the conditioning number of the 
# input class variety projected to affine 2-space. If the curve is not smooth or the points are 
# wrong, it returns an empty list and prints a reason.

def cnumaff(affdata,projvar):
    condlist = []
    # Check curve is smooth in given affine piece
    if issmooth(affdata) == False:
        print "Warning: Curve is not smooth when projecting to coordinate " + str(projvar)
        return []
    # Check affine piece contains input points
    if haspoints(affdata) == False:
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