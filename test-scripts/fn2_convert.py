import os
import chardet
import pandas as pd
from openpyxl import Workbook

w_dir = r'Z:\DataETL\FileCont1-mpd\test\1_unzip'
temp_dir = r'Z:\DataETL\FileCont1-mpd\test\2.1_temp'
out_dir = r'Z:\DataETL\FileCont1-mpd\test\2.2_convert'

#===================================
#========= Main-Functions =========
#=================================

# Fn: Checking input file-formats
def check_file_formats():
    for filename in os.listdir(w_dir):
        if filename.endswith('.txt'):
            # call Sub
            txt_to_csv(filename)
        elif filename.endswith('.csv'):
            # call Sub
            clean_csv_inconsistencies(filename)
        elif filename.endswith('.xlsx'):
            # call Sub
            excel_to_csv(filename)
        else:
            print(f"{filename}: Unknown file extension(s) ! ")

# Fn: Correcting & formatting CSV files
def csv_formatting():
    for filename in os.listdir(temp_dir):
        file_path = os.path.join(temp_dir, filename)
        # call SubTask
        used_encode = check_encoding(file_path)
        # read CSV with auto-detect delimiter
        try:
            df = pd.read_csv(file_path, sep=None, encoding=used_encode, engine='python')
        except Exception as e:
            print(f"Error reding {file_path}: {e}")
            return
        # call SubTask
        decimal_sep(df)
        # save modified DataFrame as new CSV
        path_out = os.path.join(out_dir, filename)
        df.to_csv(path_out, index=False, sep=',', encoding='utf-8')

#==================================
#========= Sub-Functions =========
#================================

# Sub: Converting TXT to CSV
def txt_to_csv(filename):
    file_path = os.path.join(w_dir, filename)
    # call SubTask
    used_encode = check_encoding(file_path)
    # different action depending on column-separator
    with open(file_path, 'r', encoding=used_encode) as file:
        first_line = file.readline()
        if ';' in first_line:
            df = pd.read_csv(file_path, sep=';', encoding=used_encode)
            # call SubTask
            decimal_sep(df)
            # call SubTask
            path_out = get_outpath(filename)
            # write DataFrame to CSV
            df.to_csv(path_out, index=False, sep=',', encoding='utf-8')
        elif '\t' in first_line:
            df = pd.read_csv(file_path, sep='\t', encoding=used_encode)
            # call SubTask
            path_out = get_outpath(filename)
            # write DataFrame to CSV
            df.to_csv(path_out, index=False, sep=',', encoding='utf-8')
        else:
            df = pd.read_csv(file_path, encoding=used_encode)
            # call SubTask
            path_out = get_outpath(filename)
            # write DataFrame to CSV
            df.to_csv(path_out, index=False, sep=',', encoding='utf-8')

# Sub: Pre-cleaning row-level inconsistencies
def clean_csv_inconsistencies(filename):
    file_path = os.path.join(w_dir, filename)
    temp_path = os.path.join(temp_dir, filename)
    # read & clean file line by line
    cleaned_lines = []
    with open(file_path, 'r') as file:
        for line in file:
            # replace quotation marks, empty spaces, etc.
            cleaned_line = line.replace('"', '').replace(' ,', ',').replace(', ', ',').replace(' ;', ';').replace('; ', ';')
            cleaned_lines.append(cleaned_line)
    # write cleaned lines to temp-dir
    with open(temp_path, 'w') as file:
        file.writelines(cleaned_lines)

# Sub: Converting XLSX to CSV
def excel_to_csv(filename):
    file_path = os.path.join(w_dir, filename)
    excel_file = pd.ExcelFile(file_path)
    df = excel_file.parse(excel_file.sheet_names[0])
    # call SubTask
    path_out = get_outpath(filename)
    # write DataFrame to CSV
    df.to_csv(path_out, index=False, sep=',', encoding='utf-8')

#==============================
#========= Sub-Tasks =========
#============================

# Task: Detecting encoding while reading files
def check_encoding(file_path):
    with open(file_path, 'rb') as file:
        raw_data = file.read()
        encode_info = chardet.detect(raw_data)
        used_encode = encode_info['encoding']
    return used_encode

# Task: Checking if decimal-sep == comma -> replace with dot
def decimal_sep(df):
    for column in df.select_dtypes(include=['object']):
        if df[column].str.contains(',').any():
            df[column] = df[column].str.replace(',', '.')

# Task: Getting path-out via basename excl.extension
def get_outpath(filename):
    basename, extension = os.path.splitext(filename)
    out_name = '{}.csv'.format(basename)
    path_out = os.path.join(out_dir, out_name)
    return path_out

#=========================================
#========= MAIN: call Functions =========
#=======================================

def main():
    check_file_formats()
    csv_formatting()

if __name__ == "__main__":
    main()