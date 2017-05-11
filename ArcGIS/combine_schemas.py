import arcpy

def get_field_values(table,*fields):
    '''Returns a list of the unique values found in the specified field'''

    if len(fields) == 1:
        data = [str(i[0]) for i in arcpy.da.SearchCursor(table,fields) if i[0] != None]

    else:
        data = [i for i in arcpy.da.SearchCursor(table,fields)]

    return list(set(data))

def field_maxlengths(tables):
    for table in tables:
        fields = [str(i.name) for i in arcpy.ListFields(table)]
        for field in fields:
            field_values = get_field_values(table,field)
            longest_value = max(map(lambda x: len(str(x)),field_values))
            print(longest_value)
