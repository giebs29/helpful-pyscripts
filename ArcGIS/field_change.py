import arcpy

def change_field_type(in_table,field,field_type,**keywords):

    if field_type not in  ['TEXT','FLOAT','DOUBLE','SHORT','LONG']:
        return

    temp_field = "temp_"+field

    if arcpy.Exists("tempTable"):
        arcpy.Delete_management("tempTable")

    tempTable = arcpy.MakeTableView_management(
        in_table = in_table,
        out_view = "tempTable")

    param_dict = {
        'in_table': tempTable,
        'field_name': temp_field,
        'field_type': field_type}

    for key in keywords.keys():
        param_dict[key] = keywords[key]

    arcpy.AddField_management(**param_dict)

    with arcpy.da.UpdateCursor(in_table,[field,temp_field]) as cursor:
        for row in cursor:
            if row[0]:
                if field_type == 'TEXT':
                    row[1] = str(row[0])
                elif field_type in ['FLOAT','DOUBLE']:
                    row[1] = float(row[0])
                elif field_type in ['SHORT','LONG']:
                    row[1] = float(row[0])
            cursor.updateRow(row)

    arcpy.DeleteField_management(
        in_table = tempTable,
        drop_field = field)

    if arcpy.Exists("tempTable"):
        arcpy.Delete_management("tempTable")

    tempTable = arcpy.MakeTableView_management(
        in_table = in_table,
        out_view = "tempTable")

    arcpy.AddField_management(
        in_table = tempTable,
        field_name = field,
        field_type = field_type)

    with arcpy.da.UpdateCursor(in_table,[temp_field,field]) as cursor:
        for row in cursor:
            row[1] = row[0]
            cursor.updateRow(row)

    arcpy.DeleteField_management(
        in_table = tempTable,
        drop_field = temp_field)

    arcpy.Delete_management("tempTable")


if __name__ == '__main__':
    arcpy.env.workspace = 'in_memory'

    table = arcpy.GetParameterAsText(0)
    field = arcpy.GetParameterAsText(1)
    field_type = arcpy.GetParameterAsText(2)

    change_field_type(
        in_table=table,
        field=field,
        field_type=field_type)
