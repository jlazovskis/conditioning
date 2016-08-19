# Name: Examples for using conditioning number finders
# Description: Contains some examples with descriptions of how to use the functions
# Created: 2016-08-18
# Last modified: 2016-08-18
# Author: Janis Lazovskis

# Navigate to the conditioning directory
# Run Python 2

execfile('curves.py')
x = thingy()
x.func = x0*x0 + x1*x2 - x1*x0
x.points = [[1,1,1],[1,1,0],[0,0,0],[2,1,-2],[0,0,0]]
x.jac = sp.Matrix([x.func]).jacobian(varlist)
# This will remove three points
checker(x)
# This will find the smallest conditioning number
finder(x)
