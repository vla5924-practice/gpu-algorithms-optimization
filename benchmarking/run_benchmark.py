import csv
import os
import re
import subprocess
import yaml

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


class ReportMetric:
    def __init__(self, name: str, code: str):
        self.name = name
        self.code = code
        self._code = "{" + code + "}:"
        self.regex = re.compile(r"\{" + code + r"\}\:[ ]*(\d+\.?\d*)")

    def in_str(self, haystack: str) -> bool:
        return self._code in haystack

    def get_float(self, haystack: str) -> float:
        match = self.regex.search(haystack)
        return float(match[1]) if match is not None else 0.0


parser = ArgumentParser()
parser.add_argument("-c", "--config",
                    help="configuration file", metavar="FILE")
args = parser.parse_args()

with open(args.config, "r") as f:
    try:
        config = yaml.safe_load(f)
    except:
        print("Error while reading configuration file.")
        exit(127)

datasets = config["datasets"]["files"]

metrics = []
for metric_data in config["reporting"]["metrics"]:
    metric = ReportMetric(metric_data["name"], metric_data["code"])
    metrics.append(metric)

report_full_file = open(config["reporting"]["full"].replace("%T", "0"), "w")
report_full_writer = csv.writer(report_full_file, delimiter=",")
row = ["Dataset", "Repetition", "Return code"]
for metric in metrics:
    row.append(metric.name)
report_full_writer.writerow(row)

report_avg_file = open(config["reporting"]["average"].replace("%T", "0"), "w")
report_avg_writer = csv.writer(report_avg_file, delimiter=",")
row = ["Dataset", "Repetitions"]
for metric in metrics:
    row.append(metric.name)
report_avg_writer.writerow(row)


logger = MiniLogger()
solved = 0
iters = int(config["execution"]["repeat"])
module_name = "bench.{}.{}".format(config["benchmark"]["provider"], config["benchmark"]["algorithm"])
for dataset in datasets:
    dataset_path = os.path.join(config["datasets"]["directory"], dataset)
    cmd = config["execution"]["command"].replace("%M", module_name).replace("%D", dataset_path)
    metric_values = {}
    for metric in metrics:
        metric_values[metric.code] = []
    logger.run(cmd)
    for iter in range(iters):
        if iters > 1:
            logger.info("Repetition: {}/{}".format(iter + 1, iters))
        res = subprocess.run(cmd, shell=True, capture_output=True)
        out = res.stdout.decode("utf-8")
        if res.stdout is None:
            logger.fail("No output, return code {}".format(res.returncode))
        for metric in metrics:
            metric_values[metric.code].append(metric.get_float(out))
        match = re.findall(r'(\[[WE]\].+?[\|\n])', out)
        if match is not None and len(match) > 0:
            print("\n".join(match))
        if res.returncode == 0:
            solved += 1
            logger.ok("Success, return code 0")
        else:
            print(out)
            print(res.stderr.decode("utf-8"))
            logger.fail("Error, return code {}".format(res.returncode))
        row = [dataset, iter, res.returncode]
        for metric in metrics:
            row.append(metric_values[metric.code][-1])
        report_full_writer.writerow(row)
    row = [dataset, iters]
    for metric in metrics:
            row.append(mean(metric_values[metric.code]))
    report_avg_writer.writerow(row)

report_avg_file.close()
report_full_file.close()

logger.info("Executed {} of {}".format(solved, len(datasets) * iters))
logger.info("Full report written to {}".format(""))
logger.info("Average report written to {}".format(""))
