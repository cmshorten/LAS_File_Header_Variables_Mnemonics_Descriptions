# LAS_File_Header_Variables_Mnemonics_Descriptions

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
/n Chilisa Shorten
cshorten@usgs.gov
12/09/21
