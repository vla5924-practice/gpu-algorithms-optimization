from argparse import ArgumentParser


def build_parser(fit_file=True, fit_size=True, test_file=True, test=True, double=True) -> ArgumentParser:
    parser = ArgumentParser()
    if fit_file:
        parser.add_argument("-ff", "--fit_file", dest="fit_file",
                            help="dataset file for fit", metavar="FILE")
    if fit_size:
        parser.add_argument("-s", "--fit_size", type=float, default=1,
                            help="portion of dataset to split and fit on (between 0 and 1)", metavar="FLOAT")
    if test_file:
        parser.add_argument("-tf", "--test_file", dest="test_file",
                            help="dataset file for test", metavar="FILE")
    if test:
        parser.add_argument("--test", action="store_true")
    if double:
        parser.add_argument("--double", action="store_true")
    return parser
