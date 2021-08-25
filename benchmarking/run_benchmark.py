import csv
import os
import re
import subprocess

from argparse import ArgumentParser
from statistics import mean


class MiniLogger:
    def info(self, message=""):
        print("[ INFO ]", message)

    def run(self, message=""):
        print("[ RUN  ]", message)

    def ok(self, message=""):
        print("[  OK  ]", message)

    def fail(self, message=""):
        print("[ FAIL ]", message)


current_dir = os.path.dirname(os.path.abspath(__file__))

parser = ArgumentParser()
parser.add_argument("-m", "--module",
                    help="bench module name (for example, bench.rapids.kmeans)", metavar="MODULE")
parser.add_argument("-r", "--root-dir", default=current_dir, dest="root_dir",
                    help="path to repository root (current directory by default)", metavar="DIRECTORY")
parser.add_argument("-d", "--datasets-dir", default=os.path.join(current_dir, "datasets"), dest="datasets_dir",
                    help="path to directory with datasets (default is ./datasets)", metavar="DIRECTORY")
parser.add_argument("-l", "--datasets-list", default="", dest="datasets_list",
                    help="comma-separated list of datasets filenames", metavar="DATASET1.NPY,DATASET2.NPY,...")
parser.add_argument("-rf", "--report-full", default=os.path.join(current_dir, "logs", "bench_full.csv"), dest="report_full",
                    help="full csv report file path (default is ./logs/bench_full.csv)", metavar="FILE")
parser.add_argument("-ra", "--report-avg", default=os.path.join(current_dir, "logs", "bench_avg.csv"), dest="report_avg",
                    help="average csv report file path (default is ./logs/bench_avg.csv)", metavar="FILE")
parser.add_argument("-e", "--executable", default="python3",
                    help="name of python executable (default is python3)", metavar="EXECUTABLE")
parser.add_argument("-i", "--iters", default=1, type=int,
                    help="number of iterations for bench execution (default is 1)", metavar="NUMBER")
parser.add_argument("extra", nargs="*",
                    help="additional arguments for bench script", metavar="ARGS")
args = parser.parse_args()

datasets = args.datasets_list.split(",") if len(
    args.datasets_list) > 0 else ["Australian.npy"]

os.chdir(args.root_dir)

report_full_file = open(args.report_full, "w")
report_full_writer = csv.writer(report_full_file, delimiter=",")
report_full_writer.writerow(["Dataset", "Iteration", "Return code",
                            "Samples dimensions", "Elapsed time", "Accuracy score"])

report_avg_file = open(args.report_avg, "w")
report_avg_writer = csv.writer(report_avg_file, delimiter=",")
report_avg_writer.writerow(["Dataset", "Iterations count",
                           "Samples dimensions", "Elapsed time", "Accuracy score"])

logger = MiniLogger()
solved = 0
for dataset in datasets:
    dataset_path = os.path.join(args.datasets_dir, dataset)
    extra_args = " ".join(
        '"' + arg.replace("%D", dataset_path) + '"' for arg in args.extra)
    cmd = f"{args.executable} -m {args.module} -ff {dataset_path} {extra_args}"
    times = []
    accuracies = []
    logger.run(cmd)
    for iter in range(args.iters):
        if args.iters > 1:
            logger.info("Iteration: {}/{}".format(iter + 1, args.iters))
        res = subprocess.run(cmd, shell=True, capture_output=True)
        out = str(res.stdout).replace("\\n", "\n").replace("'", "")
        if res.stdout is None:
            logger.fail("No output, return code", res.returncode)
        match = re.search(r'Fit time:[ ]*(\d+\.\d+)', out)
        time = float(match[1]) if match is not None else 0.0
        times.append(time)
        match = re.search(r'Fit samples:[ ]*\((\d+),[ ]*(\d+)\)', out)
        dim = "{} {}".format(match[1], match[2]) if match is not None else ""
        match = re.search(r'Accuracy score:[ ]*(\d+\.\d+)', out)
        accuracy = float(match[1]) if match is not None else 0.0
        accuracies.append(accuracy)
        match = re.findall(r'(\[[WE]\].+?[\|\n])', out)
        if match is not None:
            print("\n".join(match))
        if res.returncode == 0:
            solved += 1
            logger.ok("Success, return code 0")
        else:
            print(out)
            logger.fail("Error, return code", res.returncode)
        report_full_writer.writerow(
            [dataset, iter, res.returncode, dim, time, accuracy])
    report_avg_writer.writerow(
        [dataset, args.iters, dim, mean(times), mean(accuracies)])

report_avg_file.close()
report_full_file.close()

logger.info("Executed {} of {}".format(solved, len(datasets) * args.iters))
logger.info("Report written to", args.output)
