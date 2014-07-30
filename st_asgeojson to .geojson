"""
  Quick script to convert st_asgeojson to .geojson

  Assumes follow csv export from PostgreSQL:
    SELECT guid, st_asgeojson(st_transform(the_geom,4326)) FROM table

"""
#!/usr/bin/python
import csv
import re
import string

inputFile='fileName.csv'
outputFile='fileName.geojson'

with open(inputFile,'r') as f:
	reader=csv.reader(f)
	next(reader, None) #Skip header
	output='{ "type": "FeatureCollection","features": ['
	for row in reader:
		l=str(row)
		t=l.split(' ')
		guid=re.sub('[^0-9]','',t[0]) #Strip non numerical, adjust as needed
		t.pop(0)#Remove guid
		t=''.join(t)#Merge to string
		l= t.replace('\'','') #String cleaning
		l=l[:-1] #Clean up end
		l=string.replace(l,'coordinates','"coordinates"')
	
		output=output+' \n{"type": "Feature","geometry":'+l+',"properties": {"description":"'+str(guid)+'"}},'
		
	output=output[:-1]+']}'
	f2=open(outputFile,'w+')
	f2.write(output)
	f2.close
