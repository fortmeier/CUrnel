from sympy import *
from sympy.parsing.sympy_parser import *

from CreateKernel import *
from VectorFunctions import *
from GenerateCudaCode import *

alpha1, alpha2 = symbols('alpha1 alpha2')

#M = MatrixSymbol('M', 3, 3)

#A = Matrix([[0,0,0],[-0.5, 0, 0.5],[0,0,0]])
# pprint (d_dx)
# pprint (d_dy)
# pprint (d_dxdx)
# pprint (d_dydy)
# pprint (d_dxdy)
# pprint (d_dydx)
#a = alpha1 * u(x,y).diff(x).diff(x) + alpha2 * u(x,y).diff(x)


du_dt = alpha1 * lapl(u(x,y))
K_diff = CreateKernel(du_dt) 
generateKernelAndSource( K_diff, "diffusionKernel", ["float alpha1"])

#print "Linear-elasticity kernel:"
#mu, lamda = symbols("mu lamda")
#fx = (mu+lamda)*(dvg([u(x,y),u(x,y)])).diff(x) + mu*lapl(u(x,y))
#fy = (mu+lamda)*(dvg([u(x,y),u(x,y)])).diff(y) + mu*lapl(u(x,y))

#print fx

#dfx_dx = fx.diff(x)
#dfx_dy = fx.diff(y)

#print dfx_dx
#print (du_dt)
#pprint (CreateKernel(fx,locals()))
#pprint (CreateKernel(fy,locals()))

