# Name: Helper function file
# Description: Contains helper functions for other functions that find the conditioning number
# Created: 2016-08-18
# Last modified: 2016-08-18
# Author: Jānis Lazovskis

# Packages to import
import numpy

# Declare variables, create a list of them, define input data class
x0,x1,x2 = var('x0,x1,x2')
varlist = [x0,x1,x2]
class input:
    def __init__(self):
        self.points = [] # points to be tested (e.g. [[1,1,0],[2,1,-2]] )
        self.func = 0    # defining function (e.g. x0*x0 + x1*x2 - x1*x0 )
        self.jac = []    # Jacobian of function (always jacobian(func,tuple(varlist)) )

# Projection function
# (point, non-negative integer) -> (point)
# Projects a point from P^2 to C^2
# Example: proj([2,3,4],0) -> [3/2,2]
def proj(point,coord):
    L = []
    for i in range(len(point)):
        if i!=coord:
            L.append(point[i]/point[coord])
    return L

# Reciprocal function
# (point) -> (point)
# Gives a vector perpendicular to the input vector
# Example: reciprocal([3,5]) -> [-5,3]
def reciprocal(point):
    return [-point[1],point[0]]

# Parallel checker function
# (point, point) -> boolean
# Checks if two vectors are parallel. Returns True if they are, False otherwise
# Example: parcheck([3,3],[-1/2,-1/2]) -> True
# Example: parcheck([3,4],[7,-1]) -> False
def parcheck(point1, point2):
    if point1[0]/point2[0] == point1[1]/point2[1]:
        return True
    else:
        return False
