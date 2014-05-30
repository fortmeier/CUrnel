
#include <iostream>
#include <iomanip>

#include "deformationfield.cuh"

using namespace std;
using namespace thrust;

using namespace CUrnel;

template<typename D>
size_t getFieldLength( typename D::OrdinalType _size );

template<>
size_t getFieldLength<R2>( R2::OrdinalType _size )
{
  return _size.x * _size.y;
}


template<typename T, typename D>
DeformationField<T,D>::DeformationField( typename D::OrdinalType _size ) :
  extent (_size)
{
  size_t size = getFieldLength<D>(_size);
  hData.resize(size);
  dData.resize(size);
  dData[6*3 + 2] = make_float2(10,10);
}

template<typename D>
dim3 getBlocksHelper(D extent);

template<>
dim3 getBlocksHelper<R2::OrdinalType>(R2::OrdinalType extent)
{
  return dim3(extent.y,1,1);
}

template<typename T, typename D>
dim3 DeformationField<T,D>::getBlocks()
{
  return getBlocksHelper(extent);
}


template<typename D>
dim3 getThreadsHelper(D extent);

template<>
dim3 getThreadsHelper<R2::OrdinalType>(R2::OrdinalType extent)
{
  return dim3(extent.x,1,1);
}

template<typename T, typename D>
dim3 DeformationField<T,D>::getThreads()
{
  return getThreadsHelper(extent);
}


template<typename D>
__device__ int getIndexHelper(D pos, D extent, bool limit = true);

template<>
__device__ int getIndexHelper<R2::OrdinalType>(R2::OrdinalType pos, R2::OrdinalType extent, bool limit)
{
  int& x = pos.x;
  int& y = pos.y;
  if( limit )
    if(y < 1 || y > extent.y - 2 || x < 1 || x > extent.x -2 ) return -1;
  int id = y * extent.y + x;
  return id;
}

template<typename D>
__device__ D getPositionFromBlocksAndThreads();

template<>
__device__ R2::OrdinalType getPositionFromBlocksAndThreads<R2::OrdinalType>()
{
  return make_int2(threadIdx.x, blockIdx.x);
}

template<typename T, typename D>
__device__ int DeformationField<T,D>::getIndexFromBlocksAndThreads()
{
  typename D::OrdinalType pos = getPositionFromBlocksAndThreads<D::OrdinalType>();
  return getIndexHelper( pos, extent, true );
}

template<typename T>
__device__ void neighborsHelper( N3x3<T>* neighbors, R2::OrdinalType pos, R2::OrdinalType extent, T* data )
{
  neighbors->m11 = data[getIndexHelper(make_int2(pos.x - 1, pos.y - 1), extent, false)];
  neighbors->m21 = data[getIndexHelper(make_int2(pos.x + 0, pos.y - 1), extent, false)];
  neighbors->m31 = data[getIndexHelper(make_int2(pos.x + 1, pos.y - 1), extent, false)];

  neighbors->m12 = data[getIndexHelper(make_int2(pos.x - 1, pos.y + 0), extent, false)];
  neighbors->m22 = data[getIndexHelper(make_int2(pos.x + 0, pos.y + 0), extent, false)];
  neighbors->m32 = data[getIndexHelper(make_int2(pos.x + 1, pos.y + 0), extent, false)];

  neighbors->m13 = data[getIndexHelper(make_int2(pos.x - 1, pos.y + 1), extent, false)];
  neighbors->m23 = data[getIndexHelper(make_int2(pos.x + 0, pos.y + 1), extent, false)];
  neighbors->m33 = data[getIndexHelper(make_int2(pos.x + 1, pos.y + 1), extent, false)];


}

template<typename T, typename D>
__device__ typename NeightborType<T,D>::type DeformationField<T,D>::getNeighbors( T* data )
{
  typename NeightborType<T,D>::type neighbors;
  typename D::OrdinalType pos = getPositionFromBlocksAndThreads<D::OrdinalType>();
  neighborsHelper(&neighbors, pos, extent, data );

  return neighbors;
}



template<typename T, typename D>
ostream& DeformationField<T,D>::print( ostream &out ) const
{
  hData = dData;	
  /*for( int j = 0; j < field.h; j++ )
  {
    for( int i = 0; i < field.w; i++ )
    {
      out << std::setw( 4 ) << field.hData[i + j*field.w] << " ";
    }
    out << "\n";
  }*/
  for(int i = 0; i < hData.size(); i++ )
  {
    out << setw(8) << hData[i].x << " ";
  }
  out << endl;
  return out;
}

template<>
ostream& DeformationField<float2,R2>::print( ostream &out ) const
{
  hData = dData;	
  /*for( int j = 0; j < field.h; j++ )
  {
    for( int i = 0; i < field.w; i++ )
    {
      out << std::setw( 4 ) << field.hData[i + j*field.w] << " ";
    }
    out << "\n";
  }*/
  out << endl;
  for(int i = 0; i < extent.y; i++ )
  {
    for(int j = 0; j < extent.x; j++ )
    {
      out << setw(8) << hData[i*extent.y + j].x << " ";
    }
    out << endl;
  }
  out << endl;
  return out;
}


template class DeformationField<float2, R2>;
