# This script must be source`d from others in subdirectories

dir=`dirname $0`
repo=`realpath $dir/../..`
datasets_dir=$repo/datasets
datasets_list="Australian.npy,guillermo.npy,riccardo.npy"
logs=$repo/logs
iters=${1:-1}
miniconda_dir=/home/$USER/huawei/miniconda3
timestamp=`date "+%Y%m%d%H%M%S"`

if [ -f "$miniconda_dir/etc/profile.d/conda.sh" ]; then
    source "$miniconda_dir/etc/profile.d/conda.sh"
else
    export PATH="$miniconda_dir/bin:$PATH"
fi

conda activate rapids-0.18
