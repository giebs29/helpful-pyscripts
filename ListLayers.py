import arcpy

mxd = arcpy.mapping.MapDocument(r"X:\business\projects\stLouisCO\mapdocs\SLCPlatS.mxd")
df = arcpy.mapping.ListDataFrames(mxd)[0]
layerList = df.listLayers()
print layerList
