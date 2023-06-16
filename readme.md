
# Harmony data integration

This repo contains some example code on how to integrate Harmony data.
Currently, this is created without seeing the actual data. 

## ETL code

All ETL scripts read from stdin and write to stdout. To build the 
complete integrated dataset, some orchestration is needed.

`extract.py` reads and writes CSV and lets one select relevant columns,
as they are defined in a `SCHEMA` constant inside. The CLI flag `--var`
lets you enrich the data with a static value (e.g. to define the source 
of these records as another column).

`transform.py` applies transformations to the input and outputs another
CSV. Transformations are just functions applied to a Pandas dataframe.

`load.py` simply converts CSV to JSON.

To get started:

* Install dependencies, e.g.  `pip install -r requirements.txt`;
* Apply scripts to input, e.g.:

```bash
cat test/resources/IIVAC_Vragenlijst_B0_18_jaar_items.csv | \
    python extract.py IIVAC_vragenlijst_18 --var t 1 | \
    python transform.py IIVAC_vragenlijst_18
```


## Documentation

Desin overview for the Harmony DRE and data flow is defined in 
`docs/harmony_arch.md`. The diagram requires plantuml to generate.

E.g. to get started:

* Install [pandoc](https://pandoc.org/);
* install [pandoc-plantuml-filter](https://pypi.org/project/pandoc-plantuml-filter/);
* run: `pandoc --filter pandoc-plantuml harmony_arch.md > harmony_arch.html`.




