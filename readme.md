
# Harmony data integration

This repo contains the code and data models that were used in the Harmony project.
For more information on this project, please see the entry at the [Data Station for Life Sciences](https://lifesciences.datastations.nl/dataset.xhtml?persistentId=doi:10.17026/LS/8HWQUW)

## data-modeling
Data modeling contains the overall Harmony data model, as well as relationships between several raw data files we received from projects.

## data-prep-scripts
Some scripts were used to format the received data from .xlsx files to .csv files, and to ensure a consistent naming strategy. The scripts used can be found in this folder, along with a readme with more details on how these functions work and can be implemented.

## data-transformation
This folder contains the M (PowerQuery) scripts that were used to transform the received data into a format that could be harmonized. For some studies this is quite straightforward, for other studies this was more complicated. When you have opened the PowerQuery editor, navigate to 'Advanced Editor' and paste the scripts here. Every file in the folder should be pasted into a separate query.

## docs
The docs folder contains a broad overview of the architecture that was used in the project. For more documentation, please see our record in the [Data Station for Life Sciences](https://lifesciences.datastations.nl/dataset.xhtml?persistentId=doi:10.17026/LS/8HWQUW).







