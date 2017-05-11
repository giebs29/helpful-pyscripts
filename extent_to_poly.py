import arcpy

def list_dataframes(mxd_path):
    mxd = arcpy.mapping.MapDocument(mxd_path)
    df_list = [str(i.name) for i in arcpy.mapping.ListDataFrames(mxd)]

    print('Dataframes:', df_list)

    return df_list

def polygon_from_dataframe(mxd_path, dateframe_name, out_extent_poly):

    mxd = arcpy.mapping.MapDocument(mxd_path)

    # Retrieve dataframe object
    df = arcpy.mapping.ListDataFrames(mxd, dateframe_name)[0]

    # Get dataframe extent information and create polygon object
    dfAsFeature = arcpy.Polygon(
        arcpy.Array(
            [df.extent.lowerLeft,
             df.extent.lowerRight,
             df.extent.upperRight,
             df.extent.upperLeft]),
        df.spatialReference)

    # Export extent polygon
    arcpy.CopyFeatures_management(
        in_features = dfAsFeature,
        out_feature_class = out_extent_poly)


if __name__ == '__main__':
    # Path to map document
    mxd_path = ""

    # Name of dataframe whos extent will be used to create a polygon featureclass eg. "Duluth"
    dateframe_name = ""

    # Output extent polygon path
    out_extent_poly = ""

    # Create polygon featureclass based on dataframe extent
    polygon_from_dataframe(mxd_path,dateframe_name,out_extent_poly)
