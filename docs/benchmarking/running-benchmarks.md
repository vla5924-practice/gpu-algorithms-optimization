# Running benchmarks manual

You can run benchmarks inside `benchmarking` folder manually or automatically for many datasets and iterations with one command.


## One-by-one execution (manual)

1. Go to `benchmarking` directory.
2. Run Python script as a module with specified parameters:
   ```sh
   python3 -m bench.${provider}.${algorithm} -ff ${dataset_fit} [-tf ${dataset_test} --test] [--double]
   ```
   For example, to run benchmark for KMeans implementation by Rapids, you may use this command:
   ```sh
   python3 -m bench.rapids.kmeans -ff $HOME/datasets/classif_fit.npy -tf $HOME/datasets/classif_test.npy --test
   ```
3. Look for output manually or parse application output programmatically.


## Mass launch (automated)

1. Go to `benchmarking` directory.
2. Run `run_benchmark.py` script with specified parameters. This application will iterate over given datasets, launch the specified benchmark, and generate CSV reports.
   > Use `python3 run_benchmark.py -h` to check for available command line parameters.
