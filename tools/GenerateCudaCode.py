from sympy import *


def generateCudaKernelCode3x3( K, functionName, additionalParams ):
	code =  "__device__ float "+functionName+"( \n"

	for p in additionalParams:
		code += "                             const "+p+", \n"

	code += "                             const float& u11, const float& u21, const float& u31, \n"
	code += "                             const float& u12, const float& u22, const float& u32, \n"
	code += "                             const float& u13, const float& u23, const float& u33  \n"
	code += "                           )\n"
	code += "{\n"
	code += "  float r = 0;\n"

	for i in range(3):
		for j in range(3):
			code += "  r += " + str(K[i,j]) + " * u"+ str(i+1)+str(j+1) + ";\n"

	code += "  return r;\n"
	code += "}\n"

	return code

def generateCudaKernel( functionName, additionalParams ):
	code = "template<typename T>\n"
	code += "__global__ void kernel_"+functionName+"(\n"
	code += "                                 Field2D<T> A,\n"
	code += "                                 Field2D<T> B,\n"
	code += "                                 " + ",".join( p for p in additionalParams )
	code += "                           )\n"
	code += "{\n"
	code += "  int x = blockIdx.x * gridDim.x + threadIdx.x;\n"
	code += "  int y = blockIdx.y * gridDim.y + threadIdx.y;\n"
	code += "  if( x >= 0 && x < A.getWidth() && y >= 0 && y < A.getHeight() ) \n"
	code += "  {\n"
	code += "    T u11 = A(x-1,y-1);\n"
	code += "    T u21 = A(x,y-1);\n"
	code += "    T u31 = A(x+1,y-1);\n"
	code += "    T u12 = A(x-1,y);\n"
	code += "    T u22 = A(x,y);\n"
	code += "    T u32 = A(x+1,y);\n"
	code += "    T u13 = A(x-1,y+1);\n"
	code += "    T u23 = A(x,y+1);\n"
	code += "    T u33 = A(x+1,y+1);\n"
	code += "    T r = "+functionName+"( \n"

	for p in additionalParams:
		code += "                             "+p.split()[1]+", \n"

	code += "                              u11,  u21,  u31, \n"
	code += "                              u12,  u22,  u32, \n"
	code += "                              u13,  u23,  u33  \n"
	code += "                           );\n"
	#code += "    printf(\"%f\\n\", r);\n"
	code += "    B.at(x,y) = u22 + r;\n"
	code += "  }\n"
	code += "  \n"


	code += "}\n"

	return code

def getDeriv(field, x):
	return str(0)

def functionToString( function, inFields ):
	r = str(function)
	for field in inFields:
		r = r.replace("Derivative("+str(field)+"(x, y), x, x)", "d"+str(field)+"_dxdx");
		r = r.replace("Derivative("+str(field)+"(x, y), x, y)", "d"+str(field)+"_dxdy");
		r = r.replace("Derivative("+str(field)+"(x, y), y, x)", "d"+str(field)+"_dydx");
		r = r.replace("Derivative("+str(field)+"(x, y), y, y)", "d"+str(field)+"_dydy");
		r = r.replace("Derivative("+str(field)+"(x, y), x)", "d"+str(field)+"_dx");
		r = r.replace("Derivative("+str(field)+"(x, y), y)", "d"+str(field)+"_dy");
	return r

def generateCudaKernelFromFunction( functionName, function, inFields, additionalParams ):
	code = "template<typename T>\n"
	code += "__global__ void kernel_"+functionName+"(\n"
	code += "                                 Field2D<T> output,\n"
	code += "                                 " + ",".join( "Field2D<T> "+str(p) for p in inFields )
	code += "                                 Field2D<T> B,\n"
	code += "                                 " + ",".join( str(p) for p in additionalParams )
	code += "                           )\n"
	code += "{\n"
	code += "  int x = blockIdx.x * gridDim.x + threadIdx.x;\n"
	code += "  int y = blockIdx.y * gridDim.y + threadIdx.y;\n"
	code += "  if( x >= 0 && x < A.getWidth() && y >= 0 && y < A.getHeight() ) \n"
	code += "  {\n"

	for field in inFields:
		code += "    T d"+str(field)+"_dx = "+getDeriv(field, 0)+";\n"
		code += "    T d"+str(field)+"_dy = "+getDeriv(field, 0)+";\n"

	#code += "    printf(\"%f\\n\", r);\n"
	code += "    T r = "+functionToString(function, inFields)+";\n"
	#code += "    T r = "+functionToString(function.simplify(), inFields)+";\n"
	code += "    output.at(x,y) = r;\n"
	code += "  }\n"
	code += "  \n"


	code += "}\n"

	return code

def generateCudaKernelApplication( functionName, additionalParams ):
	code = "template<typename T>\n"
	code += "__host__ void applyConvolution_"+functionName+"(\n"
	code += "                                 Field2D<T>& A,\n"
	code += "                                 Field2D<T>& B,\n"
	code += "                                 " + ",".join( p for p in additionalParams ) + " )\n"
	code += "{\n"
	code += "  dim3 blocks( A.getWidth() / 16 + 1, A.getHeight() / 16 + 1, 1);\n"
	code += "  dim3 threads( 16, 16, 1);\n"
	code += "  kernel_diffusionKernel<T><<<blocks, threads>>>( A, B" + "".join( ", "+p.split()[1] for p in additionalParams ) + " );\n"
	code += "}\n"

	return code
			

def generateSourceFile( functionName, code ):
	f = open('./gen_src/'+functionName+'.cuh', 'w')
	f.write("#pragma once\n\n")
	f.write("#include <stdio.h>\n\n")
	f.write(code)

	f.close()


def generateKernelAndSource( K, functionName, additionalParams=[] ):
	code = generateCudaKernelCode3x3( K, functionName, additionalParams )
	code += generateCudaKernel( functionName, additionalParams )
	code += generateCudaKernelApplication( functionName, additionalParams )
	generateSourceFile( functionName, code )
	return code