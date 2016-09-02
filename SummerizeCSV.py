#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      samg
#
# Created:     04/08/2014
# Copyright:   (c) samg 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import csv
import arcpy
class csvTools():
    FilePath = ""
    num_cols = ""
    uniqueList = ""
    countList = ""
    summaryField = ""
    dataToAdd = ""

    def __init__(self,FilePath):
        self.FilePath = FilePath

    def createCSVobject(self):
        CSV = open(self.FilePath, 'rb')
        return csv.reader(CSV, delimiter=',')

    def getNumberColumns(self):
        CSV = self.createCSVobject()
        self.num_cols = len(next(CSV))
        del CSV
        return self.num_cols

    def getFieldNames(self):
        CSV = self.createCSVobject()
        position = 0
        index = 0
        for row in CSV:
            if position == 0:
                for i in range(0,self.num_cols):
                    print row[i], index
                    index +=1
                position = 1
        del CSV

    def getUniqueList(self,Field): #Returns list of unique values from column.
        tempList = []
        CSV = self.createCSVobject()
        position = 0
        for row in CSV:
            if position >= 1:
                if row[Field] in tempList:
                    pass
                else:
                    data = row[Field]
                    tempList.append(data)
            else:
                position = 1
        self.uniqueList = tempList
        del CSV
        return self.uniqueList

    def getCounts(self,EntityField,CountField):
        CSV = self.createCSVobject()
        index = 0
        dataList = []
        for row in CSV:
            if index >= 1:
                for each in self.uniqueList:
                    if row[EntityField] == each:
                        print each,row[CountField]
                        data = each,row[CountField]
                        dataList.append(data)
            else:
                index = 1
        self.dataToAdd = dataList
        del CSV

    def createNewShapefile(self):
        fc = ""
        search = arcpy.da.SearchCursor(fc,'Name')
        insert = arcpy.da.InsertCursor()

    def Summarize(self,EntityField,CountField):
        self.getNumberColumns()
        self.getFieldNames()
        self.getUniqueList(0)
        self.getCounts(EntityField,CountField)









def main():
    pass

if __name__ == '__main__':
    main()
