#!/bin/bash

################################################################################
### Arguments:                                         ######################### 
###   $1 - provider name (rapids, scikit, spark, misc) ######################### 
###   $2 - algorithm name (e.g. logistic_regression)   #########################
################################################################################

set -e

scripts_dir=$(realpath $(dirname $0)/../scripts)
provider=$1
target_dir="${scripts_dir}/${provider}"
algorithm=$2

mkdir -p "${scripts_dir}/${provider}"

echo "#!/bin/sh

#SBATCH --time=4320

set -e

. \$(dirname \$0)/../common.sh

python3 \$repo/run_benchmark.py \
    -m bench.${provider}.${algorithm} \
    -r \$repo \
    -d \$datasets_dir \
    -l \$datasets_list \
    -i \$iters \
    -rf \$logs/${provider}-${algorithm}-\$timestamp-full.csv \
    -ra \$logs/${provider}-${algorithm}-\$timestamp-avg.avg \
    -- -tf %D --double > \$logs/${provider}-${algorithm}-\$timestamp.log
" > ${target_dir}/${algorithm}.sh

chmod +x ${target_dir}/${algorithm}.sh
