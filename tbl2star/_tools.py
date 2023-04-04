import os
import glob
import sys
import re
import numpy as np
import pandas as pd
import dynamotable
import starfile
from typing import Optional

# ts_path = '/Users/hzvictor/Desktop/Membrane_Associated_Picking-main/tomograms'

def get_tbl_paths(folder_path, 
                  file_ext='*.tbl'):
    if folder_path != '.':
        folder_path = os.path.abspath(folder_path)
    file_paths = glob.glob(os.path.join(folder_path, file_ext))
    return file_paths

def read_dynamo_tbl(folder_path: Optional[str] = '.'):
    folder_path = folder_path.default if type(folder_path) != str else folder_path
    lst = get_tbl_paths(folder_path)
    tbl = pd.DataFrame()
    for tbl_paths in lst:
        tbl_temp = dynamotable.read(tbl_paths)
        tbl = pd.concat([tbl_temp, tbl])
        print(f'{tbl_paths} has been read')
    return tbl
        

def extract_ts_number(name, 
                      pattern: Optional[str] = None):
    pattern = pattern.default if type(pattern) != str else pattern
    if pattern is None:
        pattern = r'.*?(?:t|T)(?:s|S)_(\d+)'
    else:
        pattern = r".*?{}_(\d+)".format(pattern)
    match = re.search(pattern, name)
    if match is None:
        print(f"Error: No match found for pattern '{pattern}' in name '{name}'")
        sys.exit()
    else:
        ts_number = match.group(1)
        return ts_number

def get_tomo_name(ts_path,
                  tomo_num_arr,
                  pattern: Optional[str] = None):
    dirs = next(os.walk(ts_path))[1]
    tomo_name_lst = [''] * len(tomo_num_arr)
    for tomo_name in dirs:
        tomo_number = int(extract_ts_number(tomo_name, pattern))
        tomo_nameindex = np.asarray(np.where(tomo_num_arr == tomo_number))[0]
        for i in tomo_nameindex:
            tomo_name_lst[i] = tomo_name
    return tomo_name_lst

def save_dynamo_star(dataframe, filename, filepath):
    filename = filename.default if type(filename) != str else filename
    filepath = filepath.default if type(filepath) != str else filepath
    filename_n = filename if filename else 'AllCoordinates.star'
    filepath_n = str(filepath) + '/' if filepath else str(os.path.abspath('.')) + '/'
    filenamepath = os.path.join(filepath_n, filename_n)
    starfile.write(dataframe, filenamepath, overwrite=True)
    print(f'Saving relion .star file {filename_n} to {filepath_n} ...')

