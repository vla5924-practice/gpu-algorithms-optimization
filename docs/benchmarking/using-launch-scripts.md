# Using launch scripts

To automatize the execution of multiple benchmarks (for example, via `sbatch`), you can use Bash scripts which will setup environment, launch measurements, and save output to file.

In order not to write each script manually, we have `generate_launch_script.sh` tool. Usage:
```sh
./tools/generate_launch_script.sh ${provider} ${algorithm}
```

It will create the `${algorithm}.sh` executable script in `scripts/${provider}` directory. Then you only need to adjust default parameters in `scripts/common.sh` file and run that generated script:
```sh
./scripts/${provider}/${algorithm}.sh ${iterations_count}
```


## Example

Imagine you want to generate launch script for benchmark of KMeans implementation by Rapids.

1. Generate the script:
   ```sh
   ./tools/generate_launch_script.sh rapids kmeans
   ```
2. Adjust the defaults in `scripts/common.sh` file.
3. Run benchmark for 10 iterations and get logs:
   ```sh
    ./scripts/rapids/kmeans.sh 10
    ```
