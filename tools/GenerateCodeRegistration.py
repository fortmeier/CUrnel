from sympy import *
from sympy.parsing.sympy_parser import *

from CreateKernel import *
from VectorFunctions import *
from GenerateCudaCode import *

class dT(Function):
    @classmethod
    def diff(cls, x):
        return 0


class T(Function):
    @classmethod
    def diff(cls, x):
        return dT(x)

alpha1, alpha2 = symbols('alpha1 alpha2')

R = symbols('R', cls=Function)

# S = 0.5 * || grad u || ^ 2 = 0.5 * (du_dx^2 + du_dy^2)
S = 0.5 * (u(x,y).diff(x)**2 + u(x,y).diff(y)**2)

# D = (R - T)**2
# for now, only one direction
D = 0.5 * (R(x,y) - T(x+u(x,y),y))**2
#D = 0
J = D + alpha1 * S
print D.diff(u(x,y).diff(x))
print "J: "+str(J)
# Euler-Lagrange Equation gives the needed linear differential operator:
# 0 = du_dt - ...
dJ = J.diff(u(x,y)) - ( (J.diff(u(x,y).diff(x))).diff(x) + (J.diff(u(x,y).diff(y))).diff(y) )

print "dJ: " + str(dJ)
K_diff = CreateKernel(dJ, u, [R, T, dT]) 
pprint (K_diff)

