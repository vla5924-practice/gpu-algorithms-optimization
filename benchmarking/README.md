# ML Benchmark

Benchmark scripts for different ML algorithms (Rapids, Scikit, Spark).

## Usage

```
python3 run_benchmark.py [-h] [-m MODULE] [-r DIRECTORY] [-d DIRECTORY] [-f FORMAT] [-l FILE] [-e EXECUTABLE] [--double]

optional arguments:
  -h, --help            show this help message and exit
  -m MODULE, --module MODULE
                        Bench module name
  -r DIRECTORY, --root-dir DIRECTORY
                        Path to ml-benchmark repository root
  -d DIRECTORY, --datasets-dir DIRECTORY
                        Path to directory with datasets
  -f FORMAT, --datasets-format FORMAT
                        File formats of datasets (arff, svm)
  -l FILE, --log-file FILE
                        Destination log file path
  -e EXECUTABLE, --executable EXECUTABLE
                        Name of Python executable (python3 by default)
  --double
```

## Automation

Convenient shell scripts for launching in conda environment can be found in `scripts` folder.
