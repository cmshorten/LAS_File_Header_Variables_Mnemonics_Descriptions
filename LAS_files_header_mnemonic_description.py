"""
LAS File Header Variables, Mnemonics and Descriptions

Purpose:
This script searches through a folder (and all sub-folders), identifies all of the .las files, and outputs a table of
the unique mnemonics and descriptions within the files.

Input:
* folderpath = the folder/drive in which you'd like to search for .las files

Output:
* lasfilepaths.txt = list of .las filepaths
* status.txt = documents status of script as it collects the unique mnemonics and descriptions within the files
* errors.txt = documents errors that occur as lasio tries to read in the .las files
* variable_info.txt = final list of the unique mnemonics and descriptions within the files

Created by:
Chilisa Shorten
cshorten@usgs.gov
12/09/21
"""

# load in libraries
import lasio
import os
from operator import itemgetter

# Define folder path
folderpath = r'Z:\well_logs'

# delete old versions of output .txt files
for f_name in ['lasfilepaths.txt', 'status.txt', 'errors.txt', 'variable_info.txt']:
    if os.path.exists(f_name):
        os.remove(f_name)

# Create a list of .las file paths within the folder path
filepaths = []
for root, dirs, files in os.walk(folderpath):
    for name in files:
        if name.endswith((".las", ".LAS")):
            filepaths.append(os.path.join(root, name))
            print(os.path.join(root, name), file=open('lasfilepaths.txt', 'a'))

# returns the number of .las files found
print(f"number of .las files within '{folderpath}': {len(filepaths)}")

# Collect variable mnemonics and descriptions from the .las files
variable_info = []
count = len(filepaths)
for i, las_f_path in enumerate(filepaths):
    try:
        print(f'working on {las_f_path}, {i+1}/{count}', file=open('status.txt', 'a'))
        las_f = lasio.read(las_f_path, ignore_data=True, ignore_header_errors=True)
        # ignores data section, just contains header metadata section
        # sometimes the read in will report ":Remarks" error - just ignore, it's still collecting the information
        try:
            for version_info in las_f.version:
                variable_info.append((version_info.mnemonic, version_info.descr, 'version'))
            for well_info in las_f.well:
                variable_info.append((well_info.mnemonic, well_info.descr, 'well'))
            for curves_info in las_f.curves:
                variable_info.append((curves_info.mnemonic, curves_info.descr, 'curves'))
            for params_info in las_f.params:
                variable_info.append((params_info.mnemonic, params_info.descr, 'parameter'))
        except Exception as e:
            print(f'!!!Error {e} in {las_f_path}!!!', file=open('errors.txt', 'a'))
    except Exception as e:
        print(f'Error {e} in {las_f_path}; could not open file', file=open('errors.txt', 'a'))

# Compose variable mnemonics and descriptions into a .txt file
variable_info = list(set(variable_info))
variable_info.sort(key=itemgetter(0))  # key=itemgetter(0 sort by mnemonic
delim = '\t'
out_file = f'variable_info.txt'
with open(out_file, 'w') as f:
    for info in variable_info:
        f.write(f'{delim.join(info)}\n')
