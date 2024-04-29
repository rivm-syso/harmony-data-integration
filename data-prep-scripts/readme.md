# Data-preparation Scripts 
**Incl. their (sub-)functions for ETL pipeline**

## Intro

After receiving the first dataset (via DRE upload), co-developed a few 
smaller scripts (in PowerShell & Python) to check source data quality 
and test essential preparatory steps needed before the data enters an 
automated ETL pipeline (Extract>Transform>Load). This involves:

-   File management of raw data (e.g., backups, unzipping, structuring &
    naming conventions)

-   Data formatting and pre-cleaning (e.g., encoding, correct
    inconsistency, format conversion)

## Current status

> Unfortunately, the vast amount of inconsistencies between source files
> and often poor data quality did not qualify for an automated scripting
> pipeline based on code. Hence, we decided to utilize Power BI Power
> Query to perform the remaining ETL procedures.

**Storage location in DRE/VM – Latest script versions:**

-   `Z:\DataETL\FileCont1-mpd\test\(scripts)\..` \> Data-prep scripts

-   `Z:\QuickHMNY\data_out\metadata\..` \> Metadata script

## Overview of scripts (in ordered sequence)

Put together, they would constitute the first part of the pipeline – from file
uploads to uniform CSV converted (except metadata, which is for final
dataset after ETL via Power BI):

| Script-name          | Type \| Lines of code        |
|----------------------|------------------------------|
| inbox-backup         | .ps1 \| 95                   |
| fn1_unzip            | .ps1 \| 19                   |
| fn2_convert_NewFiles | .py \| 139                   |
| fn3_prefix           | .ps1 \| 155                  |
| study-prefixes       | .ps1 (schema)                |
| headername-patterns  | .ps1 (schema)                |
| extract_metadata_v2  | .py \| 165                   |
|                      |              **= 573 lines** |

<br/>

**Following sections explain the Scripts:**

---

<br/>

## [inbox-backup.ps1](inbox-backup.ps1)

This PowerShell script first sets up file system watchers for monitoring
changes in two folders to be backed up regularly (Z:\inbox\\ and
Z:\QuickHMNY\data_in). One contains uploaded raw files, the other the
converted & mapped files. Then the script calls 2x BackupFunctions:

### 1.

### `inboxSourceFolder`

#### Description:

1.  Defines a function `Copy-ItemIfNew` to copy items if they are new.

2.  Registers an event for newly created files in the inbox source
    folder.

3.  Copies existing items to the backup folder if they haven't been
    copied yet.

### 2.

### `MappedFiles`

#### Description: 

> Same function, but for the mapped files folder.

<br/>

## [fn1_unzip.ps1](fn1_unzip.ps1)

This PowerShell script has 2x short Functions:

### 1.

### `Expand-Archive`

#### Description:

> Searches for ZIP files in a folder ($inFolder) and its subdirectories.
> For each ZIP file found, extracts its content (list of files).

### 2.

### `Copy-Item`

#### Description: 

> Retrieves files with extensions .csv, .xlsx, .tsv, and .txt from the
> extracted folder content and copies files to a destination folder
> ($outFolder).

<br/>

## [fn2_convert_NewFiles.py](fn2_convert_NewFiles.py)

This Python script has 2x Main-Functions:

### 1.

### `check_file_formats()`

#### Purpose: 

> Checks input file formats (.txt, .csv, .xlsx, other).

#### Description:

> Loops through files in a directory. Based on file extensions, calls
> corresponding Sub-functions to handle conversion or cleaning

#### Sub-functions:

-   **`text_to_csv(filename)`**

&emsp;&emsp; *Based on different separator scenarios (e.g., ';' or '\t'), converts
TXT to CSV format.*

-   **`clean_csv_inconsistencies(filename)`**

&emsp;&emsp; *Cleans row-level inconsistencies (line by line) in CSV files by
removing unwanted characters or spaces.*

-   **`excel_to_csv(filename)`**

&emsp;&emsp; *Converts data from the first sheet of XLSX files to CSV format.*

### 2.

### `csv_formatting()`

#### Purpose: 

> Corrects and formats CSV files.

#### Description:

