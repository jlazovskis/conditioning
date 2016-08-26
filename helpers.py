from __future__ import division
# Name: Helper function file
# Description: Contains helper functions for other functions that find the conditioning number
# Created: 2016-08-18
# Last modified: 2016-08-21
# Author: Janis Lazovskis

# Import packages
import math
import sympy as sp

# Projection function
# (point, non-negative integer) -> (point)
# Projects a point from P^2 to C^2
# Example: proj([2,3,4],0) -> [3/2,2]
def proj(point,coord):
    L = []
    for i in range(len(point)):
        if i!=coord:
            L.append(point[i]/point[coord])
    for i in range(len(L)):
        L[i] = eval(str(L[i]))
    return L

# Reciprocal function
# (point) -> (point)
# Gives a vector perpendicular to the input vector
# Example: reciprocal([3,5]) -> [-5,3]
def reciprocal(point):
    return [-1*point[1],point[0]]

# Parallel checker function
# (point, point) -> boolean
# Checks if two vectors are parallel. Returns True if they are, False otherwise
# Example: parcheck([3,3],[-1/2,-1/2]) -> True
# Example: parcheck([3,4],[7,-1]) -> False
def parcheck(point1, point2):
    return iszero(point1[0]*point2[1] - point1[1]*point2[0])

# Approximate zero
# number -> boolean
# Checks if given number is close enough to zero. This allows for machine imprecision
def iszero(num):
    if sp.N(abs(num)) < 10**(-4):
        return True
    else:
        return False

# Norm function
# (list of number) -> number
# Finds the norm of a vector
def mynorm(point):
    ans = 0
    for p in point:
        ans += p*p
    return math.sqrt(ans)
