import arcpy

def find_duplicates(fc,field_list):

    arcpy.env.workspace = "IN_MEMORY"
    arcpy.env.overwriteOutput = True


    arcpy.FindIdentical_management(fc,"temp_file",field_list,output_record_option="ONLY_DUPLICATES")

    select_list = []
    seq_list = []

    with arcpy.da.SearchCursor("temp_file","*") as cursor:
        for row in cursor:

            seq_list.append(row[2])

            if seq_list.count(row[2]) > 1:
               select_list.append(row[1])

    query = "\"OBJECTID\"IN({0})".format(str(select_list).strip('[]'))

    arcpy.SelectLayerByAttribute_management(fc, "NEW_SELECTION", query)




