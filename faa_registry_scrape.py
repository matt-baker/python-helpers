# 2015-09-25 - Quick and dirty script to parse FAA registry page for some details using Beautiful Soup package
#              Uses a list of known n numbers and saves output to a csv file  

from bs4 import BeautifulSoup
import csv
import re
from urllib2 import urlopen, URLError

def get_faa_data(nnumber):

	output_data={'nnumber':nnumber}

	url = 'http://registry.faa.gov/aircraftinquiry/NNum_Results.aspx?NNumbertxt='+output_data['nnumber']
	try:
		resp = urlopen(url)
	except URLError as e:
		print 'An error occured fetching %s \n %s' % (url, e.reason)   

	# Get and parse table data
	soup = BeautifulSoup(resp.read(),'lxml')
	table = soup.findAll('tr')
	for row in table:
		this_row=[]
		if '<td' in str(row): # Not td, since always class etc after
			td=re.sub('<[^>]*>', '', str(row)).split('\n') #Strip HTML
			for data in td:
				if len(data) > 0:
					this_row.append(data.rstrip())

		# Extract data needed
		if len(this_row) > 0:
			if this_row[0] == 'Manufacturer Name':
				output_data['Manufacturer']=str(this_row[1])

			if this_row[0] == 'Model':
				output_data['Model']=str(this_row[1])

			if this_row[0] == 'Type Aircraft':
				output_data['TypeAircraft']=str(this_row[1])

			if 'Type Engine' in this_row:
				output_data['TypeEngine']=str(this_row[3])

	# Check the fields are populated with data
	required_field=['Manufacturer','Model','TypeAircraft','TypeEngine']
	for field in required_field:
		if field in output_data:
			pass
		else:
			output_data[field]=None

	return output_data

def write_to_csv(data):
	with open('nnumber_details.csv', 'wb') as csvfile:
		write = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
		for d in data:
			csv_row=[d['nnumber'],d['Manufacturer'],d['Model'],d['TypeAircraft'],d['TypeEngine']]
			write.writerow(csv_row)

if __name__ == '__main__':
	n_numbers=['N42GV', 'N207AM'] # List of N Numbers to scrape
	
	# Get data
	csv_data=[]
	for nnumber in n_numbers:
		csv_data.append(get_faa_data(nnumber))

  # Write data to CSV
	write_to_csv(csv_data)
