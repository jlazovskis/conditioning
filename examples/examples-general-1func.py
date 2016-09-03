# Name: Examples for using conditioning number finders for general projective varieties
# Description: Contains some examples with descriptions of how to use the functions
# Created: 2016-08-29
# Author: Janis Lazovskis

# Navigate to the conditioning directory
# Run Python 2

# Execute file
execfile('general-1func.py')
# Open file and read off points
f = open('examples/cone10.txt','r')
p = f.readline()[2:-3].split('], [')
f.close()
l = map(lambda x: [float(x[0]), float(x[1]), float(x[2])], map(lambda y: y.split(','), p))
# Declare variety
cone = variety()
x0,x1,x2 = sp.var('x0,x1,x2')
cone.varlist = [x0,x1,x2]
cone.points = l
cone.func = x0**2 + x1**2 - x2**2
# Run main function
cnumgen(cone)
