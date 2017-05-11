import arcpy
import csv

def replace_domain(workspace,old_domain,new_domain):
    # Ensure that the old and new domains exist in the workspace
    if old_domain and new_domain not in [i.name for i in arcpy.da.ListDomains(workspace)]:
        return

    arcpy.env.workspace = workspace

    for dataset in arcpy.ListDatasets():
        for fc in arcpy.ListFeatureClasses(feature_dataset=dataset):
            if [i for i in arcpy.ListFields(fc) if i.domain == old_domain]:
                for field in [i for i in arcpy.ListFields(fc) if i.domain == old_domain]:
                    arcpy.AssignDoaminToField_management(
                        intable=fc,
                        field_name=field,
                        domain_name=new_domain)


def create_temp_domain(workspace,old_domain_obj):

    arcpy.CreateDomain_management(
        in_workspace = workspace,
        domain_name = 'TEMP_DOMAIN',
        domain_description = 'Temporary domain used in domain update script',
        field_type = old_domain_obj.type,
        domain_type = "CODED")

def get_domain_object(workspace,domain):
    return [i for i in arcpy.da.ListDomains(workspace) if i.name == domain][0]

def recreate_domain(workspace,csv_path,code_field,desc_field,domain_name,old_domain_obj):

    arcpy.TableToDomain_management(
        in_table = csv_path,
        code_field = code_field,
        description_field = desc_field,
        in_workspace = workspace,
        domain_name = domain_name,
        domain_description = old_domain_obj.description,
        update_option = 'REPLACE')


if __name__ == "__main__":

    workspace = arcpy.GetParameterAsText(0)
    target_domain = arcpy.GetParameterAsText(1)
    csv_path = arcpy.GetParameterAsText(2)
    code = arcpy.GetParameterAsText(3)
    desc = arcpy.GetParameterAsText(4)

    arcpy.env.workspace = workspace

    old_domain_obj = get_domain_object(
        workspace=workspace,
        domain=target_domain)

    recreate_domain(
        workspace=workspace,
        csv_path=csv_path,
        code_field=code,
        desc_field=desc,
        domain_name= target_domain+'_1',
        old_domain_obj = old_domain_obj)

    replace_domain(
        workspace=workspace,
        old_domain=target_domain,
        new_domain=target_domain+'_1')

    arcpy.DeleteDomain_management(
        in_workspace = workspace,
        domain_name = target_domain)

    recreate_domain(
        workspace=workspace,
        csv_path=csv_path,
        code_field=code,
        desc_field=desc,
        domain_name= target_domain,
        old_domain_obj = old_domain_obj)

    replace_domain(
        workspace=workspace,
        old_domain=target_domain+'_1',
        new_domain=target_domain)

    arcpy.DeleteDomain_management(
        in_workspace = workspace,
        domain_name = target_domain+'_1')
