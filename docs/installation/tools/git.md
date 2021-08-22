# How to build Git

1. Download a source tarball with preferred Git version from [this page](https://www.kernel.org/pub/software/scm/git). For example:
   ```sh
   wget https://mirrors.edge.kernel.org/pub/software/scm/git/git-2.33.0.tar.gz
   ```
2. Unpack the archive:
   ```sh
   tar xvf git-2.33.0.tar.gz
   ```
3. Run just `make` and then `make install` inside:
   ```sh
   make -j
   make install
   ```
4. Check the installation:
   ```sh
   git --version
   ```
