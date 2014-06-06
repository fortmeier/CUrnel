#include <thrust/host_vector.h>
#include <thrust/device_vector.h>

#include <iostream>

#include "image.cuh"
#include "image2.cuh"
#include "deformationfield.cuh"

#include "diffusionKernel.cuh"
#include "diffusion.cuh"

using namespace std;
using namespace CUrnel;

void showField( Field2D<float>& A )
{
	cout << A << endl;
	return;
}

int methodA(void)
{

	Field2D<float> A1 = Field2D<float>(6, 6);
	Field2D<float> A2 = Field2D<float>(6, 6);

	A1.rand();
    
    cout << "A1 (old):" << endl;
    showField( A1 );

	float alpha = -0.1;

	for( int i = 0; i < 200; i++ )
	{
		applyConvolution_diffusionKernel( A1, A2, alpha );
		A1.swapWith( A2 );
	}
   	cout << "A1 (new):" << endl;
	showField( A1 );



    return 0;
}

int methodB(void)
{
  int2 size = make_int2(6,6);
  Image<float, R2> r;
  Image<float, R2> t;

  DeformationField<float2, R2> phi1(size);
  DeformationField<float2, R2> phi2(size);

  cout << "phi1:" << phi1 << endl;
  cout << "phi2:" << phi2 << endl;

  apply_diffusion( phi1, phi2, -0.1 );

  cout << "phi1:" << phi1 << endl;
  cout << "phi2:" << phi2 << endl;

  apply_diffusion( phi2, phi1, -0.1 );

  cout << "phi2:" << phi2 << endl;
  cout << "phi1:" << phi1 << endl;

  return 0;
}

int main(void)
{
  methodA();
  methodB();
  return 0;
}


/*
int main()
{

  imiCudaImage<float4, R3> image0;
  imiCudaDeformableImage<imiLocalDeformationField, float4, R3> image1a;
  imiCudaDeformableImage<imiDeformationField<float4, R3>, float4, R3> image1b;
  imiCuda4DMotionDeformable<imiLocalDeformationField, float4> image2a;
  imiCuda4DMotionDeformable<imiPartialDeformationField, float4> image2b;

  std::cout<<"testing"<<std::endl;
  render( image0 );
  render( image1a );
  render( image1b );
  render( image2a );
  render( image2b );

  imiLocalDeformationField& dfield = image1a.getDeformationField();
  //applyDiffusion( dfield );

  //imiCudaImage<float, R2> r;
  //imiCudaImage<float, R2> t;
  imiDeformationField<float, R2> phi;
  imiDeformationField<float, R3> phi3D;

  applyDiffusion( phi );
  applyDiffusion( phi3D );

}*/
