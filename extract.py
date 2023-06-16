"""Data preparation.

Read raw input data from stdin, validate against basic schema, possibly
enrich with static values, output as CSV to stdout.

SCHEMA constant defines known input schemas for Harmony data. Required 
columns are named with a data type. Columns in input that are not 
mentioned in SCHEMA are ignored.
"""

import argparse
import pandas
import sys


# Define sources
SCHEMA = {
    'IIVAC_vragenlijst_18': { # e.g. 'IIVAC_Vragenlijst_B0_18_jaar_items.csv'
        'source': 'IIVAC',
        'fields': { # Define data type 
            'ziekmedic': int,
            'medinfectie': int,
            'medafweerrem': int,
            'medcortico': int,
            'medallergie': int,
            'medmaagzuur': int,
            'medcholestorol': int,
            'medchemo': int,
            'medinsuline': int,
            'medhormoon': int,
            'medbloeddruk': int,
            'medbloedprod': int,
            'medbloedstol': int,
            'medceltherapie': int
        }
    }
}


def main(args):
    df = pandas.read_csv(sys.stdin, header=0, skipinitialspace=True, 
                         usecols=SCHEMA[args.SCHEMA]['fields'].keys())
    if args.var is not None:
        for name, val in args.var:
            df[name] = val
    df.to_csv(sys.stdout, index=False)


if __name__ == "__main__":
    # Invoked as script: parse arguments.

    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('SCHEMA', type=str, choices=list(SCHEMA.keys()))
    parser.add_argument('--var', nargs=2, action='append', 
                        metavar=('name', 'value'), 
                        help='Fixed value added to every row in output')
    args = parser.parse_args()
    main(args)




