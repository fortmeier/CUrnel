#include "image2.cuh"

using namespace CUrnel;

template<>
__device__ float4 Image<float4, R3>::sample( R3::ScalarType ) { return make_float4(0,0,0,0); };

template<>
__device__ float Image<float, R2>::sample( R2::ScalarType ) { return 0.0f; };