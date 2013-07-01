""""
  1. Reads directory of shapefiles
  2. Returns attributes of files (also collects spatial metadata and feld name metadata. Not currently returned by function)

"""
class Gis(object):

	gis_files = ['.shp'] # valid GIS files
		
	def get_directory_contents(self,directory):

		output = []

		directory_contents = os.listdir(directory)
		for f in directory_contents:
			if f.endswith(self.gis_files[0]):
				output.append(os.path.join(directory,f))

		return output

	def get_gis_data_attributes(self,file_path):
		desc = arcpy.Describe(file_path)

		# Spatial metadata
		spatial_meta= {}
		spatial_meta.setdefault("name",desc.spatialReference.name) 
		spatial_meta.setdefault("string",desc.spatialReference.GCS.exportToString())
	
		# Attribute metadata
		field_meta = []
		fields = arcpy.ListFields(file_path)
		for f in fields:
			if f.name == 'FID': # Ignore shapefile key
				pass
			else:
				field_meta.append(f.name)

		# Get attributes
		attributes = []
		query= arcpy.SearchCursor(file_path)
		for row in query:
			row_data = {}
			for field in field_meta:
				if field == 'Shape':
					the_geom=row.getValue(field)
					row_data.setdefault('the_geom',the_geom.WKT)
					#row_data.setdefault('the_geom_wkb',the_geom.WKB)
					#row_data.setdefault('the_geom_json',the_geom.JSON) # ESRI JSON
				else:
					row_data.setdefault(field,row.getValue(field))
				
			attributes.append(row_data)

		return attributes

import arcpy
import os

# Set working directory
if __name__ == "__main__":
	g = Gis()

	gis_directory=""

	# Get shapefiles in directory
	files=g.get_directory_contents(gis_directory)
	for f in files:
		file_attributes=g.get_gis_data_attributes(f)
