import arcpy
# arcpy.env.workspace = r'D:\gisproject\data'
countries = arcpy.GetParameterAsText(0)
populationYear = arcpy.GetParameterAsText(1)
new_population_value = arcpy.GetParameterAsText(2)
updated_countries = []

with arcpy.da.UpdateCursor(countries, ['NAME_EN', 'POP_YEAR', 'POP_EST']) as cursor:
    for row in cursor:
        country = row[0]
        population_year = row[1]
        population = row[2]

        if population_year < int(populationYear):
            row[2] = int(new_population_value)
            cursor.updateRow(row)
            updated_countries.append(country)

            country_encoded = country.encode('utf-8')
            arcpy.AddMessage("Updated population for {0}".format(country_encoded))

# list of the countries that have been updated
updated_countries_encoded = [c.encode('utf-8') for c in updated_countries]
arcpy.AddMessage("Updated countries: {0}".format(", ".join(updated_countries_encoded)))