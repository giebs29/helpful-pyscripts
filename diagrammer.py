import arcpy
import os


ws = r'X:\business\projects\blandin\Data_cleanup\SmartFor\WTS_EXPORT7_14_15.gdb'

arcpy.env.workspace = ws

fds_list = arcpy.ListDatasets()

table_list = arcpy.ListTables()

fc_list = arcpy.ListFeatureClasses()



data_dict = {
'FDS':[],
'TABLES':[],
'FC':[],
}


print 'Retrieving Data'

for table in table_list:
    temp_dict = {}
    temp_dict['name'] = str(table)
    temp_dict['fields'] = [str(i.name) for i in arcpy.ListFields(table)]
    data_dict['TABLES'].append(temp_dict)

for fc in fc_list:
    temp_dict = {}
    temp_dict['name'] = str(fc)
    temp_dict['fields'] = [str(i.name) for i in arcpy.ListFields(fc)]
    data_dict['TABLES'].append(temp_dict)


for fds in fds_list:
    new_dict = {}
    new_dict['name'] = str(fds)
    new_dict['fc_list'] = []

    path = os.path.join(ws,fds)
    arcpy.env.workspace = path
    temp_fcs = arcpy.ListFeatureClasses()

    for fc in temp_fcs:
        temp_dict = {}
        temp_dict['name'] = str(fc)
        temp_dict['fields'] = [str(i.name) for i in arcpy.ListFields(fc)]
        new_dict['fc_list'].append(temp_dict)

    data_dict['FDS'].append(new_dict)



print 'Creating HTML'
with open(r"C:\Users\samg\Desktop\module1.html", "w") as text_file:

     top_string = '<!DOCTYPE html>\n<html>\n<style>table,th{border:1px solid #dddddd;} table{width:25%;}</style>\n<body>'
     bottom_string = '\n</body>\n</html>'

     for FDS in data_dict['FDS']:

         for fc in FDS['fc_list']:
             top_string += '\n<table>'
             top_string += '\n<th style="background-color:#FF5D79;">'+ fc['name'] + '</th>'
             print 'Feature Class',fc['name']

             for field in fc['fields']:
                 top_string += '\n<tr><td>'+ field + '</td></tr>'
                 print 'Field',field
             top_string += '</table>'

     for table in data_dict['TABLES']:
         top_string += '\n<table>'
         top_string += '\n<th style="background-color:#81d8d0;">'+ table['name'] + '</th>'

         for field in table['fields']:
                 top_string += '\n<tr><td>'+ field + '</td></tr>'
                 print 'Field',field
         top_string += '</table>'

     for fc in data_dict['FC']:
         top_string += '\n<table>'
         top_string += '\n<th style="background-color:#fa5a00;">'+ fc['name'] + '</th>'

         for field in fc['fields']:
                 top_string += '\n<tr><td>'+ field + '</td></tr>'
                 print 'Field',field
         top_string += '</table>'


     top_string += bottom_string
     text_file.write(top_string)