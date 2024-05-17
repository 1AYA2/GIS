# -*- coding: utf-8 -*-
import arcpy
import os
from PIL import Image, ExifTags
arcpy.env.workspace=r"C:\Users\Win10\Desktop\GIS\project\Data"
arcpy.env.overwriteOutput=True
countries=r"C:\Users\Win10\Desktop\GIS\project\Data\ne_10m_admin_0_countries.shp"
populated_places=r"C:\Users\Win10\Desktop\GIS\project\Data\ne_10m_populated_places.shp"
roads=r"C:\Users\Win10\Desktop\GIS\project\Data\ne_10m_roads.shp"
airports=r"C:\Users\Win10\Desktop\GIS\project\Data\ne_10m_airports.shp"
ports=r"C:\Users\Win10\Desktop\GIS\project\Data\ne_10m_ports.shp"
outpath=r"C:\Users\Win10\Desktop\GIS\project\Output"
images_folder = r"C:\Users\Win10\Desktop\GIS\project\Images"
image_contents = os.listdir(images_folder)

# TODO: 1) List all data we’re working with and show them on ArcMap.
def requirement_1():
    featureList = arcpy.ListFeatureClasses()
    print (featureList)
    print ("----------------------------------------------------------------------")


# TODO: 2) Create a shapefile for countries that have “military” airports + Print them in Pycharm.
def requirement_2():
    # Create a feature layer for the airports with "military" type
    arcpy.MakeFeatureLayer_management(airports, "military_airports",""" "type"='military' OR "type"='major and military' OR  "type"='mid and military'  """)
    # Create a feature layer for the countries
    arcpy.MakeFeatureLayer_management(countries, "countries_layer")
    # Select the countries that intersect with the military airports
    arcpy.SelectLayerByLocation_management("countries_layer", "INTERSECT", "military_airports")
    # Create a new shapefile for the selected countries
    arcpy.FeatureClassToFeatureClass_conversion("countries_layer", outpath, "military_countries")
    # Create a feature layer for the new shapefile
    arcpy.MakeFeatureLayer_management(outpath + "\\military_countries.shp", "military_countries_layer")
    # Print the names of the selected countries
    with arcpy.da.SearchCursor("military_countries_layer", "NAME") as cursor:
        for row in cursor:
            print("country has military airport:{}".format(row[0]))
            print ("----------------------------------------------------------------------")

# TODO: 3) Create a shapefile for roads in “Asia” continent + Print their number in Pycharm.
def requirement_3():
    arcpy.MakeFeatureLayer_management(roads, "roads", """ "continent"='Asia' """)
    arcpy.FeatureClassToFeatureClass_conversion("roads", outpath, "roads_Asia")
    # Create a feature layer for the new shapefile
    arcpy.MakeFeatureLayer_management(outpath + "\\roads_Asia.shp", "roads_in_asia")
    count = arcpy.GetCount_management("roads_in_asia")[0]
    print("Number of roads in Asia: {}".format(count))
    print ("----------------------------------------------------------------------")

# TODO: 4) Create a shapefile for ports in countries (Italy, Spain, France)
def requirement_4():
    countries_list = ['Italy', 'Spain', 'France']
    arcpy.MakeFeatureLayer_management(ports, "ports_layer")
    for x in countries_list:
        arcpy.MakeFeatureLayer_management(countries, "countries_layer", """ "NAME"='{}' """.format(x))
        arcpy.SelectLayerByLocation_management("ports_layer", "WITHIN", "countries_layer")
        arcpy.FeatureClassToFeatureClass_conversion("ports_layer", outpath, 'ports_in_{}'.format(x))


# TODO: 5) Create a shapefile for all Arabic cities using 2 methods (1) Multiple Selections (2) If Condition
def requirement_5():
    # #Usung Multiple Selections
    arabicCountries = ['Saudi Arabia', 'Kuwait', 'United Arab Emirates', 'Qatar', 'Bahrain', 'Oman', 'Yemen', 'Iraq',
                       'Syria', 'Lebanon', 'Jordan', 'Palestine', 'Egypt', 'Libya', 'Tunisia', 'Algeria', 'Morocco']
    arcpy.MakeFeatureLayer_management(countries, "countries_layer")
    arcpy.MakeFeatureLayer_management(populated_places, "populated_places_layer")

    for country in arabicCountries:
        # Select the country feature
        arcpy.SelectLayerByAttribute_management("countries_layer", "NEW_SELECTION",
                                                """ "NAME" = '{}' """.format(country))
        # Select the populated places within the country's boundaries
        arcpy.SelectLayerByLocation_management("populated_places_layer", "WITHIN", "countries_layer")
        # Create a new shapefile for the selected populated places
        arcpy.FeatureClassToFeatureClass_conversion("populated_places_layer", outpath,"populated_places1_{}".format(country))
    # If Condition
    for row in arcpy.da.SearchCursor(countries, ["NAME"]):
        country = row[0]
        if country in arabicCountries:
            # Select the country feature
            arcpy.SelectLayerByAttribute_management("countries_layer", "NEW_SELECTION",
                                                    """ "NAME" = '{}' """.format(country))
            # Select the populated places within the country's boundaries
            arcpy.SelectLayerByLocation_management("populated_places_layer", "WITHIN", "countries_layer")
            # Create a new shapefile for the selected populated places
            arcpy.FeatureClassToFeatureClass_conversion("populated_places_layer", outpath,"populated_places2_{}".format(country))


