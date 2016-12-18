import json

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
    'RASTER':'esriFieldTypeRaster'}

    for key in field_types.keys():
        if esriFieldType == field_types[key]:
            return key

def process_fields(json_data):
    for field in json_data['fields']:
        if convert_field_type(field['type']):
            add_field('temp_table',field)
            if field['domain']:
                add_domain('gdb',field['domain'])

class FauxClass(object):
    def __init__(self,print_name=None,print_args=None):
        self.print_name = print_name
        self.print_args = print_args

    def __getattr__(self, name):
        def wrapper(*args, **kwargs):
            if self.print_name and self.print_args:
                print name,kwargs
            elif self.print_args:
                print kwargs
            elif self.print_name:
                print name
        return wrapper

# Simulate arcpy module
arcpy = FauxClass(True,True)
data = open_json(r"C:\Users\Sam\Desktop\test_data\loc_vol.json")
process_fields(data)
