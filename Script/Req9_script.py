import arcpy
# arcpy.env.workspace = r'D:\gis_task\data'
ports = arcpy.GetParameterAsText(0)
new_website = arcpy.GetParameterAsText(1)
with arcpy.da.UpdateCursor(ports, ['WEBSITE']) as cursor_sites:
    for x in cursor_sites:
        web = x[0]
        if web == " ":
            x[0] = new_website
            cursor_sites.updateRow(x)
            arcpy.AddMessage("Updated website to {0}".format(x[0]))
