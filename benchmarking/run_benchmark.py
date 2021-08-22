import os
import re
import subprocess
from statistics import mean
from argparse import ArgumentParser


def append_to_log(filename: str, log: str) -> None:
    with open(filename, "a") as file:
        file.write(log + "\n")


current_dir = os.path.dirname(os.path.abspath(__file__))

parser = ArgumentParser()
parser.add_argument("-m", "--module",
                    help="bench module name (for example, bench.rapids.kmeans)", metavar="MODULE")
parser.add_argument("-r", "--root-dir", default=current_dir, dest="root_dir",
                    help="path to ml-benchmark repository root (current directory by default)", metavar="DIRECTORY")
parser.add_argument("-d", "--datasets-dir", default=os.path.join(current_dir, "datasets"), dest="datasets_dir",
                    help="path to directory with datasets (default is ./datasets)", metavar="DIRECTORY")
parser.add_argument("-f", "--datasets-format", default="npy", dest="datasets_format",
                    help="file formats of datasets (npy, arff, svm)", metavar="FORMAT")
parser.add_argument("-l", "--log-file", default=os.path.join(current_dir, "logs", "bench.log"), dest="log_file",
                    help="destination log file path (default is ./logs/bench.log)", metavar="FILE")
parser.add_argument("-e", "--executable", default="python3",
                    help="name of python executable (default is python3)", metavar="EXECUTABLE")
parser.add_argument("-i", "--iters", default=1, type=int,
                    help="number of iterations for bench execution (default is 1)", metavar="NUMBER")
parser.add_argument("extra", nargs="*",
                    help="additional arguments for bench script", metavar="ARGS")
args = parser.parse_args()

# datasets = ("christine", "higgs", "sylvine", "albert", "australian", "guillermo",
#             "jasmine", "riccardo", "dionis", "robert", "dilbert")
datasets = ("australian", "sylvine")

os.chdir(args.root_dir)

# Clear log file contents, if any
with open(args.log_file, "w"):
    pass

solved = 0
for dataset in datasets:
    dataset_name = "{}.{}".format(dataset, args.datasets_format)
    dataset_path = os.path.join(args.datasets_dir, dataset_name)
    extra_args = " ".join(
        '"' + arg.replace("%D", dataset_path) + '"' for arg in args.extra)
    cmd = "{} -m {} -ff {} {}".format(args.executable, args.module,
                                      dataset_path, extra_args)
    times = []
    print("[ RUN  ]", cmd)
    for iter in range(args.iters):
        if args.iters > 1:
            print("[ ==== ] Iteration: {}/{}".format(iter + 1, args.iters))
        res = subprocess.run(cmd, shell=True, capture_output=True)
        out = str(res.stdout).replace("\\n", "|").replace("'", "")
        if res.stdout is None:
            print("[ FAIL ] No output, return code", res.returncode)
            append_to_log(args.log_file, ">>> {} {} no_output".format(
                dataset, res.returncode))
        time = 0.0
        match = re.search(r'Fit time:[ ]*(\d+\.\d+)', out)
        if match is not None:
            time = match[1]
            times.append(float(time))
            solved += 1
        match = re.search(r'Fit samples:[ ]*\((\d+),[ ]*(\d+)\)', out)
        dim = "{} {}".format(match[1], match[2]) if match is not None else ""
        match = re.search(r'Accuracy score:[ ]*(\d+\.\d+)', out)
        accuracy = match[1] if match is not None else 0.0
        match = re.findall(r'(\[[WE]\].+?[\|\n])', out)
        we = "|".join(match) if match is not None else ""
        if we:
            print("\n".join(match))
        if res.returncode == 0:
            print("[  OK  ] Success, return code 0")
        else:
            print("[ FAIL ] Error, return code", res.returncode)
        append_to_log(args.log_file, ">>> {} {} {} {} {} {}".format(
            dataset, res.returncode, dim, time, accuracy, we))
    if args.iters > 1 and len(times) > 0:
        append_to_log(args.log_file, ">>> {} avg_time {}".format(
            dataset, mean(times)))

append_to_log(args.log_file, ">>> Solved {} of {}".format(
    solved, len(datasets) * args.iters))
print("[ ==== ] Log written to", args.log_file)
