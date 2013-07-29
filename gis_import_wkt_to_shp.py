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
					wkt_geom=row[wkt_start:]
					output_values.append(wkt_geom)

					# Add to shapefile

					print output_values
					raise Exception('Stop drop and roll')
			
		except Exception, e:
			raise e
		
import arcpy
import csv
import os

# Set working directory
if __name__ == "__main__":
	g = Gis()

	gis_directory="C:\\tmp\WKT"

	files=g.get_directory_contents(gis_directory)
	for f in files:
		# Create shapefile

		# Parse csv content
		g.parse_csv_contents(f)	
		
