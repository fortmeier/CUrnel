from sympy import *
from sympy.parsing.sympy_parser import *

#U = symbols("U")
#U = MatrixSymbol('U', 3, 3)
#U_x = MatrixSymbol('U_x', 3, 3)
#U_y = MatrixSymbol('U_y', 3, 3)

Z = Matrix([[0,0,0],[0, 0, 0],[0,0,0]])

i = Matrix([[0,0,0],[0, 1, 0],[0,0,0]])

d_dx = Matrix([[0,0,0],[-0.5, 0, 0.5],[0,0,0]])
d_dy = d_dx.transpose()

d_dxdx = Matrix([[0,0,0],[1, -2, 1],[0,0,0]]) * 0.5
d_dydy = d_dxdx.transpose()

d_dxdy = Matrix([[1,0,-1],[0, 0, 0],[-1,0,1]]) * 0.25
d_dydx = d_dxdy.transpose()

ll = locals()

def CreateKernel(a, u, symR = []):
	a=a.replace(Subs, lambda A,B,C: A.xreplace(dict(zip(B,C))))

	for R in symR:
		print R
		a = a.replace(R(Wild("*")), 0)

	print a
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

	r = r.replace("Derivative("+str(u)+"(x, y), x, x)", "d_dxdx");
	r = r.replace("Derivative("+str(u)+"(x, y), x, y)", "d_dxdy");
	r = r.replace("Derivative("+str(u)+"(x, y), y, x)", "d_dydx");
	r = r.replace("Derivative("+str(u)+"(x, y), y, y)", "d_dydy");
	r = r.replace("Derivative("+str(u)+"(x, y), x)", "d_dx");
	r = r.replace("Derivative("+str(u)+"(x, y), y)", "d_dy");
	r = r.replace(str(u)+"(x, y)", "i");

	for R in symR:
		r = r.replace("Derivative("+str(R)+"(x, y), x, x)", "Z");
		r = r.replace("Derivative("+str(R)+"(x, y), x, y)", "Z");
		r = r.replace("Derivative("+str(R)+"(x, y), y, x)", "Z");
		r = r.replace("Derivative("+str(R)+"(x, y), y, y)", "Z");
		r = r.replace("Derivative("+str(R)+"(x, y), x)", "Z");
		r = r.replace("Derivative("+str(R)+"(x, y), y)", "Z");


	print r
	r = parse_expr(r, local_dict=ll)

	return r