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
#include "image2.cuh"

using namespace thrust;
using namespace std;

namespace CUrnel {

template<typename T, typename D>
class CudaAlterableField : public Field<T, D>
{

public:
  virtual dim3 getBlocks() {return dim3(1,1,1);}
  virtual dim3 getThreads() {return dim3(1,1,1);}

  template<typename Func>
  __device__ __inline__ void apply(Func f);

};

template<typename T, typename D>
class DeformationField : public CudaAlterableField<T, D>
{
private:
  mutable thrust::host_vector<T> hData;
  thrust::device_vector<T> dData;

  __device__ int getIndexFromBlocksAndThreads();
  __device__ typename NeightborType<T,D>::type getNeighbors( T* data );

  typename D::OrdinalType extent;

public:
  DeformationField( typename D::OrdinalType _size );

  __device__ virtual T sample( typename D::ScalarType x) { return T() * 0.0; }

  virtual dim3 getBlocks();
  virtual dim3 getThreads();

  T* getDeviceDataPointer() { return thrust::raw_pointer_cast(dData.data());}

  template<typename Func>
  __device__ __inline__ void apply(Func f, T* inData, T* outData)
  {
    int index = getIndexFromBlocksAndThreads();
    if( index < 0 ) return;
    typename NeightborType<T,D>::type n = getNeighbors( inData );

    T out = f(n);
    outData[index] = out;// make_float2(index,7);
    printf("bla %f\n", outData[index].x);

  }

  virtual std::ostream& print ( std::ostream &out ) const;

  friend std::ostream& operator<< ( std::ostream &out, const DeformationField<T,D> &field )
  {
    return field.print(out);
  }

};


class LocalDeformationField : public CudaAlterableField<float4, R3>
{
public:
  __device__ virtual float4 sample( R3::ScalarType x) { return make_float4(0,0,0,0); }
};

class PartialDeformationField : public CudaAlterableField<float4, R3>
{
public:
  __device__ virtual float4 sample( R3::ScalarType x) { return make_float4(0,0,0,0); }
};

/*
template<typename DeformationFieldType, typename ImageType, typename D>
class CudaDeformableImage : public Field<ImageType, D>
{
private:
  DeformationFieldType deformationField;
  Image<ImageType, D> image;
public:
  __device__ virtual ImageType sample( typename D::ScalarType x)
  {
    float4 u = deformationField.sample(x);
    float3 uu = make_float3( u.x, u.y, u.z );
    return image.sample( x + uu );
  }

  virtual DeformationFieldType& getDeformationField() { return deformationField; }

};*/

}