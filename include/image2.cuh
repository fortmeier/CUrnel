#pragma once
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

template<typename T, typename D>
class Image : public Field<T, D>
{
protected:
  cudaArray* dArray;
  cudaTextureObject_t texObj;
public:
  void setData( T* data, int w, int h = 0, int d = 0, int q = 0 );
  __device__ virtual T sample( typename D::ScalarType x);
};


}