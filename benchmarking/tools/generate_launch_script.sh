#!/bin/bash

set -e

scripts_dir=$(realpath $(dirname $0)/../scripts)
provider=$1
target_dir="${scripts_dir}/${provider}"
algorithm=$2
format=${3:-npy}

mkdir -p "${scripts_dir}/${provider}"

echo "#!/bin/sh

#SBATCH --time=4320

set -e

. \$(dirname \$0)/../common.sh

python3 \$repo/run_benchmark.py \
    -m bench.${provider}.${algorithm} \
    -r \$repo \
    -d \$datasets \
    -f ${format} \
    -i \$iters \
    -l \$logs/${provider}-${algorithm}-\$timestamp.log \
    -- -tf %D --double
" > ${target_dir}/${algorithm}.sh
