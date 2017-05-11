import arcpy

def get_fields(table):
    return [str(i.name) for i in arcpy.ListFields(table)]

def get_field_values(table,field):
    '''Returns a list of the unique values found in the specified field'''
    data = [str(i[0]) for i in arcpy.da.SearchCursor(table,field) if i[0] != None]

    return set(data)

def compare_lists(list_a,list_b):
    return [i for i in list_a if i not in list_b]
