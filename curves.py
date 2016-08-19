from __future__ import division
# Name: Conditioning number program for curves
# Description: Contains all the main functions for finding the conditioning number of a curve (that is, defined by a single equation in P^2)
# Created: 2016-08-18
# Last modified: 2016-08-18
# Author: Janis Lazovskis

# Import packages
import numpy as np
import sympy as sp

# Declare variables, create a list of them, define input data class
x0,x1,x2 = sp.var('x0,x1,x2')
varlist = [x0,x1,x2]
class thingy:
    def __init__(self):
        self.points = [] # points to be tested (e.g. [[1,1,0],[2,1,-2]] )
        self.func = 0    # defining function (e.g. x0*x0 + x1*x2 - x1*x0 )
        self.jac = []    # Jacobian of function (always sp.Matrix([x.func]).jacobian(varlist) )

# Import helper functions
import helpers

# Checker function
# (class input) -> void
# Performs series of checks on input data, prints all warnings
def checker(data):
    f = data.func
    plist = data.points
    J = data.jac
    
    # Check if curve is smooth
    p,q,r = sp.var('p,q,r')
    g = J[0]*p + J[1]*q + J[2]*r
    sollist = sp.solve([g.coeff(x0),g.coeff(x1),g.coeff(x2)],p,q,r)
	# Check if more than one solution
    if isinstance(sollist,dict) == False:
        raise Warning("Input curve is not smooth.")
    # Check if Jacobian vectors linearly independent
    elif len(sollist) == 1:
		if sum(sollist.values()) != 0:
			raise Warning("Input curve is not smooth.")

    # Check if the given points are actually in P^2
    while [0,0,0] in plist:
        print "Warning: Input point [0, 0, 0] is not a valid point and has been removed from plist."
        plist.remove([0,0,0])

    # Check if the given points are actually on the curve
    badptindex = []
    for i in range(len(plist)):
        val = f
        for j in [0,1,2]:
            val = val.subs({varlist[j]:plist[i][j]})
        if val!=0:
            print "Warning: Input point "+str(plist[i])+" does not lie on the curve and has been removed from plist."
            badptindex.append(i)

    # Remove all the points not on the curve
    for i in range(len(badptindex)):
        del plist[badptindex[i]-i]

# Conditioning number finder
# (class input) -> (void)
# Assuming everything is fine with the data and curve, this function actually finds the conditioning number based on the input
def finder(data):
    f = data.func
    plist = data.points
    J = data.jac
    
    # Find the value of the Jacobian at each point in plist
    dlist = []
    for point in plist:
        di = []
        for n1 in [0,1,2]:
            val = J[n1]
            for n2 in [0,1,2]:
                val = val.subs({varlist[n2]:point[n2]})
            di.append(val)
        dlist.append(di)
        
    # Find the conditioning numbers for every pair of points
    cnumlist = []
    s,t = sp.var('s,t')
    for p1 in plist[:-1]:
        for p2 in plist[plist.index(p1)+1:]:
            for n in [0,1,2]:
                # Make sure can project in each patch
                if p1[n]!=0 and p2[n]!=0 and dlist[plist.index(p1)][n]!=0 and dlist[plist.index(p2)][n]!=0:
                    pp1 = helpers.proj(p1,n)
                    pp2 = helpers.proj(p2,n)
                    rd1 = helpers.reciprocal(helpers.proj(dlist[plist.index(p1)],n))
                    rd2 = helpers.reciprocal(helpers.proj(dlist[plist.index(p2)],n))
                    # Make sure normals are not parallel
                    if helpers.parcheck(rd1,rd2)==False:
                        sollist = sp.solve([pp1[0]+s*rd1[0] - pp2[0] - t*rd2[0], pp1[1]+s*rd1[1] - pp2[1] - t*rd2[1]],s,t)
                        cnumlist.append(abs(sollist[s])*np.linalg.norm(np.array(rd1)))
                        cnumlist.append(abs(sollist[t])*np.linalg.norm(np.array(rd2)))
                        
    # Print result
    if cnumlist == []:
        print "No conditioning numbers were found"
    else:
        print str(len(list(set(cnumlist))))+" different conditioning numbers were found."
        print "The smallest of these is "+str(min(cnumlist))+"."
