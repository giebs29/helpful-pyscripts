import arcpy

mxd = arcpy.mapping.MapDocument("")
df = arcpy.mapping.ListDataFrames(mxd)[0]
layerList = df.listLayers()
print layerList
