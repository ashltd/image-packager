# Python 3

# Import modules
import xml.etree.ElementTree as ET
import os
import shutil
from zipfile import ZipFile

# Parse the XML file
tree = ET.parse('set.xml')

#Get the Root element
root = tree.getroot()

# Get the Game ID
gameID = root.attrib['gameId']
print('Game ID: ' + gameID)

# Get the Set ID and Set Name
setID = root.attrib['id']
print('Set ID: ' + setID)

setName = root.attrib['name']
print('Set Name: ' + setName)

# Build path Name
pathName = gameID + '.\\Sets\\' + setID + '\\Cards\\'
print('Image Pack Folder: ' + pathName)

# Check if the pathName exists
if not os.path.isdir(pathName):
	# Create the directory tree
	try:
		os.makedirs(pathName)
	except OSError:
		print("[ERROR]: Creation of directory [%s] failed!!!" % pathName)
		exit(-1)
	else:
		print("Directory [%s] has been created!" % pathName)
else:
	print("Directory [%s] already exists..." % pathName)
	
# Define the image extension to be used and 
# the image folder where the scans are stored
imgExt = ".jpg"
imgPath = ".\\scans\\"

# Check if the scan folder exists
if os.path.isdir(imgPath):
	print("Scan Folder [%s] is available." % imgPath)
else:
	print("[ERROR]: Scan Folder [%s] is missing!!!" % imgPath)
	exit(-1)
	
# Define the filenames
scanFile = ""
imgFile = ""

# Process the xml file
for child in root[0]:
	# Get the Card ID
	cardID = child.attrib['id']
	
	# Process all Card properties to extract the Card Number
	for prop in child.iter('property'):
		# Get the property name
		name = prop.attrib['name']
		# Check if the Property is the Card Number
		if name == 'Card Number':
			# Get the number
			cardNumber = prop.attrib['value']
			# Build file names
			scanFile = cardNumber + imgExt
			imgFile = cardID + imgExt
			
			# Check if the scan is present
			if os.path.isfile(imgPath + scanFile):
				# Copy file
				shutil.copy2(imgPath + scanFile, pathName + imgFile)
				print(scanFile + '\t\t->\t' + imgFile)
			else:
				print("[WARNING]: Scan Image [%s] is missing!!!" % scanFile)
			
	# Get the alternate element
	alt = child.find('alternate')
	# Check if we found the alternate element
	if alt:
		# Grab the Type code
		alternateType = alt.attrib['type']
		# Build file names
		scanFile = cardNumber + "." + alternateType + imgExt
		imgFile = cardID + "." + alternateType + imgExt
		
		# Check if the scan is present
		if os.path.isfile(imgPath + scanFile):
			# Copy file
			shutil.copy2(imgPath + scanFile, pathName + imgFile)
			print(scanFile + '\t->\t' + imgFile)
		else:
			print("[WARNING]: Scan Image [%s] is missing!!!" % scanFile)
			

# Create Image Package
# Define Zip name and folder to package
zipName = '[ES] ' + setName + '.o8c'
walkPath = '.\\' + gameID

# Create the zip file
with ZipFile(zipName, 'w') as zipObj:
	# Iterate over all the files in directory
	for folderName, subfolders, filenames in os.walk(walkPath):
		# Process all files
		for filename in filenames:
			#create complete filepath of file in directory
			filePath = os.path.join(folderName, filename)
			# Add file to zip
			zipObj.write(filePath, filePath)

print("Image Pack [%s] has been created" % zipName)

# Wait for user
input("Press Enter to continue...")