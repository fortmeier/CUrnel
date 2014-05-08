from sympy import *
from sympy.parsing.sympy_parser import *

#U = symbols("U")
U = MatrixSymbol('U', 3, 3)
U_x = MatrixSymbol('U_x', 3, 3)
U_y = MatrixSymbol('U_y', 3, 3)

d_dx = Matrix([[0,0,0],[-0.5, 0, 0.5],[0,0,0]])
d_dy = d_dx.transpose()

d_dxdx = Matrix([[0,0,0],[1, -2, 1],[0,0,0]]) * 0.5
d_dydy = d_dxdx.transpose()

d_dxdy = Matrix([[1,0,-1],[0, 0, 0],[-1,0,1]]) * 0.25
d_dydx = d_dxdy.transpose()

ll = locals()

def CreateKernel(a, symU=U):
	r = str(a)
	#a = a.subs(Derivative(u(x,y),x,x),d_dxdx)
	#a = a.subs(Derivative(u(x,y),x,y),d_dxdy)
	#a = a.subs(Derivative(u(x,y),y,x),d_dydx)
	#a = a.subs(Derivative(u(x,y),y,y),d_dydy)
	#a = a.subs(Derivative(u(x,y),x),d_dx)
	#a = a.subs(Derivative(u(x,y),y),d_dy)

	# r = r.replace("Derivative("+str(symu)+"(x, y), x, x)", "d_dxdx * U");
	# r = r.replace("Derivative("+str(symu)+"(x, y), x, y)", "d_dxdy * U");
	# r = r.replace("Derivative("+str(symu)+"(x, y), y, x)", "d_dydx * U");
	# r = r.replace("Derivative("+str(symu)+"(x, y), y, y)", "d_dydy * U");
	# r = r.replace("Derivative("+str(symu)+"(x, y), x)", "d_dx * U");
	# r = r.replace("Derivative("+str(symu)+"(x, y), y)", "d_dy * U");

	r = r.replace("Derivative(u(x, y), x, x)", "d_dxdx * U");
	r = r.replace("Derivative(u(x, y), x, y)", "d_dxdy * U");
	r = r.replace("Derivative(u(x, y), y, x)", "d_dydx * U");
	r = r.replace("Derivative(u(x, y), y, y)", "d_dydy * U");
	r = r.replace("Derivative(u(x, y), x)", "d_dx * U");
	r = r.replace("Derivative(u(x, y), y)", "d_dy * U");


	r = r.replace("Derivative(u_x(x, y), x, x)", "d_dxdx * U_x");
	r = r.replace("Derivative(u_x(x, y), x, y)", "d_dxdy * U_x");
	r = r.replace("Derivative(u_x(x, y), y, x)", "d_dydx * U_x");
	r = r.replace("Derivative(u_x(x, y), y, y)", "d_dydy * U_x");
	r = r.replace("Derivative(u_x(x, y), x)", "d_dx * U_x");
	r = r.replace("Derivative(u_x(x, y), y)", "d_dy * U_x");


	r = r.replace("Derivative(u_y(x, y), x, x)", "d_dxdx * U_y");
	r = r.replace("Derivative(u_y(x, y), x, y)", "d_dxdy * U_y");
	r = r.replace("Derivative(u_y(x, y), y, x)", "d_dydx * U_y");
	r = r.replace("Derivative(u_y(x, y), y, y)", "d_dydy * U_y");
	r = r.replace("Derivative(u_y(x, y), x)", "d_dx * U_y");
	r = r.replace("Derivative(u_y(x, y), y)", "d_dy * U_y");

	r = parse_expr(r, local_dict=ll)

	r = r.subs(symU,1)
	r = r.subs(U,0)
	r = r.subs(U_x,0)
	r = r.subs(U_y,0)
	r2 = str(r)
	r = parse_expr(r2, local_dict=ll)	

	return r