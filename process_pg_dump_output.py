"""
	Processes pg_dump output so that it can be checked into Git
	
	Looks for CREATE FUNCTION and saves function to file
		function is saved as functionName___functionHash. The functionHash is to account for duplicate function names
	Also collects metadata about where the function is in the output

"""
import hashlib,os, sys

class exportPostgres:
	
	def __init__(self):
		self.outputDir=os.getcwd()+'/functions'

	def getFileContents(self,fileName):
		# Read output from pg_dump
		masterCount = 0;
		with open(fileName, 'r') as f:
			counting = None
			functionDict={}
			thisFunction=[]

			checkFor = 'Type: FUNCTION;'

			for line in f:
				masterCount +=1
				
				if checkFor in line and counting == None:
					# Start counting
					thisFunctionStart=masterCount
					thisFunctionCounter=0
					counting = True

					thisFunction.append(line)
			
				elif checkFor in line and counting == True:
					# New function, handle input and reset this FunctionCounter
					self.exportFunction(thisFunction,masterCount,thisFunctionCounter)
			
					# Reset thisFunction
					del thisFunction[:]
					thisFunction = []
					thisFunction.append(line)

					thisFunctionStart=masterCount
					thisFunctionCounter=0

				elif counting == True:
					# Check for change in output of dump file. Defined by Type: TABLE
					# If true, then clean up last element
					checkForEnd = 'Type: TABLE;'
					if checkForEnd in line:
						counting = None
						self.exportFunction(thisFunction,masterCount,thisFunctionCounter)

					# Still looping through a function
					thisFunction.append(line)
					thisFunctionCounter+=1
				else:
					pass	

	def exportFunction(self,thisFunction,startsAt,numberOfRows):
		# Save function to file
		
		functionName=str(thisFunction[:1])
		
		# Hash for file name
		functionNameHash=str(hashlib.sha1(str(thisFunction)).hexdigest())
		
		# Wrangle name
		functionName=functionName.split(';')
		functionName=str(functionName[0])
		functionName=functionName[11:]
		functionName=functionName.split('(')
		functionName=functionName[0]

		# Write function to file
		functionFileName=self.outputDir+'/'+functionName+'___'+functionNameHash+'.txt'
		with open(functionFileName, 'w') as thisFile:
			#thisFile.write('Metadata: Starts on line '+str(startsAt)+', '+str(numberOfRows)+' rows')
			for line in thisFunction:
				thisFile.write(line)

if __name__ == '__main__':

	if len(sys.argv) == 1:
		print 'No pg_dump file specified'
	else:
		# Check that the file exists
		if os.path.isfile(sys.argv[1]):
			process = exportPostgres()
			process.getFileContents(sys.argv[1])
		else:
			print 'Not a valid file'

		
