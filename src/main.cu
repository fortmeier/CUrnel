#include <thrust/host_vector.h>
#include <thrust/device_vector.h>

#include <iostream>

#include "image.cuh"
#include "diffusionKernel.cuh"

using namespace std;

void showField( Field2D<float>& A )
{
	cout << A << endl;
	return;
}

int main(void)
{
	Field2D<float> A1 = Field2D<float>(6, 6);
	Field2D<float> A2 = Field2D<float>(6, 6);

	A1.rand();
    
    cout << "A1 (old):" << endl;
    showField( A1 );

	float alpha = 0.1;

	for( int i = 0; i < 200; i++ )
	{
		applyConvolution_diffusionKernel( A1, A2, alpha );
		A1.swapWith( A2 );
	}
   	cout << "A1 (new):" << endl;
	showField( A1 );



    return 0;
}