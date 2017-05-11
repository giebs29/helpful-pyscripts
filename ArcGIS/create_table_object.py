import arcpy

def table2dict(input_table,fields=False,where=False):
    data = []

    if not fields:
        fields = '*'

    if not where:
        where = ''

    with arcpy.da.SearchCursor(input_table,fields,where) as sc:
        fields = [str(i) for i in sc.fields]
        for row in sc:
            temp_dict = {}
            for col, field in enumerate(fields):
                temp_dict[field] = row[col]
            data.append(temp_dict)
    return data
