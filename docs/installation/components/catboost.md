# How to install CatBoost library

## Building from source

**Prerequisites:**
* GCC 9+
* CUDA toolkit 10+

1. Clone the repository:
   ```sh
   git clone https://github.com/catboost/catboost.git
   cd catboost
   ```
2. Build the library with `ya`:
   ```sh
   cd catboost/python-package/catboost
   ../../../ya make -r -DUSE_ARCADIA_PYTHON=no -DUSE_SYSTEM_PYTHON=3.6 -DCUDA_ROOT=/common/cuda-11.2 -DHAVE_CUDA=yes
   ```


## Installing pre-build binaries

**Prerequisites:**
* Conda

```sh
conda install catboost
```


## References

* [CatBoost repository](https://github.com/catboost/catboost)
* [Python package installation in Conda](https://catboost.ai/docs/installation/python-installation-method-conda-install.html#python-installation-method-conda-install)
* [Building from source on Linux](https://catboost.ai/docs/installation/python-installation-method-build-from-source-linux-macos.html)
