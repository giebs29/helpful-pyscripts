import arcpy

fc = arcpy.GetParameterAsText(0)
topo = arcpy.GetParameterAsText(1)
search_radius = arcpy.GetParameterAsText(2)

arcpy.env.workspace = "IN_MEMORY"

arcpy.env.overwriteOutput = True

points = arcpy.ExportTopologyErrors_management(topo,"", "topo")[0]

lyr = arcpy.MakeFeatureLayer_management(points,"lyr")

expression = "{0} = 'Must Not Have Dangles'".format(arcpy.AddFieldDelimiters(lyr, "RuleDescription"))

arcpy.SelectLayerByAttribute_management(lyr,"NEW_SELECTION",expression)

arcpy.Near_analysis(lyr,lyr,search_radius)

expression2 = "{0} > 0".format(arcpy.AddFieldDelimiters(lyr, "NEAR_DIST"))

arcpy.SelectLayerByAttribute_management(lyr,"NEW_SELECTION",expression2)

arcpy.CopyFeatures_management(lyr,fc)