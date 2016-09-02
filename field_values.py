import arcpy

def get_field_values(table,field):
    vlaues = []

    data = [str(i[0]) for i in arcpy.da.SearchCursor(table,field) if i[0] != None]

    return set(data)

def compare_lists(list_a,list_b):
    return [i for i in list_a if i not in list_b]

table = r'C:\Users\samg\Documents\MyRepos\rcra_script\rcra_boundaries.gdb\Timber_Sales'

# print field_values(table, 'wildCwd')

ts_fc = r'C:\Users\samg\Documents\MyRepos\rcra_script\rcra_boundaries.gdb\Timber_Sales'
hv_table = r'C:\Users\samg\Documents\MyRepos\rcra_script\rcra_boundaries.gdb\HARVEST'
LOCATION_PROPERTY = r'X:\business\projects\blandin\Data_cleanup\SmartFor\WTS_EXPORT7_14_15.gdb\WTS_BLANDIN_LOCATION_PROPERTY'

print get_field_values(LOCATION_PROPERTY, 'FIELD_CODE')

# # contractor
# con_table = r'C:\Users\samg\Documents\MyRepos\blandindatatools\DomainTables.gdb\contractor'
# print compare_lists(get_field_values(con_table, 'code'), get_field_values(hv_table, 'contractor'))
#
# # LANDCERT
# landCert_table = r'C:\Users\samg\Documents\MyRepos\blandindatatools\DomainTables.gdb\landCert'
# print compare_lists(get_field_values(landCert_table, 'code'), get_field_values(ts_fc, 'landCertificate'))
