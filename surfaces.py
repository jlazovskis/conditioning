from __future__ import division
# Name: Conditioning number program for surfaces
# Description: Contains all the main functions for finding the conditioning number of a surface (that is, a variety defined by a single equation in P^3)
# Created: 2016-08-19
# Last modified: 2016-08-19
# Author: Janis Lazovskis

# Import packages
import numpy as np
import sympy as sp

# Declare variables, create a list of them, define input data class
class thingy:
    def __init__(self):
        self.varlist = [] # variables to be used (e.g. [x0, x1, x2, x3] )
        self.points = []  # points to be tested (e.g. [[0,1,1,1],[1,0,1,1],[1,0,2,2]] )
        self.func = 0     # defining function (e.g. x0*x0*x1 - x2*x3*x3 +x0*x1*x2 + x2*x2*x2 )
        self.jac = []     # Jacobian of function (always sp.Matrix([x.func]).jacobian(varlist) )

# Import other files
import helpers
import curves

def finder(data):
    # List of conditioning numbers
    anslist = []
    # Class to pass to curve finder
    curvedata = thingy()
    # Declare variables
    for var in data.varlist:
        var = sp.var(str(var))
    nonzerocoords = []
    for i in range(len(data.points)-2):
        for j in range(4):
            if data.points[i][j] != 0 and data.points[i+1][j] != 0 and data.points[i+2][j] != 0:
                nonzerocoords.append(j)
        if len(nonzerocoords) == 0:
            print "Warning: Points "+str(i+1)+", "+str(i+2)+", "+str(i+3)+" do not lie in a common affine piece. Skipping them."
        else:
            for affpiece in nonzerocoords:
                # New points projected to certain affine piece
                npoints = []
                for k in [0,1,2]:
                    npoints.append(helpers.proj(data.points[i+k],affpiece))
                # Matrix for finding equation of plane spanned by three points in npoints
                M = sp.Matrix(( data.varlist[:affpiece]+data.varlist[affpiece+1:]+[1], npoints[0]+[1], npoints[1]+[1], npoints[2]+[1] ))
                planeq = sp.det(M)
                # Find some variable in equation to be replaced
                curvarind = -1
                sol = []
                while sol == []:
                    curvarind += 1
                    sol = sp.solve(planeq, data.varlist[curvarind])
                # Define new class for use by curve function
                curvedata.varlist = data.varlist[:curvarind] + data.varlist[curvarind+1:]
                curvedata.points = []
                for l in [0,1,2]:
                    curvedata.points.append(data.points[l][:curvarind] + data.points[l][curvarind+1:])
                curvedata.func = data.func.subs({data.varlist[curvarind]:sol[0]})
                curvedata.jac = sp.Matrix([curvedata.func]).jacobian(data.varlist[:curvarind] + data.varlist[curvarind+1:])
                # Pass to curve finder
                print curvedata.func
                print curvedata.points
                curves.checker(curvedata)
                anslist  = anslist + curves.finder(curvedata)  
        nonzerocoords = []
    # Print and return result
    if anslist == []:
        print "No conditioning numbers found"
        return []
    else:
        ans = min(anslist)
        print str(len(anslist))+" conditioning numbers were found."
        print "The smallest of these is "+str(ans)+"."
        return [ans]
