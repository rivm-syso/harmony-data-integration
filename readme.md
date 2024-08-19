
# Harmony data integration

## Description
This repo contains the code and data models that were used in the Harmony project.
For more information on this project, please see the entry at the [Data Station for Life Sciences](https://doi.org/10.17026/LS/8HWQUW)

## Folders
```data-modeling```: data modeling contains the overall Harmony data model, as well as relationships between several raw data files we received from projects.

```data-prep-scripts```: some scripts were used to format the received data from .xlsx files to .csv files, and to ensure a consistent naming strategy. The scripts used can be found in this folder, along with a readme with more details on how these functions work and can be implemented.

```data-transformation```: this folder contains the M (PowerQuery) scripts that were used to transform the received data into a format that could be harmonized. For some studies this is quite straightforward, for other studies this was more complicated. When you have opened the PowerQuery editor, navigate to 'Advanced Editor' and paste the scripts here. Every file in the folder should be pasted into a separate query.

```docs```: the docs folder contains a broad overview of the architecture that was used in the project. For more documentation, please see our record in the [Data Station for Life Sciences](https://doi.org/10.17026/LS/8HWQUW).

## Data
The raw data used in the M scripts is not publicly available due to GDPR constraints. Access to the resulting datasets can be requested in the [Data Station for Life Sciences](https://doi.org/10.17026/LS/8HWQUW).

## Usage
The raw files first went through the scripts in ```data-prep-scripts``` in order to create standardized .csv files. Subsequently, the data was loaded into Power BI and modified according to the M-scripts in ```data-transformation``` in the respective study folders (i.e. the raw RECOVAC files were processed by the scripts in the RECOVAC folder). Once all study files had been standardized, they were loaded into a Power BI file with the scripts in the ```data-transformation > appending``` folder. 

## Funding
The Harmony project was funded by ZonMW under projectnumber 10430072130001.






