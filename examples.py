# Name: Examples for using conditioning number finders
# Description: Contains some examples with descriptions of how to use the functions
# Created: 2016-08-18
# Last modified: 2016-08-18
# Author: Janis Lazovskis

# Navigate to the conditioning directory
# Run Python 2

# Example for a curve
execfile('curves.py')
x = thingy()
x0,x1,x2 = sp.var('x0,x1,x2')
x.varlist = [x0,x1,x2]
x.func = x0*x0 + x1*x2 - x1*x0
x.points = [[1,1,1], [1,1,0], [0,0,0], [2,1,-2], [0,0,0]]
x.jac = sp.Matrix([x.func]).jacobian(x.varlist)
# This will remove three points
checker(x)
# This will find the smallest conditioning number
finder(x)

# Example for a surface
execfile('surfaces.py')
x = thingy()
x0,x1,x2,x3 = sp.var('x0,x1,x2,x3')
x.varlist = [x0,x1,x2,x3]
x.func = x0*x0*x1 - x2*x3*x3 + x0*x1*x2 +x2*x2*x2
x.points = [[0,1,1,1], [1,0,1,1], [1,0,2,2], [1,1,-1,1]]
x.jac = sp.Matrix([x.func]).jacobian(x.varlist)
# This will raise an error because the curve is not smooth
finder(x)

# Example for a surface
execfile('surfaces.py')
x = thingy()
x0,x1,x2,x3 = sp.var('x0,x1,x2,x3')
x.varlist = [x0,x1,x2,x3]
x.func = x0*x1 - x2*x3
x.points = [[1,1,1,1], [0,1,1,0], [0,1,0,1], [2,1,1,2]]
x.jac = sp.Matrix([x.func]).jacobian(x.varlist)
finder(x)
