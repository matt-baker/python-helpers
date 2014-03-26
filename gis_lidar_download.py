#!/usr/bin/env python
# Script to download LiDAR data from MN GEO (http://www.mngeo.state.mn.us/chouse/elevation/lidar.html#data)

from ftplib import FTP

# FTP details
ftp_address = 'ftp.lmic.state.mn.us'
ftp_username = 'anonymous'
ftp_password = '' # Your email address
output_dir='lidar/'

# Data to obtain
counties=['hennepin','ramsey','dakota']
lidar_sets=['4342-21-22.gdb.zip','4321-04-22.gdb.zip'] # Populate as needed

ftp = FTP(ftp_address) # Connect
ftp.login(ftp_username,ftp_password) # Authenticate
for county in counties: #Loop through counties
	ftp.cwd('/pub/data/elevation/lidar/county/'+county+'/geodatabase') # Change to county directory
	files=ftp.nlst() # Get files in directory
	for f in files:
		if any(f in s for s in lidar_sets): # If directory contains files that we are looking for download it
			output_file=output_dir+f
			file = open(output_file, 'wb')
			ftp.retrbinary('RETR %s' % f, file.write)
			print f+' complete'	
ftp.close()
