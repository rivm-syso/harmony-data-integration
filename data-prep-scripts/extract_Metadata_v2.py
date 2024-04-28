import os
import pandas as pd
import numpy as np
import json
import re

#========================================
#========= 1. Customize Inputs =========
#======================================

data_path = 'C:\\Users\\r.unteregger\\Documents\\QuickHMNY\\data_out'
enter_filename = 'BindingAbs_20240415.csv' 
                #'Demographics_20240415.csv'
                #'Vaccinations_20240415.csv'
                #'Infections_20240415.csv'

metadata_path = 'C:\\Users\\r.unteregger\\Documents\\QuickHMNY\\data_out\\metadata'
json_output = 'StructuralMetadata_v2.json'

#===================================
#========= Main-Functions =========
#=================================

def extract_metadata(csv_file):
    # Read CSV into pandas DataFrame
    df = pd.read_csv(csv_file, low_memory=False)

    #============================
    #=== FILE LEVEL METADATA ===
    # Count rows & colums
    row_count = len(df)
    column_count = len(df.columns)
    # Get file extension
    file_ext = os.path.splitext(csv_file)[1]
    
    #=========================
    #=== LOOP ALL COLUMNS ===
    # Array for metadata, iterating through each column in DataFrame
    columns_metadata = []
    for column in df.columns:
        column_data = df[column]
        # Call Sub-Function
        n, t, u, d = counts_per_column(column_data, row_count)
        # Determine data type of column
        py_dtype = pd.api.types.infer_dtype(column_data)
        # Call Sub-Function
        d_type = get_data_type(py_dtype, column_data)

        #==============================
        #=== COLUMN LEVEL METADATA ===
        column_metadata = {
            'headername': column,
            'python_dtype': py_dtype, ## can be remove later, just for checking
            'data_type': d_type,
            'true_values': t, # count_true_values,
            'null_values': n, # count_null_values,
            'distinct_values': d, # count_distinct_values,
            'unique_values': u, # count_unique_values
        }
        # Calculate summary statistics for numeric columns
        if d_type == 'decimal':
            column_metadata['min'] = round(column_data.min(), 2)
            column_metadata['max'] = round(column_data.max(), 2)
            column_metadata['avg'] = round(column_data.mean(), 2)
        elif d_type == 'integer':
            column_metadata['min'] = round(column_data.min(), 0)
            column_metadata['max'] = round(column_data.max(), 0)
            column_metadata['avg'] = round(column_data.mean(), 0)
        
        columns_metadata.append(column_metadata) # appended column metadata

    #=============================
    #=== TABLE METADATA LEVEL ===
    table_metadata = {
        'table': {
            'file_extension': file_ext,
            'row_count': row_count,
            'column_count': column_count,
            'columns': columns_metadata # appended column metadata
        }
    }

    # Get filename without extension
    file_name = os.path.splitext(os.path.basename(csv_file))[0]
    
    # Construct metadata dictionary using filename as key
    metadata = {file_name: table_metadata}
    # Get metadata to save as JSON file in main()
    return metadata

def save_json_file(json_output, metadata):
    os.chdir(metadata_path)
    # Save metadata as JSON
    with open(json_output, 'w') as json_file:
        json.dump(metadata, json_file, indent=4)

#==================================
#========= Sub-Functions =========
#================================

def counts_per_column(column_data, row_count):
    # Count null values per column
    count_null_values = column_data.isnull().sum()
    # Count actual values per column
    count_true_values = row_count - count_null_values
    # Count distinct occurences of values per column (= distinct variants)
    count_distinct_values = column_data.nunique()
    # Count unique values per column (= occur only once)
    count_unique_values = (column_data.value_counts() == 1).sum()
    # Convert int64 values to regular Python integers
    count_null_values = convert_to_py_int(count_null_values)
    count_true_values = convert_to_py_int(count_true_values)
    count_distinct_values = convert_to_py_int(count_distinct_values)
    count_unique_values = convert_to_py_int(count_unique_values)
    # for returning  multiple vars, we assign 'n, t, u, d' when calling this Sub
    return count_null_values, count_true_values, count_unique_values, count_distinct_values
    #( n = count_null_values, t = count_true_values, u = count_unique_values, d = count_distinct_values )

def get_data_type(py_dtype, column_data): 
    # Map the data type to labels + additional checks for string & int types
    if py_dtype == 'string' and any(is_date_string(value) for value in column_data if not pd.isnull(value)):
        data_type = 'date'
    if py_dtype == 'string' and all(isinstance(value, str) for value in column_data if not pd.isnull(value)):
        data_type = 'text'
    elif py_dtype == 'floating' and all(value.is_integer() for value in column_data if not pd.isnull(value)):
        data_type = 'integer'
    elif py_dtype == 'floating' and all(isinstance(value, float) for value in column_data if not pd.isnull(value)):
        data_type = 'decimal'
    else:
        data_type = 'unknown'
    return data_type

def is_date_string(s):
# Define regular expression pattern for date format as string
    date_pattern = r'\b\d{2}/\d{2}/\d{4}\b' # Matching 'dd/mm/yyyy' format
    # Check if string matches the date pattern
    return bool(re.match(date_pattern, s))

## Just to test 'date_pattern' string True/False 
print(is_date_string('null'))
print(is_date_string('2023/04'))
print(is_date_string('2023/04/17'))
print(is_date_string('17/04/2023'))

#==============================
#========= Sub-Tasks =========
#============================

def convert_to_py_int(value):
    if isinstance(value, np.int64):
        return int(value)
    return value

#===============================================
#========= MAIN(): Functions-Pipeline =========
#=============================================

def main():
    os.chdir(data_path)
    csv_file = enter_filename
    metadata = extract_metadata(csv_file)
    save_json_file(json_output, metadata)

if __name__ == "__main__":
    main()