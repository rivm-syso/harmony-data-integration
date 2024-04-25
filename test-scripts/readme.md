
## [fn2_convert_newfiles.py](fn2_convert.py)

2x Main-Functions in this Python script:

### 1.
### `check_file_formats()`

#### Purpose: 

> Checks input file formats (.txt, .csv, .xlsx, other).

#### Description:

> Loops through files in a directory. Based on file extensions, calls corresponding Sub-functions to
    handle conversion or cleaning

#### Sub-functions:

- **`text_to_csv(filename)`**
*Based on different separator scenarios (e.g., ';' or '\t'), converts TXT to CSV format.*

- **`clean_csv_inconsistencies(filename)`**
*Cleans row-level inconsistencies (line by line) in CSV files by removing unwanted characters or spaces.*

- **`excel_to_csv(filename)`**
*Converts data from the first sheet of XLSX files to CSV format.*

### 2.
### `csv_formatting()`

#### Purpose: 

> Corrects and formats CSV files.

#### Description:

> Iterates through CSV files in a temporary directory. Detects encoding (e.g., ascii, utf-8, etc.) and reads CSV into
    pandas dataframe accordingly. Performs sub-tasks like checking & adjusting decimal separators
    (e.g., replace ‘,’ with ‘.’). Saves modified CSV files in unified format to output directory.

<br/>

---

<br/>

a relative path link:
[study-prefixes](fn-inputs/study-prefixes.ps1)

&emsp; text
<br/>
text
<br/>
text
