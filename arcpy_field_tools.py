import arcpy

ts_fc = r'C:\Users\samg\Documents\MyRepos\rcra_script\rcra_boundaries.gdb\Timber_Sales'
hv_table = r'C:\Users\samg\Documents\MyRepos\rcra_script\rcra_boundaries.gdb\HARVEST'

def list_empty_fields(table):
    empty_fields = []
    fields = [str(i.name) for i in arcpy.ListFields(table)]
    data = [i for i in arcpy.da.SearchCursor(table,'*')]
    for field in fields:
        if len([i for i in data if i[fields.index(field)] is not None]) == 0:
            empty_fields.append(field)

    return empty_fields

print 'Timber Sale', list_empty_fields(ts_fc)
print 'Harvest', list_empty_fields(hv_table)

def empty_select_fields(table, fields_save=False):

    # List field names in table
    fields = [str(i.name) for i in arcpy.ListFields(table)]

    # Remove any fields that should not be emptied
    if fields_save:
        for field in fields_save:
            try:
                fields.pop(fields.index(field))
            except:
                print(field+" Not in Table!")
                return


# Timber Sale ['range', 'manageObj', 'soilProtect', 'countyText', 'state', 'type']
# Harvest ['regenMethod', 'startDate', 'endDate', 'contractNumber', 'comments', 'harvestSystem', 'relGUID', 'status']
