import json
import arcpy

def open_json(json_path):
    with open(json_path) as json_data:
        return json.load(json_data)

def add_field(table,field):
    arcpy.AddField_management(
        in_table=table,
        field_name=field.get('name'),
        field_type=convert_field_type(field.get('type')),
        field_length=field.get('length'),
        field_alias=field.get('alias'),
        field_is_nullable='NULLABLE')

def populate_domain(gdb,domain):
    for coded_value in domain['codedValues']:
        arcpy.AddCodedValueToDomain_management(
            in_workspace=gdb,
            domain_name=domain['name'],
            code=coded_value['code'],
            code_description=coded_value['name'])

def add_domain(gdb,domain):
    arcpy.CreateDomain_management(
        in_workspace=gdb,
        domain_name=domain['name'],
        domain_description=domain.get('description'),
        domain_type='CODED')

    populate_domain(gdb,domain)

def convert_field_type(esriFieldType):
    field_types = {
    'SHORT':'esriFieldTypeSmallInteger',
    'LONG':'esriFieldTypeInteger',
    'FLOAT':'esriFieldTypeSingle',
    'DOUBLE':'esriFieldTypeDouble',
    'TEXT':'esriFieldTypeString',
    'DATE':'esriFieldTypeDate',
    'BLOB':'esriFieldTypeBlob',
    'RASTER':'esriFieldTypeRaster',
    'GUID': 'esriFieldTypeGUID'}

    for key in field_types.keys():
        if esriFieldType == field_types[key]:
            return key

def process_fields(table,json_data):
    for field in json_data['fields']:
        if convert_field_type(field['type']):
            add_field(table,field)
            # if field['domain']:
            #     add_domain('gdb',field['domain'])

def json_to_featureclass(json_path,fc_name):
    arcpy.env.preserveGlobalIds = True
    if arcpy.Exists(fc_name):
        arcpy.Delete_management(fc_name)
    arcpy.JSONToFeatures_conversion(
        in_json_file=json_path,
        out_features=fc_name)

def create_table(gdb,table_name):
    if arcpy.Exists(table_name):
        arcpy.Delete_management(table_name)

    arcpy.CreateTable_management(
        out_path=gdb,
        out_name=table_name)

def populate_table(table,json_path):
    temp_table_view = arcpy.MakeTableView_management(
        in_table=table,
        out_view='temp_table_view')

    data = open_json(json_path)

    field_list = [str(i.name) for i in arcpy.ListFields(table) if not i.required]
    with arcpy.da.InsertCursor(temp_table_view,'OBJECTID') as cursor:
        for feature in data['features']:
            row_data = []
            for field in field_list:
                row_data.append(feature['attributes'][field])
            cursor.insertRow([''])

    with arcpy.da.UpdateCursor(temp_table_view,field_list) as cursor:
        for row_num,row in enumerate(cursor):
            for field in field_list:
                print field
                row[field_list.index(field)] = data['features'][row_num]['attributes'][field]
            cursor.updateRow(row)


    arcpy.Delete_management(temp_table_view)



def main(gdb,json_path):
    # Get name and remove any spaces
    name = open_json(json_path)['name'].replace(" ", "")

    # Check whether json is a layer or table
    if open_json(json_path)['type'] == 'layer':
        json_to_featureclass(json_path,name)
    else:
        create_table(gdb,name)
        table_path = gdb + '\\' + name
        json_data = open_json(json_path)
        process_fields(table_path,json_data)
        populate_table(table_path,json_path)


# process_fields(data)
gdb = ""
arcpy.env.workspace = gdb

json_file = ""
# print open_json(json_file)
main(gdb,json_file)
