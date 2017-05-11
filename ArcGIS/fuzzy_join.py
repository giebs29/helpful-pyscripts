import arcpy
from difflib import SequenceMatcher

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

def temp_object(object_type,in_features,out_layer,where_clause=None,workspace=None,field_info=None):

    if arcpy.Exists(out_layer):
        arcpy.Delete_management(out_layer)

    if 'table' in object_type.lower():
        output = arcpy.MakeTableView_management(
            in_table = in_features,
            out_view = out_layer,
            where_clause=where_clause,
            workspace = workspace,
            field_info = field_info)
    else:
        output = arcpy.MakeFeatureLayer_management(
            in_features = in_features,
            out_layer = out_layer,
            where_clause=where_clause,
            workspace = workspace,
            field_info = field_info)

    return output

def compare_values(a,b):
    return SequenceMatcher(None,a.lower().strip(),b.lower().strip()).ratio()

# print('Writing to csv')
# with open(outCSVPath, "w") as text_file:
#     text_file.write("TARGET_ID,TARGET_ADDRESS,MASTER_ID,MASTER_ADDRESS,MATCH_SCORE,DROP_STATUS\n")
#
#     for row in tempList:
#         text_file.write(row+'\n')

if __name__ == '__main__':
    table1 = arcpy.GetParameterAsText(0)
    table1_fld = arcpy.GetParameterAsText(1)
    table2 = arcpy.GetParameterAsText(2)
    table2_fld = arcpy.GetParameterAsText(3)
    # threshold = arcpy.getParameterAsText(4)

    # Get OBJECTID fields
    table1_oid_fld = arcpy.Describe(table1).OIDFieldName
    table2_oid_fld = arcpy.Describe(table2).OIDFieldName

    # Get table data
    table1_data = table2dict(table1,[table1_oid_fld,table1_fld])
    table2_data = table2dict(table2,[table2_oid_fld,table2_fld])

    # List for storing join pairs
    join_pairs = []

    for record in table1_data:
            temp_data = [(compare_values(record[table1_fld],i[table2_fld]),i[table2_oid_fld]) for i in table2_data]
            temp_pair = (record[table1_oid_fld],max(temp_data, key=lambda x: x[0])[1])
            join_pairs.append(temp_pair)

    _temp_table = arcpy.CreateTable_management(
        out_path = "in_memory",
        out_name = "_temp_table")

    temp_table_view = temp_object(
        object_type="table",
        in_features = _temp_table,
        out_layer="temp_table_view")

    arcpy.AddField_management(
        in_table = temp_table_view,
        field_name = "TABLE1_OID",
        field_type = "SHORT")

    arcpy.AddField_management(
        in_table = temp_table_view,
        field_name = "TABLE2_OID",
        field_type = "SHORT")

    with arcpy.da.InsertCursor(temp_table_view, ["TABLE1_OID","TABLE2_OID"]) as cursor:
        for join_pair in join_pairs:
            cursor.insertRow((join_pair[0],join_pair[1]))

    table1_view = temp_object(
        object_type="table",
        in_features = table1,
        out_layer="table1_view")

    table2_view = temp_object(
        object_type="table",
        in_features = table2,
        out_layer="table2_view")

    arcpy.AddJoin_management(
        in_layer_or_view = table1_view,
        in_field = table1_oid_fld,
        join_table = temp_table_view,
        join_field = "TABLE1_OID",
        join_type = "KEEP_ALL")

    arcpy.AddJoin_management(
        in_layer_or_view = table1_view,
        in_field = "TABLE2_OID",
        join_table = table2_view,
        join_field = table2_oid_fld,
        join_type = "KEEP_ALL")
