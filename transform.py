"""Data transformation.

Read raw input data from stdin, validate against basic schema, possibly
enrich with static values, output as CSV to stdout.

SCHEMA constant defines known input schemas for Harmony data. Required 
columns are named with a data type. Columns in input that are not 
mentioned in SCHEMA are ignored.
"""

import argparse
import pandas
import sys


def IIVAC_combine_medication(df):
    cols = ['medinfectie', 'medafweerrem', 'medcortico', 'medallergie', 
            'medmaagzuur', 'medcholestorol', 'medchemo', 'medinsuline', 
            'medhormoon', 'medbloeddruk', 'medbloedprod', 'medbloedstol', 
            'medceltherapie']
    # Replace 1s in these cols with their column names and 0s with empty str.
    df.loc[:, cols] = df.loc[:, cols].mul(cols)

    def nonempty(seq):
        # Join elements into string when elements are non-empty.
        return [e for e in seq if e]

    # Combine medication use fields into 1 string
    df['medication_use'] = df[cols].agg(nonempty, axis=1)

    # Remove original medication use fields
    df.drop(cols, axis=1, inplace=True)



# List transformations (functions that are to be applied to dataframe)
TRANSFORMATIONS = {
    'IIVAC_vragenlijst_18': (
        IIVAC_combine_medication,
    )
}


def main(args):
    df = pandas.read_csv(sys.stdin, header=0, skipinitialspace=True)
    for transformation in TRANSFORMATIONS[args.TRANSFORMATION]:
        transformation(df)
    df.to_csv(sys.stdout, index=False)


if __name__ == "__main__":
    # Invoked as script: parse arguments.

    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('TRANSFORMATION', type=str, choices=list(TRANSFORMATIONS.keys()))
    args = parser.parse_args()
    main(args)




