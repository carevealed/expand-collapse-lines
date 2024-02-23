# What the script is
These scripts expand and collapse our object level metadata into item level metadata and back into object level metadata. Our repository only ingests object level metadata. Temporarily expanding the rows to item level can make certain data entry tasks easier and automized. These are meant to be in use with the AV Databaseline export. The expandLinesS4D.py script is meant for our AV Sent for Digitization export in order to create item-level records for the vendor. All of these scripts require that you use the machine-readable headers for these sheets.
## Why CA-R uses it
The exports from the California Revealed repository are currently object level. Each object has the same main identifier and end up being published on a single webpage. We use delimiters (#1::, #2::, etc.) in item-specific fields to help designate item-level information so that our repository ingests this information correctly. That means each row has the potential to hold multiple items.
## Workflow timelines
These scripts are particularly helpful post-digitization. They can be used in tandem with xml_parse_csv.py and avPriceBundles.py scripts to more easily ingest technical metadata at a batch level.
# Procedures
- You will need python3 to be able to run this script
- Download the script from this github: expand-collapse-lines
- Create a folder called "scripts" in your Documents folder. Move both scripts to this folder.
- Open terminal and change your directory (cd) to the scripts folder. You can use the command below to do so.
```
cd Documents/scripts/
```
- Now you are ready to use the expand script to create a new csv with the item level rows. Here is the beginning of the command, which will then be followed by the pathway to the original csv you want to expand, followed by the path to the new csv you will create. 
```
python3 expandLines.py [pathway/to/file.csv] [pathway/to/newfile.csv]
```
Example:
```
python3 avPriceBundles.py ./Desktop/capdhs_2021-2022_AV_QC.csv ./Desktop/capdhs_2021-22_expanded.csv 
```
- When you press enter, a new csv file will be created following the pathway you determined in the terminal. 

- Once you input your item-level information, you need to collapse the rows to be object level so it can be ingested into our system. Follow the same steps as above to create a new csv file. 
```
python3 collapseLines.py [pathway/to/file.csv] [pathway/to/newfile.csv]
```
Example:
```
python3 avPriceBundles.py ./Desktop/capdhs_2021-2022_expanded.csv ./Desktop/capdhs_2021-22_collapse.csv 
```
- When you press enter, a new csv file will be created following the pathway you determined in the terminal. 
