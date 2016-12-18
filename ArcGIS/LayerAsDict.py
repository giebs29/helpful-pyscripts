import arcpy

class LayerAsDict():

    table = ""

    def __init__(self, table):
        self.table = table


    def returnFields(self):
        '''Returns a list of field names'''
        # Generate list of field names
        fields = [str(i.name) for i in arcpy.ListFields(self.table)]
        return fields

    def returnTableAsDict(self):
        '''Returns input table as a python dict'''
        tempList = []

        # Get list of fields
        fieldList = self.returnFields()

        # Create cursor
        with arcpy.da.SearchCursor(self.table, '*') as cursor:
            for row in cursor:
                # Create dict to store row data
                newDict = {}

                # Populate dict
                for field in fieldList:
                    newDict[field] = row[fieldList.index(field)]
                # Add row dict to list
                tempList.append(newDict)

        return tempList




