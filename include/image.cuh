#pragma once

#include <iostream>
#include <iomanip>

#include <thrust/host_vector.h>
#include <thrust/device_vector.h>


using namespace thrust;
using namespace std;
/*
class Kernel3x3
{
  thrust::host_vector<T> hData;
  thrust::device_vector<T> dData;

public:

};
*/

template<typename T>
class Field2D 
{
  host_vector<T> hData;
  device_vector<T> dData;

  T* dRawPointer;

  unsigned int w;
  unsigned int h;

public:
  Field2D(int w, int h);
  void swapWith( Field2D<T>& B );
  void rand();

  __host__ __device__ unsigned int getWidth() const;
  __host__ __device__ unsigned int getHeight() const;

  template<typename t>
  friend ostream& operator<< ( ostream &out, Field2D<t>& field );

  __device__ T operator() (int x, int y ) const ;
  __device__ T& at(int x, int y);

};

template<typename T>
Field2D<T>::Field2D(int _w, int _h) :
  w(_w),
  h(_h)
{
  hData.resize(w*h);
  dData.resize(w*h);
  dRawPointer = thrust::raw_pointer_cast(&dData[0]);
}

template<typename T>
void Field2D<T>::swapWith( Field2D<T>& B )
{
  hData.swap( B.hData );
  dData.swap( B.dData );
  dRawPointer = thrust::raw_pointer_cast(&dData[0]);
  B.dRawPointer = thrust::raw_pointer_cast(&B.dData[0]);
}


__host__ static __inline__ float rand_01()
{
    return ((float)rand()/RAND_MAX);
}

template<typename T>
void Field2D<T>::rand()
{
  thrust::generate(hData.begin(), hData.end(), rand_01);
  dData = hData;
}

template<typename T>
__host__ __device__ unsigned int Field2D<T>::getWidth() const
{
  return w;
}

template<typename T>
__host__ __device__ unsigned int Field2D<T>::getHeight() const
{
  return h;
}


template<typename T>
ostream& operator<< ( ostream &out, Field2D<T> &field )
{
  field.hData = field.dData;	
  for( int j = 0; j < field.h; j++ )
  {
    for( int i = 0; i < field.w; i++ )
    {
      out << std::setw( 4 ) << field.hData[i + j*field.w] << " ";
    }
    out << "\n";
  }
  return out;
}

template<typename T>
__device__ T Field2D<T>::operator() (int x, int y) const
{
	if( x < 0 || y < 0 || x >= w || y >= h ) return 0;
	return dRawPointer[x + y * w];
}

template<typename T>
__device__ T& Field2D<T>::at(int x, int y)
{
	return dRawPointer[x + y * w];
}
/*
template<typename T>
__device__ void Field2D<T>::setDevice( int x, int y, T value )
{
	dRawPointer[x + y * w] = value;
}
*/

class Region2D
{

};