# TODO: 6) Using Search Cursor print the name, location & wikipedia for all airports which are major
def requirement_6():
    fields = ["NAME", "LOCATION", "WIKIPEDIA", "type"]
    where_clause = "type = 'major'"

    with arcpy.da.SearchCursor(airports, fields, where_clause) as cursor:
        for row in cursor:
            name = row[0]
            location = row[1]
            wikipedia = row[2]
            print("Airport name: {}".format(name.encode('utf-8')))
            print("Location: {}".format(location))
            print("Wikipedia URL: {}".format(wikipedia))
            print("--------------------------------------------------------")

# TODO: 7) Using Search Cursor create shapefiles for roads in countries based on (FID & Sovereignty) condition that
#  region is “Africa” & population > 25 million Let files names be in the format of “Roads_in_CountryName_CountryIncome”
def requirement_7():
    fields = ["FID", "SOVEREIGNT", "INCOME_GRP"]
    where_clause = "REGION_UN = 'Africa' AND POP_EST > 25000000"
    with arcpy.da.SearchCursor(countries, fields, where_clause) as cursor:
        for row in cursor:
            country = [row[1], row[2]]
            try:
                arcpy.MakeFeatureLayer_management(roads, 'roads_layer')
                arcpy.MakeFeatureLayer_management(countries, 'countries_layer',
                                                  """SOVEREIGNT = '{}'""".format(country[0]))
                arcpy.SelectLayerByLocation_management('roads_layer', 'WITHIN', 'countries_layer')
                out_name = 'Roads_in_{}_{}'.format(country[0], country[1])
                arcpy.FeatureClassToFeatureClass_conversion('roads_layer', outpath, out_name)
                arcpy.AddMessage("Created shapefile: {}".format(out_name))
                arcpy.AddMessage("----------------------------------------------------------------------")

            except Exception as e:
                arcpy.AddError("Failed to create shapefile for {}: {}".format(country[0], str(e)))
                arcpy.AddMessage("----------------------------------------------------------------------")

# TODO: 11)	Print name & type of cities fields
def requirement_11():
    fields = arcpy.ListFields(populated_places)
    for field in fields:
        print("Name: " + field.name)
        print("Type: " + field.type)
        print("----------------------------------------------------------------------")

# TODO: 12) Using Update Cursor for multiple fields, update empty or “zero” fields that are not of string datatype in cities
def requirement_12():
    Cities_field = arcpy.ListFields(populated_places)
    filtered_fields = []
    for field in Cities_field:
        if field.type != "String":
            filtered_fields.append(field.name)

    for fiel_d in filtered_fields:
        with arcpy.da.UpdateCursor(populated_places, [fiel_d]) as cities_cursor:
            for x in cities_cursor:
                if x[0] is None or x[0] == 0:
                    x[0] = 5
                    cities_cursor.updateRow(x)

# TODO: 13)	Print full path for a bunch of images & 14)Print exif Tags for these images
def requirement_13_14():
    for img in image_contents:
        full_path = os.path.join(images_folder, img)
        print (full_path)
        # 14-Print exif Tags for these images
        pillow_image = Image.open(full_path)
        print({ExifTags.TAGS[K]: v for K, v in pillow_image._getexif().items() if K in ExifTags.TAGS})


# TODO: 15)	Print GPS Tags/Info for each image indicating which is geotagged & which is not
def requirement_15():
    for img in image_contents:
        full_path = os.path.join(images_folder, img)
        pillow_image = Image.open(full_path)

        try:
            exif = {ExifTags.TAGS[k]: v for k, v in pillow_image._getexif().items() if k in ExifTags.TAGS}
            for key in exif['GPSInfo'].keys():
                print ("this is the coded value {}".format(key))
                decoded_value = ExifTags.GPSTAGS.get(key)
                print ("this is its associated label {}".format(decoded_value))
        except:
            print ("this image has no GPS Info in it {}".format(full_path))

# TODO: 16)	Print latitude & longitude for each geotagged image
def requirement_16():
    for img in image_contents:
        full_path = os.path.join(images_folder, img)
        pillow_image = Image.open(full_path)
        gbs_all = {}
        try:
            exif = {ExifTags.TAGS[k]: v for k, v in pillow_image._getexif().items() if k in ExifTags.TAGS}
            for key in exif['GPSInfo'].keys():
                decoded_value = ExifTags.GPSTAGS.get(key)
                gbs_all[decoded_value] = exif['GPSInfo'][key]
            long_ref = gbs_all['GPSLongitudeRef']
            long = gbs_all['GPSLongitude']
            lat_ref = gbs_all['GPSLatitudeRef']
            lat = gbs_all['GPSLatitude']
            print (long_ref, "    ", long)
            print (lat_ref, "    ", lat)

        except:
            print ("this image has no GPS Info in it {}".format(full_path))


if __name__ == "__main__":
    #requirement_1()
    #requirement_2()
    #requirement_3()
    #requirement_4()
    #requirement_5()
    #requirement_6()
    #requirement_7()
    #requirement_11()
    #requirement_12()
    #requirement_13_14()   #for requirement 13 & 14
    #requirement_15()
    #requirement_16()
    pass