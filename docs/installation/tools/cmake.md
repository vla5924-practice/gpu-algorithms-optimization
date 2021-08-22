# How to install CMake

**First way (easy)** is to download pre-built binaries from [the official website](https://cmake.org/download), unpack the archive, and copy files to `bin` and `share` directories respectively.

**Second way (advanced)** is to build CMake from source code.

1. Clone the repository:
   ```sh
   git clone https://github.com/Kitware/CMake.git cmake
   ```
   or, if you have GitHub CLI, use this command:
   ```sh
   gh repo clone Kitware/CMake cmake
   ```
2. Create a build directory there:
   ```sh
   mkdir cmake/build
   cd cmake/build
   ```
3. Run `bootstrap` script, then `make` and `make install`. You may use the `--prefix=<install_prefix>` script option to specify a custom installation directory for CMake.
   ```sh
    ../bootstrap
    make -j && make install
    ```
4. Check the installation:
    ```sh
    cmake --version
    ```
    > To let this work, please check if `$PATH` contains the directory with built CMake.
