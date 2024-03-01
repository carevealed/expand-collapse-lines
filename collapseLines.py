#!/usr/bin/env python3

import csv
import sys

##  Takes in a list of strings--the header row of a csv and
##  returns a list of indices of the columns that contain the substring "item"
def getItemCols(row):
    itemCols = []
    for index,heading in enumerate(row):
        if "item_parts__ip" in heading:   
            itemCols.append(index)

    return itemCols


##  Takes in a list of strings--the header row of a csv and
##  Returns the index of the "obj_object_identifier" col.
##  If no such column exists, returns 0.
def getObjectIdCol(row):
    itemCols = []
    for index,heading in enumerate(row):
        if "obj_object_identifier" in heading:   
            return index

    return 0


##  Takes multiple items with the same object_id and collapses it into a single item
##  item is a list of items with the same object_id. itemCols is a list of columns which may contain multiple item-parts
def collapseItemParts(item, itemCols):
    if (len(item) <= 1): # if there is only one part, return the item
        return item[0]

    collapsedItem = item[0] # copies all the data from the first instance of the item 

    for col in itemCols: # for each of the defined columns
        itemVal = ""
        for index, part in enumerate(item): # for each item part
            if part[col] != '' and len(part) >=1 :  # if value is not a null string and has more than one part
                itemVal+= "#"+str(index+1)+":: "+part[col]+"\n"
            
        collapsedItem[col]=itemVal.strip()  # strips the trailing \n and reassigns the column value to the collapsed version

    return collapsedItem


##  Reads a csv file and collapses any lines with the same object id into a single line with multiple parts.
##  Takes two arguments. First is the csv to read. Second is the csv to write the output.
def collapseLines():
    
    with open(sys.argv[1]) as csvfile:      # open the csv supplied by user
            reader = csv.reader(csvfile)
            headerRow = next(reader)

            itemCols = getItemCols(headerRow)   # gets a list of cols that may have item parts
            objectIdCol = getObjectIdCol(headerRow) # the index of the obj_object_identifier column, used to determine if parts belong to the same item
            allItems = []

            currId = ""
            currItem = []
            currItem.append(headerRow)   # preloads the header row

            for row in reader:
                if currId == row[objectIdCol]:    # if current row has the same object_id as the previous row
                    currItem.append(row)
                else:
                    allItems.append(collapseItemParts(currItem, itemCols))
                    currId = row[objectIdCol]
                    currItem=[]
                    currItem.append(row)
            allItems.append(collapseItemParts(currItem, itemCols))    # add the last item (otherwise not reached because no comparison occurs)

    with open(sys.argv[2], 'w',newline='') as csvfile:      # write the array to the user-specified file
        csvWriter = csv.writer(csvfile)
        for item in allItems:
            csvWriter.writerow(item)

collapseLines()
