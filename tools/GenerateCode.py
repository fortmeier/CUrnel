from sympy import *
from sympy.parsing.sympy_parser import *

from CreateKernel import *
from VectorFunctions import *
from GenerateCudaCode import *

alpha1, alpha2 = symbols('alpha1 alpha2')
mu, lamda = symbols('mu lamda')

# ===================================
#    Simple Diffusion Kernel
# ===================================
# S = 0.5 * || grad u || ^ 2 = 0.5 * (du_dx^2 + du_dy^2)
J = 0.5 * (u(x,y).diff(x)**2 + u(x,y).diff(y)**2)

# du_dt = alpha1 * lapl(u(x,y))
# better
# Euler-Lagrange Equation gives the needed linear differential operator:
# 0 = du_dt - ...
dJ = J.diff(u(x,y)) - ((J.diff(u(x,y).diff(x))).diff(x) + (J.diff(u(x,y).diff(y))).diff(y))

print "Diffusion Kernel: "
K_diff = CreateKernel(dJ) * alpha1
pprint (K_diff)
generateKernelAndSource( K_diff, "diffusionKernel", ["float alpha1"])



# ===================================
#    Linear-Elastic Kernel
# ===================================
parts = ( u_x(x,y).diff(x) + u_x(x,y).diff(x) )**2 + ( u_x(x,y).diff(y) + u_y(x,y).diff(x) )**2 + ( u_y(x,y).diff(x) + u_x(x,y).diff(y) )**2 +( u_y(x,y).diff(y) + u_x(x,y).diff(y) )**2 
Jx = mu * 0.25 * parts + lamda * 0.5 * ( u_x(x,y).diff(x) + u_x(x,y).diff(y))**2

# du_dt = alpha1 * lapl(u(x,y))
# better
# Euler-Lagrange Equation gives the needed linear differential operator:
# 0 = du_dt - ...
dJx = Jx.diff(u(x,y)) - ((Jx.diff(u_x(x,y).diff(x))).diff(x) + (Jx.diff(u_x(x,y).diff(y))).diff(y))

#print dEdiff_du
print "Linear-Elastic Kernel (x, x): "
K_LEx = CreateKernel(dJx, U_x) 
pprint (K_LEx)
#generateKernelAndSource( K_diff, "diffusionKernel", ["float alpha1"])

