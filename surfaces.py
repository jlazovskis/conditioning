from __future__ import division
# Name: Conditioning number program for surfaces
# Description: Contains all the main functions for finding the conditioning number of a surface (that is, a variety defined by a single equation in P^3)
# Created: 2016-08-19
# Last modified: 2016-08-21
# Author: Janis Lazovskis

# Import packages
import math
import sympy as sp

# Declare variables, create a list of them, define input data class
class variety:
    def __init__(self):
        self.varlist = [] # variables to be used (e.g. [x0, x1, x2, x3] )
        self.points = []  # points to be tested (e.g. [[0,1,1,1],[1,0,1,1],[1,0,2,2]] )
        self.func = 0     # defining function (e.g. x0*x0*x1 - x2*x3*x3 +x0*x1*x2 + x2*x2*x2 )

# Import other files
import helpers
import curves

# Conditioning number finder (projective, 4 coords)
# (class variety) -> (list of real number)
# If everything is fine with the input class, this function finds the conditioning number of the 
# input class variety. If the surface is not smooth or the points are wrong, it returns an empty list
# and prints a reason.
def cnumsurface(data):
    # List of conditioning numbers
    cnumlist = []
    for p1 in data.points[:-2]:
        for p2 in data.points[data.points.index(p1)+1:]:
            for p3 in data.points[data.points.index(p2)+1:]:
                # Check which affine piece(s) points lie in 
                nonzerocoords = []
                for i in range(4):
                    if p1[i] != 0 and p2[i] != 0 and p3[i] != 0:
                        nonzerocoords.append(i)
                if len(nonzerocoords) != 0:
                    for n in nonzerocoords:
                        # Declare function and points in affine A^3 piece
                        funca3 = data.func.subs({data.varlist[n]:1})
                        pointsa3 = [helpers.proj(p1,n), helpers.proj(p2,n), helpers.proj(p3,n)]
                        # Find equation of plane spanned by three points in A^3
                        planeq = sp.det(sp.Matrix(( data.varlist[:n]+data.varlist[n+1:]+[1], pointsa3[0]+[1], pointsa3[1]+[1], pointsa3[2]+[1] )))
                        # Choose first available variable to replace in funca3
                        curvarind = -1
                        sol = []
                        while sol == [] and curvarind < 3:
                            curvarind += 1
                            sol = sp.solve(planeq, data.varlist[curvarind],dict=False)
                        if sol != []:
                            # Declare variety class to pass to conditioning number finder function for curves
                            curvedata = variety()
                            curvedata.func = funca3.subs({data.varlist[curvarind]:sol[0]})
                            curvedata.points = pointsa3
                            for p in curvedata.points:
                                if n > curvarind:
                                    del p[curvarind]
                                else:
                                    del p[curvarind-1]
                            curvedata.varlist += data.varlist
                            del curvedata.varlist[n]
                            if n > curvarind:
                                del curvedata.varlist[curvarind]
                            else:
                                del curvedata.varlist[curvarind-1]
                            cnumlist.append(curves.cnumaff(curvedata,data.varlist[curvarind])) 
    # Print and return result
    if cnumlist == []:
        print "No conditioning numbers found"
        return []
    else:
        ans = min(cnumlist)
        print str(len(cnumlist))+" conditioning numbers were found."
        print "The smallest of these is "+str(ans)+"."
        return [ans]