/**
 * 1. one baseclass given to renderer
 * 2.
 */
#pragma once

#include <iostream>

#include <cuda.h>

#include <thrust/host_vector.h>
#include <thrust/device_vector.h>

#include "stdio.h"
#include "cutil_math.h"

using namespace thrust;
using namespace std;

namespace CUrnel
{

template<typename T>
struct N3x3
{
  T m11; T m21; T m31;
  T m12; T m22; T m32;
  T m13; T m23; T m33;
};

template<typename T>
struct N3x3x3
{
  T m111; T m211; T m311;
  T m121; T m221; T m321;
  T m131; T m231; T m331;

  T m112; T m212; T m312;
  T m122; T m222; T m322;
  T m132; T m232; T m332;

  T m113; T m213; T m313;
  T m123; T m223; T m323;
  T m133; T m233; T m333;
};

template<int d>
struct DimensionType {
  typedef void ScalarType;
  typedef void OrdinalType;
  static const int dimensions = 0;
};

template<>
struct DimensionType<2> {
  typedef float2 ScalarType;
  typedef int2 OrdinalType;
  static const int dimensions = 2;
};
typedef DimensionType<2> R2;

template<>
struct DimensionType<3> {
  typedef float3 ScalarType;
  typedef int3 OrdinalType;
  static const int dimensions = 3;
};
typedef DimensionType<3> R3;

template<typename T, typename D>
struct NeightborType {
  typedef void type;
};

template<typename T>
struct NeightborType<T, R2> {
  typedef N3x3<T> type;
};

template<typename T>
struct NeightborType<T, R3> {
  typedef N3x3x3<T> type;
};



template<typename T, typename D>
class Field
{
public:
  typedef T fieldtype;
  typedef D dimtype;
  __device__ virtual T sample( typename D::ScalarType x) = 0;
  __device__ virtual T diff( typename D::ScalarType x) { return T(); }


};

}