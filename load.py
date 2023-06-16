"""Data loading.

Output JSON records for all Harmony data combined.
"""

import argparse
import pandas
import sys


def main(args):
    df = pandas.read_csv(sys.stdin, header=0, skipinitialspace=True)
    df.to_json(sys.stdout, orient='index', indent=2)


if __name__ == "__main__":
    # Invoked as script: parse arguments.

    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    args = parser.parse_args()
    main(args)
