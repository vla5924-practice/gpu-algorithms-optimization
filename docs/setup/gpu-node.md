# How to login and setup GPU node on cluster

1. Acquire an available node:
   ```sh
   salloc -N 1 -n 1 -p a100 --gres=gpu:1 -t 120
   ```
   `120` is time in seconds.
2. Check for allocated node:
   ```sh
   echo $SLURM_NODELIST
   ```
3. Log into this node:
   ```sh
   ssh -X $SLURM_NODELIST
   ```

Optionally you can check and load some modules:

```sh
module avail
module load cuda/cuda-11.2
```
