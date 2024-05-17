import arcpy
arcpy.env.overwriteOutput = True
countries = arcpy.GetParameterAsText(0)
roads = arcpy.GetParameterAsText(1)
outpath = arcpy.GetParameterAsText(2)
Region = arcpy.GetParameterAsText(3)
Pop = arcpy.GetParameterAsText(4)

fields = ["FID", "SOVEREIGNT", "INCOME_GRP"]
where_clause = "REGION_UN = '{}' AND POP_EST > {}".format(Region, Pop)

with arcpy.da.SearchCursor(countries, fields, where_clause) as cursor:
    for row in cursor:
        country = [row[1], row[2]]
        try:
            arcpy.MakeFeatureLayer_management(roads, 'roads_layer')
            arcpy.MakeFeatureLayer_management(countries, 'countries_layer', """SOVEREIGNT = '{}'""".format(country[0]))
            arcpy.SelectLayerByLocation_management('roads_layer', 'WITHIN', 'countries_layer')
            out_name = 'Roads_in_{}_{}'.format(country[0], country[1])
            arcpy.FeatureClassToFeatureClass_conversion('roads_layer', outpath, out_name)
            arcpy.AddMessage("Created shapefile: {}".format(out_name))
            arcpy.AddMessage("----------------------------------------------------------------------")

        except Exception as e:
            arcpy.AddError("Failed to create shapefile for {}: {}".format(country[0], str(e)))
            arcpy.AddMessage("----------------------------------------------------------------------")
