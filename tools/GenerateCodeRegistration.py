from sympy import *
from sympy.parsing.sympy_parser import *

from CreateKernel import *
from VectorFunctions import *
from GenerateCudaCode import *

alpha1, alpha2 = symbols('alpha1 alpha2')

R, T = symbols('R D', cls=Function)

#M = MatrixSymbol('M', 3, 3)

#A = Matrix([[0,0,0],[-0.5, 0, 0.5],[0,0,0]])
# pprint (d_dx)
# pprint (d_dy)
# pprint (d_dxdx)
# pprint (d_dydy)
# pprint (d_dxdy)
# pprint (d_dydx)
#a = alpha1 * u(x,y).diff(x).diff(x) + alpha2 * u(x,y).diff(x)

# S = || grad u || ^ 2 = du_dx + du_dy
S = u(x,y).diff(x) + u(x,y).diff(y)

# D = (R - T)**2
# for now, only one direction
D = (R(x,y) - T(x+u(x,y),y))**2
E = D + alpha1 * S

# ??? gradient fuer eine richtung totales differential???
du_dt = E.diff(x) + E.diff(y)
#du_dt = alpha1 * lapl(u(x,y))

print du_dt
K_diff = CreateKernel(du_dt) 
print K_diff
#generateKernelAndSource( K_diff, "diffusionKernel", ["float alpha1"])

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

