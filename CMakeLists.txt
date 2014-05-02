cmake_minimum_required(VERSION 2.8)

PROJECT(CUrnel)


FIND_PACKAGE(CUDA)

ADD_CUSTOM_COMMAND(
  OUTPUT
  ${PROJECT_SOURCE_DIR}/gen_src/diffusionKernel.cuh
  COMMAND
  python ${PROJECT_SOURCE_DIR}/tools/GenerateCode.py
  WORKING_DIRECTORY
  ${PROJECT_SOURCE_DIR}/
  DEPENDS
  ${PROJECT_SOURCE_DIR}/tools/*.py
)

ADD_CUSTOM_TARGET(
  generatedCode
  ALL
  DEPENDS 
  ${PROJECT_SOURCE_DIR}/gen_src/diffusionKernel.cuh
)

SET( source
  src/main.cu
)

INCLUDE_DIRECTORIES(
  gen_src/
  include/
)

CUDA_ADD_EXECUTABLE( CUrnelTest ${source} )

