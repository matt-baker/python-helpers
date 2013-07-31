""""
  1. Reads directory of shapefiles
  2. Convert CSV with WKT into shp
  		CSV is in format of value, value, WKT(value, value). Python csv reader breaks, needs some formatting
  3. Output to shapefile

"""
class Gis(object):

	input_files = ['.csv'] 
		
	def get_directory_contents(self,directory):

		output = []

		directory_contents = os.listdir(directory)
		for f in directory_contents:
			if f.endswith(self.input_files[0]):
				output.append(os.path.join(directory,f))

		return output

	def parse_csv_contents(self,file_path):
		try:

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
						wkt_geom_raw[0]=wkt_geom_raw[0].replace('LINESTRING','LINESTRINGZM')
		
	
					final_wkt=', '.join(wkt_geom_raw) # Tidy up input
					esri_geom = arcpy.FromWKT(final_wkt,arcpy.SpatialReference(102384))
					

					# Add to shapefile
					cur = arcpy.InsertCursor('C:/tmp/WKT/output.shp')
					feat = cur.newRow()
					feat.shape = esri_geom
					

					cur.insertRow(feat)

					
					#raise Exception('Stop drop and roll')
			
		except Exception, e:
			raise e
		
import arcpy
from arcpy import env
import csv
import os

# Set working directory
if __name__ == "__main__":
	g = Gis()

	gis_directory="C:/tmp/WKT"

	files=g.get_directory_contents(gis_directory)
	for f in files:
		# Create shapefile
		env.workspace = "C:/tmp/WKT"
		env.overwriteOutput = True

		out_path = "C:/tmp/WKT"
		out_name = "output.shp" # use input file name
		geometry_type = "POLYLINE"
		template = ""
		has_m = "ENABLED"
		has_z = "ENABLED"

		# http://resources.arcgis.com/en/help/main/10.1/018z/pdf/projected_coordinate_systems.pdf
		srs = arcpy.SpatialReference(102384)
		arcpy.CreateFeatureclass_management(out_path, out_name, geometry_type, template, has_m, has_z, srs)

		# Parse csv content
		g.parse_csv_contents(f)	
		
