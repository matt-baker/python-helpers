""""
  1. Reads directory of CSV
  2. Convert CSV with WKT into shp
  		CSV is in format of value, value, WKT(value, value). Includes some manipulation for correcting csv input
  3. Output to shapefile

"""
class Gis(object):

	input_files = ['.csv']
	srs = 102384	# http://resources.arcgis.com/en/help/main/10.1/018z/pdf/projected_coordinate_systems.pdf
	workspace = "C:\\tmp\\WKT"
		
	def create_shapefile(self,output_name,geometry_type,template,has_z,has_m):
		srs = arcpy.SpatialReference(self.srs)
		arcpy.CreateFeatureclass_management(self.workspace, output_name, geometry_type, template, has_m, has_z, srs)

		# Create fields in feature class
		arcpy.AddField_management(out_name,"myField","TEXT",3,"",3)

	def get_directory_contents(self,directory):
		output = []
		directory_contents = os.listdir(directory)
		for f in directory_contents:
			if f.endswith(self.input_files[0]):
				output.append(f)
		return output

	def parse_csv_contents(self,file_name):
		try:
			file_path=self.workspace+'\\'+file_name;
			with open(file_path, 'rb') as this_file:
				reader = csv.reader(this_file, delimiter=',')
				for row in reader:
					
					# Find start of WKT value
					for item in row:
						
						if item.startswith('LINESTRING') is True:
							wkt_start=row.index(item)
							
					# Check for no geom
					if wkt_start is None:
						raise Exception('No WKT found')

					# Recreate WKT value												
					output_values=row[:wkt_start]
					wkt_geom_raw=row[wkt_start:]

					# Update start of LINESTRING
					if wkt_geom_raw[0].startswith('LINESTRING'):
						wkt_geom_raw[0]=wkt_geom_raw[0].replace('LINESTRING','LINESTRINGZM') # has z,m values
						final_wkt=', '.join(wkt_geom_raw) # Convert list to string for arcpy.FromWKT
						esri_geom = arcpy.FromWKT(final_wkt,arcpy.SpatialReference(self.srs)) # Create ESRI geom
					
						# Add to shapefile
						cur = arcpy.InsertCursor('C:/tmp/WKT/output.shp')
						feat = cur.newRow()
						feat.shape = esri_geom
					
						feat.setValue('myField',output_values[0])

						cur.insertRow(feat)
					
		except Exception, e:
			raise e
		
	def set_feature_row(self):
		pass

import arcpy
from arcpy import env
import csv
import os

# Set working directory
if __name__ == "__main__":
	g = Gis()

	gis_directory=g.workspace

	files=g.get_directory_contents(gis_directory)
	for f in files:
		# Create shapefile
		env.workspace = g.workspace
		env.overwriteOutput = True

		# Use csv file name for shp name
		out_name=f[:-4]+'.shp'# remove file extension
		g.create_shapefile(out_name,'POLYLINE','','ENABLED','ENABLED')

		# Parse csv content and write to feature class
		g.parse_csv_contents(f)		
		
