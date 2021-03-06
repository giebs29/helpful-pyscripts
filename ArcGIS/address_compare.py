import arcpy
from difflib import SequenceMatcher

# Path to input data sets
targetPath = ""
masterPath = ""

# Output csv file path
outCSVPath = ""

# Set field name variables
targetUnqFld = ""
targetJoinFld = ""
masterUnqFld = ""
masterJoinFld = ""

# Retrive table data as list of rows
target = [i for i in arcpy.da.SearchCursor(targetPath,[targetUnqFld,targetJoinFld])]
master = [i for i in arcpy.da.SearchCursor(masterPath,[masterUnqFld,masterJoinFld])]

tempList = []

def findSimilar(source,target):
    bestFit = 0
    rowNum = 0
    for num, row in enumerate(target):
        if row[1] and source[1]:
            ratio = SequenceMatcher(None,source[1].strip(),row[1].strip()).ratio()
            if ratio > bestFit:
                bestFit = ratio
                rowNum = num
    tempString = '{0},{1},{2},{3},{4}'.format(source[0], source[1].strip(), target[rowNum][0], target[rowNum][1].strip(), round(ratio,2))
    print tempString
    return tempString

for row in target:
    tempList.append(findSimilar(row,master))

with open(outCSVPath, "w") as text_file:
    text_file.write("TARGET_ID,TARGET_ADDRESS,MASTER_ID,MASTER_ADDRESS,MATCH_SCORE\n")

    for row in tempList:
        text_file.write(row+'\n')
