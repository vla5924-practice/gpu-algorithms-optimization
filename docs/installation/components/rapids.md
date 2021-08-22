# How to install NVIDIA Rapids

**Prerequisites:**
* Conda


## Install

```sh
conda create -n rapids-0.18 \
    -c rapidsai -c nvidia -c conda-forge -c defaults \
    rapids=0.18 python=3.8 cudatoolkit=11.2
```


## Environment

* To activate environment for Rapids, use this command:
  ```sh
  conda activate rapids-0.18
  ```
* To deactivate environment for Rapids, use this command:
  ```sh
  conda deactivate
  ```


## References

* [Rapids release selector](https://rapids.ai/start.html#rapids-release-selector)
