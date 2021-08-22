# How to install cuML

## Building from source

**Prerequisites:**
* Conda
* GCC 9
* NVCC in CUDA toolkit 10+

1. Clone the repository:
   ```sh
   git clone https://github.com/rapidsai/cuml.git
   cd cuml
   git checkout branch-0.19 # optional
   git submodule update --init --remote --recursive
   ```
2. Install dependencies
   * If you built cuDF from source, update Conda environment:
     ```sh
     conda env update --name cudf_dev --file conda/environments/cuml_dev_cuda11.2.yml
     conda activate cudf_dev
     ```
   * If you have no cuDF installed, create Conda environment:
     ```sh
     conda env create --name cuml_dev --file conda/environments/cuml_dev_cuda11.2.yml
     conda activate cuml_dev
     ``` 
3. _Optional._ Set paths to the compiler and shared libraries:
   ```sh
   export GCC=$HOME/misc/gcc-9-build
   export CC=$GCC/bin/gcc
   export CXX=$GCC/bin/c++
   export CUDATOOLKIT=/common/cuda-11.2
   export CUDACXX=$CUDATOOLKIT/bin/nvcc
   export LD_LIBRARY_PATH=$GCC/lib64:$CUDATOOLKIT/lib64:$LD_LIBRARY_PATH
   ```
4. _Carefully._ Add `#include <cstdint>` line to `cpp/include/cuml/tree/flatnode.h` file right after the line with `#pragma once`.
5. Build C++ part:
   ```sh
   cd cpp
   mkdir build && cd build
   cmake .. -DCMAKE_INSTALL_PREFIX=$CONDA_PREFIX -DCUDA_TOOLKIT_ROOT_DIR=$CUDATOOLKIT
   make -j
   make install
   ```
6. Return to the repository root:
   ```sh
   cd ../..
   ```
7. Build and install Python part:
   ```sh
   cd python
   python setup.py build_ext --inplace
   python setup.py install
   ```


## Downloading pre-built binaries

**Prerequisites:**
* Conda

```sh
conda create -n rapids-21.06 -c rapidsai -c nvidia -c conda-forge \
    cuml=21.06 python=3.8 cudatoolkit=11.2
```
