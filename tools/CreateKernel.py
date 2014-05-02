from sympy import *
from sympy.parsing.sympy_parser import *

d_dx = Matrix([[0,0,0],[-0.5, 0, 0.5],[0,0,0]])
d_dy = d_dx.transpose()

d_dxdx = Matrix([[0,0,0],[1, -2, 1],[0,0,0]]) * 0.5
d_dydy = d_dxdx.transpose()

d_dxdy = Matrix([[1,0,-1],[0, 0, 0],[-1,0,1]]) * 0.25
d_dydx = d_dxdy.transpose()

ll = locals()

def CreateKernel(a, u='u'):
	r = str(a)
	#a = a.subs(Derivative(u(x,y),x,x),d_dxdx)
	#a = a.subs(Derivative(u(x,y),x,y),d_dxdy)
	#a = a.subs(Derivative(u(x,y),y,x),d_dydx)
	#a = a.subs(Derivative(u(x,y),y,y),d_dydy)
	#a = a.subs(Derivative(u(x,y),x),d_dx)
	#a = a.subs(Derivative(u(x,y),y),d_dy)

	r = r.replace("Derivative("+str(u)+"(x, y), x, x)", "d_dxdx");
	r = r.replace("Derivative("+str(u)+"(x, y), x, y)", "d_dxdy");
	r = r.replace("Derivative("+str(u)+"(x, y), y, x)", "d_dydx");
	r = r.replace("Derivative("+str(u)+"(x, y), y, y)", "d_dydy");
	r = r.replace("Derivative("+str(u)+"(x, y), x)", "d_dx");
	r = r.replace("Derivative("+str(u)+"(x, y), y)", "d_dy");

	r = parse_expr(r, local_dict=ll)
	return r