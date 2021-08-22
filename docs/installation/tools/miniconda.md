# How to install and setup Miniconda

1. Download installation script:
   ```sh
   wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh ~/install_latest_miniconda3.sh
   ```
2. Launch the script:
   ```sh
   bash ~/install_latest_miniconda3.sh
   ```
3. Initialize the environment in auto mode:
   ```sh
   ~/miniconda3/bin/conda init
   ```
4. Re-login to host.

The last command will change `.bashrc` file and some other files to automatically enable Conda environment.
