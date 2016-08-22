# Name: Examples for using conditioning number finders
# Description: Contains some examples with descriptions of how to use the functions
# Created: 2016-08-18
# Last modified: 2016-08-21
# Author: Janis Lazovskis

# Navigate to the conditioning directory
# Run Python 2

# Example (curve)
execfile('curves.py')
x = variety()
x0,x1,x2 = sp.var('x0,x1,x2')
x.varlist = [x0,x1,x2]
x.func = x0*x0 + x1*x2 - x1*x0
x.points = [[1,1,0], [2,1,-2]]
cnumcurve(x)

# Non-example (curve)
# Use the above, but instead, put:
x.points = [[1,1,0], [2,1,-2], [0,0,0]]
# Then cnumcurve will return an empty list saying the last point isn't in P^2
cnumcurve(x)

# Non-example (curve)
# Use the above, but instead, put:
x.points = [[1,1,0], [2,1,-2], [1,1,1]]
# Then cnumcurve will return an empty list saying the last point isn't on the curve 
cnumcurve(x)

# Example surface
execfile('surfaces.py')
x = variety()
x0,x1,x2,x3 = sp.var('x0,x1,x2,x3')
x.varlist = [x0,x1,x2,x3]
x.func = x0*x1 - x2*x3
x.points = [[1,1,1,1], [0,1,1,0], [0,1,0,1], [2,1,1,2]]
cnumsurface(x)

# Non-example (surface)
execfile('surfaces.py')
x = variety()
x0,x1,x2,x3 = sp.var('x0,x1,x2,x3')
x.varlist = [x0,x1,x2,x3]
x.func = x0*x0*x1 - x2*x3*x3 + x0*x1*x2 +x2*x2*x2
x.points = [[0,1,1,1], [1,0,1,1], [1,0,2,2], [1,1,-1,1]]
# This will raise an error because the curve is not smooth
cnumsurface(x)