> Iterates through CSV files in a temporary directory. Detects encoding
> (e.g., ascii, utf-8, etc.) and reads CSV into pandas dataframe
> accordingly. Performs sub-tasks like checking & adjusting decimal
> separators (e.g., replace ‘,’ with ‘.’). Saves modified CSV files in
> unified format to output directory.

<br/>

## [fn3_prefix.ps1](fn3_prefix.ps1)

This PowerShell script first contains 2x GUIs (Windows Forms) for user
input and then 2x Main-Function blocks for file processing:

### 1.

### `InputForm - StudyPrefixes`

#### Purpose: 

> Input form for selecting study prefixes.

#### Description:

1.  Loads a list of study prefixes from a sub-function named
    `‘study-prefixes.ps1’` (here used as Schema).

2.  Creates a GUI with a ComboBox to display the list of prefixes for
    selection.

3.  Includes a "Confirm" button to close the form and return the
    selected prefix.

4.  If the form is closed without confirmation, the script exits.

### 2.

### `InputForm - SelectFiles`

#### Purpose: 

> Input form for selecting files using OpenFileDialog.

#### Description:

1.  Creates an OpenFileDialog to allow users to select multiple files.

2.  If files are selected, captures the filenames into the
    $selectedFiles variable.

3.  Exits the script if the OpenFileDialog is canceled.

### 3.

### `MainFunction - Prefix & StudySubfolders`

#### Description:

1.  Retrieves the selected study prefix from the ComboBox.

2.  Constructs the path for the study subfolder using the selected
    prefix.

3.  Checks if the subfolder already exists; if not, creates it.

### 4.

### `MainFunction – Rename based on HeaderName pattern`

#### Description:

1.  Loads an array of header names from a sub-function named
    `headername-patterns.ps1` (here used as Schema).

2.  Scans the first two rows of selected files to identify header name
    patterns.

3.  Matches header names to predefined regular expressions (e.g.,
    $regexImmun) to categorize files.

4.  Renames and copies files to a new subdirectory based on their
    category and prefix.

<br/>

## [study-prefixes.ps1 (schema)](fn-inputs/study-prefixes.ps1)

### `$prefixList (variable)`

#### Purpose:

> Used as a Schema/Template in `fn3_prefix.ps1`. Defines a list of
> study prefixes (for customization based on future project
> requirements).

<br/>

## [headername-patterns.ps1 (schema)](fn-inputs/headername-patterns.ps1)

### `$regex… (variable)`

#### Purpose:

> Used as a Schema/Template in `fn3_prefix.ps1`. Defines regular
> expression patterns for header string matching (for customization
> based on future project requirements).

#### Description:

-   Defines arrays of header strings to be checked for specific data
    categories (e.g., immunological variables, demographic info, date
    columns).

-   Constructs regular expression patterns from these arrays to match
    corresponding header strings in the files.

<br/>

## [extract_Metadata_v2.py](extract_Metadata_v2.py)

This Python script first requires custom user-inputs (file paths and
filenames) and then calls following 2x Main-Functions:

### 1.

### `extract_metadata(csv_file)`

#### Purpose: 

> Extracts metadata from a CSV file, including file-level and
> column-level information. Calculates basic summary statistics for
> numeric columns (e.g., min, max, and avg. values). Constructs a
> metadata dictionary for the CSV file, ready to be saved as a JSON
> file.

#### Sub-functions:

-   **`counts_per_column(column_data, row_count)`**

&emsp;&emsp; *Counts null values, actual values, distinct values, and unique values
per column in a DataFrame and returns the counts to the main function as
a tuple.*

-   **`get_data_type(py_dtype, column_data)`**

&emsp;&emsp; *Maps python data types to labels, with extra checks for
string and integer types to determine the data type of a column in a
DataFrame.*

-	**{ `is_date_string(s)` }**

&emsp;&emsp; *Currently not in use ! Still needs correct integration ! (For now, only to test 'date_pattern' recognition True/False)*

### 2.

### `save_json_file(json_output, metadata)`

#### Purpose: 

> This function saves the provided metadata dictionary as a JSON file
> with specified output path and indentation.

<br/>
