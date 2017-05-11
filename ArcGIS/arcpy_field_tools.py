import arcpy

def list_empty_fields(table):
    empty_fields = []
    fields = [str(i.name) for i in arcpy.ListFields(table)]
    data = [i for i in arcpy.da.SearchCursor(table,'*')]
    for field in fields:
        if len([i for i in data if i[fields.index(field)] is not None]) == 0:
            empty_fields.append(field)

    return empty_fields

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


print list_empty_fields('')
