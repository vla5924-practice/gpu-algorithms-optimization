# How to build GCC

1. Clone the source repository:
   ```sh
   git clone git://gcc.gnu.org/git/gcc.git
   ```
2. Create folder for installation:
   ```sh
   mkdir gcc-build # choose the path you prefer
   ```
3. Select the preferred branch (if needed):
   ```sh
   cd gcc
   git checkout releases/gcc-9
   ```
4. Run `configure` script and then compile:
   ```sh
   ./configure --disable-multilib --prefix=$PWD/../gcc-build
   make -j
   make install
   ```
5. Check the installation:
   ```sh
   gcc --version
   c++ --version
   ```

> Don't forget to set environment variables:
> ```sh
> export PATH=/path/to/gcc-build/bin:$PATH
> export LD_LIBRARY_PATH=/path/to/gcc-build/lib64:$LD_LIBRARY_PATH
> export CC=/path/to/gcc-build/bin/gcc # optional
> export CXX=/path/to/gcc-build/bin/c++ # optional
> ```
