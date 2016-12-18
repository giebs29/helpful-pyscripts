import arcpy
import json

class ArcpyRelationshipClass:

    def __init__(self,relate_name):
        self.relate_name = relate_name
        self.define_input_relationship_properties()
        self.define_output_relationship_properties()

    def define_input_relationship_properties(self):
        desc = arcpy.Describe(self.relate_name)
        self.input_properties = {
        'backwardPathLabel':desc.backwardPathLabel,
        'cardinality':desc.cardinality,
        'classKey':desc.classKey,
        'destinationClassKeys':desc.destinationClassKeys,
        'destinationClassNames':desc.destinationClassNames,
        'forwardPathLabel':desc.forwardPathLabel,
        'isAttachmentRelationship':desc.isAttachmentRelationship,
        'isAttributed':desc.isAttributed,
        'isComposite':desc.isComposite,
        'isReflexive':desc.isReflexive,
        'keyType':desc.keyType,
        'notification':desc.notification,
        'originClassNames':desc.originClassNames,
        'originClassKeys':desc.originClassKeys,
        'relationshipRules':desc.relationshipRules
        }

    def define_output_relationship_properties(self):
        self.output_properties = {
        'origin_table':self.input_properties['originClassNames'][0],
        'destination_table':self.input_properties['destinationClassNames'][0],
        'out_relationship_class':self.relate_name,
        'relationship_type':'SIMPLE',
        'forward_label':self.input_properties['forwardPathLabel'],
        'backward_label':self.input_properties['backwardPathLabel'],
        'message_direction':self.input_properties['notification'],
        'cardinality':self.input_properties['cardinality'],
        'attributed':None,
        'origin_primary_key':self.input_properties['originClassKeys'][0],
        'origin_foreign_key':self.input_properties['originClassKeys'][1],
        'destination_primary_key':'',
        'destination_foreign_key':''
        }
        if self.input_properties['isComposite']:
            self.output_properties['relationship_type']='COMPOSITE'
        if self.input_properties['isAttributed']:
            self.output_properties['attributed']='ATTRIBUTED'

def get_tables(gdb_path):
    arcpy.env.workspace = gdb_path
    return [i for i in arcpy.ListTables()]

def get_feature_datasets(gdb_path):
    arcpy.env.workspace = gdb_path
    return [i for i in arcpy.ListDatasets()]

def get_feature_classes(gdb_path,featureDataset=None):
    if featureDataset:
        arcpy.env.workspace = gdb_path +'\\'+ featureDataset
    else:
        arcpy.env.workspace = gdb_path
    return [i for i in arcpy.ListDatasets()]

def get_tables_and_featureclasses(gdb_path):
    tables = []
    tables += get_tables(gdb_path)
    tables += get_feature_classes(gdb_path)
    for fds in get_feature_datasets(gdb_path):
        tables += get_feature_classes(gdb_path,fds)
    return tables

def get_relationship_class_names(gdb_path,table_list):
    arcpy.env.workspace = gdb_path
    relationship_class_names = []
    for table in table_list:
        try:
            relationship_class_names += [i for i in
                arcpy.Describe(table).relationshipClassNames]
        except:
            pass
    return relationship_class_names

def create_relationship_class_objects(name_list):
    pairlist = []
    relationship_objects = []
    for name in name_list:
        rel_object = ArcpyRelationshipClass(name)
        orig,dest = rel_object.input_properties['originClassNames'],rel_object.input_properties['destinationClassNames']
        if sorted((orig,dest)) not in pairlist:
            pairlist.append(sorted((orig,dest)))
            relationship_objects.append(rel_object.input_properties)
    return relationship_objects

def get_relationship_class_objects(gdb_path):
    tables = get_tables_and_featureclasses(gdb_path)
    names = get_relationship_class_names(gdb_path,tables)
    return create_relationship_class_objects(names)

def create_relationship_classes(gdb_path,relationship_objects):
    arcpy.env.workspace = gdb_path
    for rel_object in relationship_objects:
        params = rel_object.output_properties
        arcpy.CreateRelationshipClass_management(**params)

def create_json_file(out_json_path,relationship_objects):
    with open(out_json_path, 'w') as json_file:
        json.dump(relationship_objects , json_file)

def load_json_file(in_json_path):
    with json.load(open(in_json_path)) as json_data:
        return json_data
