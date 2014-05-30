/**
 * 1. one baseclass given to renderer
 * 2.
 */

#include <iostream>

#include <cuda.h>

#include <thrust/host_vector.h>
#include <thrust/device_vector.h>

#include "stdio.h"
#include "cutil_math.h"

#include "field.cuh"

using namespace thrust;
using namespace std;

namespace CUrnel {

template<typename ImageType>
class imiCuda4DMotionField : public Field<ImageType, R3>
{

public:
  __device__ virtual ImageType sample( float3 x)
  {
    return make_float4(0,0,0,0);
  }
};

template<typename DeformationFieldType, typename ImageType>
class imiCuda4DMotionDeformable : public Field<ImageType, R3>
{
private:
  imiCudaDeformableImage<DeformationFieldType, ImageType, R3> image;
  imiCuda4DMotionField<ImageType> motion;
public:
  __device__ virtual ImageType sample( float3 x)
  {
    float4 u = motion.sample(x);
    float3 uu = make_float3( u.x, u.y, u.z );
    return image.sample( x + uu );
  }
};


}