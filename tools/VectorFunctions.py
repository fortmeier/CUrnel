from sympy import *

u = symbols('u', cls=Function)
u_x, u_y, u_z = symbols('u_x u_y u_z', cls=Function)
x, y, z= symbols('x y z')

muV = symbols('muV', cls=Function)
lamdaV = symbols('lamdaV', cls=Function)

class dvg(Function):
    @classmethod
    def eval(cls, F):
        return F[0].diff(x) + F[1].diff(y)

class grad(Function):
    @classmethod
    def eval(cls, F):
        return (F.diff(x), F.diff(y))

class lapl(Function):
    @classmethod
    def eval(cls, F):
        return dvg(grad(F))