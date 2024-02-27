#!/usr/bin/env python3

import csv
import sys


# set script parameters
item_cols_string = "item"
num_of_items_col = "obj_av_item_parts__ip_media_type"
item_delimiter = "\n"


##  Takes in a list of strings--the header row of a csv and
##  returns a list of indices of the columns that contain the substring "item"
def getItemCols(row):
    itemCols = []
    for index,heading in enumerate(row):
        if item_cols_string in heading:   
            itemCols.append(index)

    return itemCols

##  Takes in a list of strings--the header row of a csv and
##  Returns the index of the "obj_av_item_parts__ip_media_type" col.
##  If no such column exists, returns 0.
def getMediaTypeCol(row):
    itemCols = []
    for index,heading in enumerate(row):
        if num_of_items_col in heading:   
            return index

    return 0

##  Takes a single item with multiple parts and turns it into multiple items. Returns a list of item parts.
##  itemCols is a list of indices of columns that could contain multiple columns
##  typeCol is the indice of the column used to see how many parts an item has
def extractItemParts(item, itemCols, typeCol):
    numParts = item[typeCol].split(item_delimiter)
    extractedItems = []
    itemParts = []

    for col in itemCols:
        itemParts.append(item[col].split(item_delimiter)) # puts all the item parts into an array, ordered the same way as itemCols

    for index, part in enumerate(numParts):
        singleItem = item.copy()   # copies all the data from the original item

        for colIndex, col in enumerate(itemCols):
            parts = itemParts[colIndex]
            if parts == ['']:   # no data for this column, append null string
                singleItem[col] = ''
            else:
                singleItem[col] = itemParts[colIndex][index][5:].strip()  # reassigns columns with multiple values to a single value, strips leading '#X:: '

        extractedItems.append(singleItem)

    return extractedItems

    
##  Opens a csv file with items with multiple parts and writes a new file with multi-part items expanded into single parts.
##  In the output file, each row represents a part.
##  Expects two user inputs. First is the file to be read. Second is the file to be written.
def expandLines():
    with open(sys.argv[1]) as csvfile:      # open the csv supplied by user
            reader = csv.reader(csvfile)
            headerRow = next(reader)
            itemCols = getItemCols(headerRow)
            mediaTypeCol = getMediaTypeCol(headerRow)
            
            allItems = []
            allItems.append(headerRow)

            for row in reader:

                # if the item has more than one part, uses the field obj_av_item_parts__ip_media_type to check if multiple parts
                if len(row[mediaTypeCol].split(item_delimiter)) > 1:   
                    extractedItems = extractItemParts(row, itemCols, mediaTypeCol)
                    for index, item in enumerate(extractedItems):
                        item.append("%02d" % (index+1)) # make it 1-indexed instead of 0-indexed and include leading zero for 0–9
                        allItems.append(item)
                else:
                    allItems.append(row)


    with open(sys.argv[2], 'w',newline='') as csvfile:      # write the array to the user-specified file
        csvWriter = csv.writer(csvfile)
        for item in allItems:
            csvWriter.writerow(item)

expandLines()
